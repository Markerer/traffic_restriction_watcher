from abc import ABC, abstractmethod
import numpy as np


class Polygon(ABC):

    @abstractmethod
    def inside_the_polygon(self, coords: np.array) -> bool:
        pass
