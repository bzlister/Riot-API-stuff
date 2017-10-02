import requests
import random
import time

#Get champion name from id
def request(id):
	response = requests.get("https://na1.api.riotgames.com/lol/static-data/v3/champions/"+id+"?api_key=<key>")
	return response.json()['name']

#Get the mean days of the week which the top 10 most popular and least popular champions are played
def matchlist(accountID):
	seed = accountID
	most_popular = {18, 67, 412, 498, 40, 64, 117, 51, 16}
	least_popular = {106, 111, 30, 48, 223, 266, 23, 78, 68, 516}
	mostGames = []
	leastGames = []
	backup = [accountID]
	for i in range(0, 1000):
		print(i)
		seed = backup[random.randint(0,len(backup)-1)]
		match = requests.get("https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/"+str(seed)+"/recent/?api_key=<key>").json()
		while (len(match) < 2):
			seed = backup[random.randint(0,len(backup)-1)]
			time.sleep(1)
			match = requests.get("https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/"+str(seed)+"/recent/?api_key=<key>").json()
		match = match['matches'][random.randint(0, len(match['matches'])-1)]	
		
		time.sleep(1)
		n = requests.get("https://na1.api.riotgames.com/lol/match/v3/matches/"+str(match['gameId'])+"?api_key=<key>").json()
		while ((len(n) < 2) or (('player' in n['participantIdentities'][0]) == False)):
			seed = backup[random.randint(0,len(backup)-1)]
			time.sleep(1)
			match = requests.get("https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/"+str(seed)+"/recent/?api_key=<key>").json()
			while (len(match) < 2):
				seed = backup[random.randint(0,len(backup)-1)]
				time.sleep(1)
				match = requests.get("https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/"+str(seed)+"/recent/?api_key=<key>").json()
			match = match['matches'][random.randint(0, len(match['matches'])-1)]	
			
			seed = backup[random.randint(0,len(backup)-1)]
			n = requests.get("https://na1.api.riotgames.com/lol/match/v3/matches/"+str(match['gameId'])+"?api_key=<key>").json()
		
		del backup[:]
		for j in range(0, len(n['participants'])):
			if (n['participants'][j]['championId'] in most_popular):
				mostGames.append(time.localtime(match['timestamp']/1000).tm_wday)
			if (n['participants'][j]['championId'] in least_popular):
				leastGames.append(time.localtime(match['timestamp']/1000).tm_wday)		
			if (n['participantIdentities'][j]['player']['accountId'] != seed):
				backup.append(n['participantIdentities'][j]['player']['accountId'])
			
		time.sleep(1)
	sum1 = 0;
	sum2 = 0;
	for k in range(0, len(mostGames)):
		sum1+=mostGames[k];
	for p in range(0, len(leastGames)):
		sum2+=leastGames[p];
	data = {'Popular mean': sum1/len(mostGames), 'Unpopular mean': sum2/len(leastGames), 'Num popular games': len(mostGames), 'Num unpopular games': len(leastGames)}
	return data