from hunting import Hunter
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
        #mode = int(input("""Select mode\nHunting -> 1\nPlayer Finder -> 2\nEnter choice: """))
        mode = 1

        if mode == 1:
            hunter = Hunter(calculator, prefs)
            running = True
            return hunter

        elif mode == 2:
            running = True
            # (future implementation)


def main():
    mode = select_mode()
    mode.run()


if __name__ == "__main__":
    main()
