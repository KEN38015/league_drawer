from pathlib import Path
from classes import *
import random






def display(league : Table) -> None:
	sleep(.5)
	print(league)




def submit(league : Table) -> None:
	pass

def main() -> None:
	print("\n\n\n")
	print("\t\t\t\t\t&&&LEAGUE DRAWER&&&")
	sleep(1)

	league = Table()

	league.instantiate()
	league.start_season()


	while not league.ended:
		options = ["display", "submit", "history", "fixtures", "save", "exit"]
		prompts = [
			"show table", 
			"submit next scorline",
			"see previous matches",
			"see match fixtures",
			"save contents",
			"exit",
		]
		print("What do you wish to do?")
		sleep(.2)
		for prompt, option in zip(prompts, options):
			print(f"\t{prompt.capitalize()} ({option})")
			sleep(.1)

		while (choice := input().lower().strip()) not in options:
			sleep(.2)
			print("Not in choices!")
		sleep(.7)

		match choice:
			case "display":
				display(league)


			case "submit":
				submit(league)


			case "history":
				pass


			case "fixtures":
				pass


			case "save":
				pass


			case "exit":
				pass

		sleep(.5)



		







		
















if __name__ == "__main__":
	main()
