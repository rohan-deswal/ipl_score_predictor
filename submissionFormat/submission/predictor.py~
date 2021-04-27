from time import time

start = time()

from tensorflow.keras.models import load_model

print(time() - start)

import pandas as pd

### Custom definitions and classes if any ###

venue_lookup = pd.read_csv("venue.csv")
batsmen_lookup = pd.read_csv("batsmen.csv")
bowlers_lookup = pd.read_csv("bowlers.csv")

venue_lookup = venue_lookup.set_index("venue")["venue_mean_runs"].to_dict()
batsmen_lookup = batsmen_lookup.set_index("batsmen")["batsmen_mean_runs"].to_dict()
bowlers_lookup = bowlers_lookup.set_index("bowlers")["bowlers_mean_runs"].to_dict()

batsman_mean = sum(batsmen_lookup.values())/len(batsmen_lookup)
bowler_mean = sum(bowlers_lookup.values())/len(bowlers_lookup)

venue_mean = sum(venue_lookup.values())/len(venue_lookup)

dnn_model = load_model('dnn_model')

def string_match(a, b):
	if len(a)>len(b):
		a, b = b, a

	try:
		a = a.split(' ')[0][0] + ' ' + ' '.join(a.split(' ')[1:]) 
	except IndexError:
		a = a

	i, j = 0, 0

	while i<len(a):
		if a[i] == b[j]:
			i+=1
			j+=1
		else:
			j+=1
		if j>=len(b) and i!=len(a):
			return False
	return True

def batsman_data_get(name):
	global batsmen_lookup
	global batsman_mean

	keys = batsmen_lookup.keys()

	for key in keys:
		if string_match(key, name):
			name = key
			break

	return batsmen_lookup.get(name, batsman_mean)

def bowler_data_get(name):
	global bowlers_lookup
	global bowler_mean

	keys = bowlers_lookup.keys()

	for key in keys:
		if string_match(key, name):
			name = key
			break

	return bowlers_lookup.get(name, bowler_mean)

def venue_data_get(venue):
	global venue_lookup
	global venue_mean

	keys = venue_lookup.keys()

	for key in keys:
		if string_match(key, venue):
			venue = key
			break

	return venue_lookup.get(venue, venue_mean) 

def predictRuns(testInput):
    prediction = 46.5
        
    df = pd.read_csv(testInput)
    
    df["venue_mean"] = 0
    df["count_batsmen"] = 0
    df["count_bowlers"] = 0
    df["batsmen_mean"] = 0
    df["bowlers_mean"] = 0
    
    batsmen = df["batsmen"][0].strip().split(',')
    bowlers = df["bowlers"][0].strip().split(',')
    venue = df["venue"][0]
    
    df["venue_mean"] = venue_data_get(venue)
    df["count_batsmen"] = len(batsmen)
    df["count_bowlers"] = len(bowlers)
    df["batsmen_mean"] = sum([batsman_data_get(name) for name in batsmen])/len(batsmen)
    df["bowlers_mean"] = sum([bowler_data_get(name) for name in bowlers])/len(bowlers)
    
    df = df.drop(columns = ["venue", "batsmen", "bowlers", "batting_team", "bowling_team"])
    
    prediction = dnn_model.predict(df)
    
    return int(prediction[0, 0])

print(predictRuns('21_inn1.csv'))