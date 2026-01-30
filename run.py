from hunting import Hunter
from tools import Calculator, Data


# Preferences
self_ign = ""
player_data_refresh_delay = 15
base_data_refresh_delay = 600


calculator = Calculator()
data_finder = Data(self_ign)


def select_mode():
    running = False
    while not running:
        mode = input("""Select mode\nHunting -> 1\nPlayer Finder -> 2\nEnter choice: """)

        if mode == 1:
            hunter = Hunter(calculator, data_finder, player_data_refresh_delay, base_data_refresh_delay)
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
