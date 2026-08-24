from pathlib import Path
from classes import *
import random





def cycle(league : Table) -> None:
	print("Current matchup is:")
	sleep(.3)
	print(*league.get_current_matchup(), sep=" vs ")
	home, away = league.get_current_matchup()
	sleep(1)
	while not (home_score := input(f"{home} score?")).isdigit():
		sleep(.3)
		print("Can only be a natural number!")
	sleep(.5)

	while not (away_score := input(f"{away} score?")).isdigit():
		sleep(.3)
		print("Can only be a natural number!")
	sleep(.5)

	


def request_save() -> None:
	pass


def main() -> None:
	print("\n\n\n")
	print("\t\t\t\t\t&&&LEAGUE DRAWER&&&")
	sleep(1)

	league = Table()
	league.instantiate()
	sleep(.5)
	league.start_season()

	league.export()

	while not league.ended:
		cycle()
		request_save()


	


		
















if __name__ == "__main__":
	main()
