# Golden-VRU Dataset Analysis Report

Generated: 2026-01-16

## Executive Summary

The Golden-VRU dataset is a curated multi-source dataset for Vulnerable Road User (VRU) detection, combining images from BDD100K, Cityscapes, and RSUD20K. This dataset contains only images with pedestrian and/or cyclist annotations, making it ideal for training object detection models targeting VRUs.

### Dataset Overview

| Split | Images | Annotations | Pedestrians | Cyclists |
|-------|--------|-------------|-------------|----------|
| Train | 37,507 | 165,311 | 129,294 (78.2%) | 36,017 (21.8%) |
| Valid | 4,688 | 21,016 | 16,419 (78.1%) | 4,597 (21.9%) |
| Test | 4,689 | 21,486 | 16,925 (78.8%) | 4,561 (21.2%) |
| **Total** | **46,884** | **207,813** | **162,638 (78.3%)** | **45,175 (21.7%)** |

**Key Characteristics:**
- Multi-resolution: 1280x720 (BDD100K), 2048x1024 (Cityscapes), 1920x1080 (RSUD20K)
- Sources: BDD100K (USA), Cityscapes (Europe), RSUD20K (South Asia)
- Average annotations per image: 4.4
- Balanced class distribution across splits (~78% pedestrian, ~22% cyclist)
- 80/10/10 train/valid/test split with stratified sampling

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
| 0 | pedestrian | Walking pedestrians | BDD100K: pedestrian, Cityscapes: person, RSUD20K: Pedestrian |
| 1 | cyclist | Bicycles, motorcycles, and riders | BDD100K: rider/bike/motor, Cityscapes: rider/bicycle/motorcycle, RSUD20K: Rickshaw/CNG/Bike |

---

## 2. Annotation Size Distribution

COCO size thresholds: small < 32², medium 32²-96², large > 96²

| Split | Small (<1024 px²) | Medium (1024-9216 px²) | Large (>9216 px²) |
|-------|-------------------|------------------------|-------------------|
| Train | 51,653 (31.2%) | 75,163 (45.5%) | 38,495 (23.3%) |
| Valid | 6,426 (30.6%) | 9,769 (46.5%) | 4,821 (22.9%) |
| Test | 6,522 (30.4%) | 9,824 (45.7%) | 5,140 (23.9%) |

**Observations:**
1. **Balanced distribution** - Approximately 30% small, 46% medium, 23% large
2. **Consistent across splits** - Size distribution is remarkably consistent, indicating good stratification
3. **More large objects** - Higher resolution sources (Cityscapes, RSUD20K) contribute more large annotations

---

## 3. Annotation Density Distribution

| Split | Sparse (1-3) | Moderate (4-10) | Dense (11-20) | Very Dense (>20) |
|-------|--------------|-----------------|---------------|------------------|
| Train | 59.4% | 32.4% | 6.3% | 1.9% |
| Valid | 59.1% | 32.3% | 6.5% | 2.1% |
| Test | 57.7% | 33.9% | 6.3% | 2.1% |

**Observations:**
1. **Predominantly sparse scenes** - ~59% of images have 1-3 VRU annotations
2. **Consistent density** - Nearly identical distribution across all splits
3. **Typical driving scenarios** - Reflects real-world distribution

---

## 4. Image Resolution

| Source | Resolution | Aspect Ratio | Images | Percentage |
|--------|------------|--------------|--------|------------|
| BDD100K | 1280 x 720 | 16:9 | 27,775 | 59.2% |
| Cityscapes | 2048 x 1024 | 2:1 | 3,067 | 6.5% |
| RSUD20K | 1920 x 1080 | 16:9 | 16,042 | 34.2% |

**Multi-resolution handling**: Training pipelines should resize/pad images to a consistent size.

---

## 5. Category Balance Analysis

### Class Distribution

| Split | Pedestrian % | Cyclist % | Ratio |
|-------|--------------|-----------|-------|
| Train | 78.2% | 21.8% | 3.6:1 |
| Valid | 78.1% | 21.9% | 3.6:1 |
| Test | 78.8% | 21.2% | 3.7:1 |

**Key Findings:**
1. **Consistent class balance** - All splits within 1% of each other (achieved via stratified sampling)
2. **Improved cyclist representation** - 21.7% cyclists vs 13.9% in BDD100K-only version
3. **Training considerations:**
   - Class-weighted loss functions may still help
   - Per-class metrics should be reported separately

