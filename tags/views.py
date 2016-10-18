from django.shortcuts import render

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Tag
from products.models import Product
from analytics.models import TagView


class TagDetailView(DetailView):
    model = Tag

    def get_context_data(self, **kwargs):
        context = super(TagDetailView, self).get_context_data(**kwargs)
        context['coming_soon'] = Product.objects.get(slug='coming-soon')

        if self.request.user.is_authenticated():

            # custom .add_count() method handles tag analytics
            tag_analytics_object = TagView.objects.add_count(self.request.user, self.get_object())

            # analytics_object = TagView.objects.get_or_create(
            #     user=self.request.user,
            #     tag=self.get_object())[0]
            # analytics_object.count += 1
            # analytics_object.save()

        return context



class TagListView(ListView):
    model = Tag

    def get_queryset(self):
        # return Tag.objects.filter(active=True).order_by('title')
        return Tag.active_tags.all()


