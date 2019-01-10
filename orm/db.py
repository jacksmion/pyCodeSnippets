# -*- coding:utf-8 -*-


class Field(object):

    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type

    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)



class StringField(Field):

    def __init__(self, name):
        super(StringField, self).__init__(name, 'varchar(100)')


class IntegerField(Field):

    def __init__(self, name):
        super(IntegerField, self).__init__(name, 'bigint')



class ModalMetaClass(type):

    def __new__(cls, name, bases, attrs):
        if name == "Modal":
            return type.__new__(cls, name, bases, attrs)

        mappings = dict()

        for k, v in attrs.iteritems():
            if isinstance(v, Field):
                print "Found Mapping: %s==>%s" % (k, v)
                mappings[k] = v

        for k in mappings.iterkeys():
            attrs.pop(k)

        # 如果没有写表名，默认用类名做表名
        if "__tablename__" not in attrs:
            attrs['__tablename__'] = name

        attrs['__mappings__'] = mappings
        return type.__new__(cls, name, bases, attrs)


class Modal(dict):
    __metaclass__ = ModalMetaClass

    def __init__(self, **kwargs):
        super(Modal, self).__init__(**kwargs)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def save(self):
        fields = [] 
        params = []
        args = []
        for k, v in self.__mappings__.iteritems():
            fields.append(v.name)
            params.append('?')
            args.append(getattr(self, k, None))

        sql = 'insert into %s (%s) values (%s)' % (self.__tablename__, ','.join(fields), ','.join(params))
        print 'SQL: %s' % sql
        print 'ARGS: %s' % str(args)
