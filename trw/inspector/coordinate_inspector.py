from trw.shapes import Polygon
import numpy as np


class CoordinateInspector:

    def __init__(self, target_polygon: Polygon):
        self.target_polygon = target_polygon

    def inside_the_polygon(self, coords: np.array) -> bool:
        """
        Check if the given coordinates are inside the Polygon object.
        :param coords: X,Y coordinates in a numpy array format: np.array[x,y]
        :return: boolean
        """
        return self.target_polygon.inside_the_polygon(coords=coords)
