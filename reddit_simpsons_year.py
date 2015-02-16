import praw
import pickle
import datetime
import time

backup_file = 'simpsons_submissions.obj'

# setup scraper
scraper = praw.Reddit(user_agent='pc:simpsons_scraper:v0.1 (by /u/rm999)')

# constants
period_days = 1     # how long a period is
num_periods = 3      # how many periods to go back
to_date = date.today()

# get 1000 top results, period by period
submissions = []

for i in range(0,num_periods):
   end = to_date - timedelta(days = i * period_days)
   start = end - timedelta(days=period_days-1)
   
   print(start)
   print(end)
      
   postperiod = "timestamp:%s..%s" % (start.strftime("%s"),end.strftime("%s"))
   query = list(scraper.search(query=postperiod, subreddit='thesimpsons',sort='top',syntax='cloudsearch', limit = 1000))
   
   submissions += query
   # time.sleep(2) # for reddit api, just in case


# backup file
backup_conn = open(backup_file, 'w') 
pickle.dump(submissions, backup_conn)


# process results


sorted(set(map(lambda x: datetime.datetime.fromtimestamp(x.created).strftime('%Y-%m-%d'), submissions)))

for x in query:
   x.link_flair_text
   x.created
   x.link_flair_css_class == 'episode'
   x.score
   


