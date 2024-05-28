import chessgame


def main():
    mainscreen = chessgame.display.initialize()
    chessgame.game.run(mainscreen)


if __name__ == "__main__":
    main()
