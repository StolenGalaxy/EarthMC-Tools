from hunting import Hunter

from tools import Calculator, Data

hunter = Hunter()

calculator = Calculator()

data_finder = Data()

running = False
while not running:
    mode = input("""Select mode\nHunting -> 1\nPlayer Finder -> 2\nEnter choice: """)

    if mode == 1:
        running = True
        hunter.run(calculator, data_finder)
    elif mode == 2:
        running = True
        # Here for future implementation
        # player_finder.run(calculator, data_finder)
