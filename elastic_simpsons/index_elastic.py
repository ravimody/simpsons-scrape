import json
import elasticsearch

index_name = 'simpsons'


es = elasticsearch.Elasticsearch()  

# load scripts
with open('simpsons_scripts.json') as json_file:    
    scripts = json.load(json_file)

# create index 
if es.indices.exists(index_name):
    es.indices.delete(index = index_name)
    
es.indices.create(index = index_name, body = {"settings" : {"number_of_shards": 1, "number_of_replicas": 0}})   

# load index
for script in scripts:
    ep_number_string = script['ep_url'].split("episode=")[1]
    season_num = ep_number_string.split('s')[1].split('e')[0]
    episode_num = ep_number_string.split('s')[1].split('e')[1]
    episode_id = int(season_num + episode_num)
    episode_text = (" ".join(script['ep_text'])).replace('/n', '\n')
    doc = {
        'text': episode_text,
        'episode': ep_number_string,
        'season_num': season_num,
        'episode_num': episode_num
    }
    res = es.index(index=index_name, doc_type='script', id=episode_id, body=doc)
    print res['created']
    
# example search:
# es.search(index = index_name, body={
#    'query': {
#         'match': {
#             'text': "Don't worry, Homer, those crows weren't trying to kill you, they just wanted your sweet, sweet eye juices"
#         }
#     }}
# )['hits']['hits'][0]