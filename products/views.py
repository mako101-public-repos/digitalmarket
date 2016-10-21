from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, FileResponse
from mimetypes import guess_type

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView

from products.models import Product
from products.forms import ProductAddForm, ProductModelForm
from tags.models import Tag
from analytics.models import TagView

from digitalmarket.mixins import *
from .mixins import *


################################### helper functions ###############################################
def process_tags(tags, item):
    # we read the tags field, and split it on commas
    tags_list = tags.split(',')
    # these are bad tags we don't want to use
    exceptions = ['', ' ']
    for tag in tags_list:
        if tag not in exceptions:
            # we then make sure each tag is added or already is in db
            # [0] is the tag itself as .get_or_create returns a tuple
            new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
            # and we add the product that is being edited to the tag :)
            new_tag.products.add(item)


########################################## Class-Based Views :-) #########################################
class ProductCreateView(LoginRequiredMixin, FormVarsMixin, CreateView):
    model = Product
    form_class = ProductModelForm
    template_name = 'product_form.html'
    # success_url = '/products'  # url to redirect to on successful submission

    # these come from FormVarsMixin
    form_title = 'New Product Form'
    submit_btn = 'Create Product'
    reset_btn = 'Clear form'

    def form_valid(self, form):
        user = self.request.user
        form.instance.owner = user
        valid_data = super(ProductCreateView, self).form_valid(form)  # form_valid() saves the instance
        # By this point the product has already been saved to the DB
        # so we can add ManyToMany values, e.g add user to managers
        form.instance.managers.add(user)
        tags = form.cleaned_data.get('tags')
        if tags:
            process_tags(tags, form.instance)
        return valid_data

    # We only need to specify this if get_absolute_url() is not defined OR we want to overwrite it
    def get_success_url(self):
        return reverse('products:list')


class ProductEditView(ProductManagerEditMixin, FormVarsMixin, MultiSlugMixin, UpdateView):
    model = Product
    form_class = ProductModelForm
    template_name = 'product_form.html'
    # success_url = '/products'  # url to redirect to on successful submission
    form_title = 'Update Product'
    submit_btn = 'Save Changes'

    # this is for handling tags
    def get_initial(self):
        initial = super(ProductEditView, self).get_initial()
        print(initial)
        tags = self.get_object().tag_set.all()
        # we grab the already assigned tags and construct a comma-separated string from them
        # (we later break this list down into constituent tags when saving the changes ;))
        initial['tags'] = ', '.join([tag.title for tag in tags])
        return initial

    def form_valid(self, form):
        valid_data = super(ProductEditView, self).form_valid(form)
        tags = form.cleaned_data.get('tags')
        obj = self.get_object()
        # We remove all associated tags and add the set that is currently in the form(below)
        obj.tag_set.clear()
        if tags:
            process_tags(tags, obj)

        return valid_data

    # The rest is handled by ProductManagerEditMixin


class ProductDetailView(ProductManagerDetailMixin, MultiSlugMixin, DetailView):
    model = Product
    # using product_detail.html template
    # Everything else managed by ProductManagerDetailMixin

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['coming_soon'] = Product.objects.get(slug='coming-soon')
        obj = self.get_object()
        tags = obj.tag_set.all()
        if tags and self.request.user.is_authenticated():
            for tag in tags:
                tag_analytics_object = TagView.objects.add_count(self.request.user, tag)
        return context


class ProductDownloadView(ProductManagerDetailMixin, MultiSlugMixin, DetailView):
    model = Product

    def get(self, request, *args, **kwargs):
        obj = self.get_object()

        # https://docs.djangoproject.com/en/1.10/ref/request-response/#fileresponse-objects
        # https://docs.python.org/3/library/functions.html#open
        # NONE OF THIS WORKS OFF S3, FOR LOCAL FILES ONLY!!!
        # file_path = str(settings.MEDIA_URL + obj.media.name)
        # print(file_path)
        # wrapper is for handling large files efficiently, i.e without tying up lots of memory
        # file_wrapper = FileResponse(open(file_path, 'rb'))

        # Only allow users with the right permissions to download stuff
        if obj in request.user.myproducts.products.all():

            # Try to guess the MIME type of the download or just force download if unknown
            guessed_type = guess_type(obj.media.name)
            mimetype = 'application/force-download'
            if guessed_type:
                mimetype = guessed_type
            response = HttpResponse(obj.media, content_type=mimetype)

            # if the request contains 'preview', don't download the file, attempt preview
            # The product details page will have a separate link for this
            if 'preview' not in request.GET:
                response['Content-Disposition'] = 'attachment; filename={}'.format(obj.media.name)

            response['X-SendFile'] = str(obj.media.name)

            print(response)
            return response
        else:
            return HttpResponse('You are not authorized to access this download', status=403)


class ProductListView(SimpleSearchMixin, ListView):
    model = Product

    # We will set things up to work with the default auto-generated template name:
    # product_list.html
    # template_name = 'list_view.html' - not needed anymore

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data()
        print(context)
        context['coming_soon'] = Product.objects.get(slug='coming-soon')
        # context['queryset'] = self.get_queryset()
        return context


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


##