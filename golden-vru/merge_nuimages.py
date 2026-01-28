#!/usr/bin/env python3
"""
Merge nuImages VRU data into Golden-VRU dataset to create v8.0.

This script:
1. Loads annotations from both golden-vru v7.0 and nuImages VRU COCO
2. Renames nuImages images with 'nuimages_' prefix to avoid conflicts
3. Remaps image and annotation IDs
4. Copies nuImages images to golden-vru directories
5. Saves merged annotations (backs up v7.0 first)

Usage:
    python merge_nuimages.py [--dry-run]
"""

import argparse
import json
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Dict, Tuple


# Paths
BASE_DIR = Path(__file__).parent
NUIMAGES_DIR = Path("/mnt/data/nuimages/nuimages-vru-coco")
SPLITS = ['train', 'valid', 'test']


def load_annotations(path: Path) -> dict:
    """Load COCO annotations from JSON file."""
    with open(path, 'r') as f:
        return json.load(f)


def save_annotations(data: dict, path: Path):
    """Save COCO annotations to JSON file."""
    with open(path, 'w') as f:
        json.dump(data, f)


def get_max_ids(data: dict) -> Tuple[int, int]:
    """Get maximum image ID and annotation ID from COCO data."""
    max_img_id = max(img['id'] for img in data['images']) if data['images'] else 0
    max_ann_id = max(ann['id'] for ann in data['annotations']) if data['annotations'] else 0
    return max_img_id, max_ann_id


def merge_split(split: str, dry_run: bool = False) -> Dict[str, int]:
    """
    Merge a single split (train/valid/test).

    Returns statistics dict.
    """
    print(f"\n{'='*60}")
    print(f"Processing {split.upper()} split")
    print(f"{'='*60}")

    # Paths
    golden_ann_path = BASE_DIR / split / '_annotations.coco.json'
    golden_backup_path = BASE_DIR / split / '_annotations.coco.v7.0.json'
    nuimages_ann_path = NUIMAGES_DIR / split / '_annotations.coco.json'
    golden_img_dir = BASE_DIR / split
    nuimages_img_dir = NUIMAGES_DIR / split

    # Load annotations
    print(f"Loading golden-vru {split} annotations...")
    golden_data = load_annotations(golden_ann_path)
    print(f"  Images: {len(golden_data['images']):,}")
    print(f"  Annotations: {len(golden_data['annotations']):,}")

    print(f"Loading nuImages {split} annotations...")
    nuimages_data = load_annotations(nuimages_ann_path)
    print(f"  Images: {len(nuimages_data['images']):,}")
    print(f"  Annotations: {len(nuimages_data['annotations']):,}")

    # Get max IDs from golden-vru for offset
    max_img_id, max_ann_id = get_max_ids(golden_data)
    print(f"\nGolden-VRU max IDs - Image: {max_img_id}, Annotation: {max_ann_id}")

    # ID offsets for nuImages data
    img_id_offset = max_img_id + 1
    ann_id_offset = max_ann_id + 1

    # Create image ID mapping for nuImages
    nuimages_img_id_map = {}  # old_id -> new_id

    # Process nuImages images
    print(f"\nProcessing nuImages images...")
    new_nuimages_images = []
    images_to_copy = []

    for img in nuimages_data['images']:
        old_id = img['id']
        new_id = old_id + img_id_offset
        nuimages_img_id_map[old_id] = new_id

        # Rename file with prefix
        old_filename = img['file_name']
        new_filename = f"nuimages_{old_filename}"

        new_img = {
            'id': new_id,
            'file_name': new_filename,
            'width': img['width'],
            'height': img['height'],
            'source': 'nuimages'
        }
        new_nuimages_images.append(new_img)

        # Track files to copy
        src_path = nuimages_img_dir / old_filename
        dst_path = golden_img_dir / new_filename
        images_to_copy.append((src_path, dst_path))

    print(f"  Mapped {len(nuimages_img_id_map):,} image IDs")
    print(f"  Files to copy: {len(images_to_copy):,}")

    # Process nuImages annotations
    print(f"Processing nuImages annotations...")
    new_nuimages_annotations = []

    for ann in nuimages_data['annotations']:
        new_ann = {
            'id': ann['id'] + ann_id_offset,
            'image_id': nuimages_img_id_map[ann['image_id']],
            'category_id': ann['category_id'],
            'bbox': ann['bbox'],
            'area': ann['area'],
            'iscrowd': ann.get('iscrowd', 0)
        }
        new_nuimages_annotations.append(new_ann)

    print(f"  Remapped {len(new_nuimages_annotations):,} annotations")

    # Merge data
    print(f"\nMerging data...")
    merged_data = {
        'categories': golden_data['categories'],  # Use golden-vru categories
        'images': golden_data['images'] + new_nuimages_images,
        'annotations': golden_data['annotations'] + new_nuimages_annotations
    }

    print(f"  Merged images: {len(merged_data['images']):,}")
    print(f"  Merged annotations: {len(merged_data['annotations']):,}")

    # Calculate stats
    stats = {
        'golden_images': len(golden_data['images']),
        'golden_annotations': len(golden_data['annotations']),
        'nuimages_images': len(nuimages_data['images']),
        'nuimages_annotations': len(nuimages_data['annotations']),
        'merged_images': len(merged_data['images']),
        'merged_annotations': len(merged_data['annotations'])
    }

    # Count by category
    cat_counts = defaultdict(int)
    for ann in merged_data['annotations']:
        cat_counts[ann['category_id']] += 1

    cat_names = {cat['id']: cat['name'] for cat in merged_data['categories']}
    for cat_id, count in sorted(cat_counts.items()):
        stats[cat_names[cat_id]] = count

    if dry_run:
        print(f"\n[DRY RUN] Would perform the following:")
        print(f"  - Backup {golden_ann_path} to {golden_backup_path}")
        print(f"  - Copy {len(images_to_copy):,} images to {golden_img_dir}")
        print(f"  - Save merged annotations to {golden_ann_path}")
    else:
        # Backup v7.0 annotations
        print(f"\nBacking up v7.0 annotations...")
        if golden_backup_path.exists():
            print(f"  Backup already exists: {golden_backup_path}")
        else:
            shutil.copy2(golden_ann_path, golden_backup_path)
            print(f"  Saved: {golden_backup_path}")

        # Copy images
        print(f"Copying {len(images_to_copy):,} images...")
        copied = 0
        skipped = 0
        for src, dst in images_to_copy:
            if dst.exists():
                skipped += 1
            else:
                shutil.copy2(src, dst)
                copied += 1

            if (copied + skipped) % 5000 == 0:
                print(f"  Progress: {copied + skipped:,}/{len(images_to_copy):,}")

        print(f"  Copied: {copied:,}, Skipped (already exist): {skipped:,}")

        # Save merged annotations
        print(f"Saving merged annotations...")
        save_annotations(merged_data, golden_ann_path)
        print(f"  Saved: {golden_ann_path}")

    return stats


