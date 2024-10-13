import random

import numpy as np


def create_random_vector(dim: int) -> np.ndarray:
    return np.array([random.random() for _ in range(dim)])
