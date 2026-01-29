# Golden-VRU Dataset Analysis Report

Generated: 2026-01-29

## Executive Summary

The Golden-VRU dataset is a curated multi-source dataset for Vulnerable Road User (VRU) detection, combining images from BDD100K, Cityscapes, and nuImages. This dataset contains only images with pedestrian and/or cyclist annotations, making it ideal for training object detection models targeting VRUs.

**v9.0 Update:** Removed RSUD20K data due to annotation quality concerns. Small objects (area < 32x32 = 1024 px²) remain filtered out.

### Dataset Overview

| Split | Images | Annotations | Pedestrians | Cyclists |
|-------|--------|-------------|-------------|----------|
| Train | 55,878 | 178,492 | 138,806 (77.8%) | 39,686 (22.2%) |
| Valid | 7,013 | 22,886 | 17,817 (77.9%) | 5,069 (22.1%) |
| Test | 7,005 | 22,474 | 17,457 (77.7%) | 5,017 (22.3%) |
| **Total** | **69,896** | **223,852** | **174,080 (77.8%)** | **49,772 (22.2%)** |

**Key Characteristics:**
- Multi-resolution: 1600x900 (nuImages), 1280x720 (BDD100K), 2048x1024 (Cityscapes)
- Sources: nuImages (Singapore/Boston), BDD100K (USA), Cityscapes (Europe)
- Average annotations per image: 3.2
- Balanced class distribution across splits (~78% pedestrian, ~22% cyclist)
- **No small objects** - only medium (32²-96² px) and large (>96² px) annotations
- 80/10/10 train/valid/test split

---

## 1. Data Format

### COCO Detection Format

```json
{
  "categories": [
    {"id": 0, "name": "pedestrian", "supercategory": "person"},
    {"id": 1, "name": "cyclist", "supercategory": "vehicle"}
  ],
  "images": [
    {"id": int, "file_name": str, "width": int, "height": int, "source": str}
  ],
  "annotations": [
    {"id": int, "image_id": int, "category_id": int, "bbox": [x, y, w, h], "area": float, "iscrowd": int}
  ]
}
```

### Class Definitions

| ID | Name | Description | Source Mapping |
|----|------|-------------|----------------|
| 0 | pedestrian | Walking pedestrians | BDD100K: pedestrian, Cityscapes: person, nuImages: human.pedestrian.* |
| 1 | cyclist | Bicycles, motorcycles, and riders | BDD100K: rider/bike/motor, Cityscapes: rider/bicycle/motorcycle, nuImages: vehicle.bicycle/motorcycle |

---

## 2. Annotation Size Distribution

COCO size thresholds: small < 32², medium 32²-96², large > 96²

**v9.0: Small objects removed** - Only medium and large annotations remain.

| Split | Small (<1024 px²) | Medium (1024-9216 px²) | Large (>9216 px²) |
|-------|-------------------|------------------------|-------------------|
| Train | 0 (0%) | 142,624 (79.9%) | 35,868 (20.1%) |
| Valid | 0 (0%) | 18,400 (80.4%) | 4,486 (19.6%) |
| Test | 0 (0%) | 17,900 (79.7%) | 4,574 (20.3%) |

**Observations:**
1. **No small objects** - All annotations with area < 1024 px² have been removed
2. **Medium-dominant** - Approximately 80% medium, 20% large
3. **Consistent across splits** - Size distribution is consistent across all splits

---

## 3. Annotation Density Distribution

| Split | Sparse (1-3) | Moderate (4-10) | Dense (11-20) | Very Dense (>20) |
|-------|--------------|-----------------|---------------|------------------|
| Train | 70.3% | 26.2% | 3.0% | 0.5% |
| Valid | 69.8% | 26.5% | 3.0% | 0.7% |
| Test | 69.5% | 27.2% | 2.7% | 0.5% |

**Observations:**
1. **Predominantly sparse scenes** - ~70% of images have 1-3 VRU annotations
2. **Consistent density** - Nearly identical distribution across all splits
3. **Typical driving scenarios** - Reflects real-world distribution

---

## 4. Image Resolution

| Source | Resolution | Aspect Ratio | Images | Percentage |
|--------|------------|--------------|--------|------------|
| nuImages | 1600 x 900 | 16:9 | 45,677 | 65.3% |
| BDD100K | 1280 x 720 | 16:9 | 21,326 | 30.5% |
| Cityscapes | 2048 x 1024 | 2:1 | 2,893 | 4.1% |

