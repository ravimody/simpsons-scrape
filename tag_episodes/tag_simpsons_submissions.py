import elasticsearch
import pandas as pd

es = elasticsearch.Elasticsearch()  

with open('simpsons_submissions.txt') as f:
    submission_ids = f.read().splitlines()
    
submission_id = submission_ids[1]
submission = scraper.get_submission(submission_id=submission_id)

# get sum of scores of all comments by episode
scores = {}
for comment in submission.comments:
    search_result = get_episode(comment.body)
    print search_result
    if search_result['score']:
        if search_result['episode'] in scores:
            scores[search_result['episode']] += search_result['score']
        else:
            scores[search_result['episode']] = search_result['score']

# get episode from title
get_episode(submission.title)        

# get flair text
submission.link_flair_text

# function to get episode from searching transcripts
def get_episode(text):
    try: 
        ep = es.search(index = 'simpsons', body={
        'query': {'match': {'text': text}}}
        )['hits']['hits'][0]
        return {'episode': ep['_source']['episode'], 'score': ep['_score']}
    except:
        return {'episode': None, 'score': None}