def main():
    parser = argparse.ArgumentParser(description='Merge nuImages VRU data into Golden-VRU')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be done without making changes')
    args = parser.parse_args()

    print("=" * 60)
    print("Golden-VRU v8.0 Merge: Adding nuImages VRU Data")
    print("=" * 60)

    if args.dry_run:
        print("\n[DRY RUN MODE - No changes will be made]")

    print(f"\nSource: {NUIMAGES_DIR}")
    print(f"Target: {BASE_DIR}")

    # Merge all splits
    all_stats = {}
    for split in SPLITS:
        all_stats[split] = merge_split(split, dry_run=args.dry_run)

    # Print summary
    print("\n" + "=" * 60)
    print("MERGE SUMMARY")
    print("=" * 60)

    total_images = 0
    total_annotations = 0
    total_pedestrian = 0
    total_cyclist = 0

    print(f"\n{'Split':<8} {'Images':>10} {'Annotations':>12} {'Pedestrian':>12} {'Cyclist':>10}")
    print("-" * 56)

    for split in SPLITS:
        stats = all_stats[split]
        images = stats['merged_images']
        anns = stats['merged_annotations']
        ped = stats.get('pedestrian', 0)
        cyc = stats.get('cyclist', 0)

        print(f"{split.capitalize():<8} {images:>10,} {anns:>12,} {ped:>12,} {cyc:>10,}")

        total_images += images
        total_annotations += anns
        total_pedestrian += ped
        total_cyclist += cyc

    print("-" * 56)
    print(f"{'Total':<8} {total_images:>10,} {total_annotations:>12,} {total_pedestrian:>12,} {total_cyclist:>10,}")

    # Calculate percentages
    ped_pct = total_pedestrian / total_annotations * 100 if total_annotations > 0 else 0
    cyc_pct = total_cyclist / total_annotations * 100 if total_annotations > 0 else 0

    print(f"\nClass distribution:")
    print(f"  Pedestrian: {total_pedestrian:,} ({ped_pct:.1f}%)")
    print(f"  Cyclist: {total_cyclist:,} ({cyc_pct:.1f}%)")

    if args.dry_run:
        print("\n[DRY RUN] No changes were made. Run without --dry-run to merge.")
    else:
        print("\n[DONE] Golden-VRU v8.0 merge complete!")
        print("Next steps:")
        print("  1. Run: python validate_dataset.py")
        print("  2. Run: python analyze_distributions.py")
        print("  3. Update STATS.md and DATASET_REPORT.md")


if __name__ == '__main__':
    main()