**Multi-resolution handling**: Training pipelines should resize/pad images to a consistent size.

---

## 5. Category Balance Analysis

### Class Distribution

| Split | Pedestrian % | Cyclist % | Ratio |
|-------|--------------|-----------|-------|
| Train | 77.8% | 22.2% | 3.5:1 |
| Valid | 77.9% | 22.1% | 3.5:1 |
| Test | 77.7% | 22.3% | 3.5:1 |

**Key Findings:**
1. **Consistent class balance** - All splits within 0.2% of each other
2. **Good cyclist representation** - 22.2% cyclists
3. **Training considerations:**
   - Class-weighted loss functions may help
   - Per-class metrics should be reported separately

---

## 6. Lighting Distribution

| Split | Dark | Dim | Normal | Bright |
|-------|------|-----|--------|--------|
| Train | 7.3% | 20.0% | 71.2% | 1.5% |
| Valid | 7.3% | 20.0% | 71.3% | 1.5% |
| Test | 7.3% | 19.6% | 71.7% | 1.4% |

**Observations:**
1. **Predominantly normal lighting** - ~71% of images in normal lighting conditions
2. **nuImages impact** - Higher proportion of normal lighting from Singapore/Boston daytime scenes
3. **Limited bright scenes** - Only ~1.5% bright

---

## 7. Data Sources

### nuImages (65.3% of dataset)
- **Full dataset**: 93,000 annotated images from nuScenes
- **Golden-VRU subset**: 45,677 images
- **Resolution**: 1600 x 900
- **License**: CC BY-NC-SA 4.0
- **Geographic coverage**: Singapore and Boston

### BDD100K (30.5% of dataset)
- **Full dataset**: 100,000 diverse driving videos
- **Golden-VRU subset**: 21,326 images
- **Resolution**: 1280 x 720
- **License**: BSD 3-Clause
- **Geographic coverage**: United States

### Cityscapes (4.1% of dataset)
- **Full dataset**: 5,000 annotated images
- **Golden-VRU subset**: 2,893 images
- **Resolution**: 2048 x 1024
- **License**: Custom (research use)
- **Geographic coverage**: Germany (50 cities)

### Source Distribution by Split

| Split | BDD100K | Cityscapes | nuImages | Total |
|-------|---------|------------|----------|-------|
| Train | 17,017 (30.5%) | 2,320 (4.2%) | 36,541 (65.4%) | 55,878 |
| Valid | 2,156 (30.7%) | 289 (4.1%) | 4,568 (65.1%) | 7,013 |
| Test | 2,153 (30.7%) | 284 (4.1%) | 4,568 (65.2%) | 7,005 |

---

## 8. File Structure

```
golden-vru/
├── train/
│   ├── _annotations.coco.json   (55,878 images, 178,492 annotations)
│   ├── _annotations.coco.v8.0.json   (backup of v8.0)
│   └── [55,878 images]
├── valid/
│   ├── _annotations.coco.json   (7,013 images, 22,886 annotations)
│   ├── _annotations.coco.v8.0.json   (backup of v8.0)
│   └── [7,013 images]
├── test/
│   ├── _annotations.coco.json   (7,005 images, 22,474 annotations)
│   ├── _annotations.coco.v8.0.json   (backup of v8.0)
│   └── [7,005 images]
├── analysis/
│   ├── 1_class_distribution.png
│   ├── 2_size_distribution.png
│   ├── 3_density_distribution.png
│   ├── 4_lighting_distribution.png
│   └── combined_analysis.png
├── train.dvc
├── valid.dvc
├── test.dvc
├── STATS.md
├── DATASET_REPORT.md
├── analyze_distributions.py
├── filter_small_objects.py
├── extract_rsud.py
├── merge_nuimages.py
├── validate_dataset.py
└── resplit_dataset.py
```

### Image Naming Convention
- **BDD100K**: `{video_id}-{frame_id}.jpg`
- **Cityscapes**: `cityscapes_{city}_{sequence}_{frame}.png`
- **nuImages**: `nuimages_{camera}_{timestamp}.jpg`

---

## 9. Version History

### v9.0 - Removed RSUD20K (Current)
- Git tag: `v9.0`
- Removed RSUD20K data due to annotation quality concerns
- Extracted 15,961 RSUD images to `/mnt/data/rsud-vru/`
- Images: 69,896 (55,878 / 7,013 / 7,005)
- Annotations: 223,852 (-19.4% from v8.0)
- Sources: 3 (BDD100K, Cityscapes, nuImages)

