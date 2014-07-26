from django import forms


class CreateClass(forms.Form):
    class_name = forms.CharField(max_length=100)
    quantity = forms.ChoiceField(choices=[(x, x) for x in range(30, 101)])
    image_class = forms.ImageField(required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'cols' : "50", 'rows': "5", }))

    def __init__(self, *args, **kwargs):
        class_details = kwargs.pop('class_details', None)
        image_class = kwargs.pop('image_url', None) 
        super(CreateClass, self).__init__(*args, **kwargs)
        if class_details:
            self.fields['class_name'].initial = class_details['class_name']
            self.fields['quantity'].initial = class_details['quantity']
            self.fields['description'].initial = class_details['description']
        if image_class:
            self.fields['image_class'].initial = class_details['image_class']

class CreateLesson(forms.Form):
    lesson_name = forms.CharField(max_length=100)
    video_link = forms.URLField(label='Your Lesson Link')
    description = forms.CharField(widget=forms.Textarea(attrs={'cols' : "50", 'rows': "5", }))

    def __init__(self, *args, **kwargs):
        chose_lesson = kwargs.pop('chose_lesson', None)
        super(CreateLesson, self).__init__(*args, **kwargs)
        if chose_lesson:
            self.fields['lesson_name'].initial = chose_lesson['lesson_name']
            self.fields['description'].initial = chose_lesson['description']
            self.fields['video_link'].initial = chose_lesson['video_link']