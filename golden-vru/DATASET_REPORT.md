# Golden-VRU Dataset Analysis Report

Generated: 2026-01-28

## Executive Summary

The Golden-VRU dataset is a curated multi-source dataset for Vulnerable Road User (VRU) detection, combining images from BDD100K, Cityscapes, RSUD20K, and nuImages. This dataset contains only images with pedestrian and/or cyclist annotations, making it ideal for training object detection models targeting VRUs.

**v8.0 Update:** Added nuImages VRU data for Singapore and Boston geographic coverage. Small objects (area < 32x32 = 1024 px²) remain filtered out.

### Dataset Overview

| Split | Images | Annotations | Pedestrians | Cyclists |
|-------|--------|-------------|-------------|----------|
| Train | 68,647 | 221,578 | 167,055 (75.4%) | 54,523 (24.6%) |
| Valid | 8,609 | 28,191 | 21,291 (75.5%) | 6,900 (24.5%) |
| Test | 8,601 | 28,019 | 21,107 (75.3%) | 6,912 (24.7%) |
| **Total** | **85,857** | **277,788** | **209,453 (75.4%)** | **68,335 (24.6%)** |

**Key Characteristics:**
- Multi-resolution: 1600x900 (nuImages), 1280x720 (BDD100K), 1920x1080 (RSUD20K), 2048x1024 (Cityscapes)
- Sources: nuImages (Singapore/Boston), BDD100K (USA), RSUD20K (South Asia), Cityscapes (Europe)
- Average annotations per image: 3.2
- Balanced class distribution across splits (~75% pedestrian, ~25% cyclist)
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
| 0 | pedestrian | Walking pedestrians | BDD100K: pedestrian, Cityscapes: person, RSUD20K: Pedestrian, nuImages: human.pedestrian.* |
| 1 | cyclist | Bicycles, motorcycles, and riders | BDD100K: rider/bike/motor, Cityscapes: rider/bicycle/motorcycle, RSUD20K: Rickshaw/CNG/Bike, nuImages: vehicle.bicycle/motorcycle |

---

## 2. Annotation Size Distribution

COCO size thresholds: small < 32², medium 32²-96², large > 96²

**v8.0: Small objects removed** - Only medium and large annotations remain.

| Split | Small (<1024 px²) | Medium (1024-9216 px²) | Large (>9216 px²) |
|-------|-------------------|------------------------|-------------------|
| Train | 0 (0%) | 159,764 (72.1%) | 61,814 (27.9%) |
| Valid | 0 (0%) | 20,541 (72.9%) | 7,650 (27.1%) |
| Test | 0 (0%) | 19,995 (71.4%) | 8,024 (28.6%) |

**Observations:**
1. **No small objects** - All annotations with area < 1024 px² have been removed
2. **Medium-dominant** - Approximately 72% medium, 28% large
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
| nuImages | 1600 x 900 | 16:9 | 45,677 | 53.2% |
| BDD100K | 1280 x 720 | 16:9 | 21,326 | 24.8% |
| RSUD20K | 1920 x 1080 | 16:9 | 15,961 | 18.6% |
| Cityscapes | 2048 x 1024 | 2:1 | 2,893 | 3.4% |

**Multi-resolution handling**: Training pipelines should resize/pad images to a consistent size.

---

## 5. Category Balance Analysis

### Class Distribution

| Split | Pedestrian % | Cyclist % | Ratio |
|-------|--------------|-----------|-------|
| Train | 75.4% | 24.6% | 3.1:1 |
| Valid | 75.5% | 24.5% | 3.1:1 |
| Test | 75.3% | 24.7% | 3.1:1 |

**Key Findings:**
1. **Consistent class balance** - All splits within 0.3% of each other
2. **Good cyclist representation** - 24.6% cyclists
3. **Training considerations:**
   - Class-weighted loss functions may still help
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

### nuImages (53.2% of dataset)
- **Full dataset**: 93,000 annotated images from nuScenes
- **Golden-VRU subset**: 45,677 images
- **Resolution**: 1600 x 900
- **License**: CC BY-NC-SA 4.0
- **Geographic coverage**: Singapore and Boston

