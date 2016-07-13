from django import template
import datetime

register = template.Library()


@register.inclusion_tag('multiblog/footer.html')
def footer():
	return {'year':datetime.datetime.now().year}

@register.inclusion_tag('multiblog/header.html')
def header():
	return {}