from utils.current_request import set_current_request


def current_request_middleware(get_response):

    def middleware(request):
        set_current_request(request)
        response = get_response(request)
        return response

    return middleware
