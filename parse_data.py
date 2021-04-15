import pandas as pd

file_path = "files/ipl_csv2/all_matches.csv"

data = pd.read_csv(file_path, low_memory = False)

data["runs_scored"] = data["runs_off_bat"] + data["extras"]

# venue, innings, ball, batting_team, bowling_team, batsmen, bowlers
data = data.drop(columns=["season", "non_striker", "wides", "noballs",
                   "byes", "legbyes", "penalty", "wicket_type", "player_dismissed",
                   "other_wicket_type", "other_player_dismissed", "runs_off_bat", "extras"])

data = data[data["innings"] < 3]
data = data[data["ball"]<6.1]

#new_data = pd.Dataframe(columns = ["venue", "innings", "ball", "batting_team",
#                                   "bowling_team", "batsmen", "bowlers", "runs"]) 

new_data = []

batsmen = set() 
bowlers = set()

current_innings = data.loc[0, 'innings']
current_runs = 0
last_row = None

for index, row in data.iterrows():
    if row["innings"] == current_innings:
        batsmen.add(row["striker"])
        bowlers.add(row["bowler"])
        current_runs += row["runs_scored"]
        last_row = row
    else:
        if last_row["ball"] >= 5.6:
            new_data.append([last_row["venue"], last_row["innings"], last_row["ball"], last_row["batting_team"], last_row["bowling_team"],
                            ','.join(batsmen), ','.join(bowlers), current_runs])
        current_innings = row["innings"]
        current_runs = row["runs_scored"]
        batsmen = set([row["striker"]])
        bowlers = set([row["bowler"]])
        if row["innings"] == 1:
            print("Match: ", last_row["match_id"])

new_data.append([last_row["venue"], last_row["innings"], last_row["ball"], last_row["batting_team"], last_row["bowling_team"],
                        ','.join(batsmen), ','.join(bowlers), current_runs])

columns = ["venue", "innings", "ball", "batting_team", "bowling_team", "batsmen", "bowlers", "runs"]
new_data = pd.DataFrame(new_data, columns=columns)

new_data.to_csv("all_matches_relevant.csv", sep='\t')

print(new_data)

