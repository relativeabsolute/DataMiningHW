from datetime import datetime
import argparse
import sys
import json
import requests
import debug
import urllib.parse
from string import printable
from pathlib import Path
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

def clean_text(text):
    s = "".join(c for c in text if c in printable)
    return ' '.join(s.split())

def make_query(original, query_type):
    return query_types[query_type].format(original)

def get_oauth():
    return OAuth1(twitter_auth['api_key'], twitter_auth['api_secret'],
        twitter_auth['access_token'], twitter_auth['access_secret'])

# check for necessary output files, creating any directories if necessary
# returns the id of the tweet to start from (or 0 if this is the first search of this name)
def check_files(options):
    p = Path(options['output_dir']) / options['search_name']
    p.mkdir(parents=True, exist_ok=True)
    last_id_path = p / 'last_id.txt'
    since_id = 0
    if last_id_path.exists():
        with last_id_path.open('r') as last_id_file:
            since_id = int(last_id_file.read().strip())
    debug_print("Previous since id = {}".format(since_id))
    return since_id

def write_last_id(options, last_id):
    p = Path(options['output_dir']) / options['search_name'] / 'last_id.txt'
    with p.open('w') as last_id_file:
        last_id_file.write(str(last_id))

def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_dir', help='name of folder to output to.  Defaults to ./twitter, and creates the output directory if it doesn\'t exist.', default='./twitter')
    query_type_help_str = 'Type of query to execute.  Choices:\n'
    for k, v in query_descriptions.items():
        query_type_help_str += "{} : {}\n".format(k, v)
    parser.add_argument('-t', '--type', help=query_type_help_str, choices=query_types.keys(), default='default')
    parser.add_argument('search_name', help='name of query (used to group queries and detect tweets that were found previously')
    parser.add_argument('query', help='query to search for')
    parser.add_argument('-c', '--max_count', help="maximum number of tweets to store", type=int, default=5000)
    parser.add_argument('--debug', help='print verbose debug info', action='store_true')
    options = vars(parser.parse_args())
    options['full_query'] = make_query(options['query'], options['type'])

    debug.debug_flag = options['debug']
    
    debug_print("Command line options passed: {}".format(options))

    return options

def make_query_url(parameters):
    debug_print("Calling make_query_url")
    url = 'https://api.twitter.com/1.1/search/tweets.json?lang=en'
    for k, v in parameters.items():
        url += '&{}={}'.format(k, v)
    debug_print("Resulting url: {}".format(url))
    return url

def do_query_url(url):
    debug_print("Sending query to url {}".format(url))
    r = requests.get(url, auth=get_oauth())
    if r.status_code == 200:
        return r.json()
    else:
        print("Something went wrong with the query")
        debug_print(r.text)
        return None

def do_query(options, since_id):
    debug_print("Calling do_query")
    url = 'https://api.twitter.com/1.1/search/tweets.json?q={}&lang=en&since_id={}'
    url = url.format(urllib.parse.quote(options['full_query']), since_id)
    debug_print("Result of url format in do_query: {}".format(url))
    return do_query_url(url)

def write_query_general_info(response_json, options):
    output_path = Path(options['output_dir']) / options['search_name'] / (options['search_name'] + '.txt')
    with output_path.open('a') as output_file:
        output_file.write('Query general information:\n')
        output_file.write('\tExecution time: {}\n'.format(datetime.now().isoformat(' ')))
        output_file.write('\tQuery: {}\n'.format(options['full_query']))

def write_tweet_info(tweet_object, options):
    debug_print("Writing tweet info")
    output_path = Path(options['output_dir']) / options['search_name'] / (options['search_name'] + '.txt')
    with output_path.open('a') as output_file:
        output_file.write('Tweet info:\n')
        output_file.write('\tID:{}\n'.format(tweet_object['id_str']))
        output_file.write('\tCreated at:{}\n'.format(tweet_object['created_at']))
        output_file.write('\tAuthor:{}\n'.format(tweet_object['user']['screen_name']))
        output_file.write('\tText:{}\n'.format(clean_text(tweet_object['text'])))
        try:
            output_file.write('\tURL:{}\n'.format(tweet_object['entities']['urls'][0]['expanded_url']))
        except Exception:
            pass

def read_statuses(statuses, options, former_since_id):
    next_id = former_since_id
    for item in statuses:
        curr_id = int(item['id_str'])
        debug_print("Tweet current id = {}".format(curr_id))
        if curr_id > next_id:
            debug_print("Next id updated from {} to {}".format(next_id, curr_id))
            next_id = curr_id
        if curr_id > former_since_id:
            debug_print("Tweet id more recent than id {}".format(former_since_id))
            write_tweet_info(item, options)
    return next_id

 
def handle_successful_response(response_json, options, former_since_id):
    debug_print("Successful response received")
    debug_print("Writing general query info")
    write_query_general_info(response_json, options)
    debug_print("General query info written successfully")
    count = 0
    last_id = 0
    while count < options['max_count']:
        statuses = response_json['statuses']
        count += len(statuses)
        debug_print("{} statuses received".format(count))
        last_id = read_statuses(statuses, options, former_since_id)
        debug_print("Next since id = {}".format(former_since_id))
        try:
            next_results = response_json['search_metadata']['next_results']
        except:
            debug_print("End of results")
            break
        # get rid of the ? character and split parameters
        kw_args = dict([kv.split('=') for kv in next_results[1:].split('&')])
        debug_print("Next query args = {}".format(str(kw_args)))
        response_json = do_query_url(make_query_url(kw_args))
    write_last_id(options, last_id)        

# top level query to run
def run_query(options):
    since_id = check_files(options)
    response = do_query(options, since_id)
    if response:
       handle_successful_response(response, options, since_id)
    

def main():
    run_query(handle_args())

if __name__ == "__main__":
    main()
