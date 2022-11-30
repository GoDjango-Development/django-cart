from django.test import TestCase
from django.urls import reverse
from .apps import SingleCart, MultiCart
from clients.models import Product
from security.models import User
from .utils.utils import MappedDict

class CartTest(TestCase):
    def setUp(self):
        User.objects.get_or_create(username="user", password="pass", business_name="business_name")
        Product.objects.get_or_create(id=1)

    def test_single_add(self,):
        response = self.client.post(reverse("cart_single_add", kwargs={"id": 1}))
        self.assertEqual(response.json()["total"], 1) # Testing amount is correct 
        self.assertTrue(response.json().get("cart").get(str(1), None) is not None) # Testing product does exists in cart
        response = self.client.post(reverse("cart_single_add", kwargs={"id": 1}), 
            {
                "quantity": 1000
            }
        )
        self.assertLess(response.json()["total"], 1001) # Testing it does overwrite previous value 'cause this method is intend it to do so

    def test_multi_add(self, ):
        response = self.client.post(reverse("cart_multi_add", kwargs={"id": 1, "cart_id": 1}), data={
            "custom_product_id": 1
        })
        self.assertEqual(response.json()["total"], 1) # Testing amount is correct 
        self.assertTrue(response.json().get("cart").get(str(1), {}).get(str(1), False)) # Testing product does exists in cart
        response = self.client.post(reverse("cart_multi_add", kwargs={"id": 1, "cart_id": 1}), 
            {
                "custom_product_id": 1,
                "quantity": 1000
            }
        )
        self.assertLess(response.json()["total"], 1001) # Testing it does overwrite previous value 'cause this method is intend it to do so
    
    def test_single_clear(self, ):
        response = self.client.post(reverse("cart_single_clear"))
        self.assertTrue(len(response.json()["cart"].keys()) == 0)
    
    def test_multi_clear(self, ):
        response = self.client.post(reverse("cart_multi_clear"))
        self.assertTrue(len(response.json()["cart"].keys()) == 0)
    
    def test_single_add_to(self, ):
        response = self.client.post(reverse("cart_single_add_to", kwargs={"id": 1}))
        self.assertTrue(response.json().get("cart", {}).get(str(1), False), "The recently added element it does not exists \n Elements are: %s"%response.json()) # Testing the element it does exists in cart
        self.assertEqual(response.json()["total"], 1 ) # Testing total is equal to 2 because it most be right now :)
        

    def test_multi_add_to(self, ):
        response = self.client.post(reverse("cart_multi_add_to", kwargs={"id": 1, "cart_id": 3}), {
            "quantity": 2,
        })
        data = response.json()
        self.assertTrue(data.get("cart", {}).get(str(3), {}).get(str(1), False), "This recently added element it does not exists \n Elements are: %s"%(data)) # Testing the element it does exists in cart
        self.assertEqual(data["total"], 2) # Testing total is equal to 2 because it most be right now :)


    def test_single_sub_to(self, ):
        response = self.client.post(reverse("cart_single_sub_to", kwargs={"id": 1}), {
            "quantity": 2
        })
        

    def test_multi_sub_to(self, ):
        response = self.client.post(reverse("cart_multi_sub_to", kwargs={"id": 1, "cart_id": 1}), {
            "quantity": 2
        })
    
    def test_recursive_set(self, ):
        data = MappedDict()
        args = ("actions", "views", "product")
        data.rset(*args, value="Value")
        args = ("actions", "views", "site")
        print("result: ", data.rset(*args, value="Value"))
