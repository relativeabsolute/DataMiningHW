import argparse
import sys
import json
import requests
import debu
from debug import debug_print
from requests_oauthlib import OAuth1

auth_code = ''
with open('twitter_auth.txt', 'r') as auth_file:
    auth_code += auth_file.read()
exec(auth_code)

query_types = {
    'default' : '{}',
    'exact' : '\"{}\"',
    'hashtag' : '#{}',
    'from' : 'from:{}',
    'to' : 'to:{}',
    'at' : '@{}' }

query_descriptions = {
    'default' : 'Simply search for the word(s) contained in the query',
    'exact' : 'Search for the exact phrase in the query',
    'hashtag' : 'Search for a hashtag',
    'from' : 'Search for tweets authored by someone',
    'to' : 'Search for tweets in reply to someone',
    'at' : 'Search for tweets mentioning someone' }

def make_query(original, query_type):
    return query_types[query_type].format(original)

def get_oauth():
    return OAuth1(twitter_auth['api_key'], twitter_auth['api_secret'],
        twitter_auth['access_token'], twitter_auth['access_secret'])

def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', help='name of the file to output search results to.', default='output.txt')

    query_type_help_str = 'Type of query to execute.  Choices:\n'
    for k, v in query_descriptions:
        query_type_help_str += "{} : {}\n".format(k, v)
    parser.add_argument('-t', '--type', help=query_type_help_str, choices=query_types.keys(), default='default')
    parser.add_argument('query', help='query to search for')
    options = vars(parser.parse_args())

    debug.debug_flag = options['debug']

    return options

def run_query(options):
    url = 'https://api.twitter.com/1.1/search/tweets.json?q={}&lang=en'
    url.format(make_query(options['query'], options['type']))
    r = requests.get(url, auth=get_oauth())
    

def main():
    url = .format(sys.argv[1])
    r = requests.get(url, auth=get_oauth())
    if r.status_code == 200:
        print(json.dumps(r.json()))
    else:
        print(str(r.status_code))
        print(r.text)
       
    

if __name__ == "__main__":
    main()
