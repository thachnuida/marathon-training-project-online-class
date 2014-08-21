# -*- coding: utf-8 -*- 
from django import forms
from django.utils.safestring import mark_safe
from django.forms import ModelForm, CharField, TextInput


class CreateClass(forms.Form):
    class_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size': '28','title':'Max length 100', 'placeholder': 'Ex: Java,...'}))
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'size': '28','title':'Only Number', 'placeholder': 'Ex: 50,...'}))
    image_class = forms.ImageField(required=False)
    description = forms.CharField(max_length=300, widget=forms.Textarea(attrs={'cols' : "62", 'rows': "5"}))

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
    lesson_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size': '30','title':'Max length 100', 'placeholder': 'Ex: Swing,...'}))
    video_link = forms.CharField(widget=forms.TextInput(attrs={'size': '30','title':'Video Link', 'placeholder': 'Ex: //www.youtube.com/embed/H1Tsjn40mg0'}))
    description = forms.CharField(max_length=300,widget=forms.Textarea(attrs={'cols' : "62", 'rows': "5"}))

    def __init__(self, *args, **kwargs):
        chosen_lesson = kwargs.pop('chosen_lesson', None)
        super(CreateLesson, self).__init__(*args, **kwargs)
        if chosen_lesson:
            self.fields['lesson_name'].initial = chosen_lesson['lesson_name']
            self.fields['description'].initial = chosen_lesson['description']
            self.fields['video_link'].initial = chosen_lesson['video_link']

class CreateTest(forms.Form):
    test_name = forms.CharField(max_length=100, label="Exercise Name", widget=forms.TextInput(attrs={'title':'Max length 100', 'placeholder': 'Ex: Swing Exercise,...'}))

class CreateQuestion(forms.Form):
    CHOICES=[('A','A'), ('B','B'), ('C','C'), ('D','D')]
    question = forms.CharField(max_length=255,label="",widget=forms.Textarea(attrs={'cols' : "40", 'rows': "3", 'title':'Max length 255'}))
    answerA = forms.CharField(max_length=255, label="A. ", widget=forms.Textarea(attrs={'cols' : "37", 'rows': "2", 'title':'Max length 255'}))
    answerB = forms.CharField(max_length=255, label="B. ", widget=forms.Textarea(attrs={'cols' : "37", 'rows': "2", 'title':'Max length 255'}))
    answerC = forms.CharField(max_length=255, label="C. ", widget=forms.Textarea(attrs={'cols' : "37", 'rows': "2", 'title':'Max length 255'}))
    answerD = forms.CharField(max_length=255, label="D. ",  widget=forms.Textarea(attrs={'cols' : "37", 'rows': "2", 'title':'Max length 255'}))
    image_ques =  forms.ImageField(required=False, label="Question Image")
    right_answer = forms.ChoiceField( choices=CHOICES, widget=forms.RadioSelect())