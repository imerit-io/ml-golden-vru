# Golden VRU Dataset Statistics

Generated: 2026-01-27

## Current Version: v7.0 (Medium + Large Objects Only)

This dataset is designed for training RF-DETR models on Vulnerable Road User (VRU) detection.
Small objects (area < 32x32 = 1024 px²) have been removed to focus on medium and large VRUs.

## Dataset Summary

| Split | Images | Annotations | Pedestrian | Cyclist |
|-------|--------|-------------|------------|---------|
| Train | 32,106 | 113,658 | 83,284 (73.3%) | 30,374 (26.7%) |
| Valid | 4,041 | 14,590 | 10,644 (73.0%) | 3,946 (27.0%) |
| Test | 4,033 | 14,964 | 11,105 (74.2%) | 3,859 (25.8%) |
| **Total** | **40,180** | **143,212** | **104,933 (73.3%)** | **38,279 (26.7%)** |

## Size Distribution

| Split | Medium (32²-96² px) | Large (>96² px) |
|-------|---------------------|-----------------|
| Train | 75,163 (66.1%) | 38,495 (33.9%) |
| Valid | 9,769 (67.0%) | 4,821 (33.0%) |
| Test | 9,824 (65.7%) | 5,140 (34.3%) |
| **Total** | **94,756 (66.2%)** | **48,456 (33.8%)** |

## Image Resolution

| Source | Resolution | Images | Percentage |
|--------|------------|--------|------------|
| BDD100K | 1280 x 720 | 27,775 | 59.2% |
| Cityscapes | 2048 x 1024 | 3,067 | 6.5% |
| RSUD20K | 1920 x 1080 | 16,042 | 34.2% |

## Categories

| ID | Name | Description |
|----|------|-------------|
| 0 | pedestrian | Walking pedestrians |
| 1 | cyclist | Bicycles, motorcycles, and riders |

## Version History

### v7.0 - Medium + Large Objects Only (current)
Git tag: `v7.0-medium-large-only`

Removed small objects (area < 32x32 = 1024 px²) from v6.0 to focus on medium and large VRUs.
Images with no remaining annotations after filtering were also removed.

| Metric | v6.0 | v7.0 | Change |
|--------|------|------|--------|
| Images | 46,884 | 40,180 | -14.3% |
| Annotations | 207,813 | 143,212 | -31.1% |
| Small objects | 64,601 | 0 | -100% |
| Cyclist ratio | 21.7% | 26.7% | +5.0% |

| Split | Images | Annotations | Pedestrian | Cyclist |
|-------|--------|-------------|------------|---------|
| Train | 32,106 | 113,658 | 83,284 (73.3%) | 30,374 (26.7%) |
| Valid | 4,041 | 14,590 | 10,644 (73.0%) | 3,946 (27.0%) |
| Test | 4,033 | 14,964 | 11,105 (74.2%) | 3,859 (25.8%) |
| **Total** | **40,180** | **143,212** | **104,933 (73.3%)** | **38,279 (26.7%)** |

### v6.0 - 80/10/10 Split
Git tag: `v6.0-80-10-10-split`

Re-split dataset to standard 80/10/10 ratios using stratified sampling to maintain:
- Source distribution (BDD100K, Cityscapes, RSUD20K)
- Class distribution (pedestrian vs cyclist)
- Lighting distribution (dark, dim, normal, bright)

| Split | BDD100K | Cityscapes | RSUD20K | Total Images | Annotations |
|-------|---------|------------|---------|--------------|-------------|
| Train | 22,220 | 2,453 | 12,834 | 37,507 | 165,311 |
| Valid | 2,777 | 307 | 1,604 | 4,688 | 21,016 |
| Test | 2,778 | 307 | 1,604 | 4,689 | 21,486 |
| **Total** | **27,775** | **3,067** | **16,042** | **46,884** | **207,813** |

### v5.0 - BDD100K + Cityscapes + RSUD20K
Git tag: `v5.0-bdd-cityscapes-rsud`

Added RSUD20K data for South Asian traffic scene diversity.

| Split | BDD100K | Cityscapes | RSUD20K | Total Images | Annotations |
|-------|---------|------------|---------|--------------|-------------|
| Train | 24,258 | 2,616 | 14,716 | 41,590 | 182,403 |
| Valid | 2,461 | 0 | 795 | 3,256 | 13,539 |
| Test | 1,056 | 451 | 531 | 2,038 | 11,871 |
| **Total** | **27,775** | **3,067** | **16,042** | **46,884** | **207,813** |

