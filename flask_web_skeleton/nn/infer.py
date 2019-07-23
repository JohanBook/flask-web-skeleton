from PIL import Image
import PIL

from flask_web_skeleton.nn.model import load

mnist_model = load("storage/mnist_cnn.pth")


def infer(path):
    return mnist_model(Image.open(path))


if __name__== '__main__':
    import torch
    from flask_web_skeleton.nn.dataset import get_data_loaders
    train, test = get_data_loaders()

    data, labels = next(iter(train))
    print(data.shape)

    preds = mnist_model(data)
    preds = torch.argmax(preds, dim=1)
    print(preds.shape, 'vs', labels.shape)

    accuracy = 100*torch.sum(preds == labels).item()/len(labels)

    print('Batch accuracy\n', accuracy, '%\n')

    num = 0
    for x, d in zip(data, labels):
        x = x.view(1, 1, 28, 28)
        preds = mnist_model(x)
        preds = torch.argmax(preds, dim=1)
        num += (preds == d).item()
    print('Inference accuracy\n', 100*num / len(data), '%')


