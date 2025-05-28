class Cart:
    def __init__(self):
        self.items = []

    def add_product(self, product):
        self.items.append(product)

    def get_total_price(self):
        return sum(product.price for product in self.items)

    def get_items(self):
        return self.items