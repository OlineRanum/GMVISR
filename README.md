# The NGT200 Dataset: Geometric Multi-View Isolated Sign Recognition

[![GRaM @ ICML 2024](https://img.shields.io/badge/ICML%202024-GRaM%20Workshop-blue)](https://openreview.net/forum?id=idkNzTC67X)
[![Dataset](https://img.shields.io/badge/Dataset-OSF-green)](https://osf.io/5zuyd/)
[![License](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey)](https://creativecommons.org/licenses/by/4.0/)

**Authors**: Oline Ranum · David Wessels · Gomèr Otterspeer · Erik J. Bekkers · Floris Roelofsen · Jari I. Andersen
**Affiliation**: SignLab Amsterdam & AMLab, University of Amsterdam
**Contact**: o.ranum@surrey.ac.uk

[Paper](https://openreview.net/forum?id=idkNzTC67X) | [Dataset (OSF)](https://osf.io/5zuyd/) | [Project Page](https://olineranum.github.io/GMVISR/)

---

## Abstract

Sign Language Processing (SLP) provides a foundation for a more inclusive future in language technology; however, the field faces several significant challenges that must be addressed to achieve practical, real-world applications. This work addresses multi-view isolated sign recognition (MV-ISR), and highlights the essential role of 3D awareness and geometry in SLP systems. We introduce the **NGT200 dataset**, a novel spatio-temporal multi-view benchmark, establishing MV-ISR as distinct from single-view ISR (SV-ISR). We demonstrate the benefits of synthetic data and propose conditioning sign representations on spatial symmetries inherent in sign language. Leveraging an SE(2)-equivariant model improves MV-ISR performance by **8–22% over the baseline**.

---

## Dataset

The NGT200 dataset contains pose and video data for **200 common NGT (Sign Language of the Netherlands) signs** captured from three viewpoints (−25°, 0°, +25°) with both human signers and a synthetic avatar.

| Property | Value |
|---|---|
| Signs | 200 NGT glosses |
| Viewpoints | 3 (left −25°, front 0°, right +25°) |
| Signers | 3 Deaf signers + 1 synthetic avatar |
| Landmarks | 75 per frame (Holistic MediaPipe) |
| Modalities | Spatio-temporal pose, video |
| License | CC BY 4.0 |

**Download**: [osf.io/5zuyd](https://osf.io/5zuyd/) — unzip pose and metadata files to `data/`.

---

## Key Results

| Model | Training Views | Top-1 Acc (Front) | Top-1 Acc (Side avg.) |
|---|---|---|---|
| SL-GCN | Front only | 0.49 | 0.09 |
| SL-GCN | All 3 views | 0.49 | 0.46 |
| **Temporal-PONITA** | **All 3 views** | **0.59** | **0.53** |

- Training on a single frontal view leads to >50% relative accuracy drop on side views.
- SE(2)-equivariant Temporal-PONITA improves over SL-GCN by **8–22%** across all view conditions.
- Temporal-PONITA is also **40% faster** in total runtime (145 vs. 357 epochs to convergence).

---

## Setup

### SL-GCN (Sections 4 & 5)

```bash
conda env create -f src/models/slgcn/setup/env.yml
conda activate openhands
python train_slgcn.py
python test_slgcn.py
```

### Temporal-PONITA (Section 6)

```bash
conda create --yes --name ponita python=3.10 numpy scipy matplotlib
conda activate ponita
conda install pytorch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 pytorch-cuda=11.7 -c pytorch -c nvidia -y
conda install pyg==2.3.1 -c pyg -y
pip install wandb pytorch_lightning==1.8.6
pip install pyg_lib torch_scatter torch_sparse torch_cluster torch_spline_conv \
    -f https://data.pyg.org/whl/torch-1.13.1+cu117.html
python run_temporal_ponita.py
```

---

## Repository Structure

```
GMVISR/
├── data/               # Metadata and k-fold splits (download poses from OSF)
├── train_slgcn.py      # SL-GCN training script
├── test_slgcn.py       # SL-GCN evaluation script
├── run_temporal_ponita.py  # Temporal-PONITA training & evaluation
└── docs/               # GitHub Pages project page
```

---

## Citation

```bibtex
@inproceedings{ranum2024ngt200,
  title     = {The NGT200 Dataset: Geometric Multi-View Isolated Sign Recognition},
  author    = {Ranum, Oline and Wessels, David and Otterspeer, Gom{\`e}r and
               Bekkers, Erik J. and Roelofsen, Floris and Andersen, Jari I.},
  booktitle = {Proceedings of the GRaM Workshop at the 41st International
               Conference on Machine Learning (ICML)},
  series    = {Proceedings of Machine Learning Research},
  volume    = {251},
  publisher = {PMLR},
  year      = {2024},
  url       = {https://openreview.net/forum?id=idkNzTC67X}
}
```

---

## License

The NGT200 dataset is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Code in this repository is released under MIT.
