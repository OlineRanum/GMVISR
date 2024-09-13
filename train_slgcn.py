import omegaconf
from src.models.slgcn.openhands.apis.classification_model import ClassificationModel
from src.models.slgcn.openhands.core.exp_utils import get_trainer
import sys

cfg = omegaconf.OmegaConf.load("src/models/slgcn/configs/example_train.yaml")
trainer = get_trainer(cfg)

model = ClassificationModel(cfg=cfg, trainer=trainer)
model.init_from_checkpoint_if_available()
model.fit()
