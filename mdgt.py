from pathlib import Path
import json
from element import Element


def jsonPrint(dataDict):
    print(json.dumps(dataDict))


def consolePrint(dataDict):
    for k in dataDict.keys():
        v = dataDict[k]
        if type(v) is list:
            buf = ''
            outStr = k + ': '
            for i in range(len(k) + 2):
                buf = buf + ' '
            for e in v:
                print(outStr + e)
                outStr = buf
        else:
            print(k + ': ' + v)


def listMods():
    p = Path('elem')
    print("Available elements:")
    mods = list(p.glob('*.json'))
    for m in mods:
        print("- " + m.stem)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    # Required arguments
    parser.add_argument(
        'element',
        nargs='?',
        help="Which element to call (or, the type of object to query).")
    parser.add_argument(
        'query',
        nargs='?',
        help="The query for the element to consume.")
    # Other options
    parser.add_argument('-e', '--elements', action='store_true',
                        help="List available elements and exit.")
    # These arguments affect the output and are exclusive
    outputGroup = parser.add_mutually_exclusive_group()
    outputGroup.add_argument('-c', '--console', action='store_true',
                             help="Output console-formatted text (default).")
    outputGroup.add_argument('-j', '--json', action='store_true',
                             help="Output json.")
    args = parser.parse_args()

    if args.elements:
        listMods()
    elif (not args.element) and (not args.query):
        print("Element and query required. See --help")
    elif args.json:
        mod = Element(args.element)
        jsonPrint(mod.scrape(args.query))
    else:
        mod = Element(args.element)
        consolePrint(mod.scrape(args.query))
