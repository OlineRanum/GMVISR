import torch
import torch.nn.functional as F
import torchmetrics
import math 
from ..core.losses import CrossEntropyLoss, SmoothedCrossEntropyLoss
from .inference import InferenceModel
import torch
from torch.utils.data import DataLoader, Subset
from sklearn.model_selection import KFold
import pytorch_lightning as pl

class ClassificationModel(InferenceModel):
    """
    Classification Model initializer

    Args:
        cfg (dict): configuration set.
        trainer (object): trainer object from Pytorch Lightning.

    """
    def __init__(self, cfg, trainer):
        super().__init__(cfg, stage="fit")
        self.trainer = trainer
        self.setup_metrics()
        self.loss = self.setup_loss(self.cfg.optim)


    def training_step(self, batch, batch_idx):
        """
        Lightning calls this inside the training loop with the data from the training dataloader
        passed in as `batch` and calculates the loss and the accuracy.
        """
        # assert 1 == 2
        # This was updated in newest version 
        params = self.cfg.data.train_pipeline.parameters
        y_hat, y_hat_params = self.model(batch["frames"])

        
        # self.model._modules['decoder']._modules['param_clfs']._modules['Handshape']._parameters['weight'].requires_grad
        # self._datamodule.train_dataset.id_to_gloss
        # This was updated in newest version 
        loss = self.loss(y_hat, batch["labels"])
        if params:
            loss += sum([self.loss(y_hat_params[p], batch["params"][p]) for p in params])
        # This was updated in newest version 
        acc = self.accuracy_metric(F.softmax(y_hat, dim=-1), batch["labels"])
        if params:
            acc += sum([self.accuracy_metric(F.softmax(y_hat_params[p], dim=-1), batch["params"][p]) for p in params])
            # This should probably be the average, in validation it does not matter as we are doing it per phoneme
            acc = acc/(len(params) + 1)

        self.log("train_loss", loss, batch_size = len(batch['files']))
        # This was updated in newest version 
        self.log("train_acc", acc, on_step=False, on_epoch=True, prog_bar=True, batch_size = len(batch['files']))
        # self.log("train_acc", acc / len(params), on_step=True, on_epoch=False, prog_bar=True)

        return {"loss": loss, "train_acc": acc}

    def validation_step(self, batch, batch_idx):
        """
        Lightning calls this inside the training loop with the data from the validation dataloader
        passed in as `batch` and calculates the loss and the accuracy.
        """
        params = self.cfg.data.valid_pipeline.parameters
        y_hat, y_hat_params = self.model(batch["frames"])

        
        # This was updated in newest version 
        loss = self.loss(y_hat, batch["labels"])
        if params:
            param_loss = sum([self.loss(y_hat_params[p], batch["params"][p]) for p in params])
            # If the batch[params] parameter is only zeros then the loss is nan 
            # TODO: Do we want to fix this? 
            if not math.isnan(param_loss): 
                loss += param_loss
    
        preds = F.softmax(y_hat, dim=-1)
        acc_top1 = self.accuracy_metric(preds, batch["labels"])
        acc_top3 = self.accuracy_metric(preds, batch["labels"], top_k=3)
        acc_top5 = self.accuracy_metric(preds, batch["labels"], top_k=5)

        if params:
            for p in params:
                preds_p = F.softmax(y_hat_params[p], dim=-1)
                p_acc_top1 = self.accuracy_metric(preds_p, batch["params"][p])
                self.log(p + "_acc", p_acc_top1, on_step=False, on_epoch=True, prog_bar=True, batch_size = len(batch['files']))

        self.log("val_loss", loss,  batch_size = len(batch['files']))
        self.log("val_acc", acc_top1, on_step=False, on_epoch=True, prog_bar=True, batch_size = len(batch['files']))
        self.log("val_acc_top3", acc_top3, on_step=False, on_epoch=True, prog_bar=True, batch_size = len(batch['files']))
        self.log("val_acc_top5", acc_top5, on_step=False, on_epoch=True, prog_bar=True, batch_size = len(batch['files']))

        return {"valid_loss": loss, "valid_acc": acc_top1}
    def configure_optimizers(self):
        """
        Returns the optimizer and the LR scheduler to be used by Lightning.
        """
        return self.get_optimizer(self.cfg.optim)

    def setup_loss(self, conf):
        """
        Initializes the loss function based on the loss parameter mentioned in the config.
        """
        loss = conf.loss
        assert loss in ["CrossEntropyLoss", "SmoothedCrossEntropyLoss"]
        if loss == "CrossEntropyLoss":
            # This was updated in newest version from ignore_index -1 ??????
            return CrossEntropyLoss(ignore_index=0)
        return SmoothedCrossEntropyLoss()

    def setup_metrics(self):
        """
        Intializes metric to be logged. Accuracy is used here currently.
        """
        self.accuracy_metric = torchmetrics.functional.accuracy

    def get_optimizer(self, conf):
        """
        Parses the config and creates the optimizer and the LR scheduler.
        """
        optimizer_conf = conf["optimizer"]
        optimizer_name = optimizer_conf.get("name")
        optimizer_params = {}
        if hasattr(optimizer_conf, "params"):
            optimizer_params = optimizer_conf.params

        optimizer = getattr(torch.optim, optimizer_name)(
            params=self.model.parameters(), **optimizer_params
        )

        if "scheduler" not in conf:
            return [optimizer]

        scheduler_conf = conf["scheduler"]
        scheduler_name = scheduler_conf.get("name")
        scheduler_params = {}
        if hasattr(scheduler_conf, "params"):
            scheduler_params = scheduler_conf.params
        scheduler = getattr(torch.optim.lr_scheduler, scheduler_name)(
            optimizer=optimizer, **scheduler_params
        )

        return [optimizer], [scheduler]

    def fit(self):
        """
        Method to be called to start the training.
        """
        self.trainer.fit(self, self.datamodule)


    