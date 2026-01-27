#!/usr/bin/env python3
"""
Filter small objects from Golden-VRU dataset.

Creates v7.0 by removing annotations with area < 32² (1024 px²)
and removing images that have no remaining annotations.
"""

import json
import os
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

# Constants
BASE_DIR = Path(__file__).parent
SPLITS = ['train', 'valid', 'test']
SIZE_THRESHOLD = 32 * 32  # 1024 pixels - COCO small object threshold


def load_coco_annotations(split: str) -> dict:
    """Load COCO annotations for a split."""
    ann_path = BASE_DIR / split / '_annotations.coco.json'
    with open(ann_path, 'r') as f:
        return json.load(f)


def save_coco_annotations(data: dict, split: str, backup: bool = True):
    """Save COCO annotations for a split."""
    ann_path = BASE_DIR / split / '_annotations.coco.json'

    # Create backup
    if backup:
        backup_path = BASE_DIR / split / '_annotations.coco.v6.0.json'
        if not backup_path.exists():
            shutil.copy(ann_path, backup_path)
            print(f"  Backup created: {backup_path.name}")

    with open(ann_path, 'w') as f:
        json.dump(data, f)


def filter_small_objects(data: dict) -> Tuple[dict, Dict[str, int]]:
    """
    Filter out small objects (area < 32²) from COCO annotations.

    Returns:
        Tuple of (filtered_data, statistics)
    """
    stats = {
        'original_annotations': len(data['annotations']),
        'original_images': len(data['images']),
        'removed_annotations': 0,
        'removed_images': 0,
        'small_pedestrian': 0,
        'small_cyclist': 0,
    }

    # Get category mapping
    categories = {cat['id']: cat['name'] for cat in data['categories']}

    # Filter annotations
    filtered_annotations = []
    for ann in data['annotations']:
        if ann['area'] >= SIZE_THRESHOLD:
            filtered_annotations.append(ann)
        else:
            stats['removed_annotations'] += 1
            cat_name = categories.get(ann['category_id'], 'unknown')
            if cat_name == 'pedestrian':
                stats['small_pedestrian'] += 1
            elif cat_name == 'cyclist':
                stats['small_cyclist'] += 1

    # Get image IDs that still have annotations
    image_ids_with_annotations = set(ann['image_id'] for ann in filtered_annotations)

    # Filter images
    filtered_images = []
    removed_image_files = []
    for img in data['images']:
        if img['id'] in image_ids_with_annotations:
            filtered_images.append(img)
        else:
            stats['removed_images'] += 1
            removed_image_files.append(img['file_name'])

    # Create filtered data
    filtered_data = {
        'categories': data['categories'],
        'images': filtered_images,
        'annotations': filtered_annotations,
    }

    # Copy over any additional keys (like 'info', 'licenses')
    for key in data:
        if key not in filtered_data:
            filtered_data[key] = data[key]

    stats['final_annotations'] = len(filtered_annotations)
    stats['final_images'] = len(filtered_images)
    stats['removed_image_files'] = removed_image_files

    return filtered_data, stats


def remove_image_files(split: str, file_names: List[str], dry_run: bool = False):
    """Remove image files from the split directory."""
    split_dir = BASE_DIR / split
    removed_count = 0

    for file_name in file_names:
        file_path = split_dir / file_name
        if file_path.exists():
            if not dry_run:
                os.remove(file_path)
            removed_count += 1

    return removed_count


def get_class_distribution(data: dict) -> Dict[str, int]:
    """Get class distribution from annotations."""
    categories = {cat['id']: cat['name'] for cat in data['categories']}
    class_counts = defaultdict(int)

    for ann in data['annotations']:
        cat_name = categories[ann['category_id']]
        class_counts[cat_name] += 1

    return dict(class_counts)


def get_size_distribution(data: dict) -> Dict[str, int]:
    """Get size distribution from annotations."""
    SIZE_MEDIUM = 96 * 96
    size_counts = {'small': 0, 'medium': 0, 'large': 0}

    for ann in data['annotations']:
        area = ann['area']
        if area < SIZE_THRESHOLD:
            size_counts['small'] += 1
        elif area < SIZE_MEDIUM:
            size_counts['medium'] += 1
        else:
            size_counts['large'] += 1

    return size_counts


