# Decorator
from decorator import decorator

__all__ = ['datatable']

def datatable(datatable_class, name='datatable'):
    def datatable(f, request, *args, **kwargs):
        datatable_instance = datatable_class(request.GET, name)
        setattr(request, name, datatable_instance)
        return f(request, *args, **kwargs)
    return decorator(datatable)
