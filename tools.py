from definitions import Player, Coordinates
from requests import get

PLAYERS_ENDPOINT = "https://map.earthmc.net/tiles/players.json"
MARKERS_ENDPOINT = "https://map.earthmc.net/tiles/minecraft_overworld/markers.json"


class Calculator:
    def __init__(self, prefs):
        self.self_ign = prefs["self_ign"]

        self.player_refresh_delay = prefs["player_data_refresh_delay"]
        self.player_activity_timeout = 15

        self.recent_players = {}  # visible within last 30 seconds +-
        self.logged_players = []  # visible ever

    def refresh_player_data(self, exclude_self: bool = True) -> list:
        self.visible_players = []  # Visible right now

        response = get(PLAYERS_ENDPOINT).json()

        for player in response["players"]:
            if exclude_self:
                if player["name"] == self.self_ign:
                    continue

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
                    self.recent_players[player_name].time_since_visible += self.player_refresh_delay

                    if self.recent_players[player_name].time_since_visible > self.player_activity_timeout:
                        self.recent_players.pop(player_name)

    def refresh_base_data(self):
        response = get(MARKERS_ENDPOINT).json()

        towns = response[0]["markers"]

        map = []

        self.nation_spawns = {}

        # towns_coords and town_coords are specifically for determining whether a point is in any town
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
            else:
                nation_name = str(town["tooltip"]).split("(Capital of ")[1]
                nation_name = (nation_name.split(")\n")[0]).strip()

                blacklisted_nation_spawns = []
                with open("blacklisted_spawns.csv", "r") as file:
                    for line in file:
                        blacklisted_nation_spawns.append(line.strip().lower())

                if nation_name.lower() in blacklisted_nation_spawns:
                    continue

                nation_spawn_point = Coordinates(town["point"]["x"], 0, town["point"]["z"])
                self.nation_spawns[nation_name] = nation_spawn_point

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

    def find_out_of_town_players(self):
        out_of_town_players = []
        for player in self.recent_players:
            in_town = self.is_player_in_town(player)
            if not in_town:
                out_of_town_players.append(player)
        return sorted(out_of_town_players)

    def calculate_coords_separation(self, coords_1, coords_2):
        x_gap = abs(coords_2.X - coords_1.X)
        z_gap = abs(coords_2.Z - coords_1.Z)

        separation = int((x_gap**2 + z_gap**2)**(1/2))
        return separation

    def calculate_player_separation(self, player_1_name: str, player_2_name: str) -> int:

        # check players are recent
        if player_1_name in self.recent_players and player_2_name in self.recent_players:
            player_1 = self.recent_players[player_1_name]
            player_2 = self.recent_players[player_2_name]

            separation = self.calculate_coords_separation(player_1.coords, player_2.coords)
            return separation

    def calculate_distance_to_player(self, target_player: str) -> int:

        distance = self.calculate_player_separation(self.my_name, target_player)
        return distance

    def find_nearest_nation_spawn(self, coords):
        closest_spawn = ""
        closest_spawn_distance = 999999
        for nation_spawn in self.nation_spawns:
            distance = self.calculate_coords_separation(coords, self.nation_spawns[nation_spawn])
            if distance < closest_spawn_distance:
                closest_spawn_distance = distance
                closest_spawn = nation_spawn
        return (closest_spawn, closest_spawn_distance)

    def find_nearest_nation_spawn_to_player(self, player_name) -> tuple[str, int]:
        coords = self.recent_players[player_name].coords
        closest_spawn = self.find_nearest_nation_spawn(coords)
        return closest_spawn


# Hopefully in future, seperate data from calculator
