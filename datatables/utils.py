# Django
from django.utils.copycompat import deepcopy
from django.utils import simplejson

__all__ = ['hungarian_to_python', 'lookupattr']

def dumpjs(obj, *args, **kwargs):
    """Dump a Python object as Javascript, with support for a __json__ method."""
    class Encoder(simplejson.JSONEncoder):
        def iterencode(self, o, _one_shot=False):
            #print o
            if hasattr(o, '__json__'):
                if callable(o.__json__):
                    print 'foo', o
                    return o.__json__()
                else:
                    return o.__json__
            else:
                return super(Encoder, self).iterencode(o)#, _one_shot=_one_shot)
    kwargs['cls'] = Encoder
    kwargs['sort_keys'] = True
    #return simplejson.dumps(obj, *args, **kwargs)
    output = simplejson.dumps(obj, *args, **kwargs)
    for key, val in obj.items():
        if 'fn' == key[0:2]:
            output = output.replace(simplejson.dumps(val), val)
    return output

class fn(object):
    """Wrapper for a Javascript function that should be encoded without escaping."""
    def __init__(self, fndef):
        self.fndef = unicode(fndef)
    def __getattr__(self, name):
        return getattr(self.fndef, name)
    def __repr__(self):
        return 'fn(%r)' % self.fndef
    def __unicode__(self):
        return self.fndef
    def __json__(self):
        return unicode(self.fndef)
    def __deepcopy__(self, memo):
        return deepcopy(self.fndef, memo)
        #return self.__class__(deepcopy(self.fndef, memo))

def hungarian_to_python(name, value):
    """Validate DataTable options specified in Hungarian notation."""
    if value is None:
        return value
    elif name.startswith('fn') and name[2].isupper():
        return fn(value)
    elif name.startswith('n') and name[1].isupper():
        return value
    elif name.startswith('m') and name[1].isupper():
        return value
    elif name.startswith('o') and name[1].isupper():
        d = {}
        for k, v in dict(value).iteritems():
            d[k] = hungarian_to_python(k, v)
        return d
    elif name.startswith('a') and name[1].isupper():
        return list(value)
    elif name.startswith('a') and name[1] in 'abfimnos' and name[2].isupper():
        a = []
        for i in list(value):
            a.append(hungarian_to_python(name[1:], i))
        return a
    elif name.startswith('s') and name[1].isupper():
        return unicode(value)
    elif name.startswith('b') and name[1].isupper():
        return bool(str(value).lower() in ('t', 'true', 'yes', 'y', '1'))
    elif name.startswith('f') and name[1].isupper():
        return float(value)
    elif name.startswith('i') and name[1].isupper():
        return int(value)
    else:
        raise NameError, 'name "%s" is not in hungarian notation' % name

def lookupattr(obj, name, default=None):
    """Recursively lookup an attribute or key on an object."""
    name = name.replace('__', '.')
    for element in name.split('.'):
        try:
            attr = obj.__getattribute__(element)
        except AttributeError:
            try:
                attr = obj.__dict__[element]
            except (KeyError, AttributeError):
                try:
                    attr = obj[element]
                except (KeyError, TypeError):
                    attr = default
                    break
        except:
            attr = default
            break
        if callable(attr):
            obj = attr()
        else:
            obj = attr
    if callable(attr):
        return attr()
    else:
        return attr
