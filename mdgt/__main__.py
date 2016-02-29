import argparse
from .mdgt import consolePrint, jsonPrint, listProvs
from .provider import Provider
from .webserve import serve as webserve

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
    webserve(int(args.webserver))
elif (not args.provider) and (not args.query):
    print("Provider and query required. See --help")
elif args.json:
    prov = Provider(args.provider)
    jsonPrint(prov.scrape(args.query))
else:
    prov = Provider(args.provider)
    consolePrint(prov.scrape(args.query))