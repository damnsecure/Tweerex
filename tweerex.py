#!/usr/bin/python

from sys import stdout
import tweetstream, pprint, string, re

print ">> Name: Tweerex"
print ">> Dev: Ruben Thijssen (@rubenthijssen)"
print ">> Ver: 0.2"

# Load all the regexes
# Format: <regex> # <desc>
regexes = []
for line in open('regexes.txt'):
	regex = line.split("#")
	regexes.append(regex)

print "[*] - Regexes successfully loaded"

# Loading login credentials
try:
	login_file = open("login", "r").readlines()
	username = login_file[0].strip() #First line in 'login' has username
	password = login_file[1].strip() #Second line in 'login' has password
	print "[*] - Login credentials found"
except:
	print "[!] - Could not read login file make sure it exists and has the right format..."
	quit()

# Logging into the twitter API
try:
	print "[*] - Logging in " + username + ":****" 
	stream = tweetstream.SampleStream(username, password)
except:
	print "[!] - Could not login..."
	quit()

# Read twitter public stream and look for matches
print "[*] - Lets see what this baby can do"
try:
	for tweet in stream:
		for regex in regexes:
			if tweet.has_key("text"):
				match = re.search(regex[0].strip(), tweet["text"])

				if match:
					if tweet.has_key("user") and tweet["user"].has_key("screen_name"):
						print tweet["user"]["screen_name"] + " - " + tweet["text"] + "\t\t<< " + regex[1].strip()
					else:
						print "@{unknown} - " + tweet["text"] + "\t\t<< " + regex[1].strip()

except KeyboardInterrupt:
	print "[*] Shutting down..."
	stream.close()
except tweetstream.ConnectionError, e:
	print "Disconnected from twitter. Reason:", e.reason
except Exception, e:
	print "[!] - Unknown excpetion occured, shutting down.", e
