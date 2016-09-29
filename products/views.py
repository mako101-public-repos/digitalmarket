from django.shortcuts import render
from django.http import Http404

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView

from .models import Product
from .forms import ProductAddForm, ProductModelForm
from digitalmarket.mixins import *


########################################## Class-Based Views :-) #########################################
class ProductCreateView(FormVarsMixin, CreateView):
    model = Product
    form_class = ProductModelForm
    template_name = 'product_form.html'
    success_url = '/products'  # url to redirect to on successful submission

    # these come from FormVarsMixin
    form_title = 'New Product Form'
    submit_btn = 'Create Product'
    reset_btn = 'Clear form'

    def form_valid(self, form):
        user = self.request.user
        form.instance.owner = user
        valid_data = super(ProductCreateView, self).form_valid(form)
        # By this point the product has already been saved to the DB
        # so we can add ManyToMany values, e.g add user to managers
        form.instance.managers.add(user)
        return valid_data

    # This customization has been moved to FormVarsMixin :)
    # need to customise this to pass form variables
    # def get_context_data(self, **kwargs):
    #     context = super(ProductCreateView, self).get_context_data()
    #     # Here are the form variables
    #     context['form_title'] = 'New Product Form'
    #     context['submit_btn'] = 'Create Product'
    #     context['reset_btn'] = 'Clear form'
    #     return context


class ProductEditView(FormVarsMixin, MultiSlugMixin, UpdateView):
    model = Product
    form_class = ProductModelForm
    template_name = 'product_form.html'
    success_url = '/products'  # url to redirect to on successful submission
    form_title = 'Update Product'
    submit_btn = 'Save Changes'

    def get_object(self, *args, **kwargs):
        user = self.request.user
        obj = super(ProductEditView, self).get_object(*args, **kwargs)
        if obj.owner == user or user in obj.managers.all():
            return obj
        else:
            raise Http404('You are not authorised to edit this product!')


class ProductDetailView(MultiSlugMixin, DetailView):
    model = Product
    # using product_detail.html template

    # can overwrite class methods here as needed
    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        user = self.request.user

        # Pass the variable to the template to show the edit button for owners and managers
        obj = super(ProductDetailView, self).get_object()
        if obj.owner == user or user in obj.managers.all():
            context['allowed_to_edit'] = True

        print('Using detail view!\n')
        print(context)
        return context
        # context['queryset'] = self.get_queryset()
        # return context


class ProductListView(ListView):
    model = Product

    # We will set things up to work with the default auto-generated template name:
    # product_list.html
    # template_name = 'list_view.html' - not needed anymore

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data()
        print(context)
        context['queryset'] = self.get_queryset()
        return context

    # narrow down the set of results returned
    def get_queryset(self):
        qs = super(ProductListView, self).get_queryset()
        qs = qs.filter(price__lte=9.99)
        return qs


############################# Function-based views ##################################################
def detail_view(request, object_id=None):
    # this will be visible in the console/logs!
    print("The request is {}.\nThe user is {}.\nAuthenticated: {}."
          .format(request, request.user, request.user.is_authenticated))

    # and we can use this right away!!
    if request.user.is_authenticated:
        greeting = 'Hello {}'.format(str(request.user).capitalize())
    else:
        greeting = 'I don\'t know you'

    product = get_object_or_404(Product, id=object_id)
    template = 'detail_view.html'
    context = {'greeting': greeting,
               'object': product,
               }
    return render(request, template, context)


def create_view(request):
    # None is so that we can load an empty page
    # and only raise validation errors when the data has been submitted

    # Here we create a instance of a product simply by saving the instance of the form
    form = ProductModelForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        instance = form.save(commit=False)    # grab an instance of the filled form, but don't save it yet
        if not instance.sale_price:
            instance.sale_price = instance.price  # can add stuff to the instance here!
        instance.save()
    template = 'create_view.html'
    form_title = 'New Product Form'
    submit_btn = 'Create Product'
    reset_btn = 'Clear form'
    context = {
        'form': form,
        'form_title': form_title,
        'submit_btn': submit_btn,
        'reset_btn': reset_btn
    }
    return render(request, template, context)


def update_view(request, object_id=None):
    product = get_object_or_404(Product, id=object_id)
    form = ProductModelForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
    template = 'update_view.html'
    context = {
               'form': form,
               }
    return render(request, template, context)

    # form = ProductAddForm(request.POST or None)
    # print(request.POST)
    # if form.is_valid():
    #     # turns request data from QueryDict to a dictionary and removes CSRF token
    #     # will only include valid fields!
    #     data = form.cleaned_data
    #     print(data)
    #     # now we extract values from the clean data and
    #     # and construct a new Product instance with them, then save it
    #     title = data.get('title')
    #     description = data.get('description')
    #     price = data.get('price')
    #     is_available = data.get('is_available')
    #     new_product = Product.objects.create(
    #         title=title, description=description, price=price, is_available=is_available
    #     )
    #  #  new_product.save()  # this is not needed, the new item is already saved


def detail_slug_view(request, slug=None):
    print('The slug is', slug)
    product = get_object_or_404(Product, slug=slug)
    # product = 1
    greeting = 'Hello!'
    template = 'detail_view.html'
    context = {'greeting': greeting,
                'object': product,
               }
    return render(request, template, context)


def list_view(request):
    queryset = Product.objects.all()
    template = 'list_view.html'
    context = {
        'queryset': queryset
    }
    return render(request, template, context)
