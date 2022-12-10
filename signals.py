from django.core.signals import Signal

# All registered receivers with below signal can return a dict containing an extra_context keyword. 
will_add_item = Signal()
will_remove_item = Signal()
will_drop_item = Signal()
will_clear_cart = Signal()
item_added_to_cart = Signal() # Call when item is added to cart
item_removed_from_cart = Signal() # Call when item is removed from the cart
cart_cleared = Signal() # Called when cart is cleared
item_dropped_from_cart = Signal() # Called when a whole group of the same item is dropped from cart