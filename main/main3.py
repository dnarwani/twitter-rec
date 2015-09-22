import twitter
import time
from recsys.algorithm.dbconn import DBConn
import pymongo

db = DBConn()

# api = twitter.Api(consumer_key='YUlt3YfFNYpdQ1FjLcQhBOOIC',
#                   consumer_secret='eVQhzjNfWhgkw01gvQi2PRzrc5CF4fX4JkYfqr7Gbbh1xFSIXI',
#                   access_token_key='3398680881-xxyD85BZ0W0AAe4u0vhRH84Z4m9uSPwimblrEcJ',
#                   access_token_secret='R4NBLV6i4HRKWbRIU78ivsLRc0TfRWShd9EmFpAWe0K8A')

people = db.get_people_sorted_artists()

for person in people:
    print person["artist_distinct_count"]




