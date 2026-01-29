#!/usr/bin/env python3
"""
Extract RSUD20K data from Golden-VRU dataset.

Creates v9.0 by removing RSUD20K images and annotations and copying them
to a separate directory at /mnt/data/rsud-vru/.
"""

import json
import os
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

# Constants
BASE_DIR = Path(__file__).parent
RSUD_OUTPUT_DIR = Path('/mnt/data/rsud-vru')
SPLITS = ['train', 'valid', 'test']
SOURCE_TO_REMOVE = 'rsud20k'


def load_coco_annotations(split: str) -> dict:
    """Load COCO annotations for a split."""
    ann_path = BASE_DIR / split / '_annotations.coco.json'
    with open(ann_path, 'r') as f:
        return json.load(f)


def save_coco_annotations(data: dict, path: Path):
    """Save COCO annotations to a file."""
    with open(path, 'w') as f:
        json.dump(data, f)


def create_backup(split: str):
    """Create a backup of the current annotations."""
    ann_path = BASE_DIR / split / '_annotations.coco.json'
    backup_path = BASE_DIR / split / '_annotations.coco.v8.0.json'
    if not backup_path.exists():
        shutil.copy(ann_path, backup_path)
        print(f"  Backup created: {backup_path.name}")


def separate_rsud_data(data: dict) -> Tuple[dict, dict, Dict[str, int]]:
    """
    Separate RSUD data from the dataset.

    Returns:
        Tuple of (remaining_data, rsud_data, statistics)
    """
    stats = {
        'original_images': len(data['images']),
        'original_annotations': len(data['annotations']),
        'rsud_images': 0,
        'rsud_annotations': 0,
        'remaining_images': 0,
        'remaining_annotations': 0,
    }

    # Separate images by source
    rsud_images = []
    remaining_images = []
    rsud_image_ids = set()

    for img in data['images']:
        if img.get('source') == SOURCE_TO_REMOVE:
            rsud_images.append(img)
            rsud_image_ids.add(img['id'])
        else:
            remaining_images.append(img)

    stats['rsud_images'] = len(rsud_images)
    stats['remaining_images'] = len(remaining_images)

    # Separate annotations based on image source
    rsud_annotations = []
    remaining_annotations = []

    for ann in data['annotations']:
        if ann['image_id'] in rsud_image_ids:
            rsud_annotations.append(ann)
        else:
            remaining_annotations.append(ann)

    stats['rsud_annotations'] = len(rsud_annotations)
    stats['remaining_annotations'] = len(remaining_annotations)

    # Get file names for deletion/copying
    stats['rsud_files'] = [img['file_name'] for img in rsud_images]

    # Create remaining data (for golden-vru)
    remaining_data = {
        'categories': data['categories'],
        'images': remaining_images,
        'annotations': remaining_annotations,
    }

    # Copy over any additional keys
    for key in data:
        if key not in remaining_data:
            remaining_data[key] = data[key]

    # Create RSUD data
    rsud_data = {
        'categories': data['categories'],
        'images': rsud_images,
        'annotations': rsud_annotations,
    }

    for key in data:
        if key not in rsud_data:
            rsud_data[key] = data[key]

    return remaining_data, rsud_data, stats


def copy_rsud_images(split: str, file_names: List[str], dry_run: bool = True) -> int:
    """Copy RSUD images to the rsud-vru directory."""
    src_dir = BASE_DIR / split
    dst_dir = RSUD_OUTPUT_DIR / split

    if not dry_run:
        dst_dir.mkdir(parents=True, exist_ok=True)

    copied_count = 0
    for file_name in file_names:
        src_path = src_dir / file_name
        dst_path = dst_dir / file_name
        if src_path.exists():
            if not dry_run:
                shutil.copy2(src_path, dst_path)
            copied_count += 1

    return copied_count


def delete_rsud_images(split: str, file_names: List[str], dry_run: bool = True) -> int:
    """Delete RSUD images from golden-vru."""
    split_dir = BASE_DIR / split
    deleted_count = 0

    for file_name in file_names:
        file_path = split_dir / file_name
        if file_path.exists():
            if not dry_run:
                os.remove(file_path)
            deleted_count += 1

    return deleted_count


def get_class_distribution(data: dict) -> Dict[str, int]:
    """Get class distribution from annotations."""
    categories = {cat['id']: cat['name'] for cat in data['categories']}
    class_counts = defaultdict(int)

    for ann in data['annotations']:
        cat_name = categories[ann['category_id']]
        class_counts[cat_name] += 1

    return dict(class_counts)


def get_source_distribution(data: dict) -> Dict[str, int]:
    """Get source distribution from images."""
    source_counts = defaultdict(int)

    for img in data['images']:
        source = img.get('source', 'unknown')
        source_counts[source] += 1

    return dict(source_counts)


