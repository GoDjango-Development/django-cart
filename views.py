from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse
from .apps import SingleCart, MultiCart
from django_plugins import import_string, get_plugin
from .settings import PLUGIN_NAME
from .signals import *
Product = import_string(get_plugin(PLUGIN_NAME).get("product_model"))
# Create your views here.
@require_POST
def cart_single_add(request: HttpRequest, *args, **kwargs):
    product = Product.objects.get(id=kwargs.get("id", None))
    cart = SingleCart(request)
    try:
        will_add_item.send(cart_single_add, **{
            "cart": cart,
            "product": product, 
            "quantity": request.POST.get("quantity", 1)
        })
    except ValueError:
        return # Stop execution on error
    
    cart = cart.add(
        product=product,
        quantity=request.POST.get("quantity", 1),
        custom_product_id=getattr(product, "id", None))

    responses = item_added_to_cart.send(cart_single_add, **{
        "cart": cart,
        "product": product, 
        "quantity": request.POST.get("quantity", 1)
    })
    extra_context = {}
    for response in responses:
        response = response[1] or {}
        extra_context.update(response.get("extra_context", {}))
    return JsonResponse({
        "total": cart.cart.get_total_prod_of("quantity", request.POST.get("price_field", "price")),
        "cart": cart.car.get(str(kwargs.get("id", None))),
        "extra_context": extra_context
    })

@require_POST
def cart_multi_add(request: HttpRequest, *args, **kwargs):
    product = Product.objects.get(id=kwargs.get("id", None))
    quantity = request.POST.get("quantity", 1)
    custom_id = request.POST.get("custom_product_id", None)
    cart = MultiCart(request)
    try:
        will_add_item.send(cart_multi_add, **{
            "cart": cart,
            "product": product, 
            "quantity": quantity,
            "custom_id": custom_id
        })
    except ValueError:
        return #
    cart = cart.add(cart_id=kwargs.get("cart_id", 0), 
        product=product,
        quantity=quantity, 
        custom_product_id=custom_id)
    responses = item_added_to_cart.send(cart_multi_add, **{
        "cart": cart,
        "product": product, 
        "quantity": quantity,
        "custom_id": custom_id
    })
    extra_context = {}
    for response in responses:
        response = response[1] or {}
        extra_context.update(response.get("extra_context", {}))
    return JsonResponse({
        "total": cart.cart.get_total_prod_of("quantity", request.POST.get("price_field", "price")),
        "cart": cart.cart.get(str(kwargs.get("cart_id", 0))).get(str(kwargs.get("id", None))),
        "extra_context": extra_context
    })

@require_POST
def cart_single_clear(request: HttpRequest, *args, **kwargs):
    cart = SingleCart(request)
    try:
        will_clear_cart.send(cart_single_clear, **{
            "cart": cart,
        })
    except ValueError:
        return #
    cart = cart.clear()
    responses = cart_cleared.send(cart_single_clear, **{
        "cart": cart,
    })

    extra_context = {}
    for response in responses:
        response = response[1] or {}
        extra_context.update(response.get("extra_context", {}))

    return JsonResponse({
        "total": cart.cart.get_total_prod_of("quantity", request.POST.get("price_field", "price")),
        "cart": cart.cart,
        "extra_context": extra_context
    })

@require_POST
def cart_multi_clear(request: HttpRequest, *args, **kwargs):
    cart = MultiCart(request)
    try:
        will_clear_cart.send(cart_multi_clear, **{
            "cart": cart,
        })
    except ValueError:
        return #
    cart = cart.clear()
    responses = cart_cleared.send(cart_multi_clear, **{
        "cart": cart,
    })

    extra_context = {}
    for response in responses:
        response = response[1] or {}
        extra_context.update(response.get("extra_context", {}))

    return JsonResponse({
        "total": cart.cart.get_total_prod_of("quantity", request.POST.get("price_field", "price")),
        "cart": cart.cart,
        "extra_context": extra_context
    })

@require_POST
def cart_single_add_to(request: HttpRequest, *args, **kwargs):
    product = Product.objects.get(id=kwargs.get("id"))
    quantity = request.POST.get("quantity", 1)
    cart = SingleCart(request)
    try:
        will_add_item.send(cart_single_add_to, **{
            "cart": cart,
            "product": product, 
            "quantity": quantity,
        })
    except ValueError:
        return #
    cart = cart.add_to(product_id=product.id, 
        product=product,
        quantity=quantity)
    responses = item_added_to_cart.send(cart_single_add_to, **{
        "cart": cart,
        "product": product, 
        "quantity": quantity,
    })
    extra_context = {}
    for response in responses:
        response = response[1] or {}
        extra_context.update(response.get("extra_context", {}))

    return JsonResponse({
        "total": cart.cart.get_total_prod_of("quantity", request.POST.get("price_field", "price")),
        "cart": cart.cart.get(str(kwargs.get("id", None))),
        "extra_context": extra_context
    })

