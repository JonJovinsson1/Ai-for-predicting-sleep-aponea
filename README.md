# Predicting Obstructive Sleep Apnoea (OSA) with 3D Craniofacial AI

A deep learning approach to detecting Obstructive Sleep Apnoea using 3D facial morphology.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-EE4C2C)
![Status](https://img.shields.io/badge/Status-Completed-success)

---

## Overview

This project explores the application of deep learning algorithms to detect **Obstructive Sleep Apnoea (OSA)** using 3D craniofacial scans. Unlike traditional Polysomnography (PSG), which is expensive, time-consuming, and invasive, this solution proposes a non-invasive, rapid screening approach based on the correlation between craniofacial morphology and OSA.

The system uses an automated pipeline that ingests 3D scans, extracts morphological landmarks using **Deep-MVLM**, and feeds these features into a custom **PyTorch classifier** to predict the presence of OSA.

**Note:** This project was developed as a capstone project (Group 16) at Edith Cowan University (ECU).

---

## Key Features

- End-to-end pipeline from raw 3D scan to binary OSA classification.
- Automated 3D landmark detection using **Deep-MVLM** (OBJ, VTK, PLY support).
- Custom PyTorch classifier with Batch Normalization and Dropout.
- Web-based user interface for scan upload and analysis.

---

## Methodology & Architecture

The solution uses a two-stage deep learning pipeline:

### 1. Preprocessing & Feature Extraction

- **Input:** 3D craniofacial scans (`.obj`, `.ply`, `.vtk`)
- **Tool:** Deep-MVLM (Multi-view Consensus CNN)
- **Output:** 3D landmark coordinates (`.txt`, `.vtk`)

### 2. Classification

- **Input:** Landmark vector features
- **Model:** Custom Multi-Layer Perceptron (MLP) built with PyTorch
- **Output:** Probability score and binary classification (OSA / Non-OSA)

### Classifier Architecture

The predictive model includes:
- **Hidden Layers:** ReLU activation
- **Output Layer:** Sigmoid activation for binary classification
- **Optimizer:** Adam with learning-rate scheduling
- **Regularization:** Dropout (0.4) and Batch Normalization to reduce overfitting

## Results

Model evaluation was performed using 5-fold and 10-fold cross-validation.

| Metric           | Result  | Description                                                   
Mean AUC             0.77     Area Under the ROC Curve with optimized architecture
Validation Accuracy  100%     Achieved on selected internal folds
Novel Data Accuracy  60–70%   Performance on previously unseen external data

## Installation

### Prerequisites

- Python 3.7+
- PyTorch 1.2+
- VTK 8.2

### Setup

## 1. Clone the repository:

git clone https://github.com/yourusername/OSA-Detection-3D.git
cd OSA-Detection-3D
Install dependencies:
pip install -r requirements.txt

Ensure the following dependencies (used by Deep-MVLM) are installed:
scikit-image
scipy
matplotlib
imageio
vtk
absl-py

## Usage
1. Feature Extraction (Deep-MVLM)
Generate 3D landmarks from a scan:
python predict.py --c configs/DTU3D-RGB.json --n assets/patient_scan.obj

2. Classification
Run the trained classifier on extracted landmarks:
python classifier_inference.py --input assets/patient_landmarks.txt


### Acknowledgments & Citations
This project relies on Deep-MVLM for automated 3D landmark placement.

If you use this code, please cite the original authors:
Multi-view Consensus CNN for 3D Facial Landmark Placement
Paulsen, Rasmus R.; Juhl, Kristine Aavild; Haspang, Thilde Marie; Hansen, Thomas; Ganz, Melanie; Einarsson, Gudmundur.
Asian Conference on Computer Vision (ACCV), 2018.

BibTeX
bibtex
Copy code
@inproceedings{paulsen2018multi,
  title={Multi-view Consensus CNN for 3D Facial Landmark Placement},
  author={Paulsen, Rasmus R and Juhl, Kristine Aavild and Haspang, Thilde Marie and Hansen, Thomas and Ganz, Melanie and Einarsson, Gudmundur},
  booktitle={Asian Conference on Computer Vision},
  pages={706--719},
  year={2018},
  organization={Springer}
}


### Supervision
Special thanks to Dr. Syed Mohammed Shamsul Islam and the ECU School of Science for their support and supervision.

### Disclaimer
This project is for research and educational purposes only. It is not a certified medical diagnostic tool and must not be used as a substitute for professional medical advice or Polysomnography (PSG).
