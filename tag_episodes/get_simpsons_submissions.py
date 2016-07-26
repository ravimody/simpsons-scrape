import praw
import datetime
import time
import re

# setup scraper
scraper = praw.Reddit(user_agent='pc:simpsons_scraper:v0.1 (by /u/rm999)')

# constants
period_days = 7     # how long a period is
num_periods = 52 * 6      # how many periods to go back
to_date = datetime.date.today()

# get 1000 top results, period by period
submissions = []
for i in range(num_periods + 1,num_periods + 36):
   print i
   end = to_date - datetime.timedelta(days = i * period_days - 1) 
   start = end - datetime.timedelta(days=period_days) 
   postperiod = "timestamp:%s..%s" % (start.strftime("%s"),end.strftime("%s"))
   query = list(scraper.search(query=postperiod, subreddit='thesimpsons',sort='top',syntax='cloudsearch', limit = 1000))
   submissions += query
   time.sleep(1) # for reddit api, just in case

# backup submission ids
thefile = open('simpsons_submissions.txt', 'w')
for item in map(lambda x: x.id, submissions):
  thefile.write("%s\n" % item)

