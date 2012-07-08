import tweetstream, pprint, string, re
from BeautifulSoup import *

regexes_file = file("regexes.txt", "r");

bs = BeautifulSoup(regexes_file)

class Matcher:
    string_regex = None
    regex = None
    tags = []
   
    def __init__(self, regex):
        self.string_regex = regex.strip()
        self.regex = re.compile(regex.strip())
        self.tags = []

    def get_str_regex(self):
        return self.string_regex

    def get_regex(self):
        return self.regex

    def set_tags(self, tags):    
        self.tags = tags

    def get_tags(self):
        return self.tags

regexes = []

for t in bs.findAll("item"):
    matcher = None
    tmp = re.search(r"<regex>(.*?)</regex>", str(t))
    if tmp:
        matcher = Matcher(tmp.group(1))

    if t.tags:
        tags = t.tags.findAll("tag")
        obj = []
        for tag in tags:
            obj.append(tag)

        matcher.set_tags(obj)

        regexes.append(matcher)

counter = 0
try:
    print "[*] - Lets see what this baby can do"
    stream = tweetstream.SampleStream("<username>", "<password>")
    for tweet in stream:
        try:
            if counter % 10000 is 0:
                regexes = []
                regexes_file = file("regexes.txt", "r");

                bs = BeautifulSoup(regexes_file)
                for t in bs.findAll("item"):
                    matcher = None
                    tmp = re.search(r"<regex>(.*?)</regex>", str(t))
                    if tmp:
                        matcher = Matcher(tmp.group(1))

                    if matcher:
                        tags = t.findAll("tag")
                        obj = []
                        for tag in tags:
                            obj.append(tag)

                        matcher.set_tags(obj)

                        regexes.append(matcher)
                counter = 0
        except Exception, e:
            print e
            counter = 0

        for regex in regexes:
            text_match = False
            if tweet.has_key("text"):
                match = re.search(regex.get_regex(), tweet["text"])
                if match and "5555555555555555" not in tweet["text"]: #Nasty hack because long strings containing 5555 created heaps of false positives. Don't think this will affect our normal analysis flow...
                    print "-" * 128
                    if tweet.has_key("user") and tweet["user"].has_key("screen_name"):
                        print tweet["user"]["screen_name"] + " - " + tweet["text"]
                    else:
                        print "@{unknown} - " + tweet["text"]

                    tags = ""
                    for t in regex.get_tags():
                        tags += " " + str(t)
                
                    print "Matching: " + regex.get_str_regex()
                    print "Tags:" + tags
                    print "-" * 128
        counter += 1
except KeyboardInterrupt:
    stream.close() 
except tweetstream.ConnectionError, e:
    print "Disconnected from twitter. Reason:", e.reason
