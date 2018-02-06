import json
import keys
import argparse
import requests
import debug
from datetime import datetime
from debug import debug_print
from util import clean_text

def collect_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--output', help='name of the file to output search results to.', default='output.txt')

    engines_help_str = "Name of custom search engine to use.\n\nAvailable custom search engines:\n\n"
    for k, v in keys.engine_descriptions.items():
        engines_help_str += "{} : {}\n".format(k, v)

    parser.add_argument('engine', help=engines_help_str)
    parser.add_argument('query', help='term(s) to search for.')
    parser.add_argument('--debug', help='print verbose debug info.', action='store_true')
    parser.add_argument('-c', '--count', help='maximum number of search results to return', type=int, default=30)

    options = vars(parser.parse_args())

    debug.debug_flag = options['debug']

    return options

def do_query(custom_engine_name, query_string, start = 1):
    url = 'https://www.googleapis.com/customsearch/v1?key={}&cx={}&q={}&start={}'
    url = url.format(keys.cse_keys['api_key'], keys.cse_keys[custom_engine_name], query_string, start)
    debug_print("Executing query with url {}".format(url))
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        print("Something went wrong with the query.")
        debug_print(r.text())
        return None



def write_query_general_info(file_handle, response_json):
    file_handle.write("Query general information:\n")
    file_handle.write("\tExecution time: {}\n".format(datetime.now().isoformat(' ')))
    file_handle.write("\tResults: {}\n".format(response_json['searchInformation']['totalResults']))
    file_handle.write("\tCustom search engine name: {}\n".format(response_json['context']['title']))

def write_query_result(file_handle, response_json, start = 1):
    file_handle.write("Query results {} through {}\n".format(start,
        start + int(response_json['queries']['request'][0]['count']) - 1))
    index = 0
    for item in response_json['items']:
        file_handle.write('\tTitle: {}\n'.format(clean_text(item['title'])))
        file_handle.write('\tSnippet: {}\n'.format(clean_text(item['snippet'])))
        file_handle.write('\tLink: {}\n'.format(item['link']))
        file_handle.write('\tResult number: {}\n'.format(start + index))
        index += 1

def handle_success_response(options, response_json):
    with open(options['output'], 'w') as output_file:
        write_query_general_info(output_file, response_json)
        write_query_result(output_file, response_json)
        for start in range(11, min(options['count'], int(response_json['searchInformation']['totalResults'])), 10):
            nested_response = do_query(options['engine'], options['query'], start)
            if nested_response:
                write_query_result(output_file, nested_response, start)


def run_query(options):
    # top level query call (to avoid infinite recursion between do_query and handle_success_response)
    response_json = do_query(options['engine'], options['query'])
    if response_json:
        handle_success_response(options, response_json)

def main():
    run_query(collect_args()) 

if __name__ == "__main__":
    main()
