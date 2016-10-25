from  django.http import Http404


# Defining custom decorator
def ajax_required(function):

    """
    This is a doc string that is used by the .__doc__ method
    """

    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

