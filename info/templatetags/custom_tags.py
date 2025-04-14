from django import template 
register = template.Library()

# Index for list in django template
@register.filter(name="index")
def get(indexable, i):
    return indexable[i]

# Set Variable in Django
@register.simple_tag
def setVar(val=None):
  return val

# For Division
@register.filter
def div( value, arg ):
    '''
    Divides the value; argument is the divisor.
    Returns empty string on any error.
    '''
    try:
        value = int( value )
        arg = int( arg )
        if arg: return value / arg
    except: pass
    return ''

# For Modulus
@register.filter
def modulus( value, arg ):
    '''
    Divides the value; argument is the remainder.
    Returns empty string on any error.
    '''
    try:
        value = int( value )
        arg = int( arg )
        if arg: return value % arg
    except: pass
    return ''