### v8.0 - Added nuImages
- Git tag: `v8.0`
- Added nuImages VRU data for Singapore/Boston coverage
- Images: 85,857 (68,647 / 8,609 / 8,601)
- Annotations: 277,788 (+94.0% from v7.0)
- Sources: 4 (BDD100K, Cityscapes, RSUD20K, nuImages)

### v7.0 - Medium + Large Objects Only
- Git tag: `v7.0-medium-large-only`
- Removed small objects (area < 32x32 = 1024 px²)
- Removed images with no remaining annotations
- Images: 40,180 (32,106 / 4,041 / 4,033)
- Annotations: 143,212

### v6.0 - 80/10/10 Split
- Git tag: `v6.0-80-10-10-split`
- Re-split with stratified sampling for balanced distributions
- Images: 46,884 (37,507 / 4,688 / 4,689)
- Annotations: 207,813

### v5.0 - BDD100K + Cityscapes + RSUD20K
- Git tag: `v5.0-bdd-cityscapes-rsud`
- Added RSUD20K for geographic diversity
- Images: 46,884 (41,590 / 3,256 / 2,038)

### v4.0 - BDD100K + Cityscapes
- Git tag: `v4.0-bdd-cityscapes`
- Added Cityscapes for European scenes
- Images: 30,842

### v3.0 - BDD100K Only
- Git tag: `v3.0-bdd100k-only`
- Images: 27,775

---

## 10. Usage

### Loading with pycocotools

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

# Get category info
cats = coco_train.loadCats(coco_train.getCatIds())
print(cats)  # [{'id': 0, 'name': 'pedestrian', ...}, {'id': 1, 'name': 'cyclist', ...}]
```

### DVC Download

```bash
# Clone repository
git clone <repo-url>
cd <repo>

# Download data from S3
dvc pull

# Verify
ls golden-vru/train/*.jpg golden-vru/train/*.png | wc -l  # Should be 55,878
```

---

## 11. Training Recommendations

### Model Selection
- **Recommended**: RF-DETR, DETR variants, or YOLO for real-time inference
- **Input size**: Resize to common sizes (640x640, 1024x1024) due to mixed resolutions

### Data Augmentation
1. **Scale augmentation**: Multi-scale training to handle varying VRU sizes
2. **Photometric augmentation**: Brightness, contrast for different lighting conditions
3. **Mosaic/MixUp**: Can help with multi-resolution images

### Evaluation
- Use COCO mAP metrics (AP50, AP75, mAP)
- Report per-class AP separately (pedestrian vs cyclist)
- Consider size-based evaluation (APmedium, APlarge)

### v7.0 Test Baseline: YOLOv8x (COCO person class) — mAP@50: 0.478, F1: 0.578

---

## 12. Comparison with Individual Sources

| Metric | Golden-VRU v9.0 | nuImages (VRU) | BDD100K (VRU) | Cityscapes (VRU) |
|--------|-----------------|----------------|---------------|------------------|
| Total Images | 69,896 | 45,677 | 21,326 | 2,893 |
| Total Annotations | 223,852 | 134,576 | ~90,000 | ~31,000 |
| Avg Ann/Image | 3.2 | 2.9 | 4.2 | 10.7 |
| Pedestrian % | 77.8% | 77.6% | 86.1% | 70.9% |
| Cyclist % | 22.2% | 22.4% | 13.9% | 29.1% |
| Geographic | Multi-region | Singapore/Boston | USA | Europe |

**Key Differentiators:**
- Large combined VRU dataset by image count
- Geographic diversity (3 regions across 3 continents)
- Consistent class distribution across splits
- No small objects (medium and large only)

---

## Appendix: Validation

Dataset passes COCO format validation:

```
Golden-VRU v9.0: PASSED
  - Keys: ['categories', 'images', 'annotations']
  - Categories: [pedestrian (0), cyclist (1)]
  - Image fields: id, file_name, width, height, source
  - Annotation fields: id, image_id, category_id, bbox, area, iscrowd
  - All image IDs referenced in annotations exist
  - All category IDs in annotations are valid
  - Split ratios: 80.0% / 10.0% / 10.0%
  - Class distribution variance across splits: <0.5%
```
