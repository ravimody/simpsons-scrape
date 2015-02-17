import praw
import datetime
import time
import re
from pandas import DataFrame

backup_file = 'simpsons_submissions.txt'

# setup scraper
scraper = praw.Reddit(user_agent='pc:simpsons_scraper:v0.1 (by /u/rm999)')

# constants
period_days = 7     # how long a period is
num_periods = 52 * 6      # how many periods to go back
to_date = datetime.date.today()

# get 1000 top results, period by period
submissions = []
for i in range(0,num_periods):
   end = to_date - datetime.timedelta(days = i * period_days - 1) 
   start = end - datetime.timedelta(days=period_days) 
   postperiod = "timestamp:%s..%s" % (start.strftime("%s"),end.strftime("%s"))
   query = list(scraper.search(query=postperiod, subreddit='thesimpsons',sort='top',syntax='cloudsearch', limit = 1000))
   submissions += query
   time.sleep(2) # for reddit api, just in case

# backup submission ids
# http://stackoverflow.com/questions/24748803/praw-serializing-comment-and-submission-objects-as-json
thefile = open(backup_file, 'w')
for item in map(lambda x: x.id, submissions):
  thefile.write("%s\n" % item)


# process results
submissions_cleaned = filter(lambda x: process_season_num(x.link_flair_text) is not None,   # episodes only
   filter(lambda x: x.score > 10, submissions)  # highish scoring
)

submissions_time_season = map(lambda x: [x.created, process_season_num(x.link_flair_text)], submissions_cleaned)
submissions_df = DataFrame(submissions_time_season, columns=['dt','season'])
submissions_df.date = submissions_df.dt
 

for x in query:
   x.link_flair_text
   x.created
   x.link_flair_css_class == 'episode'
   x.score


from pylab import *
import numpy



# helper functions:

def process_season_num(x):
   if x is None:
      return(None)
   matchObj = re.match(r's([0-9]+)e([0-9]+)', x, re.M)
   if matchObj:
      return([int(matchObj.group(1))]) #  , int(matchObj.group(2))])
   


# sorted(set(map(lambda x: datetime.datetime.fromtimestamp(x.created).strftime('%Y-%m-%d'), submissions)))