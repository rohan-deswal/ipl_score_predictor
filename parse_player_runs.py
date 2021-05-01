import pandas as pd

file_path = "files/ipl_csv2/all_matches.csv"

df = pd.read_csv(file_path, low_memory = False)

df["runs_scored"] = df["runs_off_bat"] + df["extras"]

df = df.drop(columns=["season", "non_striker", "wides", "noballs",
                   "byes", "legbyes", "penalty", "wicket_type", "player_dismissed",
                   "other_wicket_type", "other_player_dismissed", "runs_off_bat", "extras"])

df = df[df["innings"] < 3]
df = df[df["ball"] < 6.1]

#['name', r]
batsmen = []
bowlers = []

current_innings = df.loc[0, "innings"]
current_batsmen = {}
current_bowlers = {}

for index, row in df.iterrows():
	striker = row["striker"]
	bowler = row["bowler"]
	runs = row["runs_scored"]
	
	if row["innings"] == current_innings:
		if striker not in current_batsmen:
			current_batsmen[striker] = [runs, 1]
		else:
			current_batsmen[striker][0] += runs
			current_batsmen[striker][1] += 1

		if bowler not in current_bowlers:
			current_bowlers[bowler] = [runs, 1]
		else:
			current_bowlers[bowler][0] += runs
			current_bowlers[bowler][1] += 1

	else:
		current_innings = row["innings"]
		unique_batsmen = [unique_batsmen[0] for unique_batsmen in batsmen]
		unique_bowlers = [unique_bowlers[0] for unique_bowlers in bowlers]
		for batsman in current_batsmen:
			if batsman in unique_batsmen:
				i = unique_batsmen.index(batsman)
				batsmen[i].append(current_batsmen[batsman][0]/current_batsmen[batsman][1])
			else:
				batsmen.append([batsman, current_batsmen[batsman][0]/current_batsmen[batsman][1]])

		for bowler in current_bowlers:
			if bowler in unique_bowlers:
				i = unique_bowlers.index(bowler)
				bowlers[i].append(current_bowlers[bowler][0]/current_bowlers[bowler][1])
			else:
				bowlers.append([bowler, current_bowlers[bowler][0]/current_bowlers[bowler][1]]) 

		current_batsmen = {}
		current_bowlers = {}

weighted_index = lambda x: x**0.5
weighted_sum = lambda n: sum([weighted_index(x) for x in range(1, n+1)])

for i in range(len(batsmen)):
	batsmen[i][1:] = [sum([weighted_index(i+1)*score for i, score in enumerate(batsmen[i][1:])])/weighted_sum(len(batsmen[i][1:]))]

for i in range(len(bowlers)):
	bowlers[i][1:] = [sum([weighted_index(i+1)*score for i, score in enumerate(bowlers[i][1:])])/weighted_sum(len(bowlers[i][1:]))]

batsmen = pd.DataFrame(batsmen, columns = ["batsmen", "batsmen_mean_runs"])
bowlers = pd.DataFrame(bowlers, columns = ["bowlers", "bowlers_mean_runs"])

batsmen.to_csv("batsmen.csv", index = False)
bowlers.to_csv("bowlers.csv", index = False)