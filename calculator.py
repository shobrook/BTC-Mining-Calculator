"""
Simple command-line tool for predicting the amount of Bitcoin your device
can mine in the next 24hrs.

This was the first Python script I ever wrote (back when I was 15). I've
updated it to support Python 3.
"""


import sys
import requests

# ASCII color codes
YELLOW = '\033[33m'
RED = '\033[31m'
END = '\033[0m'


def estimate(device_hash_rate, coin="BTC"):
	block_reward = int(requests.get(url="https://blockchain.info/q/bcperblock").json())
	difficulty = int(requests.get(url="https://blockchain.info/q/getdifficulty").json())
	exchange_rate = int(requests.get(url="https://blockchain.info/q/24hrprice").json())

	return str(86400 * block_reward * (device_hash_rate / (4294.67 * difficulty)))


def main():
	while True:
		sys.stdout.write(''.join(["What is your device's hash rate (in MH/s)? ", YELLOW]))

		try:
			device_hash_rate = int(input())
			sys.stdout.write(''.join([END, "\nExpected return in the next 24hrs: ", YELLOW, estimate(device_hash_rate), " BTC", END, '\n']))

			return
		except ValueError:
			sys.stdout.write(''.join([END, RED, "Please input an integer.\n\n", END]))


if __name__ == "__main__":
	main()