@require_POST
def cart_multi_add_to(request: HttpRequest, *args, **kwargs):
    product = Product.objects.get(id=kwargs.get("id"))
    quantity = request.POST.get("quantity", 1)
    cart_id = kwargs.get("cart_id", 0)
    cart = MultiCart(request)
    try:
        will_add_item.send(cart_multi_add_to, **{
            "cart": cart,
            "product": product,
            "cart_id": cart_id,
            "quantity": quantity,
        })
    except ValueError:
        return #
    cart = cart.add_to(cart_id=cart_id, 
        product_id=product.id, 
        product=product,
        quantity=quantity)
    responses = item_added_to_cart.send(cart_multi_add_to, **{
        "cart": cart,
        "product": product,
        "cart_id": cart_id,
        "quantity": quantity,
    })

    extra_context = {}
    for response in responses:
        response = response[1] or {}
        extra_context.update(response.get("extra_context", {}))
    
    return JsonResponse({
        "total": cart.cart.get_total_prod_of("quantity", request.POST.get("price_field", "price")),
        "cart": cart.cart.get(str(cart_id)).get(str(product.id)),
        "extra_context": extra_context
    })

@require_POST
def cart_single_sub_to(request: HttpRequest, *args, **kwargs):
    product = Product.objects.get(id=kwargs.get("id"))
    quantity = request.POST.get("quantity", 1)
    cart = SingleCart(request)
    try:
        will_remove_item.send(cart_single_sub_to, **{
            "cart": cart,
            "product": product, 
            "quantity": quantity,
        })
    except ValueError:
        return #
    cart = cart.decrease_from(product_id=kwargs.get("id"), 
        product=product,
        quantity=quantity)
    responses = item_removed_from_cart.send(cart_single_sub_to, **{
        "cart": cart,
        "product": product,
        "quantity": quantity,
    })

    extra_context = {}
    for response in responses:
        response = response[1] or {}
        extra_context.update(response.get("extra_context", {}))
    return JsonResponse({
        "total": cart.cart.get_total_prod_of("quantity", request.POST.get("price_field", "price")),
        "cart": cart.cart.get(str(product.id)),
        "extra_context": extra_context
    })

@require_POST
def cart_multi_sub_to(request: HttpRequest, *args, **kwargs):
    product = Product.objects.get(id=kwargs.get("id"))
    quantity = request.POST.get("quantity", 1)
    cart = MultiCart(request)
    try:
        will_remove_item.send(cart_multi_sub_to, **{
            "cart": cart,
            "product": product, 
            "quantity": quantity,
        })
    except ValueError:
        return #
    cart = cart.decrease_from(cart_id=kwargs.get("cart_id", 0), 
        product_id=product.id, 
        product=product,
        quantity=quantity
    )
    responses = item_removed_from_cart.send(cart_multi_sub_to, **{
        "cart": cart,
        "product": product,
        "quantity": quantity,
    })

    extra_context = {}
    for response in responses:
        response = response[1] or {}
        extra_context.update(response.get("extra_context", {}))

    return JsonResponse({
        "total": cart.cart.get_total_prod_of("quantity", request.POST.get("price_field", "price")),
        "cart": cart.cart.get(str(kwargs.get("cart_id", 0))).get(str(kwargs.get("id", None))),
        "extra_context": extra_context
    })

@require_POST
def cart_single_del(request: HttpRequest, *args, **kwargs):
    cart = SingleCart(request)
    try:
        will_drop_item.send(cart_single_del, **{
            "cart": cart,
            "product_id": kwargs.get('id'),
        })
    except ValueError:
        return #
    cart = cart.clear_product(product_id=kwargs.get("id"))
    responses = item_dropped_from_cart.send(cart_single_del, **{
        "cart": cart,
        "product_id": kwargs.get("id"),
    })

    extra_context = {}
    for response in responses:
        response = response[1] or {}
        extra_context.update(response.get("extra_context", {}))
    
    return JsonResponse({
        "total": cart.cart.get_total_prod_of("quantity", request.POST.get("price_field", "price")),
        "cart": cart.cart,
        "extra_context": extra_context
    })

@require_POST
def cart_multi_del(request: HttpRequest, *args, **kwargs):
    cart = MultiCart(request)
    try:
        will_drop_item.send(cart_multi_del, **{
            "cart": cart,
        })
    except ValueError:
        return #
    cart = cart.clear_product(cart_id=kwargs.get("cart_id", 0), 
        product_id=kwargs.get("id"))
    responses = item_dropped_from_cart.send(cart_single_del, **{
        "cart": cart,
        "cart_id": kwargs.get("cart_id", 0),
        "product_id": kwargs.get("id"),
    })

    extra_context = {}
    for response in responses:
        response = response[1] or {}
        extra_context.update(response.get("extra_context", {}))

    return JsonResponse({
        "total": cart.cart.get_total_prod_of("quantity", request.POST.get("price_field", "price")),
        "cart": cart.cart,
        "extra_context": extra_context
    })

@require_POST
def cart_single_view(request: HttpRequest, *args, **kwargs):
    return JsonResponse(SingleCart(request).cart)

@require_POST
def cart_multi_view(request: HttpRequest, *args, **kwargs):
    return JsonResponse(MultiCart(request).cart)
