from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.
def detail_view(request, object_id=None):
    # this will be visible in the console/logs!
    print("The request is {}.\nThe user is {}.\nAuthenticated: {}."
          .format(request, request.user, request.user.is_authenticated))

    # and we can use this right away!!
    if request.user.is_authenticated:
        greeting = 'Hello {}'.format(str(request.user).capitalize())
    else:
        greeting = 'I don\'t know you '

    product = get_object_or_404(Product, id=object_id)
    template = 'detail_view.html'
    context = {'greeting': greeting,
               'object': product,
               }
    return render(request, template, context)


def list_view(request):
    template = 'list_view.html'
    context = {}
    return render(request, template, context)
