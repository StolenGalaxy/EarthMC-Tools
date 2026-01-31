# Might add more map functionality in future

import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from multiprocessing import Process


class Map:
    def __init__(self):
        pass

    def plot_map(self, map, fill_colour: str = "red", border_colour: str = "black"):
        fig, ax = plt.subplots()

        collection = PolyCollection(map, facecolor=fill_colour, edgecolor=border_colour)

        ax.add_collection(collection)

        ax.autoscale_view()
        plt.show()

        if not self.already_plotted:
            self.already_plotted = True
            plot_process = Process(target=self.plot_map, args=(map, ))
            plot_process.start()


class Geometry:
    def __init__(self):
        pass

    def is_point_in_polygon(self, point: tuple[int, int], polygon: list[int]) -> bool:
        shapely_point = Point(point[0], point[1])

        shapely_polygon = Polygon(polygon)

        point_in_polygon = shapely_polygon.contains(shapely_point)

        return point_in_polygon
