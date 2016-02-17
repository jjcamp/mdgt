from lxml import html
from pathlib import Path
import requests
import json

def loadMod(name):
	p = Path("./mod/" + name + ".json")
	if p.exists() == False:
		raise RuntimeError("Module " + name + " does not exist.")
	with p.open() as f:
		return json.loads(f.read())

def scrape(mod, query):
	# Get search information
	search = mod['search']
	uriSearch = search['uriRoot'] + search['searchPath'].replace('*', query)
	page = requests.get(uriSearch)
	tree = html.fromstring(page.content)
	# Some sources may have a feeling lucky option, so this part is optional
	if 'firstResultXpath' in search:
		resNode = tree.xpath(search['firstResultXpath'])[0]
		resUri = resNode.get('href')
		# Check for a relative path
		if resUri[0] == '/':
			resUri = search['uriRoot'] + resUri
		page = requests.get(resUri)
		tree = html.fromstring(page.content)

	# Start with the MD object's root and recurse through the tree
	data = dict()
	parseNode(tree, mod['root'], data)
	return data
	#print(json.dumps(data))

def parseNode(parentTree, modNode, dataDict):
	dataList = []
	tree = parentTree.xpath(modNode['xpath'])
	# If repeat is not present or set to true, then just use the first result
	if 'repeat' not in modNode or modNode['repeat'] == False:
		tree = tree[0:1]
	for t in tree:
		if 'value' in modNode:
			val = modNode['value']
			if val['type'] == 'text':
				dataList.append(t.text.strip())
			elif val['type'] == 'attr':
				dataList.append(t.get(val['attr']))
			if len(dataList) == 1:
				dataDict[val['name']] = dataList[0]
			elif len(dataList) > 1:
				dataDict[val['name']] = dataList
		if 'items' in modNode:
			for i in modNode['items']:
				parseNode(t, i, dataDict)

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
	p = Path('mod')
	print("Available modules:")
	mods = list(p.glob('*.json'))
	for m in mods:
		print("- " + m.stem)

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	# Required arguments
	parser.add_argument('module', nargs = '?',
	               help = "Which module to call (or, the type of object to query).")
	parser.add_argument('query', nargs = '?',
	               help = "The query for the module to consume.")
	# Other options
	parser.add_argument('-m', '--modules', action = 'store_true',
	               help = "List available modules and exit.")
	# These arguments affect the output and are exclusive
	outputGroup = parser.add_mutually_exclusive_group()
	outputGroup.add_argument('-c', '--console', action = 'store_true',
	                  help = "Output console-formatted text (default).")
	outputGroup.add_argument('-j', '--json', action = 'store_true',
	                  help = "Output json.")
	args = parser.parse_args()

	if args.modules:
		listMods()
	elif (not args.module) and (not args.query):
		print("Module and query required. See --help")
	elif args.json:
		jsonPrint(scrape(loadMod(args.module), args.query))
	else:
		consolePrint(scrape(loadMod(args.module), args.query))
