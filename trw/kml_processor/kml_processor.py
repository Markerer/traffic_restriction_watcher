from pathlib import Path
from pykml import parser
from typing import List, Tuple, Union
import numpy as np
from .exceptions import NoPathProvidedException, InvalidKMLException


class KMLProcessor:

    def __init__(self, path: Path = None):
        """
        Initializing the KMLProcessor class and optionally parsing and processing
        the given KML file.
        :param path: Path object pointing to the KML file [optional].
        """
        self.kml_object = None
        self._path = path

    def _check_init_and_function_path(self, path: Union[Path, None]) -> Path:
        if path is not None:
            return path
        if self._path is None:
            raise NoPathProvidedException
        else:
            return self._path

    def _check_kml_object(self):
        if self.kml_object is None:
            raise InvalidKMLException

    def parse_kml(self, path: Path = None):
        """
        Parses the KML file under the given path.
        :param path: Path object pointing to the KML file [optional - if not provided, class attribute will be used].
        :return: parsed KML object.
        """
        path = self._check_init_and_function_path(path=path)
        if not path.is_file():
            raise FileNotFoundError(f'{path} file not found.')
        self.kml_object = parser.parse(fileobject=path)
        return self.kml_object

    def get_coords_list_from_kml(self) -> List[Tuple[str, str]]:
        """
        Extracts all coordinates from the previously parsed KML object.
        :return: List of the unique coordinate sets.
        """
        self._check_kml_object()
        lat_coords = []
        lon_coords = []
        coord_list = []
        root = self.kml_object.getroot().Document
        for folder in root.Folder:
            for placemark in folder.Placemark:
                if placemark.find('{http://www.opengis.net/kml/2.2}LineString') is not None:
                    coord_list = (entry.strip() for entry in
                                  list(placemark.LineString.coordinates.text.strip().split('\n')))

                elif placemark.find('{http://www.opengis.net/kml/2.2}Polygon') is not None:
                    coord_list = (entry.strip() for entry in
                                  list(placemark.Polygon.outerBoundaryIs\
                                       .LinearRing.coordinates.text.strip().split('\n')))

                for coord in coord_list:
                    tmp = coord.split(',')
                    lon_coords.append(tmp[0])
                    lat_coords.append(tmp[1])

        # removing duplicates with set
        return list(set(zip(lat_coords, lon_coords)))

    def get_coords_np_array_from_kml(self) -> np.array:
        """
        Extracts all coordinates from the previously parsed KML object.
        :return: List of the unique coordinate sets in a numpy array object.
        """
        return np.array(self.get_coords_list_from_kml())
