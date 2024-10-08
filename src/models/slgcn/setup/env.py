name: openhands
channels:
  - pytorch
  - nvidia
  - conda-forge
  - defaults
dependencies:
  - python=3.11.5
  - pip=23.3.1
  - pytorch-cuda=11.8
  - pytorch=2.1.0
  - torchvision=0.16.0
  - torchaudio=2.1.0
  - pip:
    - pytorch-lightning==2.1.0
    - torchmetrics==0.7.0
    - tensorboard==2.14.1
    - tabulate>=0.8.9
    - tqdm>=4.62.3
    - pillow>=8.0.1
    - notebook>=6.4.5
    - jupyterlab>=3.2.1
    - matplotlib>=3.4.3
    - seaborn>=0.11.2
    - ipywidgets>=7.6.5
    - wandb==0.16.0
    - qudida==0.0.4
    - flatbuffers>=2.0
    - opencv-python==4.8.1.78
    - opencv-contrib-python==4.8.1.78
    - opencv-python-headless==4.8.1.78
    - omegaconf==2.3.0
    - pytorchvideo==0.1.5
    - albumentations==1.3.1
    - hydra-core==1.3.2
    - natsort==8.4.0
    - h5py==3.9.0
    - timm==0.9.10
    - transformers==4.32.1