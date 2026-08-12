
from classes import *
import random





def main() -> None:
    print("\n\n\n")
    print(" " * 40 + "***LEAGUE DRAWER***")
    sleep(.5)
    premier_league = Table("Premier League")
    premier_league.import_preset()
    print(premier_league)
    while (change := input("add/remove teams?")) not in ["add", "remove", "no"]:
        pass
    # if change == "add":
    #     premier_league.add_team()

    if len(clubs) % 2:
        print("Amount of clubs cannot be negative!")
        sleep(1.5)
        main()
    premier_league.start_season()




















if __name__ == "__main__":
	main()
