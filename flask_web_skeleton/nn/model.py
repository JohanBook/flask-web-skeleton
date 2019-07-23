"""
Module for training and creating neural networks
for image classification.
"""
import os
from abc import ABC

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from .accuracy import loader_accuracy
from .dataset import get_data_loaders

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class Model(nn.Module, ABC):
    def infer(self, x):
        return self(np.array(x))


class Flatten(nn.Module):
    def forward(self, x):
        return x.view(x.size()[0], -1)


class CNN(Model):
    def __init__(self):
        super(CNN, self).__init__()
        self.arch = nn.Sequential(
            nn.Conv2d(1, 6, kernel_size=5, stride=1),
            nn.MaxPool2d(2),
            nn.Conv2d(6, 16, kernel_size=5, stride=1),
            nn.MaxPool2d(2),
            # 4x4 image
            Flatten(),
            nn.Linear(16 * 4 * 4, 120),
            nn.Linear(120, 84),
            nn.Linear(84, 10),
        )

    def forward(self, x):
        return F.log_softmax(self.arch(x), dim=1)


def create_model(epochs=1, save_to=None):
    """
    Create amd train a model.

    Args:
        epochs (int): Number of epochs to train for. If
            set to -1, then train until convergence
            (default -1).
        save_to (str): Where to save model when done.
            (default None).

    Returns:
        the trained model.

    Example:
        >>> model = create_model(0)
    """
    model = CNN()
    model.to(DEVICE)

    train_loader, test_loader = get_data_loaders()
    optim = torch.optim.Adam(model.parameters(), lr=0.001)
    for epoch in range(epochs):
        total_loss = 0
        model.train()
        for data, labels in train_loader:
            preds = model(data.to(DEVICE))
            loss = F.cross_entropy(preds, labels)
            loss.backward()
            total_loss += loss.item()

            optim.step()
            optim.zero_grad()
        model.eval()
        acc = loader_accuracy(test_loader, model)
        print(f"EPOCH {epochs+1} loss {total_loss:.2f} val acc {acc:.2f}%")

    if save_to:
        torch.save(model.state_dict(), save_to)

    return model


def load(path):
    """
    Load a saved model from specified path.

    Args:
        path (str): Path to model.

    Returns:
        loaded model.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Unable to locate file at {path}")
    extension = path.split(".")[-1]
    if not extension == "pth":
        raise ValueError(f"Expected pth extension, got {extension}")

    model = CNN()
    model.load_state_dict(torch.load(path))
    model.to(DEVICE)
    return model
