from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

# Mixins are custom classes that can be added to other classes to enhance functionality!!


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    # dispatch ids the method used to send data
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class StaffRequiredMixin(object):
    @method_decorator(staff_member_required)
    # dispatch ids the method used to send data
    def dispatch(self, request, *args, **kwargs):
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)


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


# This mixin class customises get_context_data() in order to pass variables to the HTML form
class FormVarsMixin(object):

    form_title = None
    submit_btn = None
    reset_btn = None

    def get_context_data(self, **kwargs):
        context = super(FormVarsMixin, self).get_context_data()
        # Here are the form variables
        context['form_title'] = self.form_title
        context['submit_btn'] = self.submit_btn
        context['reset_btn'] = self.reset_btn
        return context

