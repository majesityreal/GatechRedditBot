import requests
import requests.auth
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

# function to get posts and their comments from a subreddit
def get_subreddit_posts(subreddit, headers, limit=100, after=None):
    global request_count
    posts = []
    url = f"https://oauth.reddit.com/r/{subreddit}/hot?limit={limit}"
    
    if after:
        url += f"&after={after}"

    res = requests.get(url, headers=headers)
    request_count += 1  # Increment the request counter

    if res.status_code == 200:
        content = res.json()
        for post in content['data']['children']:
            post_data = post['data']
            post_details = {
                'title': post_data['title'],
                'score': post_data['score'],
                'id': post_data['id'],
                'url': post_data['url'],
                'created_utc': post_data['created_utc'],
                'num_comments': post_data['num_comments'],
                'selftext': post_data['selftext']
            }

            # fetch comments for the post
            comments_url = f"https://oauth.reddit.com/r/{subreddit}/comments/{post_data['id']}?limit=100"
            comments_res = requests.get(comments_url, headers=headers)
            request_count += 1
            if comments_res.status_code == 200:
                comments_content = comments_res.json()
                post_details['comments'] = parse_comments(comments_content[1]['data']['children'])

            posts.append(post_details)
        
        # check to see if there's more to fetch
        after = content['data'].get('after')
        if after:
            posts.extend(get_subreddit_posts(subreddit, headers, limit, after))
    
    return posts


#authentication information
auth = requests.auth.HTTPBasicAuth('fuHSQXgJfhJZDtn-0I8DBw', 'e84VuhD2YyCCLiFySE-7siDkhV52UA')
data = {'grant_type': 'password', 'username': 'HelluvaWreckFromTech', 'password': '!Yourmom123'}
headers = {'User-Agent': 'MyBot/0.0.1'}

# get the access token
res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
TOKEN = res.json()['access_token']

# we upadte headers with the access token
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

request_count = 0

# fetch posts from r/gatech
posts = get_subreddit_posts('gatech', headers)

# write data to a JSON file
with open('gatech_posts_with_comments_1.json', 'w') as f:
    json.dump(posts, f, indent=4)

print("Data saved to gatech_posts_with_comments_1.json")
print(f"Total number of requests made: {request_count}")