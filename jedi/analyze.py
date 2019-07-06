import numpy as np


def analyze_image(image):
    image = np.array(image)

    data = {}
    data['shape'] = image.shape
    data['pixels'] = np.product(image.shape)
    data['average'] = np.mean(image)
    return data


def formated_analysis(image):
    def format(v):
        if isinstance(v, float):
            return f'{v:.2f}'
        if isinstance(v, int):
            return f'{v:,}'.format(',', ' ')
        return v
    data = {k.capitalize(): format(v) for k, v in analyze_image(image).items()}
    return data
