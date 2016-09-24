from django import forms
from .models import Product

AVAILABILITY_CHOICES = ((True, 'Yes'), (False, 'No'))  # tuple for all choice options


# Here is a creating all the fields in the form manually
class ProductAddForm(forms.Form):
    title = forms.CharField(label='Product Title')
    description = forms.CharField(label='',
                                  widget=forms.Textarea(
                                      attrs={                              # empty label to not show any description
                                        'class': 'my-custom-class',
                                        'placeholder': 'Description ...',  # passing HTML attributes as a dictionary
                                        'cols': '30',
                                        'rows': '5',
                                        'some-attribute': 'some-value',  # can pass anything you want!
                                        }
                                  ))

    price = forms.DecimalField()
    # available = forms.ChoiceField(choices=AVAILABILITY_CHOICES)  # default option is drop-down menu
    is_available = forms.ChoiceField(label='Is available for sale',
                                     widget=forms.RadioSelect,
                                     choices=AVAILABILITY_CHOICES,
                                     initial=True)  # initial is the default value!


    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 1:
            raise forms.ValidationError('Price must be higher than $1')
        elif price >= 100:
            raise forms.ValidationError('Price must be less than $100')
        else:
            return price

    # this function HAS to be called clean_(valid attribute name) or it doesnt apply!
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError('Title must be 5 characters or longer')
        else:
            return title


# Now we will create a from from a model!
class ProductModelForm(forms.ModelForm):

    # We can also define fields/widgets manually here -> helps keep the code style consistent with the 'manual' form
    is_available = forms.ChoiceField(label='Is available for sale', widget=forms.RadioSelect,
                                     choices=AVAILABILITY_CHOICES, initial=True)

    description = forms.CharField(label='', widget=forms.Textarea(
                                          attrs={
                                              'placeholder': 'Description ...',
                                              'cols': '30',
                                              'rows': '5',
                                          }))

    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'price',
            'sale_price',
            'is_available'
        ]

        # Or widgets can be defined here, however cant pass all the params as easily here
        widgets = {
            'title': forms.TextInput(
                  attrs={'placeholder': 'Product Title'}
            ),
            'price': forms.TextInput(
                attrs={'placeholder': 'Price'}
            ),
        }

    # The same validation methods work here!
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 1:
            raise forms.ValidationError('Price must be higher than $1')
        elif price >= 100:
            raise forms.ValidationError('Price must be less than $100')
        else:
            return price

    # this function HAS to be called clean_(valid attribute name) or it doesnt apply!
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError('Title must be 5 characters or longer')
        else:
            return title


