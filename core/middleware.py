

from urllib import response


class LoggingMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response
        self.request_count = 0

    def __call__(self, request):
        print('This is a request!')
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if (view_func.__name__ != 'manifest' and view_func.__name__ != 'service_worker'):
            # print(f"view name: {view_func.__name__} being accessed by {request.user}")
            self.request_count += 1
            # print(self.request_count)
        
        pass

    def process_exception(self, request, exception):
        pass

    def process_template_response(self, request, response):
        # print('This is a template response!')
        response.context_data['template_data'] = 'this is the message gotten from the middleware'
        return response

    def process_response(self, request, response):
        # print(f"being accessed by {request.user}")

        # print(response)
        return response



