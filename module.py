class module:
	def __init__(self, name):
		from pathlib import Path
		import json

		self.name = name
		p = Path("./mod/" + name + ".json")
		if p.exists() == False:
			raise RuntimeError("Module " + name + " does not exist.")
		with p.open() as f:
			self.modJson = json.loads(f.read())

	def scrape(self, query):
		from lxml import html
		import requests

		# Get search information
		search = self.modJson['search']
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
		module.parseNode(tree, self.modJson['root'], data)
		return data

	def parseNode(parentTree, modNode, dataDict):
		from lxml import html

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
					module.parseNode(t, i, dataDict)
