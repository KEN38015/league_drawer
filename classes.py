from time import sleep
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

	def __init__(self, 
				title : str,) -> None:
		self.title : str = title
		self.teams : List[Team] = []
		self.matchups = []
		self.started : bool = False
		self.sort_table()

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

	def import_matchups(self) -> list:
		pass


	def create_matchups(self, auto : bool) -> list:
		pairings = []
		remaining = self.teams[:]
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
			while (choice := input("import?\n").lower()) not in ["y", "n", "yes", "no"]:
				pass
			sleep(.3)
			if "y" in choice:
				return import_matchups()

			codes = {list(map(lambda x: x.code, self.teams))}
			
			n = len(self.teams)
			
			team_matches = (n-1)*(2)
			home_available = [team_matches] * n
			away_available = [team_matches] * n
			total = n*team_matches
			for i in range(total):
				print(f"{i}/{total} matches completed")
				sleep(.3)
				print(f"teams available for home: {" ".join([codes[ind] for ind in range(n) if home_available[ind]])}")
				while (home := input("home team? (3-digit code)\n")) not in codes:
					if home_available[codes.index(home)]:
						break
					sleep(.3)
				home_index = codes.index(home)
				home_available[codes.index(home)] -= 1
				sleep(.5)
				

				print(f"teams available for away: {" ".join([codes[ind] for ind in range(n) if away_available[ind]].remove(home))}")
				while (away := input("home team? (3-digit code)\n")) not in codes:
					if away_available[codes.index(away)]:
						break
					sleep(.3)
				away_index = codes.index(away)
				away_available[codes.index(away)] -= 1

				pairings.append([self.teams[home_index], self.teams[away_index]])

			return





	def start_season(self) -> None:
		self.started = True
		while (choice := input("Manual or Automatic (does not account stadium) match creation?\n").lower()) not in {"manual", "automatic", "auto"}:
			pass
		sleep(.3)
		matchups = self.create_matchups("auto" in choice)
		print(*matchups, sep="\n")

	def sort_table(self) -> None:
		if not self.started:
			self.teams.sort(key=lambda t: (-t.points, -t.goal_difference, -t.away_goals))
		self.teams.sort(key=lambda t: t.abbr)


	

	
	# home then away
	def add_result(self, data1 : Tuple[Team, int], data2 : Tuple[Team, int]):
		team1, res1 = data1
		team2, res2 = data2

		team1.add_scoreline(res1, res2, home=True)
		team2.add_scoreline(res2, res1, home=False)
			# /unfinished	!!!/



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
		self.name : str = name
		self.abbr : str = abbreviation.capitalize()
		self.code : str = code
		self.points : int = 0
		self.wins : int = 0 ; self.draws : int = 0 ; self.losses : int = 0
		self.matches_played : int = 0
		self.home_goals : int = 0 ; self.away_goals : int = 0
		self.goals_scored : int = 0 ; self.goals_conceded : int = 0 ; self.goal_difference : int = 0

	# resets dependencies
	def recalibrate(self) -> None:
		self.points = 3 * self.wins + self.draws
		self.matches_played = self.wins + self.draws + self.losses
		self.goals_scored = self.home_goals + self.away_goals
		self.goal_difference = self.goals_scored - self.goals_conceded


	def add_scoreline(self, scored : int, conceded : int, *, home : bool) -> None:
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

	def __eq__(self, other) -> bool:
		return self.name == other.name


	def __str__(self) -> str:
		return self.name



