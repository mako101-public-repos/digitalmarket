from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.views.generic import View


# Create your views here.
class CheckoutTestView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'checkout/test.html')
        # return HttpResponse('Hello, World!')

    def post(self, request, *args, **kwargs):
        request_data = request.POST.get('testData')
        token = request.POST.get('csrfmiddlewaretoken')
        print(request_data)
        print('The CSRF token is: {}'.format(token))
        if request.is_ajax():
            data = {
                'works': True,
                'time': datetime.now()
            }
            return JsonResponse(data)


        return HttpResponse(request_data)

