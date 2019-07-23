import torch
import torchvision
import torchvision.transforms as transforms


def get_data_loaders(transform=None):
    if not transform:
        transform = transforms.Compose(
            [transforms.ToTensor(), transforms.Normalize((0.0,), (1.0,))]
        )

    trainset = torchvision.datasets.MNIST(
        root="/storage", train=True, download=True, transform=transform
    )

    trainloader = torch.utils.data.DataLoader(
        trainset, batch_size=100, shuffle=True, num_workers=2, pin_memory=True
    )

    testset = torchvision.datasets.MNIST(
        root="/storage", train=False, download=True, transform=transform
    )

    testloader = torch.utils.data.DataLoader(
        testset, batch_size=100, shuffle=True, num_workers=2, pin_memory=True
    )
    return trainloader, testloader
