import requests
import pandas as pd
from datetime import datetime
import json
import time

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
    # print("result json: " + str(res.json()))
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

batchNumber = 1 # which number we start at


while 1:
    data = []
    # loop through X times, batch requesting
    for i in range(4):
        # make request
        res = requests.get("https://oauth.reddit.com/r/gatech/old",
                        headers=headers,
                        params=params)
        # res = requests.get(f'https://oauth.reddit.com/r/gatech/new.json?sort=new&show=all&after=t3\_{params['after']}&limit=100',
        #                    headers=headers)
        
        if res.status_code == 200:

            # get dataframe from response
            postData = get_subreddit_posts(res, headers)

            if len(postData) == 0:
                print('length of post data is 0!!!')
                print(postData)
            # getting the last data chunk that was returned, in order to get the subsequent batch after that
            row = postData[len(postData)-1]
            # create fullname (Reddit specific stuff here)
            fullname = row['kind'] + '_' + row['id']
            if i == 3:
                print("SAVING AT THIS ONE! fullname is: " + fullname)
            else:
                print("fullname is: " + fullname)
            # params['after'] = fullname
            
            # append new_df to data
            data.append(postData)
        else:
            print('error: ' + str(res.status_code) + ' iterator i: ' + str(i))
            if str(res.status_code) == '429':
                print('we hit limit of requests, waiting')
                time.sleep(120) # sleep for 2 minutes before trying again
                i -= 1
            continue
    # at the end of batch of 4, write data to JSON file
    # write data to a JSON file
    with open('data/random' + str(batchNumber) + '.json', 'w') as f:
        json.dump(data, f, indent=4)

    batchNumber += 1 # increment batch number at the very end

    # t3_195a2yd