### v4.0 - BDD100K + Cityscapes
Git tag: `v4.0-bdd-cityscapes`

| Split | Images | Annotations |
|-------|--------|-------------|
| Train | 26,874 | 132,002 |
| Valid | 2,461 | 10,616 |
| Test | 1,507 | 10,397 |
| **Total** | **30,842** | **153,015** |

### v3.0 - BDD100K Only
Git tag: `v3.0-bdd100k-only`

| Split | Images | Annotations |
|-------|--------|-------------|
| Train | 24,258 | 106,153 |
| Valid | 2,461 | 10,616 |
| Test | 1,056 | 4,754 |
| **Total** | **27,775** | **121,523** |

### v2.0 - BDD100K + nuScenes (archived)
Git tag: `v2.0-bdd100k-nuscenes`

**Note:** This version is no longer available in DVC remote storage.

### v1.0 - BDD100K Only (legacy)
Git tag: `v1.0-bdd100k-only`

## Data Sources

### BDD100K
- **License**: BSD 3-Clause
- **Image Resolution**: 1280 x 720
- **Geographic**: United States driving scenes
- **Images included**: Only those with VRU annotations

### Cityscapes
- **License**: Custom (research use)
- **Image Resolution**: 2048 x 1024
- **Geographic**: European urban scenes (Germany)
- **Images included**: Only those with VRU annotations

### RSUD20K
- **License**: Custom (research use)
- **Image Resolution**: 1920 x 1080
- **Geographic**: South Asian urban scenes (Bangladesh)
- **Images included**: Only those with VRU annotations

## File Structure

```
golden-vru/
├── train/
│   ├── _annotations.coco.json
│   └── [37,507 images]
├── valid/
│   ├── _annotations.coco.json
│   └── [4,688 images]
├── test/
│   ├── _annotations.coco.json
│   └── [4,689 images]
├── analysis/
│   └── [distribution charts]
├── STATS.md
└── DATASET_REPORT.md
```

## Image Naming

- **BDD100K**: `{video_id}-{frame_id}.jpg`
- **Cityscapes**: `cityscapes_{city}_{sequence}_{frame}.png`
- **RSUD20K**: `rsud_{split}{index}.jpg`

## Annotation Format

COCO Detection format with:
- `bbox`: [x, y, width, height] (top-left corner + dimensions)
- `category_id`: 0 (pedestrian) or 1 (cyclist)
- `area`: width * height
- `iscrowd`: 0
- `source`: "bdd100k", "cityscapes", or "rsud20k"

## Usage

```python
from pycocotools.coco import COCO

# Load annotations
coco_train = COCO("golden-vru/train/_annotations.coco.json")
coco_valid = COCO("golden-vru/valid/_annotations.coco.json")
coco_test = COCO("golden-vru/test/_annotations.coco.json")

# Get all image IDs
img_ids = coco_train.getImgIds()

# Get annotations for an image
ann_ids = coco_train.getAnnIds(imgIds=[img_ids[0]])
anns = coco_train.loadAnns(ann_ids)
```

## Version Control with DVC

Dataset is tracked with DVC for efficient versioning.

### Download Dataset

```bash
git clone <repo-url>
dvc pull
```

### Switch Versions

```bash
git checkout v4.0-bdd-cityscapes
dvc checkout
```

### Storage

- **S3 Remote**: `s3://imerit-ml-data-playground/data/golden-vru/`
- **Total size**: ~21 GB

## Notes

1. Mixed resolutions require handling during training (resize/padding)
2. Cityscapes val split is used for golden-vru test (annotations not available for Cityscapes test)
3. Better cyclist representation with RSUD20K (21.7% vs 17% in v4.0)
4. Geographic diversity: USA (BDD), Europe (Cityscapes), South Asia (RSUD)
5. v6.0 uses stratified sampling to ensure consistent class distribution across all splits (~78% pedestrian, ~22% cyclist)

## Detailed Analysis

For comprehensive analysis including training recommendations and dataset comparisons, see [DATASET_REPORT.md](./DATASET_REPORT.md).
