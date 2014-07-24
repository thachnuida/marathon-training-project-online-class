from django import forms


class CreateClass(forms.Form):
    class_name = forms.CharField(max_length=100)
    quantity = forms.ChoiceField(choices=[(x, x) for x in range(30, 101)])
    image_class = forms.ImageField(required=False)
    description = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        class_details = kwargs.pop('class_details', None)
        super(CreateClass, self).__init__(*args, **kwargs)
        if class_details:
            self.fields['class_name'].initial = class_details['class_name']
            self.fields['quantity'].initial = class_details['quantity']
            self.fields['description'].initial = class_details['description']
