import threading
from time import sleep
from pathlib import Path
import random




class Table:
	# format {stat : (abbr, width)}
	#					width 0 if custom / dependent

	# name & rank show always
	existing_stats = {
		# "name" : ("Name", 0),
		"points" : ("Pts", 3),
		"wins" : ("W", 2),
		"draws" : ("D", 2),
		"losses" : ("L", 2),
		"matches played" : ("MP", 2),
		"home goals" : ("HG", 2),
		"away goals" : ("AG", 2),
		"goals scored" : ("GF", 2),
		"goals conceded" : ("GA", 2),
		"goal difference" : ("GD", 2),
	}
	stats_showing = [
		"matches played",
		"wins",
		"draws",
		"losses",
		"points",
		
	]

	skipped = True

	def recieve_inp(self) -> None:
		input()
		self.skipped = False

	def await_inp(self) -> None:
		threading.Thread(target=self.recieve_inp, daemon=True).start()

	def __init__(self, title : str = "LEAGUE",) -> None:
		self.title : str = title
		self.teams : List[Team] = []
		self.ties : List[Team] = []
		self.matchups : List[List[Team]]= []
		self.started : bool = False
		self.ended : bool = False

		self.matchup_no : int = -1
		self.results : list = [] # = {(matchup) : (scoreline resprectively)}



		self.sort_table()

	def copy(self) -> tuple:
		return self.title, self.teams, self.ties, self.matchups, self.started, self.ended

	def paste(self, data : tuple) -> None:
		self.title, self.teams, self.ties, self.matchups, self.started, self.ended = data







	def get_teams(self) -> list:
		return self.teams


	def add_team(self, team : Team) -> None:
		if len(self.teams) >= 99:
			print("Limit Reached!")
			return
		self.teams.append(team)


	def remove_team(self, team : Team) -> bool:
		if self.started:
			return True

		self.teams.remove(team)
		return False


	def add_matchup(self, to_add : Tuple(Team)) -> None:
		self.matchups.append(to_add)

	def remove_matchup(self, to_remove : Tuple(Team)) -> None:
		self.matchups.remove(to_remove)



	def load_preset(self) -> None:
		print("Searching...")
		preset_folder = Path("data/table_presets")
		sleep(.5)
		# scan for presets
		available_presets = [folder for folder in preset_folder.iterdir() 
					if folder.is_dir() and folder.suffix == ".preset"]
		print(f"Found {len(available_presets)} preset{"s" if len(available_presets) - 1 else ""}!")
		sleep(.5)
		print("Select preset:")
		sleep(.2)
		for ind, preset in enumerate(available_presets):
			preset = preset.with_suffix("")
			print(f"{ind+1} - {preset.name.replace("-", "/")}")
			sleep(.4)
		def ask() -> int:
			choice = input("\n")
			return (int(choice) if 1 <= int(choice) <= len(available_presets) else ask()) if choice.isdigit() else ask()
		choice = ask()
		chosen_preset = available_presets[int(choice) - 1]
		print(f"Loading {available_presets[int(choice) - 1].with_suffix("")} preset...")
		sleep(1)
		
		parent = Path("data/table_presets/Premier League 26-27.preset")
		league_data = (parent / "league_data.hex").read_text()
		matchups = (parent / "matchups.hex").read_text()
		
		key = Security()
		key.set_code(league_data)
		league_data = key.dehex_code().split("\n")
		key.set_code(matchups)
		matchups = key.dehex_code().split("\n")
		new = Table(league_data.pop(0))
		for data in league_data:
			new.add_team(Team(*data.split(",")))
		codes = list(map(Team.get_code, new.teams))
		for matchup in matchups:
			new.add_matchup(list(map(lambda team: new.teams[codes.index(team)], matchup.split(", "))))
		sleep(1)

		print("Complete!")
		sleep(.5)

		self.paste(new.copy())


		

		
		

		



	def team_config(self) -> None:
		while (change := input("add/remove teams or no?\n")) not in ["add", "remove", "no"]:
		    pass
		if change == "add":
			while (name := input("Name?\n").strip()) in list(map(Team.get_name, self.get_teams())):
				print("Already registered!")
				sleep(.2)
			sleep(.2)

			while (abbr := input("The name that shows up on the table?\n").strip()) in list(map(Team.get_abbr, self.get_teams())):
				print("Already registered!")
				sleep(.2)
			sleep(.2)
			print(f"Teams: ", end="")
			print(*list(map(Team.get_code, self.get_teams())), sep=", ")
			while not (code := input("3-digit code?\n").upper().strip()).isalpha() or len(code) != 3 or code in list(map(Team.get_code, self.get_teams())):
				pass
			sleep(.2)
			self.add_team(Team(name, abbr, code))
			print("Successfully appended team!")
			sleep(.5)
		elif change == "remove":
			if not self.get_teams():
				print("There are no teams yet!")
				sleep(.3)
			else:
				codes = list(map(lambda x: x.code, self.get_teams()))
				print(f"Teams: ", end="")
				print(*codes, sep=", ")
				while (name := input("3-digit code of team to remove:    ").upper()) not in codes:
					print("not in list!")
					sleep(.3)
			self.remove_team(self.get_teams()[codes.index(name)])
		else:
			if not self.get_teams():
				print("There are no teams!")
				sleep(.3)
				self.team_config()

			if len(self.get_teams()) % 2:
				print("Number of teams cannot be odd!")
				sleep(.3)
				self.team_config()

			return

		sleep(.5)
		print("Teams: ", end="")
		print(*list(map(Team.get_abbr, self.get_teams())), sep=", ")
		self.team_config()


	def create_matchups(self, auto : bool) -> list:
		pairings = []
		remaining = self.teams[:]
		n = len(self.teams)
		opponents = (n-1)
		home_available = [opponents] * n
		away_available = [opponents] * n
		total = n*opponents

		for team in self.get_teams():
			team.max_matches = opponents * n

		if auto:
			for home in self.teams[::-1]:
				for away in remaining:
					if home == away:
						continue
					pairings.append([home, away])
				remaining.remove(home)
			n = len(pairings)
			return random.sample(pairings, n) + list(map(lambda pair: pair[::-1], random.sample(pairings, n)))
		else:
			codes = list(map(lambda x: x.code, self.teams))
			

			
			for i in range(total):
				print(f"{i}/{total} matches completed")
				sleep(.1)
				print(f"teams available for home: {" ".join([codes[ind] for ind in range(n) if home_available[ind]])}")
				while (home := input("home team? (3-digit code)\n").upper().strip()) not in codes:
					if home_available[codes.index(home)]:
						break
					sleep(.3)
				home_index = codes.index(home)
				home_available[codes.index(home)] -= 1
				sleep(.2)
				
				print(f"teams available for away: {" ".join([codes[ind] for ind in range(n) if away_available[ind] and codes[ind] != home])}")
				while (away := input("away team? (3-digit code)\n").upper().strip()) not in codes:
					if away_available[codes.index(away)]:
						break
					sleep(.3)
				away_index = codes.index(away)
				away_available[codes.index(away)] -= 1

				pairings.append([self.teams[home_index], self.teams[away_index]])
				sleep(.2)
				input(f"{home} vs {away} add success - continue?\n")
				print("\n\n\n")
			return pairings


	def instantiate(self) -> None:
		while (ask := input("preset, custom or load prev team creation?\n").lower().strip()) not in {"preset", "custom", "load"}:
			sleep(.3)
		sleep(.5)
		match ask:
			case "preset":
				self.load_preset()

			case "custom":
				self.team_config()
				while (choice := input("Manual or Automatic (does not account stadium) match creation?\n").lower().strip()) not in {"manual", "automatic", "auto"}:
					pass
					sleep(.3)
					self.matchups = self.create_matchups("auto" in choice)
					print("Match creation complete!")
					sleep(.4)

			case "load":
				self.import_save()

			case "cancel":
				return

		while (ask := input("show matchups?\n").strip().lower()) not in {"y", "n", "yes", "no"}:
			pass

		if "y" in ask:
			
			while "code" not in (ask := input("print in team name or team code?\n").strip().lower()):
				if "name" in ask:
					break
				sleep(.2)

			while not (ask := input("miliseconds of delay for each display?\n").strip()).isdigit():
				print("whole number!")
				sleep(.3)
			sleep(.3)
			print("(enter to skip)")
			sleep(.5)

			
			self.await_inp()
			for ind, matchup in enumerate(self.matchups):
				matchup = list(map(Team.get_name if ask == "name" else Team.get_code, matchup))
				print(f"{ind+1} - ", end="")
				print(*matchup, sep=" vs ")
				if self.skipped:
					sleep(int(ask) / 1000)




	def start_season(self) -> None:
		self.started = True
		self.matchup_no = 0
		self.results = [(-1, -1)] * len(self.get_teams())
		for team in self.get_teams():
			team.max_matches = len(self.teams) - 2
		if self.matchups:
			return
		
		sleep(.3)
		print("START SEASON!!!")
		sleep(1)

	def end_season(self) -> None:
		pass

	def sort_table(self) -> None:
		if not self.started:
			self.teams.sort(key=lambda t: (-t.points, -t.goal_difference, -t.away_goals))
		self.teams.sort(key=lambda t: t.abbr)
		self.ties = [self.teams[i] for i in range(len(self.teams) - 1) if self.teams[i].get_tiebreaker_values() == self.teams[i + 1].get_tiebreaker_values()]



	def export(self) -> None:
		directory = Path("data/in_use") / (self.title.replace(" ", "_") + ".league")
		directory.mkdir(parents=True, exist_ok=True)

		with open(directory / "league_data.hex", "w") as league_data_file:
			league_data_file.write("\n".join(list(map(Security.enhex,
				list(map(str, [
				self.title,
				*list(map(Team.get_code,  self.ties)),
				self.started,
				self.ended,
				self.matchup_no,
				]))))))

		with open(directory / "matchups.hex", "w") as matchups_file:
			for matchup, score in zip(self.matchups, self.results):
				print(Security.enhex(f"{" ".join(list(map(Team.get_code, matchup)))}" + "-" + f"{" ".join(list(map(str, score)))}"), file=matchups_file)

		with open(directory / "team_data.hex", "w") as team_data_file:
			for team in self.get_teams():
				print(Security.enhex(" ".join(list(map(str, team.export_data())))), file=team_data_file)

	def import_save(self) -> None:
		print("Searching...")
		save_folder = Path("data/in_use")

		# scan for presets
		available_leagues = [folder for folder in save_folder.iterdir() 
					if folder.is_dir() and folder.suffix == ".league"]
		sleep(.4)
		print(f"Found {len(available_leagues)} league{"s" if len(available_leagues) - 1 else ""} in use!")
		sleep(.5)
		print("Select preset:")
		sleep(.2)
		for ind, league in enumerate(available_leagues):
			league = league.with_suffix(".league")
			print(f"{ind+1} - {league.name.replace("-", "/")}")
			sleep(.4)

		def ask() -> int:
			choice = input("\n")
			return (int(choice) if 1 <= int(choice) <= len(available_leagues) else ask()) if choice.isdigit() else ask()
		choice = ask()
		chosen_preset = available_leagues[int(choice) - 1]
		print(f"Loading {available_leagues[int(choice) - 1].with_suffix("")} preset...")
		sleep(1)
		


		parent = Path("data/table_presets/Premier League 26-27.preset")
		league_data = Security.dehex((parent / "league_data.hex").read_text()).split("\n")
		matchups = Security.dehex((parent / "matchups.hex").read_text()).split("\n")
		team_data = Security.dehex((parent / "team_data.hex").read_text()).split("\n")
		
		

		new = Table(league_data[0])


		# import from team_data file
		'''
		self.name,
		self.abbr,
		self.code,
		self.points,
		self.wins,
		self.draws,
		self.losses,
		self.matches_played,
		self.max_matches,
		self.home_goals,
		self.away_goals,
		self.goals_scored, self.goals_conceded, self.goal_difference
		'''

		# import from league_data file

		for data in team_data:
			data = data.split()
			team = Team(data[0])
			team.load(data)
		new.add_team(data)
			


		new.ties = list(map(lambda x: new.get_teams()[list(map(Team.get_code, new.get_teams())).index(x)], league_data[1].split()))
		new.started = league_data[2] == "True"
		new.ended = league_data[3] == "True"
		new.matchup_no = int(league[4])
 



		# import from matchups
		# Security.enhex(f"{" ".join(list(map(Team.get_code, matchup)))}" + "-" + f"{" ".join(score)}")
		matchups = matchups.split("-")
		for m in matchups[0]:
			m = m.split("-")
			t1, t2 = list(map(lambda x: new.teams[list(map(Team.get_code, new.teams)).index(x)], m[0]))
			result = tuple(map(int, m[1].split()))
			new.add_matchup(t1, t2)
		matchups[0]



		sleep(1)

		print("Complete!")
		sleep(.5)

		self.paste(new.copy())


	
	# home then away
	def add_result(self, data1 : Tuple[Team, int], data2 : Tuple[Team, int]):
		team1, res1 = data1
		team2, res2 = data2

		team1.add_scoreline(res1, res2, home=True)
		team2.add_scoreline(res2, res1, home=False)



	def __str__(self) -> str:

		self.sort_table()
		total_width : int = sum(
						[
						5, # rank column
						len(max(self.teams, key=lambda x: len(x.abbr)).abbr) + 2, # longest name + 2 trailings
						sum(
							
							list(map(lambda x: self.existing_stats[x][1] * 2 + len(self.existing_stats[x][0]), self.stats_showing))
							
						),
						len(self.stats_showing) # number of posts

						]
							)
		center = total_width // 2
		lines : list = []

		def border(char : str) -> str:
			return str(" " + char * (total_width - 1))


		# title
		lines.append(" " * (center - len(self.title)//2) + self.title.upper())
		
		lines.append(border("_"))


		identifiers : list = ["| R |"]
		
		longest_name = len(max(self.teams, key=lambda x: len(x.abbr)).abbr) + 2
		identifiers.append(" " * (longest_name // 2 - 2) + "Name" + " " * (longest_name // 2 - 2) + "|")
		for stat in self.stats_showing:
			key, trailings = self.existing_stats[stat]
			identifiers.append(" " * trailings + key + " " * trailings + "|")
			
		lines.append("".join(identifiers) + "")
		lines.append(border("="))

		for rank, team in enumerate(self.teams):
			text = [f"| {rank+1}{" " if rank+1 < 10 else ""}", f" {" ".join(list(map(str.capitalize, team.abbr.split())))}" + " " * (longest_name - len(team.abbr) - 1)]
			info = team.get_info()
			for stat in self.stats_showing:
				trailings = self.existing_stats[stat][1]
				text.append(" " * trailings + str(info[stat]) + " " * (trailings + len(self.existing_stats[stat][0]) - len(str(info[stat]))))



			lines.append("|".join(text) + "|")

		lines.append(border("="))
		return "\n".join(lines)


'''                                                      												  
			 		PREMIER LEAGUE
 _____________________________________________________
| R |     Name     |  MP  |  W  |  D  |  L  |   Pts   |
 =====================================================
| 1 | Liverpool    |  38  |  25 |  9  |  4  |   84    |
| 2 | Arsenal      |  38  |  20 |  14 |  4  |   74    |
| 3 | Man City     |  38  |  21 |  8  |  9  |   71    |
| 4 | Chelsea      |  38  |  20 |  9  |  9  |   69    |
| 5 | Newcastle    |  38  |  20 |  6  |  12 |   66    |
| 6 | Aston Villa  |  38  |  19 |  9  |  10 |   66    |
| 7 | Nottm Forest |  38  |  19 |  8  |  11 |   65    |
 =====================================================




'''







class Team:
	
	def __init__(self,
				name : str,
				abbreviation : str,
				code : str,
				):
		self.name : str = name.strip()
		self.abbr : str = "".join(map(str.capitalize, abbreviation.split())).strip()
		self.code : str = code.strip()
		self.points : int = 0
		self.wins : int = 0 ; self.draws : int = 0 ; self.losses : int = 0
		self.matches_played : int = 0
		self.max_matches : int
		self.home_goals : int = 0 ; self.away_goals : int = 0
		self.goals_scored : int = 0 ; self.goals_conceded : int = 0 ; self.goal_difference : int = 0

	def get_name(self) -> str:
		return self.name

	def get_abbr(self) -> str:
		return self.abbr

	def get_code(self) -> str:
		return self.code
	# resets dependencies
	def recalibrate(self) -> None:
		self.points = 3 * self.wins + self.draws
		self.matches_played = self.wins + self.draws + self.losses
		self.goals_scored = self.home_goals + self.away_goals
		self.goal_difference = self.goals_scored - self.goals_conceded


	def add_scoreline(self, scored : int, conceded : int, *, home : bool) -> None:
		if self.matches_played >= self.max_matches:
			print("Already played all the matches!")
			delay(.5)
			return

		state = "lose" if scored < conceded else ("win" if scored > conceded else "draw")
		if home:
			self.home_goals += scored
		else:
			self.away_goals += scored
		
		match state:
			case "win":
				self.wins += 1
			case "draw":
				self.draws += 1
			case "lose":
				self.losses += 1

		self.recalibrate()
		return

	def get_info(self) -> dict:

		return {
		# "name" : ("Name", 0),
		"points" : self.points,
		"wins" : self.wins,
		"draws" : self.draws,
		"losses" : self.losses,
		"matches played" : self.matches_played,
		"home goals" : self.home_goals,
		"away goals" : self.away_goals,
		"goals scored" : self.goals_scored,
		"goals conceded" : self.goals_conceded,
		"goal difference" :self.goal_difference,
		}

	def get_tiebreaker_values(self) -> list:
		return [
			self.points,
			self.goal_difference,
			self.goals_scored
		]

	def export_data(self) -> List:
		return [
		self.name,
		self.abbr,
		self.code,
		self.points,
		self.wins,
		self.draws,
		self.losses,
		self.matches_played,
		self.max_matches,
		self.home_goals,
		self.away_goals,
		self.goals_scored, self.goals_conceded, self.goal_difference
		]

	def load(self, data : List) -> None:
		self.abbr = data[1]
		self.code = data[2]
		self.points = int(data[3])
		self.wins = int(data[4])
		self.draws = int(data[5])
		self.losses = int(data[6])
		self.matches_played = int(data[7])
		self.max_matches = int(data[8])
		self.home_goals = int(data[9])
		self.away_goals = int(data[10])
		self.goals_scored  = int(data[11])
		self.goals_conceded = int(data[12])
		self.goal_difference = int(data[13])

	def __eq__(self, other) -> bool:
		return self.name == other.name


	def __str__(self) -> str:
		return self.name

















class Security:
	def __init__(self):
		self.code = ""

	def set_code(self, code : str) -> None:
		self.code = code

	def get_code(self) -> str:
		return self.code

	@staticmethod
	def enhex(code : str) -> str:
		return "\n".join(["{:04x}".format(ord(char)) for char in code])

	@staticmethod
	def dehex(code : str) -> str:
		return "".join([chr(int(num, 16)) for num in code.split("\n")])


	def enhex_code(self) -> str:
		return "\n".join(["{:04x}".format(ord(char)) for char in self.code])

	def dehex_code(self) -> str:
		return "".join([chr(int(num, 16)) for num in self.code.split("\n")])



# key = Security()
# f = Path("data/table_presets/Premier League 26-27.preset/matchups.hex")
# key.set_code(f.read_text())
# f.write_text(key.enhex())
# print(key.dehex())