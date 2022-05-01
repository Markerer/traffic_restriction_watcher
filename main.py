from pykml import parser
from pathlib import Path
from typing import Tuple
import numpy as np


def parse_kml(path: Path):
    if not path.is_file():
        raise FileNotFoundError(f'{path} file not found.')
    with open(path) as f:
        return parser.parse(fileobject=f)


def process_kml(kml) -> zip:
    lat_coords = []
    lon_coords = []
    coord_list = []
    print(kml.getroot().Document.name)
    root = kml.getroot().Document
    for folder in root.Folder:
        for placemark in folder.Placemark:
            if placemark.find('{http://www.opengis.net/kml/2.2}LineString') is not None:
                coord_list = (entry.strip() for entry in
                              list(placemark.LineString.coordinates.text.strip().split('\n')))

            elif placemark.find('{http://www.opengis.net/kml/2.2}Polygon') is not None:
                coord_list = (entry.strip() for entry in
                              list(placemark.Polygon.outerBoundaryIs.LinearRing.coordinates.text.strip().split('\n')))

            for coord in coord_list:
                tmp = coord.split(',')
                lon_coords.append(tmp[0])
                lat_coords.append(tmp[1])

    return zip(lat_coords, lon_coords)


def inside_the_rectangle(coords: Tuple[str, str]) -> bool:
    target_rectangle = {
        'top_left': np.array([47.503500, 19.088696]),
        'bottom_left': np.array([47.501645, 19.088696]),
        'top_right': np.array([47.503500, 19.092250])
    }

    # Point is inside the rectangle if
    # (0 < AM * AB < AB * AB) && (0 < AM * AD < AD * AD)
    # where M is the point to evaluate
    M = np.array(list(coords)).astype(float)
    AM = M - target_rectangle.get('top_left')
    AB = target_rectangle.get('top_right') - target_rectangle.get('top_left')
    AD = target_rectangle.get('bottom_left') - target_rectangle.get('top_left')

    ABdotAB = np.dot(AB, AB)
    AMdotAB = np.dot(AM, AB)
    ADdotAD = np.dot(AD, AD)
    AMdotAD = np.dot(AM, AD)

    return (0 < AMdotAB and AMdotAB < ABdotAB) and (0 < AMdotAD and AMdotAD < ADdotAD)


if __name__ == '__main__':
    test_kml_path = Path('./resources/forg_korl_teszt.kml')
    kml_object = parse_kml(path=test_kml_path)
    coords_zip = process_kml(kml=kml_object)
    coords_list = list(set(coords_zip))
    print(coords_list)
    print(len(coords_list))
    print(inside_the_rectangle(('47.502415', '19.090600')))

