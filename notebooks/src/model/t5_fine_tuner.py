from transformers import (
    T5ForConditionalGeneration,
    AdamW,
    get_linear_schedule_with_warmup,
)
import torch
import pytorch_lightning as pl


class T5FineTuner(pl.LightningModule):
    def __init__(
        self, pretrained_model_name_or_path, train_dataloader, val_dataloader, **hparams
    ):
        super().__init__()
        self.model = T5ForConditionalGeneration.from_pretrained(
            pretrained_model_name_or_path
        )
        self.save_hyperparameters()
        self.train_dataloader = train_dataloader
        self.val_dataloader = val_dataloader
        self.hparams = hparams

    def forward(self, input_ids, attention_mask, labels=None, **kwargs):
        outputs = self.model(
            input_ids=input_ids, attention_mask=attention_mask, labels=labels
        )
        return outputs

    def common_step(self, batch):
        outputs = self(**batch)
        loss = outputs.loss

        return loss

    def training_step(self, batch, batch_idx):
        loss = self.common_step(batch, batch_idx)
        # logs metrics for each training_step,
        # and the average across the epoch
        self.log("training_loss", loss)

        return loss

    def validation_step(self, batch, batch_idx):
        loss = self.common_step(batch, batch_idx)
        self.log("validation_loss", loss, on_epoch=True)

        return loss

    def test_step(self, batch, batch_idx):
        loss = self.common_step(batch, batch_idx)

        return loss

    def configure_optimizers(self):
        # create optimizer
        optimizer = torch.optim.AdamW(
            self.parameters,
            lr=self.hparams.learning_rate,
            eps=self.hparams.adam_epsilon,
        )
        # create learning rate scheduler
        num_train_optimization_steps = self.hparams.num_train_epochs * len(
            self.train_dataloader
        )
        lr_scheduler = {
            "scheduler": get_linear_schedule_with_warmup(
                optimizer,
                num_warmup_steps=self.hparams.warmup_steps,
                num_training_steps=num_train_optimization_steps,
            ),
            "name": "learning_rate",
            "interval": "step",
            "frequency": 1,
        }

        return {"optimizer": optimizer, "lr_scheduler": lr_scheduler}

    def train_dataloader(self):
        return self.train_dataloader

    def val_dataloader(self):
        return self.val_dataloader
