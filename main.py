from pathlib import Path
from kml_processor import KMLProcessor
from inspector import CoordinateInspector
from shapes import Rectangle
import numpy as np

if __name__ == '__main__':
    # TODO: pull KML with scrapy
    # TODO: maintain a list of already scanned documents and only scan the new ones
    # TODO: Last scanned date file could also work
    test_kml_path = Path('./resources/forg_korl_teszt.kml')
    kml_processor = KMLProcessor(path=test_kml_path)
    kml_processor.parse_kml()
    coords_np = kml_processor.get_coords_np_array_from_kml()

    target_rectangle = Rectangle(
        a_coords=np.array([47.503500, 19.088696]),
        b_coords=np.array([47.501645, 19.088696]),
        d_coords=np.array([47.503500, 19.092250])
    )

    coord_inspector = CoordinateInspector(target_polygon=target_rectangle)
    for coord in coords_np:
        if coord_inspector.inside_the_polygon(coords=coord):
            # TODO: send notification with link and some message (maybe from the description).
            print("You are inside the danger zone.")

    # target_rectangle = {
    #     'top_left': np.array([47.503500, 19.088696]),
    #     'bottom_left': np.array([47.501645, 19.088696]),
    #     'top_right': np.array([47.503500, 19.092250])
    # }
    print(coord_inspector.inside_the_polygon(coords=np.array(['47.502415', '19.090600'])))
