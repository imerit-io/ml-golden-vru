# Golden VRU Dataset Statistics

Generated: 2026-01-29

## Current Version: v9.0 (BDD100K + Cityscapes + nuImages)

This dataset is designed for training RF-DETR models on Vulnerable Road User (VRU) detection.
Small objects (area < 32x32 = 1024 px²) have been removed to focus on medium and large VRUs.

## Dataset Summary

| Split | Images | Annotations | Pedestrian | Cyclist |
|-------|--------|-------------|------------|---------|
| Train | 55,878 | 178,492 | 138,806 (77.8%) | 39,686 (22.2%) |
| Valid | 7,013 | 22,886 | 17,817 (77.9%) | 5,069 (22.1%) |
| Test | 7,005 | 22,474 | 17,457 (77.7%) | 5,017 (22.3%) |
| **Total** | **69,896** | **223,852** | **174,080 (77.8%)** | **49,772 (22.2%)** |

## Size Distribution

| Split | Medium (32²-96² px) | Large (>96² px) |
|-------|---------------------|-----------------|
| Train | 142,624 (79.9%) | 35,868 (20.1%) |
| Valid | 18,400 (80.4%) | 4,486 (19.6%) |
| Test | 17,900 (79.7%) | 4,574 (20.3%) |
| **Total** | **178,924 (79.9%)** | **44,928 (20.1%)** |

## Image Resolution

| Source | Resolution | Images | Percentage |
|--------|------------|--------|------------|
| nuImages | 1600 x 900 | 45,677 | 65.3% |
| BDD100K | 1280 x 720 | 21,326 | 30.5% |
| Cityscapes | 2048 x 1024 | 2,893 | 4.1% |

## Source Distribution by Split

| Split | BDD100K | Cityscapes | nuImages | Total |
|-------|---------|------------|----------|-------|
| Train | 17,017 (30.5%) | 2,320 (4.2%) | 36,541 (65.4%) | 55,878 |
| Valid | 2,156 (30.7%) | 289 (4.1%) | 4,568 (65.1%) | 7,013 |
| Test | 2,153 (30.7%) | 284 (4.1%) | 4,568 (65.2%) | 7,005 |
| **Total** | **21,326 (30.5%)** | **2,893 (4.1%)** | **45,677 (65.3%)** | **69,896** |

## Categories

| ID | Name | Description |
|----|------|-------------|
| 0 | pedestrian | Walking pedestrians |
| 1 | cyclist | Bicycles, motorcycles, and riders |

## Version History

### v9.0 - Removed RSUD20K (current)
Git tag: `v9.0`

Removed RSUD20K data due to annotation quality concerns. RSUD images extracted to `/mnt/data/rsud-vru/`.

| Metric | v8.0 | v9.0 | Change |
|--------|------|------|--------|
| Images | 85,857 | 69,896 | -18.6% |
| Annotations | 277,788 | 223,852 | -19.4% |
| Sources | 4 | 3 | -1 |
| Cyclist ratio | 24.6% | 22.2% | -2.4% |

| Split | Images | Annotations | Pedestrian | Cyclist |
|-------|--------|-------------|------------|---------|
| Train | 55,878 | 178,492 | 138,806 (77.8%) | 39,686 (22.2%) |
| Valid | 7,013 | 22,886 | 17,817 (77.9%) | 5,069 (22.1%) |
| Test | 7,005 | 22,474 | 17,457 (77.7%) | 5,017 (22.3%) |
| **Total** | **69,896** | **223,852** | **174,080 (77.8%)** | **49,772 (22.2%)** |

### v8.0 - Added nuImages
Git tag: `v8.0`

Added nuImages VRU data for Singapore and Boston geographic coverage.

| Metric | v7.0 | v8.0 | Change |
|--------|------|------|--------|
| Images | 40,180 | 85,857 | +113.7% |
| Annotations | 143,212 | 277,788 | +94.0% |
| Sources | 3 | 4 | +1 |
| Cyclist ratio | 26.7% | 24.6% | -2.1% |

| Split | Images | Annotations | Pedestrian | Cyclist |
|-------|--------|-------------|------------|---------|
| Train | 68,647 | 221,578 | 167,055 (75.4%) | 54,523 (24.6%) |
| Valid | 8,609 | 28,191 | 21,291 (75.5%) | 6,900 (24.5%) |
| Test | 8,601 | 28,019 | 21,107 (75.3%) | 6,912 (24.7%) |
| **Total** | **85,857** | **277,788** | **209,453 (75.4%)** | **68,335 (24.6%)** |

### v7.0 - Medium + Large Objects Only
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

### nuImages
- **License**: CC BY-NC-SA 4.0
- **Image Resolution**: 1600 x 900
- **Geographic**: Singapore and Boston driving scenes
- **Images included**: Only those with VRU annotations (medium/large objects only)

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

## File Structure

```
golden-vru/
├── train/
│   ├── _annotations.coco.json
│   └── [55,878 images]
├── valid/
│   ├── _annotations.coco.json
│   └── [7,013 images]
├── test/
│   ├── _annotations.coco.json
│   └── [7,005 images]
├── analysis/
│   └── [distribution charts]
├── STATS.md
└── DATASET_REPORT.md
```

## Image Naming

- **BDD100K**: `{video_id}-{frame_id}.jpg`
- **Cityscapes**: `cityscapes_{city}_{sequence}_{frame}.png`
- **nuImages**: `nuimages_{camera}_{timestamp}.jpg`

## Annotation Format

COCO Detection format with:
- `bbox`: [x, y, width, height] (top-left corner + dimensions)
- `category_id`: 0 (pedestrian) or 1 (cyclist)
- `area`: width * height
- `iscrowd`: 0
- `source`: "bdd100k", "cityscapes", or "nuimages"

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
- **Total size**: ~38 GB

## Baseline (v7.0 Test)

YOLOv8x (COCO person class): mAP@50=0.478, F1=0.578

## Notes

1. Mixed resolutions require handling during training (resize/padding)
2. Cityscapes val split is used for golden-vru test (annotations not available for Cityscapes test)
3. Geographic diversity: USA (BDD), Europe (Cityscapes), Singapore/Boston (nuImages)
4. v9.0 removes RSUD20K data (15,961 images) due to annotation quality concerns

## Detailed Analysis

For comprehensive analysis including training recommendations and dataset comparisons, see [DATASET_REPORT.md](./DATASET_REPORT.md).