---

## 6. Lighting Distribution

| Split | Dark | Dim | Normal | Bright |
|-------|------|-----|--------|--------|
| Train | 15.2% | 36.0% | 46.1% | 2.8% |
| Valid | 15.1% | 36.3% | 45.8% | 2.8% |
| Test | 15.2% | 35.7% | 46.4% | 2.7% |

**Observations:**
1. **Diverse lighting conditions** - Good coverage of dark/dim scenarios
2. **Consistent distribution** - Stratified sampling maintains lighting balance
3. **Limited bright scenes** - Only ~3% bright (typical for driving datasets)

---

## 7. Data Sources

### BDD100K (59.2% of dataset)
- **Full dataset**: 100,000 diverse driving videos
- **Golden-VRU subset**: 27,775 images
- **Resolution**: 1280 x 720
- **License**: BSD 3-Clause
- **Geographic coverage**: United States

### Cityscapes (6.5% of dataset)
- **Full dataset**: 5,000 annotated images
- **Golden-VRU subset**: 3,067 images
- **Resolution**: 2048 x 1024
- **License**: Custom (research use)
- **Geographic coverage**: Germany (50 cities)

### RSUD20K (34.2% of dataset)
- **Full dataset**: 20,000 road scene images
- **Golden-VRU subset**: 16,042 images
- **Resolution**: 1920 x 1080
- **License**: Custom (research use)
- **Geographic coverage**: Bangladesh (South Asia)

### Source Distribution by Split

| Split | BDD100K | Cityscapes | RSUD20K | Total |
|-------|---------|------------|---------|-------|
| Train | 22,220 (59.2%) | 2,453 (6.5%) | 12,834 (34.2%) | 37,507 |
| Valid | 2,777 (59.2%) | 307 (6.5%) | 1,604 (34.2%) | 4,688 |
| Test | 2,778 (59.2%) | 307 (6.5%) | 1,604 (34.2%) | 4,689 |

---

## 8. File Structure

```
golden-vru/
├── train/
│   ├── _annotations.coco.json   (37,507 images, 165,311 annotations)
│   └── [37,507 images]
├── valid/
│   ├── _annotations.coco.json   (4,688 images, 21,016 annotations)
│   └── [4,688 images]
├── test/
│   ├── _annotations.coco.json   (4,689 images, 21,486 annotations)
│   └── [4,689 images]
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
└── resplit_dataset.py
```

### Image Naming Convention
- **BDD100K**: `{video_id}-{frame_id}.jpg`
- **Cityscapes**: `cityscapes_{city}_{sequence}_{frame}.png`
- **RSUD20K**: `rsud_{split}{index}.jpg`

---

## 9. Version History

### v6.0 - 80/10/10 Split (Current)
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
ls golden-vru/train/*.jpg golden-vru/train/*.png | wc -l  # Should be 37,507
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
- Consider size-based evaluation (APsmall, APmedium, APlarge)

---

## 12. Comparison with Individual Sources

| Metric | Golden-VRU v6.0 | BDD100K (VRU) | Cityscapes (VRU) | RSUD20K (VRU) |
|--------|-----------------|---------------|------------------|---------------|
| Total Images | 46,884 | 27,775 | 3,067 | 16,042 |
| Total Annotations | 207,813 | 121,523 | 31,492 | 54,798 |
| Avg Ann/Image | 4.4 | 4.4 | 10.3 | 3.4 |
| Pedestrian % | 78.3% | 86.1% | 70.9% | 64.2% |
| Cyclist % | 21.7% | 13.9% | 29.1% | 35.8% |
| Geographic | Multi-region | USA | Europe | South Asia |

**Key Differentiators:**
- Largest combined VRU dataset by image count
- Geographic diversity (3 continents)
- Better cyclist representation than BDD100K alone
- Consistent class distribution across splits (stratified sampling)

---

## Appendix: Validation

Dataset passes COCO format validation:

```
Golden-VRU v6.0: PASSED
  - Keys: ['categories', 'images', 'annotations']
  - Categories: [pedestrian (0), cyclist (1)]
  - Image fields: id, file_name, width, height, source
  - Annotation fields: id, image_id, category_id, bbox, area, iscrowd
  - All image IDs referenced in annotations exist
  - All category IDs in annotations are valid
  - Split ratios: 80.0% / 10.0% / 10.0%
  - Class distribution variance across splits: <1%
```
