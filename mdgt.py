from lxml import html
from pathlib import Path
import requests
import json

def scrapeIMDB(url):
	page = requests.get(url)
	tree = html.fromstring(page.content)

	# Get the first itemscope
	itemTree = tree.xpath('//*[@itemscope]')[0]
	# Get the item type for future delegation
	itemType = itemTree.get("itemtype")
	print("Schema: " + itemType)
	# From here on we assume this is a move for now
	# Get the movie name
	name = itemTree.xpath('//*[@itemprop="name"]')[0]
	print("Title: " + name.text)
	ratingTree = itemTree.xpath('//*[@itemprop="aggregateRating"]')[0]
	ratingVal = ratingTree.xpath('//*[@itemprop="ratingValue"]')[0]
	ratingMax = ratingTree.xpath('//*[@itemprop="bestRating"]')[0]
	print("Rating: " + ratingVal.text + "/" + ratingMax.text)
	contentRating = itemTree.xpath('//*[@itemprop="contentRating"]')[0]
	print("Content: " + contentRating.get("content"))
	duration = itemTree.xpath('//*[@itemprop="duration"]')[0]
	print("Duration: " + duration.get("datetime"))
	genres = itemTree.xpath('//span[@itemprop="genre"]')
	genresStr = ""
	for g in genres:
		genresStr = genresStr + g.text + " "
	print("Genres: " + genresStr)
	released = itemTree.xpath('//*[@itemprop="datePublished"]')[0]
	print("Release: " + released.get("content"))
	poster = itemTree.xpath('//*[@itemprop="image"]')[0]
	print("Poster: " + poster.get("src"))
	description = itemTree.xpath('//*[@itemprop="description"]')[0]
	print("Description: " + description.text.strip())

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
	tree = parentTree.xpath(modNode['xpath'])[0]
	if 'value' in modNode:
		val = modNode['value'];
		if val['type'] == 'text':
			print(val['name'] + ": " + tree.text)
		elif val['type'] == 'attr':
			print(val['name'] + ": " + tree.get(val['attr']))
	if 'items' in modNode:
		for i in modNode['items']:
			parseNode(tree, i)

#if __name__ == "__main__":
#    import sys
scrape(loadMod("imdb"))
