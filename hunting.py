from requests import get
from time import sleep

from multiprocessing import Process

import pyperclip

refresh_delay = 10
player_activity_timeout = 15
base_refresh_delay = 120


class Hunter:
    def __init__(self, calculator: GeneralCalculations, data: GetData):
        self.calculator = calculator

    def find_optimal_target_with_spawn(self) -> tuple[str, str]:
        potential_targets = self.find_out_of_town_players()
        if self.my_name in potential_targets:
            potential_targets.remove(self.my_name)

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

            closest_nation_spawn = self.find_nearest_nation_spawn_to_player(target)

            distance = closest_nation_spawn[1]

            if distance < shortest_distance:
                shortest_distance = distance
                optimal_target = target
                closest_spawn = closest_nation_spawn[0]
                player_coords = self.recent_players[target].coords

        return (optimal_target, player_coords, closest_spawn, shortest_distance)

    def run(self,):
        number_of_refreshes = 0
        while True:
            self.data.refresh_player_data()

            if number_of_refreshes * refresh_delay > base_refresh_delay or number_of_refreshes == 0:
                self.data.refresh_base_data()
                number_of_refreshes = 0

            target_data = self.find_optimal_target_with_spawn()
            print("-----------------------------\n\n")
            print(f"Optimal target: {target_data[0]}\nCoordinates: ({target_data[1].X}, {target_data[1].Z})\nNearest nation spawn is {target_data[2]} which is {target_data[3]} blocks away")
            print("\n\n-----------------------------")

            pyperclip.copy(f"#goto {target_data[1].X} {target_data[1].Z}")

            sleep(refresh_delay)
            number_of_refreshes += 1
