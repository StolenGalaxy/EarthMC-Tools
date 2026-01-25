from requests import get
from time import sleep

PLAYERS_ENDPOINT = "https://map.earthmc.net/tiles/players.json"
MARKERS_ENDPOINT = "https://map.earthmc.net/tiles/minecraft_overworld/markers.json"

refresh_delay = 5
player_activity_timeout = 30


class Player:
    def __init__(self):
        self.name = ""
        self.coords = ""

        self.visible = True
        self.time_since_visible = 0


class Coordinates:
    def __init__(self, X, Y, Z):
        self.X = X
        self.Y = Y
        self.Z = Z


class Main:
    def __init__(self, my_name):
        self.my_name = my_name

        self.active_players = {}
        self.logged_players = []

    def update_player_data(self) -> list:

        response = get(PLAYERS_ENDPOINT).json()

        for player in response["players"]:
            if player["name"] not in self.logged_players:
                self.logged_players.append(player["name"])

            coords = Coordinates(player["x"], player["y"], player["z"])
            if player["name"] not in self.active_players:
                new_player = Player()
                new_player.name = player["name"]
                new_player.coords = coords

                self.active_players[player["name"]] = new_player

            else:
                self.active_players[player["name"]].coords = coords


    # def calculate_player_seperation(self, player_1_name, player_2_name):

    #     player_1 = self.active_players[player_1_name]
    #     player_2 = self.active_players[player_2_name]

    #     x_distance = abs(player_2.coords.X - player_1.coords.X)
    #     z_distance = abs(player_2.coords.Z - player_1.coords.Z)

    #     print(x_distance, z_distance)

    def run(self):
        while True:
            self.update_player_data()

            sleep(refresh_delay)


main = Main(my_name="")

main.run()
