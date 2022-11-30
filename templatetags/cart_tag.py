from hashlib import md5
from django_cart.apps import SingleCart, MultiCart
from django_cart.utils.utils import MappedDict
from django import template
register = template.Library()

@register.filter()
def cart_proxy(cart: SingleCart | MultiCart, func_name, *args):
    if len(args) > 0:
        return cart.__getattribute__(func_name).__call__(args)
    return cart.__getattribute__(func_name).__call__()

@register.filter()
def multiply(value, arg):
    return float(value) * float(arg)

@register.filter()
def get_sum_of(cart, key):
    return sum(map(lambda x: float(x[key]), cart.all()))

@register.filter()
def paginate(array: list, amount: int):
    return range(0, len(array), amount)

@register.filter()
def week_to_str(isoweek: int):
    if isoweek == 0:
        return "Mon"
    elif isoweek == 1:
        return "Tue"
    elif isoweek == 2:
        return "Wed"
    elif isoweek == 3:
        return "Thu"
    elif isoweek == 4:
        return "Fri"
    elif isoweek == 5:
        return "Sat"
    elif isoweek == 6:
        return "Sun"

@register.filter
def str_md5(value:str):
    return md5(value.encode()).hexdigest()

@register.filter()
def get_values(data: dict, key: str):
    return data[str(key)]

@register.filter()
def firsts(array: list, amount: int):
    return array[:amount]

@register.filter()
def lasts(array: list, amount: int):
    return array[-amount:]

@register.filter()
def model(data: dict):
    return data[data.keys().first()]

@register.filter()
def from_model(data: dict, attr: str):
    return data.get(str(attr), None)

@register.simple_tag()
def total(data: dict, *args):
    data = MappedDict(data)
    if len(args) == 0:
        args = ("quantity", "price")
    total = data.get_total_prod_of(*args)
    return total
