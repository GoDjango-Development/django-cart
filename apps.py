from django.apps import AppConfig
# Related to apps classes
from .utils.wrapper import Wrapper
from .utils.utils import MappedDict
from django.conf import settings

# App Config 
class CartConfig(AppConfig):
    name = 'django_cart'
    verbose_name = "Shop"


# Function for merging two dicts | is not used for backward compatibility
def merge(dict1:dict, dict2:dict):
        for i in dict2.keys():
            dict1[i] = dict2[i]
        return dict1

# Single cart class for handling single class carts
class SingleCart():
    def __init__(self, request):
        self.request = request
        self.cart = MappedDict(self.request.session.get(settings.CART_SESSION_ID, {}))

    def all(self, ):
        print(self.request.session)
        return self.cart.values()

    def decrease_from(self, product_id, product, quantity=1):
        quantity, product_id = int(quantity), str(product_id)
        assert quantity > 0, "Please use a positive value"
        if self.cart.keys().__contains__(str(product_id)):
            merge(self.cart[product_id], Wrapper(product))
            self.cart[product_id]["quantity"] =  self.cart[product_id]["quantity"] - quantity
            if self.cart[product_id]["quantity"] == 0:
                del self.cart[product_id]
            self.save()
        return self

    def clear_product(self, product_id):
        product_id = str(product_id)
        if self.cart.keys().__contains__(product_id):
            del self.cart[product_id]
        self.save()
        return self

    def clear(self,):
        self.cart = MappedDict()
        self.save()
        return self

    def get_product(self, product_id, default=None):
        product_id = str(product_id)
        return self.cart.get(product_id, default)

    def get(self, ):
        return self.request.session[settings.CART_SESSION_ID]

    def __str__(self, ):
        return str(self.request.session[settings.CART_SESSION_ID])

    def find(self, product_id):
        product_id = str(product_id)
        def lookup(target):
            for p_id in target.keys():
                if p_id == product_id:
                    return target[p_id]
            return None
        return lookup(self.cart)

    def find_by(self, key, value):
        def lookup(target):
            for p_id in target.keys():
                if target[p_id].keys().__contains__(key) and target[p_id][key] == value:
                    return target[p_id]
        return lookup(self.cart)

    def add(self, product, quantity = 1, custom_product_id=None):
        quantity, custom_product_id = int(quantity), (None if custom_product_id is None else str(custom_product_id))
        last_index = str(custom_product_id or int(self.cart.get_last_key() or -1) + 1)
        self.cart[last_index] = Wrapper(product)
        self.cart[last_index]["quantity"] = quantity
        self.save()
        return self

    def add_to(self, product_id, product, quantity=1):
        quantity, product_id = int(quantity), str(product_id)
        assert quantity > 0, "Please ensure that you are using a quantity higher than 0" 
        if not self.cart.keys().__contains__(str(product_id)):
            return self.add(product, quantity, custom_product_id=product_id)
        
        if self.cart.get(product_id, None) is not None:
            self.cart[product_id]["quantity"] += quantity
            self.save()
            return self

        merge(self.cart[product_id], Wrapper(product))
        self.cart[product_id]["quantity"] =  self.cart[product_id]["quantity"] + quantity
        self.save()
        return self

    def save(self):
        print("saving: ", self.cart)
        self.request.session[settings.CART_SESSION_ID] = self.cart

# Multi cart class for handling multi class carts
class MultiCart():
    def __init__(self, request):
        self.request = request
        self.cart = MappedDict(self.request.session.get(settings.CART_SESSION_ID, {}))

    def all(self, ):
        return self.cart.values()

    def add(self, cart_id, product, quantity = 1, custom_product_id=None):
        quantity, cart_id, custom_product_id = int(quantity), str(cart_id), (None if custom_product_id is None else str(custom_product_id))
        if self.cart.get(cart_id, None) is None:
            self.cart[cart_id] = MappedDict()
        assert hasattr(product, "id") or custom_product_id is not None
        index = str(custom_product_id if custom_product_id is not None else product.id)
        if self.cart.get(cart_id, {}).get(index, None) is not None:
            merge(self.cart[cart_id][index], Wrapper(product))
            self.cart[cart_id][index]["quantity"] += quantity
            self.save()
            return self
        self.cart[cart_id][index] = Wrapper(product)
        self.cart[cart_id][index]["quantity"] = quantity
        self.save()
        return self

    def add_to(self, cart_id, product_id, product, quantity=1):
        quantity, cart_id, product_id = int(quantity), str(cart_id), str(product_id)
        assert quantity > 0, "Please ensure that you are using a quantity higher than 0"
        if not self.cart.keys().__contains__(str(cart_id)) or not self.cart[cart_id].keys().__contains__(str(product_id)):
            #print("Error it may be: %s"%product_id)
            return self.add(cart_id=cart_id, product=product, quantity=quantity, custom_product_id=product_id)
        merge(self.cart[cart_id][product_id], Wrapper(product))
        self.cart[cart_id][product_id]["quantity"] =  self.cart[cart_id][product_id]["quantity"] + quantity
        self.save()
        return self

    def decrease_from(self, cart_id, product_id, product, quantity=1):
        quantity, cart_id, product_id = int(quantity), str(cart_id), str(product_id)
        assert quantity > 0, "Please use a positive value or instead use add_to"
        if self.cart.keys().__contains__(cart_id) and self.cart[cart_id].keys().__contains__(str(product_id)):
            merge(self.cart[cart_id][product_id], Wrapper(product))
            self.cart[cart_id][product_id]["quantity"] =  self.cart[cart_id][product_id]["quantity"] - quantity
            if self.cart[cart_id][product_id]["quantity"] == 0:
                del self.cart[cart_id][product_id]
            self.save()
        return self

    def clear_product(self, cart_id, product_id):
        cart_id, product_id = str(cart_id), str(product_id)
        assert self.cart.keys().__contains__(cart_id), "Cart doesnt exists"
        if self.cart[cart_id].keys().__contains__(product_id):
            del self.cart[cart_id][product_id]
        self.save()
        return self
    
    def clear_cart(self, cart_id):
        cart_id= str(cart_id)
        if self.cart.keys().__contains__(cart_id):
            del self.cart[cart_id]
        self.save()
        return self

    def clear(self,):
        self.cart = MappedDict({})
        self.save()
        return self

    def get_cart(self, cart_id):
        cart_id = str(cart_id)
        return self.cart.get(cart_id, None)

    def get_product(self, cart_id, product_id, default=None):
        product_id = str(product_id)
        return self.cart.get(cart_id, {}).get(product_id, default)

    def get(self, ):
        return self.cart

    def __str__(self, ):
        return str(self.request.session[settings.CART_SESSION_ID])

    def find(self, product_id):
        product_id = str(product_id)
        def lookup(target):
            for p_id in target.keys():
                if p_id == product_id:
                    return target[p_id]
        for cart_id in self.cart.keys():
            res = lookup(self.cart[cart_id])
            if res:
                return res
        return None

    def find_by(self, key, value):
        def lookup(target):
            for p_id in target.keys():
                if target[p_id].keys().__contains__(key) and target[p_id][key] == value:
                    return target[p_id]
        for cart_id in self.cart.keys():
            res = lookup(self.cart[cart_id])
            if res:
                return res
        return None

    def save(self, ):
        # upload changes to the session...
        self.request.session[settings.CART_SESSION_ID] = self.cart
        #self.request.session.modified = True
