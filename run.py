from target_classes import Hunter, PlayerFinder
from tools import Calculator


# Preferences

prefs = {
    "self_ign": "",
    "player_data_refresh_delay": 3,
    "base_data_refresh_delay": 600

}


calculator = Calculator(prefs)


def select_mode():
    running = False
    while not running:
        mode = int(input("""------------- Select mode -------------\nHunting -> 1\nAnalysing -> 2\nEnter choice: """))

        if mode == 1:
            hunter = Hunter(calculator, prefs)
            running = True
            return hunter

        elif mode == 2:
            # temp
            required_properties = {
                "in_town": False,
                "minimum_spawn_distance": 0,
                "maximum_spawn_distance": 10000
            }

            player_finder = PlayerFinder(calculator, prefs, required_properties)
            running = True
            return player_finder


def main():
    mode = select_mode()
    mode.run()


if __name__ == "__main__":
    main()
