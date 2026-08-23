from pathlib import Path
from classes import *
import random





def cycle() -> None:
	while True:
		score = 0


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
