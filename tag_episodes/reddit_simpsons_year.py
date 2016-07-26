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
submissions_df['date'] = map(lambda x: datetime.datetime.fromtimestamp(x).strftime('%Y-%m-%d'), submissions_df.dt)
 


from pylab import *
import matplotlib.pyplot as plt
plt.figure()
histo,xedges,yedges = numpy.histogram2d((submissions_df.dt - 1414540313) / (1424146056 - 1414540313),
   submissions_df.season / 26,
   bins=[30, 26],
   range=[[0, 1],[0,1]]
)
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1] ]
plt.imshow(histo.T,extent=extent,interpolation='nearest')
colorbar()
show()



# helper functions:

def process_season_num(x):
   if x is None:
      return(None)
   matchObj = re.match(r's([0-9]+)e([0-9]+)', x, re.M)
   if matchObj:
      return(int(matchObj.group(1))) #  , int(matchObj.group(2))])
   


# sorted(set(map(lambda x: datetime.datetime.fromtimestamp(x.created).strftime('%Y-%m-%d'), submissions)))