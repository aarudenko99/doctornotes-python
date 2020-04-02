from contextvars import ContextVar
current_request = ContextVar('current_request', default=None)


def get_current_request():
    return current_request.get()


def set_current_request(request):
    current_request.set(request)
