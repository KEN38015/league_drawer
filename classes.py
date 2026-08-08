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
		self.teams : List[Team] = [Team("LIV"), Team("NOTTM FOREST")]
		self.started : bool = False
		self.both_ways = input("Play home and away?\n")
		while self.both_ways.lower() not in ("y", "n", "yes", "no"):
			self.both_ways = input("Play home and away?\n")


	def add_team(self, team : Team) -> None:
		self.teams.append(team)


	def remove_team(self, team : Team) -> bool:
		if self.started:
			return True
		self.teams.remove(team)
		return False

	def sort_table(self) -> None:
		if not self.started:
			self.teams.sort(key=lambda t: (-t.points, -t.goal_difference, -t.away_goals))
		self.teams.sort(key=Team.name)
	
	def add_result(self, data1 : Tuple[Team, int], data2 : Tuple[Team, int]):
		team1, res1 = data1
		team2, res2 = data2
			# /unfinished	!!!/



	def __str__(self) -> str:

		total_width : int = sum(
						[
						5, # rank column
						len(max(self.teams, key=lambda x: x.name).name) + 2, # longest name + 2 trailings
						sum(
							
							list(map(lambda x: self.existing_stats[x][-1] * 2 + len(self.existing_stats[x][0]), self.stats_showing))
							
						),
						len(self.stats_showing) # number of posts

						]
							)
		center = total_width // 2
		lines : list = []

		# title
		lines.append(" " * (center - len(self.title)//2) + self.title.upper())
		
		lines.append("_" * total_width)


		identifiers : list = ["| R |"]
		longest_name = len(max(self.teams, key=lambda x: x.name).name) + 2
		identifiers.append(" " * (longest_name // 2 - 2) + "Name" + " " * (longest_name // 2 - 2) + "|")
		for stat in self.stats_showing:
			key, trailings = self.existing_stats[stat]
			identifiers.append(" " * trailings + key + " " * trailings + "|")
			
		lines.append("".join(identifiers))
		lines.append(" " + "=" * (total_width-2) + " ")


		return "\n".join(lines)


'''                                                      												  
			 		PREMIER LEAGUE
 _____________________________________________________
| R |     Name     |  MP  |  W  |  D  |  L  |   Pts   |

| R |     Name     |  MP  |  W  |  D  |  L  |   Pts   |
 =====================================================
| 1 | LIVERPOOL    |  38  | 25  |  9  |  4  |   84    |
| 2 | ARSENAL      |  38  | 20  |  14 |  4  |   74    |
| 3 | MAN CITY     |  38  | 21  |  8  |  9  |   71    |
| 4 | CHELSEA      |  38  | 20  |  9  |  9  |   69    |
| 5 | NEWCASTLE    |  38  | 20  |  6  |  12 |   66    |
| 6 | ASTON VILLA  |  38  | 19  |  9  |  10 |   66    |
| 7 | NOTTM FOREST |  38  | 19  |  8  |  11 |   65    |
======================================================




'''







class Team:
	
	def __init__(self,
				name : str,
				):
		self.name : str = name
		self.points : int = 0
		self.wins : int = 0 ; self.draws : int = 0 ; self.losses : int = 0
		self.matches_played : int = 0
		self.home_goals : int = 0 ; self.away_goals : int = 0
		self.goals_scored : int = 0 ; self.goals_conceded : int = 0 ; self.goal_difference : int = 0


	def calculate() -> None:
		pass


	def get_info() -> List:

		return [

		]






i = Table("PL")
print(i)
