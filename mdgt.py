'''
mdgt
A Microdata-Parsing Microservice

Command-line usage:
    python mdgt.py --help
'''
from pathlib import Path
import json
from provider import Provider
import webserve


def jsonPrint(dataDict):
    '''Outputs parsed information as json to stdout.'''
    print(json.dumps(dataDict))


def consolePrint(dataDict):
    '''Outputs parsed information in a console-friendly format to stdout.'''
    for k in dataDict.keys():
        v = dataDict[k]
        if type(v) is list:
            buf = ""
            outStr = "{}: ".format(k)
            for i in range(len(k) + 2):
                buf = "{} ".format(buf)
            for e in v:
                print("{}{}".format(outStr, e))
                outStr = buf
        else:
            print("{}: {}".format(k, v))


def listProvs():
    '''Outputs a list of all available providers to stdout.'''
    p = Path('providers')
    print("Available providers:")
    provs = list(p.glob('*.json'))
    for prov in provs:
        print("- {}".format(prov.stem))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    # Required arguments
    parser.add_argument(
        'provider',
        nargs='?',
        help="Which provider to use (or, the type of object to query).")
    parser.add_argument(
        'query',
        nargs='?',
        help="The query for the provider to consume.")
    # Other options
    parser.add_argument('-p', '--providers', action='store_true',
                        help="List available providers and exit.")
    # These arguments affect the output and are exclusive
    outputGroup = parser.add_mutually_exclusive_group()
    outputGroup.add_argument('-c', '--console', action='store_true',
                             help="Output console-formatted text (default).")
    outputGroup.add_argument('-j', '--json', action='store_true',
                             help="Output json.")
    outputGroup.add_argument('-w', '--webserver', nargs='?', const=8181,
                             help="Start as a web server daemon on the \
                             specified port (default 8181).")
    args = parser.parse_args()

    if args.providers:
        listProvs()
    elif args.webserver:
        # TODO: Add error checking once the config file is implemented.
        webserve.serve(int(args.webserver))
    elif (not args.provider) and (not args.query):
        print("Provider and query required. See --help")
    elif args.json:
        prov = Provider(args.provider)
        jsonPrint(prov.scrape(args.query))
    else:
        prov = Provider(args.provider)
        consolePrint(prov.scrape(args.query))
