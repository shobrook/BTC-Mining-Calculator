from joblib import Parallel, delayed
from pymongo import MongoClient
import urllib2
import simplejson
import multiprocessing
import time
import math

############################GLOBALS############################
apikey = '526efde4952e4d71a68f3a989cb17dae'
hashrates = {'DGB' : 100, 'GLD' : 100, 'CNC' : 100, 'NVC' : 100, 'GAME' : 100, 'PPC' : 100, 'BTC' : 100, 'ZET' : 100, 'MZC' : 100, 'TEK' : 100}

inputs = ['DGB', 'GLD', 'CNC', 'NVC', 'GAME', 'PPC', 'BTC', 'ZET', 'MZC', 'TEK']
inputs_scrypt = ['DGB', 'GLD', 'CNC', 'NVC', 'GAME']
inputs_sha = ['PPC', 'BTC', 'ZET', 'MZC', 'TEK']

expcoin_historical = []
metrics = dict.fromkeys(inputs, 0)
volatilities = dict.fromkeys(inputs_scrypt, 0)

###########################FUNCTIONS###########################
def estimate(i):
	devhash = hashrates[i]
	print 'Calculating expected daily profit (in USD) for... ' + i
	rlambda = (simplejson.load(urllib2.urlopen('http://www.coinwarz.com/v1/api/coininformation/?apikey=' + apikey + '&cointag=' + i))).get('Data').get('BlockReward')
	# diff = [tlambda * nethash] / 4294.97 --> Scaled to 1 MH/sec
	diff = (simplejson.load(urllib2.urlopen('http://www.coinwarz.com/v1/api/coininformation/?apikey=' + apikey + '&cointag=' + i))).get('Data').get('Difficulty')
	exrate = float((simplejson.load(urllib2.urlopen('http://www.cryptonator.com/api/ticker/' + i + '-usd'))).get('ticker').get('price'))
	# takes [4294.97 * diff] hashes to solve a block
	expcoin = round((86400*(devhash/(4294.97*diff))*(exrate*rlambda)), 2)
	return expcoin

def average(x):
	return sum(x) / len(x)

def delta(tuples):
	# percent change over a period, u_t = ln(P_t / P_t-1) for time t
	return [(v / tuples[abs(i - 1)]) - 1 for i, v in enumerate(tuples)]

def variance(tuples):
	perc = delta(tuples)
	avg = average(perc)
	return [(x - avg)**2 for x in perc]

def calcUncert(scrypt):
	client = MongoClient("ec2-54-191-245-35.us-west-2.compute.amazonaws.com")
	db = client.miner_io
	for document in db[scrypt].find().skip(db[scrypt].count() - 48):
		expcoin_historical.append(document.get('daily_profit'))
	expcoin_historical.reverse()
	print('Calculating expected profit volatility for... ' + scrypt)
	var = variance(expcoin_historical)
	volatility = math.sqrt(average(var))
	uncertainty = round((expcoin_historical[0] * volatility), 2)
	return uncertainty

##############################MAIN#############################
<<<<<<< HEAD
=======
print ''

>>>>>>> master
timestamp = int(time.time())
outputs = Parallel(n_jobs=multiprocessing.cpu_count())(delayed(estimate)(i) for i in inputs)

outputs = Parallel(n_jobs=multiprocessing.cpu_count())(delayed(estimate)(i) for i in inputs)
for x in range(len(inputs)):
	metrics[inputs[x]] = float(outputs[x])
ranked_profit = (sorted(metrics.items(), key=lambda x: x[1]))
ranked_profit.reverse()

<<<<<<< HEAD
=======
expcoin_historical = []

print ''

>>>>>>> master
outputs_adj = Parallel(n_jobs=multiprocessing.cpu_count())(delayed(calcUncert)(scrypt) for scrypt in inputs_scrypt)
for x in range(len(inputs_scrypt)):
	volatilities[inputs_scrypt[x]] = float(outputs_adj[x])
ranked_uncert = (sorted(volatilities.items(), key=lambda x: x[1]))
ranked_uncert.reverse()

print "\n***SHA-256 CURRENCIES***"
for x in range(len(ranked_profit)):
	if str(ranked_profit[x][0]) in inputs_sha:
		print "Profitability of " + str(ranked_profit[x][0]) + " is $" + str(ranked_profit[x][1])

print "\n***SCRYPT CURRENCIES***"
for x in range(len(ranked_profit)):
	if str(ranked_profit[x][0]) in inputs_scrypt:
		print "Profitability of " + str(ranked_profit[x][0]) + " is $" + str(ranked_profit[x][1]) + " +/- " + str(ranked_uncert[x][1]) # attributed tolerance to each expcoin output (scrypt)
