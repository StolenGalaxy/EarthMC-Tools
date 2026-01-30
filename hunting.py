from time import sleep

import pyperclip

refresh_delay = 10
player_activity_timeout = 30
base_refresh_delay = 120


class Hunter:
    def __init__(self, calculator, prefs):
        self.calculator = calculator

        self.player_refresh_delay = prefs["player_data_refresh_delay"]
        self.base_refresh_delay = prefs["base_data_refresh_delay"]

    def find_optimal_target_with_spawn(self) -> tuple[str, str]:
        potential_targets = self.calculator.find_out_of_town_players()

        shortest_distance = 999999
        optimal_target = ""
        closest_spawn = ""
        player_coords = ""

        blacklisted_players = []

        with open("blacklisted_players.csv", "r") as file:
            for line in file.readlines():
                blacklisted_players.append(line.strip().lower())

        for target in potential_targets:

            if target.lower() in blacklisted_players:
                continue

            closest_nation_spawn = self.calculator.find_nearest_nation_spawn_to_player(target)

            distance = closest_nation_spawn[1]

            if distance < shortest_distance:
                shortest_distance = distance
                optimal_target = target
                closest_spawn = closest_nation_spawn[0]
                player_coords = self.calculator.recent_players[target].coords

        return (optimal_target, player_coords, closest_spawn, shortest_distance)

    def run(self):
        number_of_refreshes = 0
        while True:
            self.calculator.refresh_player_data()

            if number_of_refreshes * refresh_delay > base_refresh_delay or number_of_refreshes == 0:
                self.calculator.refresh_base_data()
                number_of_refreshes = 0

            target_data = self.find_optimal_target_with_spawn()
            print("-----------------------------\n\n")
            print(f"Optimal target: {target_data[0]}\nCoordinates: ({target_data[1].X}, {target_data[1].Z})\nNearest nation spawn is {target_data[2]} which is {target_data[3]} blocks away")
            print("\n\n-----------------------------")

            pyperclip.copy(f"#goto {target_data[1].X} {target_data[1].Z}")

            sleep(refresh_delay)
            number_of_refreshes += 1
