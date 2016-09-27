from django.shortcuts import get_object_or_404


# Mixins are custom classes that can be added to other classes to enhance functionality!!
class MultiSlugMixin(object):
    model = None

    # we will overwrite the get_object() method to be able to handle non-unique slugs
    def get_object(self):
        # this will print the keyword arguments the method is using to retrieve data
        print(self.kwargs)
        # This will equal to None if slug was not used, ie. a PK was used
        slug = self.kwargs.get('slug')
        ModelClass = self.model
        # if the slug is passed:
        if slug is not None:
            try:
                obj = get_object_or_404(ModelClass, slug=slug)
            except ModelClass.MultipleObjectsReturned:
                # Return the first match if multiples are found

                obj = ModelClass.objects.filter(slug=slug).order_by('title').first()
        # Default method for when querying with PK
        else:
            obj = super(MultiSlugMixin, self).get_object()
        return obj
