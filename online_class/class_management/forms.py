from django import forms


class CreateClass(forms.Form):
    class_name = forms.CharField(max_length=100)
    slug = forms.SlugField()
    # description = forms.TextArea(required=False)
    quantity = forms.IntegerField()
    image_class = forms.ImageField(required=False)
   