# Decorator
from decorator import decorator

__all__ = ['datatable']

def datatable(datatable_class, name='datatable'):
    def datatable(f, request, *args, **kwargs):
        datatable_instance = datatable_class(request.GET, name)
        response = datatable_instance.process_request(request, name)
        if response is not None:
            return response
        response = f(request, *args, **kwargs)
        return datatable_instance.process_response(request, response)
    return decorator(datatable)
