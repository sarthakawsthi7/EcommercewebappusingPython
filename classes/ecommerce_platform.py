from classes.user import User
from classes.product import Product
from classes.cart import Cart

class ECommercePlatform:
    def __init__(self):
        self.users = {}
        self.products = []
        self.carts = {}

        self.products.append(Product(1, "Smartphone", 699.99))
        self.products.append(Product(2, "Laptop", 999.99))
        self.products.append(Product(3, "Headphones", 199.99))
        self.products.append(Product(4, "Smartwatch", 299.99))

    def register_user(self, username, password):
        if username in self.users:
            return False
        self.users[username] = User(username, password)
        self.carts[username] = Cart()
        return True

    def login_user(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
            return user
        return None

    def get_products(self):
        return self.products

    def add_to_cart(self, username, product_id):
        cart = self.carts.get(username)
        if not cart:
            return False
        product = next((p for p in self.products if p.id == product_id), None)
        if product:
            cart.add_product(product)
            return True
        return False

    def get_cart_items(self, username):
        cart = self.carts.get(username)
        if cart:
            return cart.get_items()
        return []

    def get_cart_total(self, username):
        cart = self.carts.get(username)
        if cart:
            return cart.get_total_price()
        return 0