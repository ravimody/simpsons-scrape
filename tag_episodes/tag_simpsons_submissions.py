import elasticsearch
import pandas as pd

es = elasticsearch.Elasticsearch()  

with open('simpsons_submissions.txt') as f:
    submission_ids = f.read().splitlines()
    
    
episode_df = pd.DataFrame(columns= [
    'submission_id', 'submission_created', 'submission_url', 'submission_permalink', 'submission_is_self',
    'submission_ups', 'submission_downs',
    'comments_ep', 'comments_score', 'num_comments',
    'title_ep', 'title_score',
    'flair_text'
    ]
)

for submission_id in submission_ids:
    submission = scraper.get_submission(submission_id=submission_id)

    # get sum of scores of all comments by episode
    scores = {}
    for comment in submission.comments:
        search_result = get_episode(comment.body)
        if search_result['score']:
            if search_result['episode'] in scores:
                scores[search_result['episode']] += search_result['score']
            else:
                scores[search_result['episode']] = search_result['score']

    num_comments = len(submission.comments)
    if scores:
        comments_ep = max(scores, key=scores.get)
        comments_score = scores[comments_ep]
    else:
        comments_ep = None
        comments_score = None

    # get episode from title
    title = get_episode(submission.title)
    title_ep = title['episode']
    title_score = title['score']

    # get flair text
    flair_text = submission.link_flair_text

    episode_df.loc[len(episode_df)]=[
        submission_id, submission.created, submission.url, submission.permalink, submission.is_self,
        submission.ups, submission.downs,
        comments_ep, comments_score, num_comments,
        title_ep, title_score,
        flair_text
    ]
    print len(episode_df.index)


# function to get episode from searching transcripts
def get_episode(text):
    try: 
        ep = es.search(index = 'simpsons', body={
        'query': {'match': {'text': text}}}
        )['hits']['hits'][0]
        return {'episode': ep['_source']['episode'], 'score': ep['_score']}
    except:
        return {'episode': None, 'score': None}



