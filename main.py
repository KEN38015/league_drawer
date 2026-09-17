from pathlib import Path
from classes import *
import random






def display(league : Table) -> None:
	sleep(.5)
	print(league)




def submit(league : Table) -> tuple(int):
	def ask_score() -> int:
		inp = input()
		return int(inp) if inp.isdigit() else ask_score()

	home_team, away_team = league.get_current_matchup()
	print(f"Current matchup is {home_team} against {away_team}")
	sleep(.4)

	print(f"Score for {home_team} (home team)?")
	home_score = ask_score()
	sleep(.6)

	print(f"Score for {away_team} (away team)?")
	away_score = ask_score()
	sleep(.6)

	print(f"Submitting score for {home_team} vs {away_team}:")
	print(f"{home_score} - {away_score}?")
	sleep(.5)
	while (choice := input("Submit? ")) not in {"yes", "no", "y", "n"}:
		sleep(.2)
		print("?")

	if "n" in choice:
		print("Exitting...")
		return

	return (home_score, away_score)



def show_fixtures(league : Table) -> None:
	print("Show all matches (all) or a single match (single)?")
	while (choice := input().lower()) not in {"all", "single"}:
		sleep(.2)
	if choice == "all":
		league.show_fixtures()
	else:
		print("What match number?")
		while not (num := input()).isdigit():
			sleep(.3)
		sleep(.5)
		print(f"match no {int(num)}:\n")
		print(*league.matchups[int(num)], sep=" vs ")



def show_history(league : Table) -> None:
	sleep(.3)
	if league.matchup_no < 1:
		print("No matches were played yet!")
		return
	print(f"{league.matchup_no} matche{"s" if league.matchup_no - 1 else ""} were played!")
	for ind in range(1, league.matchup_no+1):
		print(f"{ind}. {league.matchups[ind][0]} - {league.matchups[ind][1]}")
		print(f"\t{league.results[ind][0]} {league.results[ind][1]}")


def main() -> None:
	print("\n\n\n")
	print("\t\t\t\t\t&&&LEAGUE DRAWER&&&")
	sleep(1)

	league = Table()

	league.instantiate()
	league.start_season()


	while not league.ended:
		options = ["display", "submit", "history", "fixtures", "save", "delete", "exit"]
		prompts = [
			"show table", 
			"submit next scorline",
			"see previous matches",
			"see match fixtures",
			"save contents",
			"delete table",
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
				league.submit_scoreline(league.get_current_matchup, submit(league))


			case "history":
				show_history(league)


			case "fixtures":
				show_fixtures(league)


			case "save":
				league.save()

			case "delete":
				pass
			case _:
				break

		sleep(.5)
	else:
		pass
		# league ended type shit


		







		
















if __name__ == "__main__":
	main()
