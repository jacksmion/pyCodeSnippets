# -*- coding:utf-8 -*-

class Foo(object):

    def __init__(self, name):
        self.name = name

    def __getattr__(self, name):
        print "__getattr__"
    
    def __getattribute__(self, name):
        print "__getattribute__"
        return object.__getattribute__(self, name)
    
    def __get__(self, obj, own):
        print "get"
        return self

f = Foo('test')
print f.x