### BDD100K (24.8% of dataset)
- **Full dataset**: 100,000 diverse driving videos
- **Golden-VRU subset**: 21,326 images
- **Resolution**: 1280 x 720
- **License**: BSD 3-Clause
- **Geographic coverage**: United States

### RSUD20K (18.6% of dataset)
- **Full dataset**: 20,000 road scene images
- **Golden-VRU subset**: 15,961 images
- **Resolution**: 1920 x 1080
- **License**: Custom (research use)
- **Geographic coverage**: Bangladesh (South Asia)

### Cityscapes (3.4% of dataset)
- **Full dataset**: 5,000 annotated images
- **Golden-VRU subset**: 2,893 images
- **Resolution**: 2048 x 1024
- **License**: Custom (research use)
- **Geographic coverage**: Germany (50 cities)

### Source Distribution by Split

| Split | BDD100K | Cityscapes | RSUD20K | nuImages | Total |
|-------|---------|------------|---------|----------|-------|
| Train | 17,017 (24.8%) | 2,320 (3.4%) | 12,769 (18.6%) | 36,541 (53.2%) | 68,647 |
| Valid | 2,156 (25.0%) | 289 (3.4%) | 1,596 (18.5%) | 4,568 (53.1%) | 8,609 |
| Test | 2,153 (25.0%) | 284 (3.3%) | 1,596 (18.6%) | 4,568 (53.1%) | 8,601 |

---

## 8. File Structure

```
golden-vru/
├── train/
│   ├── _annotations.coco.json   (68,647 images, 221,578 annotations)
│   ├── _annotations.coco.v7.0.json   (backup of v7.0)
│   └── [68,647 images]
├── valid/
│   ├── _annotations.coco.json   (8,609 images, 28,191 annotations)
│   ├── _annotations.coco.v7.0.json   (backup of v7.0)
│   └── [8,609 images]
├── test/
│   ├── _annotations.coco.json   (8,601 images, 28,019 annotations)
│   ├── _annotations.coco.v7.0.json   (backup of v7.0)
│   └── [8,601 images]
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
├── merge_nuimages.py
├── validate_dataset.py
└── resplit_dataset.py
```

### Image Naming Convention
- **BDD100K**: `{video_id}-{frame_id}.jpg`
- **Cityscapes**: `cityscapes_{city}_{sequence}_{frame}.png`
- **RSUD20K**: `rsud_{split}{index}.jpg`
- **nuImages**: `nuimages_{camera}_{timestamp}.jpg`

---

## 9. Version History

### v8.0 - Added nuImages (Current)
- Git tag: `v8.0-with-nuimages`
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
ls golden-vru/train/*.jpg golden-vru/train/*.png | wc -l  # Should be 68,647
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

| Metric | Golden-VRU v8.0 | nuImages (VRU) | BDD100K (VRU) | RSUD20K (VRU) | Cityscapes (VRU) |
|--------|-----------------|----------------|---------------|---------------|------------------|
| Total Images | 85,857 | 45,677 | 21,326 | 15,961 | 2,893 |
| Total Annotations | 277,788 | 134,576 | ~90,000 | ~50,000 | ~31,000 |
| Avg Ann/Image | 3.2 | 2.9 | 4.2 | 3.1 | 10.7 |
| Pedestrian % | 75.4% | 77.6% | 86.1% | 64.2% | 70.9% |
| Cyclist % | 24.6% | 22.4% | 13.9% | 35.8% | 29.1% |
| Geographic | Multi-region | Singapore/Boston | USA | South Asia | Europe |

**Key Differentiators:**
- Largest combined VRU dataset by image count
- Geographic diversity (4 regions across 3 continents)
- Consistent class distribution across splits
- No small objects (medium and large only)

---

## Appendix: Validation

Dataset passes COCO format validation:

```
Golden-VRU v8.0: PASSED
  - Keys: ['categories', 'images', 'annotations']
  - Categories: [pedestrian (0), cyclist (1)]
  - Image fields: id, file_name, width, height, source
  - Annotation fields: id, image_id, category_id, bbox, area, iscrowd
  - All image IDs referenced in annotations exist
  - All category IDs in annotations are valid
  - Split ratios: 80.0% / 10.0% / 10.0%
  - Class distribution variance across splits: <0.5%
```
