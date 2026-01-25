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

        self.is_visible = True
        self.time_since_visible = 0


class Coordinates:
    def __init__(self, X, Y, Z):
        self.X = X
        self.Y = Y
        self.Z = Z


class Main:
    def __init__(self, my_name):
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

    def calculate_player_separation(self, player_1_name: str, player_2_name: str) -> int:

        # check players are recent
        if player_1_name in self.recent_players and player_2_name in self.recent_players:
            player_1 = self.recent_players[player_1_name]
            player_2 = self.recent_players[player_2_name]

            x_gap = abs(player_2.coords.X - player_1.coords.X)
            z_gap = abs(player_2.coords.Z - player_2.coords.Z)

            separation = int((x_gap**2 + z_gap**2)**(1/2))
            return separation

    def run(self):
        while True:
            self.refresh_player_data()

            print("-----------------------------\n\n")
            print(f"Currently visible players: {len(self.visible_players)}\nRecently visible players: {len(self.recent_players)}\nAll known players: {len(self.logged_players)}")
            print("\n\n-----------------------------")

            sleep(refresh_delay)


main = Main(my_name="")

main.run()
