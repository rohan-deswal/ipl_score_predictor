import pandas as pd

file_path = "files_relevant/all_matches.tsv"

df = pd.read_csv(file_path, sep = '\t')
venue_lookup = pd.read_csv("venue.csv")
batsmen_lookup = pd.read_csv("batsmen.csv")
bowlers_lookup = pd.read_csv("bowlers.csv")

venue_lookup = venue_lookup.set_index("venue")["venue_mean_runs"].to_dict()
batsmen_lookup = batsmen_lookup.set_index("batsmen")["batsmen_mean_runs"].to_dict()
bowlers_lookup = bowlers_lookup.set_index("bowlers")["bowlers_mean_runs"].to_dict()

df["venue_mean"] = 0
df["count_batsmen"] = 0
df["count_bowlers"] = 0
df["batsmen_mean"] = 0
df["bowlers_mean"] = 0

batsman_mean = sum(batsmen_lookup.values())/len(batsmen_lookup)
bowler_mean = sum(bowlers_lookup.values())/len(bowlers_lookup)

for index, row in df.iterrows():
    batsmen = row["batsmen"].strip().split(',')
    bowlers = row["bowlers"].strip().split(',')
    venue = row["venue"]

    df.loc[index, "venue_mean"] = venue_lookup[venue]
    df.loc[index, "count_batsmen"] = len(batsmen)
    df.loc[index, "count_bowlers"] = len(bowlers)
    df.loc[index, "batsmen_mean"] = sum([batsmen_lookup.get(name, batsman_mean) for name in batsmen])/len(batsmen)
    df.loc[index, "bowlers_mean"] = sum([bowlers_lookup.get(name, bowler_mean) for name in bowlers])/len(bowlers)

df = df.drop(columns = ["venue", "batsmen", "bowlers", "batting_team", "bowling_team", "Unnamed: 0"])

df.to_csv("all_matches_numeric.csv", index = False)