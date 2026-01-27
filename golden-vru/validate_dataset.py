#!/usr/bin/env python3
"""
Validate Golden-VRU dataset integrity.

Checks:
1. All image files referenced in annotations exist
2. All annotations have valid category IDs
3. No small objects remain (area >= 1024)
4. Image counts match annotation file
5. Annotation counts are consistent
"""

import json
import os
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

# Constants
BASE_DIR = Path(__file__).parent
SPLITS = ['train', 'valid', 'test']
SIZE_THRESHOLD = 32 * 32  # 1024 pixels


def load_coco_annotations(split: str) -> dict:
    """Load COCO annotations for a split."""
    ann_path = BASE_DIR / split / '_annotations.coco.json'
    with open(ann_path, 'r') as f:
        return json.load(f)


def validate_split(split: str) -> Tuple[bool, List[str]]:
    """Validate a single split."""
    errors = []
    warnings = []

    print(f"\nValidating {split}...")
    print("-" * 40)

    # Load annotations
    data = load_coco_annotations(split)
    split_dir = BASE_DIR / split

    # Get valid category IDs
    valid_cat_ids = {cat['id'] for cat in data['categories']}
    categories = {cat['id']: cat['name'] for cat in data['categories']}
    print(f"  Categories: {categories}")

    # Build image ID to filename mapping
    image_id_to_file = {img['id']: img['file_name'] for img in data['images']}
    image_ids_in_annotations = set(image_id_to_file.keys())

    # Check 1: All image files exist
    print(f"  Checking image files exist...")
    missing_files = 0
    for img in data['images']:
        file_path = split_dir / img['file_name']
        if not file_path.exists():
            missing_files += 1
            if missing_files <= 5:
                errors.append(f"Missing image file: {img['file_name']}")

    if missing_files > 5:
        errors.append(f"... and {missing_files - 5} more missing files")

    if missing_files == 0:
        print(f"  [PASS] All {len(data['images']):,} image files exist")
    else:
        print(f"  [FAIL] {missing_files:,} image files missing")

    # Check 2: Count actual image files in directory
    print(f"  Checking image file count...")
    actual_files = list(split_dir.glob('*.jpg')) + list(split_dir.glob('*.png'))
    actual_count = len(actual_files)
    expected_count = len(data['images'])

    if actual_count == expected_count:
        print(f"  [PASS] Image count matches: {actual_count:,}")
    else:
        diff = actual_count - expected_count
        if diff > 0:
            warnings.append(f"Extra image files: {diff} files not in annotations")
            print(f"  [WARN] {diff:,} extra image files not in annotations")
        else:
            errors.append(f"Missing image files: {-diff} files referenced but not found")
            print(f"  [FAIL] {-diff:,} image files missing")

    # Check 3: All annotations reference valid images
    print(f"  Checking annotation image references...")
    invalid_image_refs = 0
    for ann in data['annotations']:
        if ann['image_id'] not in image_ids_in_annotations:
            invalid_image_refs += 1

    if invalid_image_refs == 0:
        print(f"  [PASS] All annotations reference valid images")
    else:
        errors.append(f"Invalid image references: {invalid_image_refs}")
        print(f"  [FAIL] {invalid_image_refs:,} annotations reference invalid images")

    # Check 4: All annotations have valid category IDs
    print(f"  Checking category IDs...")
    invalid_cat_ids = 0
    for ann in data['annotations']:
        if ann['category_id'] not in valid_cat_ids:
            invalid_cat_ids += 1

    if invalid_cat_ids == 0:
        print(f"  [PASS] All annotations have valid category IDs")
    else:
        errors.append(f"Invalid category IDs: {invalid_cat_ids}")
        print(f"  [FAIL] {invalid_cat_ids:,} annotations have invalid category IDs")

    # Check 5: No small objects remain
    print(f"  Checking for small objects (area < {SIZE_THRESHOLD})...")
    small_objects = 0
    for ann in data['annotations']:
        if ann['area'] < SIZE_THRESHOLD:
            small_objects += 1

    if small_objects == 0:
        print(f"  [PASS] No small objects found")
    else:
        errors.append(f"Small objects found: {small_objects}")
        print(f"  [FAIL] {small_objects:,} small objects still in dataset")

    # Check 6: All annotations have required fields
    print(f"  Checking annotation fields...")
    required_fields = ['id', 'image_id', 'category_id', 'bbox', 'area']
    missing_fields = defaultdict(int)

    for ann in data['annotations']:
        for field in required_fields:
            if field not in ann:
                missing_fields[field] += 1

    if not missing_fields:
        print(f"  [PASS] All required fields present")
    else:
        for field, count in missing_fields.items():
            errors.append(f"Missing field '{field}': {count} annotations")
        print(f"  [FAIL] Missing required fields")

    # Summary statistics
    print(f"\n  Summary:")
    print(f"    Images: {len(data['images']):,}")
    print(f"    Annotations: {len(data['annotations']):,}")

    class_counts = defaultdict(int)
    size_counts = {'medium': 0, 'large': 0}
    SIZE_MEDIUM = 96 * 96

    for ann in data['annotations']:
        cat_name = categories.get(ann['category_id'], 'unknown')
        class_counts[cat_name] += 1

        if ann['area'] < SIZE_MEDIUM:
            size_counts['medium'] += 1
        else:
            size_counts['large'] += 1

    total = sum(class_counts.values())
    for cat_name, count in sorted(class_counts.items()):
        pct = count / total * 100 if total > 0 else 0
        print(f"    {cat_name}: {count:,} ({pct:.1f}%)")

    print(f"    Size: medium {size_counts['medium']:,}, large {size_counts['large']:,}")

    is_valid = len(errors) == 0
    return is_valid, errors, warnings


def main():
    """Main validation function."""
    print("=" * 60)
    print("Golden-VRU Dataset Validation")
    print("=" * 60)

    all_valid = True
    all_errors = []
    all_warnings = []

    for split in SPLITS:
        is_valid, errors, warnings = validate_split(split)
        if not is_valid:
            all_valid = False
            all_errors.extend([f"[{split}] {e}" for e in errors])
        all_warnings.extend([f"[{split}] {w}" for w in warnings])

    print("\n" + "=" * 60)
    print("VALIDATION RESULT")
    print("=" * 60)

    if all_warnings:
        print("\nWarnings:")
        for w in all_warnings:
            print(f"  - {w}")

    if all_errors:
        print("\nErrors:")
        for e in all_errors:
            print(f"  - {e}")

    if all_valid:
        print("\n[PASSED] Dataset validation successful!")
        return 0
    else:
        print(f"\n[FAILED] Dataset validation failed with {len(all_errors)} error(s)")
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