def main(dry_run: bool = True):
    """Main function to extract RSUD data from all splits."""
    print("=" * 60)
    print("Golden-VRU v9.0: Extract RSUD20K Data")
    print("=" * 60)
    print(f"\nSource to remove: {SOURCE_TO_REMOVE}")
    print(f"Output directory: {RSUD_OUTPUT_DIR}")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print()

    all_stats = {}
    total_stats = {
        'original_images': 0,
        'original_annotations': 0,
        'rsud_images': 0,
        'rsud_annotations': 0,
        'remaining_images': 0,
        'remaining_annotations': 0,
    }

    for split in SPLITS:
        print(f"\nProcessing {split}...")
        print("-" * 40)

        # Load annotations
        data = load_coco_annotations(split)
        print(f"  Original: {len(data['images']):,} images, {len(data['annotations']):,} annotations")

        # Show source distribution before
        source_dist = get_source_distribution(data)
        print(f"  Sources: {source_dist}")

        # Separate RSUD data
        remaining_data, rsud_data, stats = separate_rsud_data(data)
        all_stats[split] = stats

        # Update totals
        for key in total_stats:
            total_stats[key] += stats[key]

        print(f"  RSUD to extract: {stats['rsud_images']:,} images, {stats['rsud_annotations']:,} annotations")
        print(f"  Remaining: {stats['remaining_images']:,} images, {stats['remaining_annotations']:,} annotations")

        # Show class distribution for remaining
        class_dist = get_class_distribution(remaining_data)
        total_ann = sum(class_dist.values())
        if total_ann > 0:
            print(f"  Remaining class dist: pedestrian {class_dist.get('pedestrian', 0):,} "
                  f"({class_dist.get('pedestrian', 0)/total_ann*100:.1f}%), "
                  f"cyclist {class_dist.get('cyclist', 0):,} "
                  f"({class_dist.get('cyclist', 0)/total_ann*100:.1f}%)")

        if not dry_run:
            # Create backup
            create_backup(split)

            # Copy RSUD images to output directory
            copied = copy_rsud_images(split, stats['rsud_files'], dry_run=False)
            print(f"  Copied: {copied} RSUD images to {RSUD_OUTPUT_DIR / split}")

            # Save RSUD annotations
            rsud_ann_path = RSUD_OUTPUT_DIR / split / '_annotations.coco.json'
            save_coco_annotations(rsud_data, rsud_ann_path)
            print(f"  Saved: RSUD annotations to {rsud_ann_path}")

            # Delete RSUD images from golden-vru
            deleted = delete_rsud_images(split, stats['rsud_files'], dry_run=False)
            print(f"  Deleted: {deleted} RSUD images from golden-vru")

            # Update golden-vru annotations
            save_coco_annotations(remaining_data, BASE_DIR / split / '_annotations.coco.json')
            print(f"  Saved: Updated golden-vru annotations")

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"\nOriginal dataset: {total_stats['original_images']:,} images, "
          f"{total_stats['original_annotations']:,} annotations")
    print(f"\nRSUD extracted: {total_stats['rsud_images']:,} images, "
          f"{total_stats['rsud_annotations']:,} annotations")
    print(f"\nRemaining (v9.0): {total_stats['remaining_images']:,} images, "
          f"{total_stats['remaining_annotations']:,} annotations")

    # Print per-split summary table
    print("\n" + "-" * 60)
    print(f"{'Split':<8} {'Original':>12} {'RSUD':>10} {'Remaining':>12}")
    print("-" * 60)

    for split in SPLITS:
        stats = all_stats[split]
        print(f"{split.capitalize():<8} {stats['original_images']:>12,} "
              f"{stats['rsud_images']:>10,} {stats['remaining_images']:>12,}")

    print("-" * 60)
    print(f"{'Total':<8} {total_stats['original_images']:>12,} "
          f"{total_stats['rsud_images']:>10,} {total_stats['remaining_images']:>12,}")

    # Verify expected counts
    print("\n" + "-" * 60)
    print("VERIFICATION")
    print("-" * 60)

    expected_remaining = 69896
    expected_rsud = 15961
    actual_remaining = total_stats['remaining_images']
    actual_rsud = total_stats['rsud_images']

    if actual_remaining == expected_remaining:
        print(f"[PASS] Remaining images: {actual_remaining:,} (expected {expected_remaining:,})")
    else:
        print(f"[WARN] Remaining images: {actual_remaining:,} (expected {expected_remaining:,})")

    if actual_rsud == expected_rsud:
        print(f"[PASS] RSUD images: {actual_rsud:,} (expected {expected_rsud:,})")
    else:
        print(f"[WARN] RSUD images: {actual_rsud:,} (expected {expected_rsud:,})")

    if dry_run:
        print("\n*** DRY RUN - No changes were made ***")
        print("Run with --apply to make changes")
    else:
        print("\n*** Changes applied successfully ***")
        print(f"\nRSUD data extracted to: {RSUD_OUTPUT_DIR}")
        print("\nNext steps:")
        print("  1. Run: python validate_dataset.py")
        print("  2. Update STATS.md and DATASET_REPORT.md")
        print("  3. Run: python analyze_distributions.py")
        print("  4. Run: dvc add train valid test")
        print("  5. Run: git add -A && git commit -m 'v9.0: Remove RSUD20K data'")
        print("  6. Run: git tag v9.0")
        print("  7. Run: dvc push")


if __name__ == '__main__':
    import sys

    dry_run = '--apply' not in sys.argv

    if dry_run:
        print("Running in DRY RUN mode. Use --apply to make changes.\n")

    main(dry_run=dry_run)
