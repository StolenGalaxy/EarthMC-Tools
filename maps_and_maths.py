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
            # uncomment to enable map
            plot_process = Process(target=self.plot_map, args=(map, ))
            plot_process.start()


class Geometry:
    def __init__(self):
        pass

    def is_point_in_polygon(self, point: tuple[int, int], polygon: list[int]) -> bool:
        shapely_point = Point(point[0], point[1])

        in_a_town = False
        for town_coords in self.towns_coords:
            town_shape = Polygon(town_coords)
            if town_shape.contains(shapely_point):
                in_a_town = True
        return in_a_town