def main(dry_run: bool = False):
    """Main function to filter small objects from all splits."""
    print("=" * 60)
    print("Golden-VRU v7.0: Filtering Small Objects")
    print("=" * 60)
    print(f"\nThreshold: area < {SIZE_THRESHOLD} px² (32x32)")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print()

    all_stats = {}
    total_stats = {
        'original_annotations': 0,
        'original_images': 0,
        'removed_annotations': 0,
        'removed_images': 0,
        'final_annotations': 0,
        'final_images': 0,
        'small_pedestrian': 0,
        'small_cyclist': 0,
    }

    for split in SPLITS:
        print(f"\nProcessing {split}...")
        print("-" * 40)

        # Load annotations
        data = load_coco_annotations(split)
        print(f"  Original: {len(data['images']):,} images, {len(data['annotations']):,} annotations")

        # Filter small objects
        filtered_data, stats = filter_small_objects(data)
        all_stats[split] = stats

        # Update totals
        for key in total_stats:
            if key in stats:
                total_stats[key] += stats[key]

        print(f"  Removed: {stats['removed_annotations']:,} annotations "
              f"({stats['small_pedestrian']:,} pedestrian, {stats['small_cyclist']:,} cyclist)")
        print(f"  Removed: {stats['removed_images']:,} images (no remaining annotations)")
        print(f"  Final: {stats['final_images']:,} images, {stats['final_annotations']:,} annotations")

        # Get new distributions
        class_dist = get_class_distribution(filtered_data)
        size_dist = get_size_distribution(filtered_data)

        total_ann = sum(class_dist.values())
        print(f"  Class distribution: pedestrian {class_dist.get('pedestrian', 0):,} "
              f"({class_dist.get('pedestrian', 0)/total_ann*100:.1f}%), "
              f"cyclist {class_dist.get('cyclist', 0):,} "
              f"({class_dist.get('cyclist', 0)/total_ann*100:.1f}%)")
        print(f"  Size distribution: small {size_dist['small']:,}, "
              f"medium {size_dist['medium']:,}, large {size_dist['large']:,}")

        if not dry_run:
            # Save filtered annotations
            save_coco_annotations(filtered_data, split)
            print(f"  Saved: _annotations.coco.json")

            # Remove image files
            if stats['removed_image_files']:
                removed = remove_image_files(split, stats['removed_image_files'])
                print(f"  Deleted: {removed} image files")

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"\nTotal annotations removed: {total_stats['removed_annotations']:,} "
          f"({total_stats['removed_annotations']/total_stats['original_annotations']*100:.1f}%)")
    print(f"  - Pedestrian: {total_stats['small_pedestrian']:,}")
    print(f"  - Cyclist: {total_stats['small_cyclist']:,}")
    print(f"\nTotal images removed: {total_stats['removed_images']:,} "
          f"({total_stats['removed_images']/total_stats['original_images']*100:.1f}%)")
    print(f"\nFinal dataset:")
    print(f"  - Images: {total_stats['final_images']:,}")
    print(f"  - Annotations: {total_stats['final_annotations']:,}")

    # Print per-split summary table
    print("\n" + "-" * 60)
    print(f"{'Split':<8} {'Images':>10} {'Annotations':>12} {'Pedestrian':>12} {'Cyclist':>10}")
    print("-" * 60)

    for split in SPLITS:
        data = load_coco_annotations(split) if not dry_run else None
        if dry_run:
            # Recalculate from stats
            imgs = all_stats[split]['final_images']
            anns = all_stats[split]['final_annotations']
            # We'd need to track these separately for dry run
            print(f"{split.capitalize():<8} {imgs:>10,} {anns:>12,}")
        else:
            class_dist = get_class_distribution(data)
            total = sum(class_dist.values())
            ped = class_dist.get('pedestrian', 0)
            cyc = class_dist.get('cyclist', 0)
            print(f"{split.capitalize():<8} {len(data['images']):>10,} {total:>12,} "
                  f"{ped:>12,} ({ped/total*100:.1f}%) {cyc:>10,} ({cyc/total*100:.1f}%)")

    print("-" * 60)

    if dry_run:
        print("\n*** DRY RUN - No changes were made ***")
        print("Run with --apply to make changes")
    else:
        print("\n*** Changes applied successfully ***")
        print("\nNext steps:")
        print("  1. Update STATS.md with new v7.0 statistics")
        print("  2. Run: git add -A && git commit -m 'v7.0: Remove small objects'")
        print("  3. Run: git tag v7.0-medium-large-only")
        print("  4. Run: dvc add train valid test")
        print("  5. Run: dvc push")


if __name__ == '__main__':
    import sys

    dry_run = '--apply' not in sys.argv

    if dry_run:
        print("Running in DRY RUN mode. Use --apply to make changes.\n")

    main(dry_run=dry_run)
