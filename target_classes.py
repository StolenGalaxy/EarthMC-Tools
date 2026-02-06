from time import sleep

import pyperclip


class Hunter:
    def __init__(self, calculator, prefs):
        self.calculator = calculator
        self.player_refresh_delay = prefs["player_data_refresh_delay"]
        self.base_refresh_delay = prefs["base_data_refresh_delay"]

    def find_optimal_target_with_spawn(self) -> tuple[str, str]:
        potential_targets = self.calculator.find_players_by_town_status(False)

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

            if number_of_refreshes * self.player_refresh_delay > self.base_refresh_delay or number_of_refreshes == 0:
                self.calculator.refresh_base_data()
                number_of_refreshes = 0

            target_data = self.find_optimal_target_with_spawn()
            print("-----------------------------\n\n")
            print(f"Optimal target: {target_data[0]}\nCoordinates: ({target_data[1].X}, {target_data[1].Z})\nNearest nation spawn is {target_data[2]} which is {target_data[3]} blocks away")
            print("\n\n-----------------------------")

            pyperclip.copy(f"#goto {target_data[1].X} {target_data[1].Z}")

            sleep(self.player_refresh_delay)
            number_of_refreshes += 1


class PlayerFinder:
    def __init__(self, calculator, prefs, required_properties):
        self.calculator = calculator
        self.player_refresh_delay = prefs["player_data_refresh_delay"]
        self.base_refresh_delay = prefs["base_data_refresh_delay"]

        self.properties = required_properties

    def search_players(self):
        self.calculator.refresh_player_data()
        self.calculator.refresh_base_data()
        if "in_town" in self.properties:
            available_players = self.calculator.find_players_by_town_status(self.properties["in_town"])
        else:
            available_players = [player for player in self.calculator.recent_players]

        check_minimum_spawn = False
        check_maximum_spawn = False
        if "minimum_spawn_distance" in self.properties:
            check_minimum_spawn = True
        if "maximum_spawn_distance" in self.properties:
            check_maximum_spawn = True
        for player in available_players:
            nearest_spawn, nearest_spawn_distance = self.calculator.find_nearest_nation_spawn_to_player(player)

            if check_minimum_spawn:
                if nearest_spawn_distance < self.properties["minimum_spawn_distance"]:
                    available_players.remove(player)
                    continue

            if check_maximum_spawn:
                if nearest_spawn_distance > self.properties["maximum_spawn_distance"]:
                    available_players.remove(player)

        return available_players

    def run(self):
        results = self.search_players()

        print(results)
