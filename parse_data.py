import pandas as pd

file_path = "files/ipl_csv2/all_matches.csv"

data = pd.read_csv(file_path, low_memory = False)

data["runs_scored"] = data["runs_off_bat"] + data["extras"]

data["runs"] = data["runs_scored"]

data = data.drop(columns=["season", "non_striker", "wides", "noballs",
                   "byes", "legbyes", "penalty", "wicket_type", "player_dismissed",
                   "other_wicket_type", "other_player_dismissed", "runs_off_bat", "extras"])

data = data[data["innings"] < 3]

data["chase"] = 0

current_innings = data.loc[0, "innings"]
for i in range(1, len(data)):
    try:
        if data.loc[i, "innings"] == current_innings:
            data.loc[i, "runs"] += data.loc[i-1, "runs"]
            data.loc[i, "chase"] = data.loc[i-1, "chase"] - data.loc[i, "runs_scored"]
        else:
            current_innings = data.loc[i, "innings"]
            if current_innings == 2:
                data.loc[i, "chase"] = data.loc[i-1, 'runs']
            else:
                print(f"New Match {data.loc[i, 'match_id']}")
    except:
        print("Error occured")
data.loc[data["innings"]==1, "chase"] = 0

data = data[data["ball"]<6.1]

data.to_csv("all_matches_relevant.csv", index = False)

print(data)

