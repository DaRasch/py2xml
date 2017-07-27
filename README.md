# Magic declarative XML building tool

### Example

```python
class Page(Document):
    # Simple html document
    with html() as root:
        with head():
            link(rel='stylesheet', type='text/css', href='main.css')
        with body() as b:
            b.append(some_xml_ETree)
            with html.div() as x:
                p('This is text')

Page.root # Access to the generated ETree
print(Page(doctype='html'))
```
