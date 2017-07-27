#!/usr/bin/env python3.5
#-*- coding:utf-8 -*-

'''Magic declarative XML building tool.

The only exported objects are the `Document` and `ContextStack` classes.

Example
=======

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

'''

import contextlib
import collections

try:
    import lxml.etree as etree
except ImportError:
    import xml.etree.ElementTree as etree

__version__ = '0.1.0'

__all__ = ['Document', 'ContextStack']


class ContextStack(object):
    '''Keeps track of open contexts and allows appending to the top.'''

    def __init__(self):
        self._stack = []

    def add(self, node: 'Element'):
        '''Append to the top of the stack.'''
        if self._stack:
            self._stack[-1].append(node)

    def push(self, node: 'Element'):
        '''Push onto the stack.'''
        self._stack.append(node)

    def pop(self):
        '''Remove the top of the stack.'''
        self._stack.pop()

CTX = ContextStack()


class ElementFactory(object):
    '''Thin wrapper around `etree.Element` with context manager capabilities.'''

    def __init__(self, tag: 'str', context: 'ContextStack'):
        self._tag = tag
        self._context = context
        self.element = None

    def __call__(self, text: 'str'=None, attrib: 'Dict[str, Any]'=None, nsmap: 'Dict[str, Any]'=None, **extra: 'Any'):
        if attrib:
            attrib = {key: str(val) for key, val in attrib.items()}
        if extra:
            extra = {key: str(val) for key, val in extra.items()}
        self.element = etree.Element(self._tag, attrib, nsmap, **extra)
        if text:
            self.element.text = text
        self._context.add(self.element)
        return self

    def __enter__(self):
        self._context.push(self.element)
        return self.element

    def __exit__(self, *args, **kwargs):
        self._context.pop()

    def append(self, item: 'Element'):
        self.element.append(item)


class CommentFactory(ElementFactory):
    def __call__(self, text: 'str'=None):
        self.element = etree.Comment(text or '')
        self._context.add(self.element)
        return self

    def __enter__(self):
        raise AttributeError('__enter__')

    def __exit__(self, *args, **kwargs):
        raise AttributeError('__exit__')



class ElementMap(collections.abc.MutableMapping):
    '''Returns a new `ElementFactory` for all nonexistent lookups.

    Keys with double underscores are not allowed.
    The default blacklist only contains the builtins.
    If a whitelist is given, it overrules the blacklist.
    '''
    _blacklist = frozenset(__builtins__.keys())

    def __init__(self, context: 'ContextStack', whitelist: 'Iterable[str]'=None, blacklist: 'Iterable[str]'=None):
        # whitelist overrides blacklist
        self._context = context
        self._map = {'Comment': CommentFactory('Comment', context)}

        self._whitelist = set(whitelist or set())
        self._blacklist = set(blacklist or self.__class__._blacklist)

    def __getitem__(self, key: 'str'):
        with contextlib.suppress(KeyError):
            return self._map[key]
        if not key.startswith('__'):
            if key in self._whitelist:
                return ElementFactory(key, self._context)
            elif not self._whitelist and key not in self._blacklist:
                return ElementFactory(key, self._context)
        raise KeyError(key)

    def __setitem__(self, key: 'str', value: 'Any'):
        self._map.__setitem__(key, value)

    def __delitem__(self, key: 'str'):
        self._map.__delitem__(key)

    def __iter__(self):
        return self._map.__iter__()

    def __len__(self):
        return self._map.__len__()


class DocumentMeta(type):
    '''Classes of this type build an element tree.'''

    def __new__(cls, name: 'str', bases: 'Sequence[type]', namespace: 'Mapping[str, Any]', **kwargs):
        return type.__new__(cls, name, bases, dict(namespace))

    @classmethod
    def __prepare__(mcls, name: 'str', bases: 'Sequence[type]', whitelist=None, blacklist=None, ctx=None):
        return ElementMap(ctx or CTX, whitelist, blacklist)

    def __call__(cls, *, doctype: 'str'=None, encoding='utf-8', declaration=None, pretty=False):
        if 'root' not in cls.__dict__:
            raise AttributeError('document must have root')
        if doctype is not None:
            doctype = f'<!DOCTYPE {doctype}>'
        return etree.tostring(cls.root, doctype=doctype, encoding=encoding,
            xml_declaration=declaration, pretty_print=pretty)


class Document(metaclass=DocumentMeta):
    '''Uses DocumentMeta for easy subclassing.'''
    pass
