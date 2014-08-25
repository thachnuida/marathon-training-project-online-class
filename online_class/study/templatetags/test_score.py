from django import template
from study.models import *
from django.db.models import Max

from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
register = template.Library()

@register.simple_tag
def get_score(user, test):
    return Score.objects.filter(test=test, user=user).aggregate(Max('score'))['score__max']

@register.simple_tag
def get_latest_date(user, test):
	try:
	    test_date = Score.objects.filter(test=test, user=user).latest('test_date').test_date
	    df = DateFormat(test_date)
	    return str(df.format('H:i d/m/Y'))
	except:
		return "You Haven't Done"
@register.filter
def divide(value, arg):
	return "%.2f" % ((float)(value) / arg * 100)