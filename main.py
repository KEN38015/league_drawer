
from classes import *
import random










def main() -> None:
	premier_league = Table("Premier League")
	clubs = {
    "Arsenal" : 				Team("Arsenal", "Arsenal", "ARS"),
    "Aston Villa" :				Team("Aston Villa", "Aston Villa", "AVL"),
    "Bournemouth": 				Team("Bournemouth", "Bournemouth", "BOU"),
    "Brentford" : 				Team("Brentford", "Brentford", "BRE"),
    "Brighton & Hove Albion" : 	Team("Brighton & Hove Albion", "Brighton", "BHA"),
    "Chelsea" : 				Team("Chelsea", "Chelsea", "CHE"),
    "Crystal Palace" : 			Team("Crystal Palace", "Crystal Palace", "CRY"),
    "Everton" : 				Team("Everton", "Everton", "EVE"),
    "Fulham" : 					Team("Fulham", "Fulham", "FUL"),
    "Leeds United" : 			Team("Leeds United", "Leeds", "LEE"),
    "Liverpool" : 				Team("Liverpool", "Liverpool", "LIV"),
    "Manchester City" : 		Team("Manchester City", "Man City", "MCI"),
    "Manchester United" : 		Team("Manchester United", "Man Utd", "MUN"),
    "Newcastle United" : 		Team("Newcastle United", "Newcastle", "NEW"),
    "Nottingham Forest" : 		Team("Nottingham Forest", "Nott'm Forest", "NFO"),
    "Sunderland" : 				Team("Sunderland", "Sunderland", "SUN"),
    "Tottenham Hotspur" : 		Team("Tottenham Hotspur", "Spurs", "TOT"),
    "Coventry City" : 			Team("Coventry City", "Coventry", "COV"),
    "Ipswich Town" : 			Team("Ipswich Town", "Ipswich", "IPS"),
    "Hull City" : 				Team("Hull City", "Hull", "HUL"),
}
	for team, data in clubs.items():
		premier_league.add_team(data)
	print(premier_league)
	premier_league.start_season()




















if __name__ == "__main__":
	main()
