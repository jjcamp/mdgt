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

def scrape(mod):
	# Load the page from the specified URI
	uri = mod['uri']
	page = requests.get(uri)
	tree = html.fromstring(page.content)

	# Start with the MD object's root and recurse through the tree
	parseNode(tree, mod['root'])

def parseNode(parentTree, modNode):
	tree = parentTree.xpath(modNode['xpath'])
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

#if __name__ == "__main__":
#    import sys
scrape(loadMod("imdb"))
