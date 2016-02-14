from lxml import html
from pathlib import Path
import requests
import json
import sys

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
	parseNode(tree, mod['root'])

def parseNode(parentTree, modNode):
	tree = parentTree.xpath(modNode['xpath'])
	# If repeat is not present or set to true, then just use the first result
	if 'repeat' not in modNode or modNode['repeat'] == False:
		tree = tree[0:1]
	for t in tree:
		if 'value' in modNode:
			val = modNode['value']
			if val['type'] == 'text':
				print(val['name'] + ": " + t.text.strip())
			elif val['type'] == 'attr':
				print(val['name'] + ": " + t.get(val['attr']))
		if 'items' in modNode:
			for i in modNode['items']:
				parseNode(t, i)

if __name__ == "__main__":
	import sys
	if len(sys.argv) < 3 or sys.argv[1] == '--help':
		print("Usage: " + sys.argv[0] + " [module] [query]")
	else:
		scrape(loadMod(sys.argv[1]), sys.argv[2])
