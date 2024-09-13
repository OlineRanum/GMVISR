
### DEVELOPMENT OF REPO IN PROGRESS ---------------------------- Check back later.

# The NGT200 Dataset: Geometric Multi-View Isolated Sign Recognition

**Authors**: Oline Ranum, David Wessels, Gomer Otterspeer, Erik J Bekkers, Floris Roelofsen, Jari I. Andersen  
**Affiliation**: SignLab Amsterdam, University of Amsterdam  
**Contact**: o.a.ranum@uva.nl

---

## Table of Contents

1. [Introduction](#introduction)
2. [Dataset Description](#dataset-description)
3. [SetUp](#SetUp)
4. [Usage](#usage)
5. [Evaluation](#evaluation)
6. [Benchmarks and Baselines](#benchmarks-and-baselines)
7. [License and Citation](#license-and-citation)
8. [Contributing](#contributing)
9. [Acknowledgements](#acknowledgements)

## Introduction

This repository contains the code for the paper [The NGT200 Dataset: Geometric Multi-View Isolated Sign Recognition](https://openreview.net/forum?id=idkNzTC67X)

## The NGT200 Dataset

The NGT200 Dataset is available through our [OSF Server](https://osf.io/5zuyd/).
To reproduce the experiments of the NGT200 paper please download the pose- and metadata files available at the OSF server and unzip to 


- **Domain**: Sign Language Processing
- **Type**: Spatio-temporal pose point clouds, videos
- **Size**: 200 glosses, 4 unique signers, 3 views per video. (e.g., Number of samples, Total size in GB, etc.)
- **Data Source**: Human signers (captured in Lab), Synthetic signer
- **License**: CC BY 4.0

## Experiments 

### Reproduction of experiments Section 4 & 5 (Baseline)

The experiments in sections 4 and 5 are conducted using the SL-GCN.

#### SetUp

To reproduce the experiments using the SLGCN please install the following environment:

``` Install environment SLGCN
conda env create -f src/models/slgcn/setup/env.yml
conda activate openhands
```

#### Run Experiments

To train the SLGCN run

``` 
python train_slgcn.py
```

To evaluate the SLGCN run
``` 
python test_slgcn.py
```

### Reproduction of experiments Section 6 (Geometric)

In order to run the code for the geometric model (Temporal-PONITA) described in Section 6 install the following conda environment

```Install environment for temporal-PONITA
conda create --yes --name ponita python=3.10 numpy scipy matplotlib
conda activate ponita
conda install pytorch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 pytorch-cuda=11.7 -c pytorch -c nvidia -y
conda install pyg==2.3.1 -c pyg -y
pip3 install wandb
pip3 install pytorch_lightning==1.8.6
pip3 install pyg_lib torch_scatter torch_sparse torch_cluster torch_spline_conv -f https://data.pyg.org/whl/torch-1.13.1+cu117.html
```

To train and evaluate the temporal-PONITA run
``` 
python run_temporal_ponita.py
```

## License and Citation
- **License**: The NGT200 dataset is released under a CC BY 4.0 license. 

## Citation
If you use this dataset in your research, please cite:

```bibtex
@inproceedings{ranum24b,
  title={The NGT200 Dataset: Geometric Multi-View Isolated Sign Recognition},
  author={Oline Ranum and David Wessels and Gomer Otterspeer and Erik J. Bekkers and Floris Roelofsen and Jari I. Andersen},
  booktitle={Proceedings of the Geometry-grounded Representation Learning and Generative Modeling Workshop (GRaM) at the 41st International Conference on Machine Learning},
  year={2024},
  volume={251},
  series={Proceedings of Machine Learning Research},
  publisher={PMLR},
}
```

