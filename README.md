# Magic declarative XML building tool

```python
from py2xml import Document, ContextStack

def dynamic_subtree(id, text):
    # Add the content of SubPage to the current context
    class SubPage(Document, blacklist=['text', 'id', 'str']):
        # The blacklist protects names of arguments and external functions
        with div(id=str(id), **{'class': 'someclass'}) as root:
            p(text)
    return SubPage.root

def split_context(id, text):
    # Create a seperate document for SubPage
    class SubPage(Document, whitelist=['div', 'p'], ctx=ContextStack()):
        # The whitelist limits the available names
        with div(id=str(id), **{'class': 'someclass'}) as root:
            p(text)
    return SubPage.root

class Page(Document, blacklist=dir()):
    # blacklist=dir() is handy do be able to acces all defined names
    # Simple html document
    with html() as root:
        with head():
            link(rel='stylesheet', type='text/css', href='main.css')
        with body() as b:
            with div():
                p('This is text')
            # No append required
            dynamic_subtree(0, 'test')
            # Requires append because of different Context
            b.append(split_context(1, 'more text'))


Page.root # Access to the generated ETree
print(Page(doctype='html'))

# Result:
'!DOCTYPE html>\n<html><head><link href="main.css" rel="stylesheet" type="text/css"/></head><body><div><p>This is text</p></div><div class="someclass" id="0"><p>test</p></div><div class="someclass" id="1"><p>more text</p></div></body></html>'
```
