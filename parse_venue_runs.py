import pandas as pd

filepath = "files_relevant/all_matches.tsv"

df = pd.read_csv(filepath, sep = '\t')

venue = []

for v in df.venue.unique():
	venue.append([v, df.loc[df["venue"]==v, "runs"].mean()])

venue = pd.DataFrame(venue, columns = ["venue", "venue_mean_runs"])
venue.to_csv("venue.csv", index = False)