
def lookupattr(obj, name, default=None):
    """Recursively lookup an attribute or key on an object."""
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
        obj = attr

    if callable(attr):
        return attr()
    else:
        return attr
