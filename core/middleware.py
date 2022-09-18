

# from urllib import response
from concurrent.futures import process
from django.shortcuts import redirect
from analysis.models import ViewRequest, Request, CountryRequest
from django.db.models import F
class LoggingMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response
        self.invalid_view_list = ('manifest', 'service_worker', 'add_view', 'i18n_javascript',
        'changelist_view', 'change_view','serve')

    def __call__(self, request):
        # if request.META['PATH_INFO'] == '/':
            # return redirect('quiz:quizzes')
        response = self.get_response(request)
        # return self.process_request(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        view_name = view_func.__name__
        if view_name not in self.invalid_view_list:
        # if (view_name != 'manifest' and view_name != 'service_worker'):
            # print(f"view name: {view_func.__name__} being accessed by {request.user}")
            Request.objects.update(requests=F('requests')+1)
            try:
                view_request = ViewRequest.objects.get(name=view_name)
                view_request.requests+=1
                view_request.save()
                # return
            except:
                ViewRequest.objects.create(name=view_name, requests=1)
                pass
            country = None
            try:
                country = request.META['HTTP_CF_IPCOUNTRY']
                print(country)
            except:
                pass
            if country is not None:
                try:
                    view_request = CountryRequest.objects.get(name=country)
                    view_request.requests+=1
                    view_request.save()
                    # return
                except:
                    CountryRequest.objects.create(name=country, requests=1)
                    pass

            # print(self.request_count)
        return


    # def process_request(self, request):
    #     response = self.get_response(request)
    #     print('This is the new request!')
    #     return response

    def process_exception(self, request, exception):
        pass

    # def process_template_response(self, request, response):
    #     print('This is a template response!')
    #     response.context_data['template_data'] = 'this is the message gotten from the middleware'
    #     return response

    # def process_response(self, request, response):
    #     print(f"being accessed by {request.user}")

    #     print(response)
    #     return response



# class StaticMiddleware:
#     def __init__(self, get_response) -> None:
#         self.get_response = get_response
#         self.request_count = 0

#     def __call__(self, request):
#         print('This is a request!')
#         response = self.get_response(request)
#         return self.process_template_response(request, response)
#         return response

#     # def process_request(self, resquest):
#     #     pass

#     def process_view(self, request, view_func, view_args, view_kwargs):
#         if (view_func.__name__ != 'manifest' and view_func.__name__ != 'service_worker'):
#             print(f"view name: {view_func.__name__} being accessed by {request.user}")
#             self.request_count += 1
#             print(self.request_count)
        
#             pass

#     def process_exception(self, request, exception):
#         pass

#     def process_template_response(self, request, response):
#         print('This is a template response!')
#         # response.context_data["static_request"] = '123456678'
#         return response


#     def process_response(self, request, response):
#         print(f"being accessed by {request.user}")
#         # return self.process_template_response(request, response)
#         # print(response)
#         return response
