from pathlib import Path
from classes import *
import random






def display(league : Table) -> None:
	sleep(.5)
	OUTPUT(league)




def submit(league : Table) -> tuple(int):
	def ask_score() -> int:
		inp = input()
		return int(inp) if inp.isdigit() else ask_score()

	home_team, away_team = league.get_current_matchup()
	OUTPUT(f"Current matchup is {home_team} against {away_team}")
	sleep(.4)

	OUTPUT(f"Score for {home_team} (home team)?")
	home_score = ask_score()
	sleep(.6)

	OUTPUT(f"Score for {away_team} (away team)?")
	away_score = ask_score()
	sleep(.6)

	OUTPUT(f"Submitting score for {home_team} vs {away_team}:")
	OUTPUT(f"{home_score} - {away_score}?")
	sleep(.5)
	while (choice := input("Submit? ")) not in {"yes", "no", "y", "n"}:
		sleep(.2)
		OUTPUT("?")

	if "n" in choice:
		while (is_exit := input("Exit (exit) or submit new (new)? ")) not in {"exit", "new"}:
			sleep(.2)
			OUTPUT("?")
		if is_exit == "exit":
			OUTPUT("Exitting...")
			return None
		return submit(league)

	return (home_score, away_score)



def show_fixtures(league : Table) -> None:
	OUTPUT("Show all matches (all) or a single match (single)?")
	while (choice := input().lower()) not in {"all", "single"}:
		sleep(.2)
	if choice == "all":
		league.show_fixtures()
	else:
		OUTPUT("What match number?")

		while True:
			num = input()
			sleep(.3)
			if not num.isdigit():
				OUTPUT("Positive whole numbers only!")
				sleep(.5)
				continue
			if not len(league.matchups)+1 > int(num) > 0:
				OUTPUT("match number out of range!")
				sleep(.5)
				continue
			break
		sleep(.3)
		OUTPUT(f"match no {int(num)}:\n")
		OUTPUT(*league.matchups[int(num)-1], sep=" vs ")



def show_history(league : Table) -> None:
	sleep(.3)
	if league.matchup_no < 1:
		OUTPUT("No matches were played yet!")
		return
	OUTPUT(f"{league.matchup_no} match{"es" if league.matchup_no - 1 else ""} were played!")
	for ind in range(1, league.matchup_no):
		OUTPUT(f"{ind}. {league.matchups[ind][0]} - {league.matchups[ind][1]}")
		home_res, away_res = league.results[ind][0], league.results[ind][1]
		symbol = "=" if home_res == away_res else (">" if home_res > away_res else "<")
		OUTPUT(f"\t{home_res} {symbol} {away_res}")


def delete(league : Table) -> None:
	sleep(.3)
	OUTPUT("CONFIRM DELETE???")
	while (is_del := input()) not in {"y", "n", "yes", "no"}:
		sleep(.3)
	sleep(.5)
	OUTPUT("deleting", end=".")
	for _ in range(5):
		OUTPUT(".", end="")
	directory = Path("data/in_use") / (self.title.replace(" ", "_") + ".league")
	for child in directory.iterdir():
		child.unlink()
	directory.rmdir()
	OUTPUT(f"Deleted file {directory.name}, exitting to main menu")
	sleep(1)

def main() -> None:
	OUTPUT("\n\n\n")
	OUTPUT("\t\t\t\t\t&&&LEAGUE DRAWER&&&")
	sleep(1)

	league = Table()

	league.instantiate()
	league.start_season()


	while not league.ended:
		options = ["display", "config", "submit", "history", "fixtures", "save", "delete", "exit"]
		prompts = [
			"show table", 
			"configure table",
			"submit next scorline",
			"see previous matches",
			"see match fixtures",
			"save contents",
			"delete table",
			"exit",
		]
		OUTPUT("What do you wish to do?")
		sleep(.2)
		for prompt, option in zip(prompts, options):
			OUTPUT(f"\t({option}) {prompt.capitalize()}")
			sleep(.1)

		while (choice := input().lower().strip()) not in options:
			sleep(.2)
			OUTPUT("Not in choices!")
		sleep(.7)

		match choice:
			case "display":
				display(league)


			case "submit": 
				if (s := submit(league)) is None:
					continue
				league.add_result(league.get_current_matchup(), s)


			case "history":
				show_history(league)


			case "fixtures":
				show_fixtures(league)


			case "save":
				league.save()

			case "delete":
				delete(league)
				main()

			case "config":
				league.config_table()

			case "exit":
				main()


		sleep(.5)
	else:
		pass
		# league ended type shit


		







		
















if __name__ == "__main__":
	main()
