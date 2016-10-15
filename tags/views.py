from django.shortcuts import render

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Tag


class TagDetailView(DetailView):
    model = Tag

    def get_context_data(self, **kwargs):
        context = super(TagDetailView, self).get_context_data(**kwargs)
        print(context)
        print(self.get_object().products.count)
        return context


class TagListView(ListView):
    model = Tag

    def get_queryset(self):
        return Tag.objects.filter(active=True).order_by('title')


