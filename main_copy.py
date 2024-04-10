import requests
import pandas as pd
from datetime import datetime
import json

def parse_comments(comments):
    parsed_comments = []
    for item in comments:
        if 'kind' in item and item['kind'] == 't1':  # check to see if it is a comment
            comment_data = item['data']
            parsed_comment = {
                'id': comment_data['id'],
                'body': comment_data.get('body', ''),  # using get to avoid KeyError
                'author': comment_data.get('author', ''),
                'score': comment_data.get('score', 0),
                'replies': parse_comments(comment_data['replies']['data']['children']) if comment_data.get('replies') else []
            }
            parsed_comments.append(parsed_comment)
    return parsed_comments

# we use this function to convert responses to dataframes
def get_subreddit_posts(res, headers):
    posts = []
    # loop through each post pulled from res and append to df
    for post in res.json()['data']['children']:
        post_data = post['data']
        post_details = {
            'title': post_data['title'],
            'selftext': post_data['selftext'],
            'upvote_ratio': post_data['upvote_ratio'],
            'ups': post_data['ups'],
            'downs': post_data['downs'],
            'score': post_data['score'],
            'num_comments': post_data['num_comments'],
            'created_utc': datetime.fromtimestamp(post_data['created_utc']).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'id': post_data['id'],
            'url': post_data['url'],
            'kind': post['kind']
        }

        # fetch comments for the post
        comments_url = f"https://oauth.reddit.com/r/gatech/comments/{post_data['id']}?limit=100"
        comments_res = requests.get(comments_url, headers=headers)
        if comments_res.status_code == 200:
            comments_content = comments_res.json()
            post_details['comments'] = parse_comments(comments_content[1]['data']['children'])

        posts.append(post_details)
    return posts

# authenticate API
auth = requests.auth.HTTPBasicAuth('fuHSQXgJfhJZDtn-0I8DBw', 'e84VuhD2YyCCLiFySE-7siDkhV52UA')
data = {
    'grant_type': 'password',
    'username': 'HelluvaWreckFromTech',
    'password': '!Yourmom123'
}
headers = {'User-Agent': 'myBot/0.0.1'}

# send authentication request for OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
# extract token from response and format correctly
token = f"bearer {res.json()['access_token']}"
# update API headers with authorization (bearer token)
headers = {**headers, **{'Authorization': token}}

# initialize dataframe and parameters for pulling data in loop
data = []
params = {'limit': 100}
params['after'] = 't3_1brqzao'

# need to get these ones first:
# fullname is: t3_1brqzao
# fullname is: t3_1b0zaki
# fullname is: t3_1anpksc
# fullname is: t3_1abl52x
# fullname is: t3_195a2yd

# loop through 10 times (returning 1K posts)
for i in range(6):
    # make request
    res = requests.get("https://oauth.reddit.com/r/gatech/new",
                       headers=headers,
                       params=params)
    if res.status_code == 200:

        # get dataframe from response
        new_df = get_subreddit_posts(res, headers)

        # getting the last data frame that was returned, in order to get the subsequent data
        row = new_df[len(new_df)-1]
        # create fullname
        fullname = row['kind'] + '_' + row['id']
        print("fullname is: " + fullname)
        params['after'] = fullname
        
        # append new_df to data
        data.append(new_df)
    else:
        print('error: ' + str(res.status_code))

# write data to a JSON file
with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)


    # t3_195a2yd