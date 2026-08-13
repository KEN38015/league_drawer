
from classes import *
import random






def main() -> None:
    print("\n\n\n")
    print(" " * 40 + "***LEAGUE DRAWER***")
    sleep(.5)

    league = Table()
    league.import_preset()
    
    print(league.get_teams())
    if len(league.get_teams()) % 2:
        print("Amount of clubs cannot be negative!")
        sleep(1.5)
        main()
    league.start_season()




















if __name__ == "__main__":
	main()
