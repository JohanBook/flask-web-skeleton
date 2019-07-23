import torch

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def loader_accuracy(loader, model):
    with torch.no_grad():
        cum_acc = 0
        for x, y in loader:
            cum_acc += accuracy(x.to(DEVICE), y.to(DEVICE), model)
        return cum_acc / len(loader)


def accuracy(x, y, model):
    with torch.no_grad():
        pred = model(x).argmax(dim=1, keepdim=True)
        corrects = pred.eq(y.view_as(pred)).sum().item()
        acc = corrects * 100 / len(x)
        return acc
