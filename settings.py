PLUGIN_NAME = "DJANGO_CART"
INSTALLED_APPS = [
    ...,
    "django_cart"
]
INSTALLED_PLUGINS = {
    "DJANGO_CART": {
        "version": "1.0.0",
        "product_model": "dotted.path",
    }
}