from requests import get
from time import sleep

import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


PLAYERS_ENDPOINT = "https://map.earthmc.net/tiles/players.json"
MARKERS_ENDPOINT = "https://map.earthmc.net/tiles/minecraft_overworld/markers.json"

refresh_delay = 1
player_activity_timeout = 60
refresh_base_data_timer = 300


class Player:
    def __init__(self):
        self.name = ""
        self.coords = ""

        self.is_visible = True
        self.time_since_visible = 0


class Coordinates:
    def __init__(self, X: int, Y: int, Z: int):
        self.X = X
        self.Y = Y
        self.Z = Z


class Main:
    def __init__(self, my_name: str):
        self.my_name = my_name

        self.recent_players = {}  # Visible in short term
        self.logged_players = []  # Visible at any point

    def refresh_player_data(self) -> list:
        self.visible_players = []  # Visible right now

        response = get(PLAYERS_ENDPOINT).json()

        for player in response["players"]:
            self.visible_players.append(player["name"])
            if player["name"] not in self.logged_players:
                self.logged_players.append(player["name"])

            coords = Coordinates(player["x"], player["y"], player["z"])
            if player["name"] not in self.recent_players:
                new_player = Player()
                new_player.name = player["name"]
                new_player.coords = coords

                self.recent_players[player["name"]] = new_player

            else:
                self.recent_players[player["name"]].coords = coords
                self.recent_players[player["name"]].is_visible = True
                self.recent_players[player["name"]].time_since_visible = 0

        for player_name in self.logged_players:
            if player_name not in self.visible_players:

                if player_name in self.recent_players:
                    self.recent_players[player_name].is_visible = False
                    self.recent_players[player_name].time_since_visible += refresh_delay

                    if self.recent_players[player_name].time_since_visible > player_activity_timeout:
                        self.recent_players.pop(player_name)

    def get_base_data(self):
        response = get(MARKERS_ENDPOINT).json()

        towns = response[0]["markers"]

        map = []

        # towns_coords and town_coords is specifically for determining whether a point is in any town
        # visualisation_coords is for visualising coordinates (both require a different format)
        towns_coords = []

        for town in towns:
            if "points" in str(town):

                border_points = town["points"][0][0]

                visualisation_coords = []
                town_coords = []
                for point in border_points:
                    visualisation_coords.append([point["x"], point["z"] * -1])

                    town_coords.append((point["x"], point["z"]))
                towns_coords.append(town_coords)
                self.towns_coords = towns_coords

                map.append(visualisation_coords)


        # Displaying map
        # fig, ax = plt.subplots()

        # collection = PolyCollection(map, facecolor="red", edgecolor="black")

        # ax.add_collection(collection)

        # ax.autoscale_view()
        #plt.show()

    def get_player_visibility_status(self, player_name):
        if player_name in self.visible_players:
            return "visible"
        elif player_name in self.recent_players:
            return "recent"
        elif player_name in self.logged_players:
            return "logged"
        else:
            return "unknown"

    def is_player_in_town(self, player_name):

        player_coords = self.recent_players[player_name].coords

        point = Point(player_coords.X, player_coords.Z)

        in_a_town = False
        for town_coords in self.towns_coords:
            town_shape = Polygon(town_coords)
            if town_shape.contains(point):
                in_a_town = True
        return in_a_town

    def find_out_of_town_players(self):
        out_of_town_players = []
        for player in self.recent_players:
            in_town = self.is_player_in_town(player)
            if not in_town:
                out_of_town_players.append(player)
        return sorted(out_of_town_players)

    def calculate_player_separation(self, player_1_name: str, player_2_name: str) -> int:

        # check players are recent
        if player_1_name in self.recent_players and player_2_name in self.recent_players:
            player_1 = self.recent_players[player_1_name]
            player_2 = self.recent_players[player_2_name]

            x_gap = abs(player_2.coords.X - player_1.coords.X)
            z_gap = abs(player_2.coords.Z - player_2.coords.Z)

            separation = int((x_gap**2 + z_gap**2)**(1/2))
            return separation

    def calculate_distance_to_player(self, target_player: str) -> int:

        distance = self.calculate_player_separation(self.my_name, target_player)

        return distance

    def run(self):
        self.get_base_data()
        while True:
            self.refresh_player_data()

            number_of_refreshes = 0
            if number_of_refreshes * refresh_delay > refresh_base_data_timer:
                self.get_base_data()
            print(self.find_out_of_town_players())


            #print("-----------------------------\n\n")
            #print(f"Currently visible players: {len(self.visible_players)}\nRecently visible players: {len(self.recent_players)}\nAll known players: {len(self.logged_players)}")
            #print("\n\n-----------------------------")

            sleep(refresh_delay)


main = Main(my_name="")

main.run()
