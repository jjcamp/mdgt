Provider API
====
Providers are what tell **mdgt** how to find microdata.  Writing your own is pretty simple.

XPath
-----
**mdgt** providers use XPath syntax to crawl the document tree.  Because of this, providers
can find data even if the source isn't using [schema.org](http://schema.org) microdata
schemas.  [W3Schools](http://www.w3schools.com/xsl/xpath_syntax.asp) has an excellent
overview of XPath syntax.

Provider Files
----
Providers are written using JSON, and the name of the file is used to call the provider
from **mdgt** (e.x. `stock.json` is called with `mdgt stock [symbol]`).  Providers are
structured in such a way:
```
{
    "search":{
        "uriRoot":"http://a.website.com",
        "searchPath":"/search.html?q=*",
        "firstResultXpath":"//xpath/for/first/result/link"
    },
    "root":{
        "xpath":"/xpath/for/root/microdata/element",
        "items":[
            {
                "xpath":"/first/item",
                "value":{
                    "name":"Name for the element",
                    "type":"text"
                }
            },
            {
                "xpath":"/second/item",
                "value":{
                    "name":"Another name",
                    "type":"attr",
                    "attr":"attributeName"
                }
            }
        ]
    }
}
```
**Explanation**:
* The `search` object tells **mdgt** how to use the query it is given by the user.
    * `uriRoot` is the base URI for the provider website
    * `searchPath`, when added to `uriRoot`, is the URI for the provider's search
      page.  The `*` will be replaced by the user's query.
    * `firstResultXpath` is an optional XPath string to the link for the first
      search result.  If the provider's search returns a list of results instead
      of immediately taking you to the most relevant result, then use this.
* The `root` object is the base element, or *node* (usually a `div`) that contains
  all of the microdata.

**Node Syntax**:
* `xpath`: The XPath query to the node (element). *Required for all nodes.*
* `items`: A list of child nodes.  Any node may have an `items` list.
* `value`: An object which tells the parser that this node contains a value.
  * `name`: This is the name that **mdgt** will output for the value
  * `type`: Can be one of:
    * `text`: The text of the element between its opening and closing tags. Cannot
      contain any elements inside of this element.
    * `striptext`: The text of the element between its opening and closing tags,
      but this node contains child elements which should be ignored.
    * `attr`: The text of an element attribute.
  * `attr`: Required if `type` is `attr`, the attribute containing the value.
* `repeat`: When this exists and is `true`, it tells the parser that this node
  should be parsed for multiple occurances.
  
Repeat example snippet:
```
"xpath":"//ul",
"items":[
    "xpath":"//li",
    "repeat":true,
    "value":{
        "name":"List Items",
        "type":"text"
    }
]
```
This would return the text of all the `li` elements under their parent `ul`, and
place them in an array called "List Items". 