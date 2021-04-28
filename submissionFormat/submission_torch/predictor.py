from time import time
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import pandas as pd
### Custom definitions and classes if any ###

def hidden_init(layer):
    fan_in = layer.weight.data.size()[0]
    lim = 1. / np.sqrt(fan_in)
    return (-lim, lim)  

class Actor(nn.Module):
    """Actor (Policy) Model."""

    def __init__(self, state_size, action_size, seed, h):
        """Initialize parameters and build model.
        Params
        ======
            state_size (int): Dimension of each state
            action_size (int): Dimension of each action
            seed (int): Random seed
            fc1_units (int): Number of nodes in first hidden layer
            fc2_units (int): Number of nodes in second hidden layer
        """
        super(Actor, self).__init__()
        self.seed = torch.manual_seed(seed)
        self.fc1 = nn.Linear(state_size, h)
        self.fc2 = nn.Linear(h, h)
        self.fc3 = nn.Linear(h, action_size)
        self.reset_parameters()

    def reset_parameters(self):
        self.fc1.weight.data.uniform_(*hidden_init(self.fc1))
        self.fc2.weight.data.uniform_(*hidden_init(self.fc2))
        self.fc3.weight.data.uniform_(-3e-3, 3e-3)

    def forward(self, state):
        """Build an actor (policy) network that maps states -> actions."""
        x = F.relu(self.fc1(state))
        x = F.relu(self.fc2(x))

        return self.fc3(x)

venue_lookup = pd.read_csv("venue.csv")
batsmen_lookup = pd.read_csv("batsmen.csv")
bowlers_lookup = pd.read_csv("bowlers.csv")

venue_lookup = venue_lookup.set_index("venue")["venue_mean_runs"].to_dict()
batsmen_lookup = batsmen_lookup.set_index("batsmen")["batsmen_mean_runs"].to_dict()
bowlers_lookup = bowlers_lookup.set_index("bowlers")["bowlers_mean_runs"].to_dict()

batsman_mean = sum(batsmen_lookup.values())/len(batsmen_lookup)
bowler_mean = sum(bowlers_lookup.values())/len(bowlers_lookup)

venue_mean = sum(venue_lookup.values())/len(venue_lookup)

dnn_model=Actor(6,1,time(),64)
dnn_model.load_state_dict(torch.load("pytorch_model.pt"))

weights = [np.array([ 1.497406 , 45.812748 ,  3.3521402,  3.5544746,  1.0940305,
         1.2861433], dtype=np.float32),
 np.array([0.24999326, 7.7099004 , 1.1658807 , 0.4999508 , 0.01168746,
        0.01274876], dtype=np.float32)]

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
    df = df.to_numpy()
    df = (df - weights[0])/(np.sqrt(weights[1]) + 0.001)
    df = torch.from_numpy(df.astype(np.float32))

    prediction = dnn_model(df)
    
    return int(prediction)