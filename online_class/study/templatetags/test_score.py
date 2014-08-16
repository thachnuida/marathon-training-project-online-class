from django import template
from study.models import *
from django.db.models import Max
register = template.Library()

@register.simple_tag
def get_score(user, test):
    return Score.objects.filter(test=test, user=user).aggregate(Max('score'))['score__max']

@register.filter
def divide(value, arg):
	return "%.2f" % ((float)(value) / arg * 100)