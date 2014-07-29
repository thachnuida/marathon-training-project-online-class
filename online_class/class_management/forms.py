from django import forms
from django.utils.safestring import mark_safe


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

class CreateTest(forms.Form):
    test_name = forms.CharField(max_length=100)

class CreateQuestion(forms.Form):
    CHOICES=[('A','A'), ('B','B'), ('C','C'), ('D','D')]
    question = forms.CharField(max_length=255, label=mark_safe('Nhap cau hoi<br/>'),widget=forms.Textarea(attrs={'cols' : "50", 'rows': "5", }))
    answerA = forms.CharField(max_length=255, label=mark_safe('<br/> Nhap cac lua chon <br/><br/>A. '), widget=forms.Textarea(attrs={'cols' : "47", 'rows': "2", }))
    answerB = forms.CharField(max_length=255, label="B. ", widget=forms.Textarea(attrs={'cols' : "47", 'rows': "2", }))
    answerC = forms.CharField(max_length=255, label="C. ", widget=forms.Textarea(attrs={'cols' : "47", 'rows': "2", }))
    answerD = forms.CharField(max_length=255, label="D. ",  widget=forms.Textarea(attrs={'cols' : "47", 'rows': "2", }))
    image_ques =  forms.ImageField(required=False)
    right_answer = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())