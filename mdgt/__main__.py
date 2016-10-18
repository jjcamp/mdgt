import argparse
import configparser
import sys
from io import StringIO
from pathlib import Path
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
outputGroup.add_argument('-f', '--config', nargs='?', const=None,
                         help="Path to configuration file to use.")
outputGroup.add_argument('-j', '--json', action='store_true',
                         help="Output json.")
outputGroup.add_argument('-pd', '--provider-dir', nargs='?', const=None,
                         help="Directory that contains provider files.")
outputGroup.add_argument('-w', '--webserver', nargs='?', const=8181,
                         help="Start as a web server daemon on the \
                         specified port (default 8181).")
args = parser.parse_args()

# Config file
if args.config:
    conf_file = Path(args.config)

    if not conf_file.exists():
        sys.exit("Configuration file not found")

else:
    conf_file = Path('./mdgt.conf')

if conf_file.exists():
    # Override args
    conf_parser = configparser.ConfigParser()

    # Add dummy section for reading
    conf_parser.read_string(
        StringIO("[mdgt]\n%s" % conf_file.open().read()).read()
    )

    section = conf_parser['mdgt']

    args.console = args.console or section.getboolean('console', True)
    args.json = args.json or section.getboolean('json', False)
    args.provider_dir = args.provider_dir or section.get('provider-dir')

if args.providers:
    listProvs()
elif args.webserver:
    # TODO: Add error checking once the config file is implemented.
    webserve(int(args.webserver))
elif (not args.provider) and (not args.query):
    print("Provider and query required. See --help")
elif args.json:
    prov = Provider(args.provider, args.provider_dir)
    jsonPrint(prov.scrape(args.query))
else:
    prov = Provider(args.provider, args.provider_dir)
    consolePrint(prov.scrape(args.query))
