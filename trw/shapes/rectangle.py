import numpy as np
from .polygon import Polygon


class Rectangle(Polygon):

    def __init__(
            self,
            a_coords: np.array,
            b_coords: np.array,
            d_coords: np.array
    ):
        self.a_coords = a_coords
        self.b_coords = b_coords
        self.d_coords = d_coords

    def inside_the_polygon(self, coords: np.array) -> bool:
        """
        Check if the given coordinates are inside the rectangle.
        :param coords: X,Y coordinates in a numpy array format: np.array[x,y]
        :return: boolean
        """
        m_coords = coords.astype(float)
        AM = m_coords - self.a_coords
        AB = self.b_coords - self.a_coords
        AD = self.d_coords - self.a_coords

        ABdotAB = np.dot(AB, AB)
        AMdotAB = np.dot(AM, AB)
        ADdotAD = np.dot(AD, AD)
        AMdotAD = np.dot(AM, AD)

        return (0 < AMdotAB < ABdotAB) and (0 < AMdotAD < ADdotAD)
