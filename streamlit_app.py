import streamlit as st
class Product:
    def __init__(self, product_id, name, category, price, stock):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock

    def reduce_stock(self, qty):
        if qty <= self.stock:
            self.stock -= qty
            return True
        return False

    def increase_stock(self, qty):
        self.stock += qty

class CartItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def total_price(self):
        return self.product.price * self.quantity

class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, product, quantity):
        # Check if product already in cart
        for item in self.items:
            if item.product.product_id == product.product_id:
                item.quantity += quantity
                return
        # else add new item
        self.items.append(CartItem(product, quantity))

    def remove_item(self, product_id):
        self.items = [item for item in self.items if item.product.product_id != product_id]

    def update_quantity(self, product_id, new_qty):
        for item in self.items:
            if item.product.product_id == product_id:
                if new_qty <= 0:
                    self.remove_item(product_id)
                else:
                    item.quantity = new_qty
                return

    def total_cost(self):
        return sum(item.total_price() for item in self.items)

    def clear(self):
        self.items = []

class Store:
    def __init__(self):
        self.products = {}
        self.load_sample_products()

    def load_sample_products(self):
        # Sample products - you can add more
        sample_products = [
            Product(1, "Smartphone", "Mobile", 699.99, 10),
            Product(2, "Laptop", "Computers", 999.99, 5),
            Product(3, "Wireless Headphones", "Audio", 199.99, 15),
            Product(4, "Smartwatch", "Wearables", 249.99, 8),
            Product(5, "Bluetooth Speaker", "Audio", 129.99, 12),
            Product(6, "Gaming Mouse", "Accessories", 49.99, 20),
        ]
        for p in sample_products:
            self.products[p.product_id] = p

    def get_product(self, product_id):
        return self.products.get(product_id, None)

    def list_products(self):
        return list(self.products.values())

# --- Streamlit App UI & Logic ---

def main():
    st.title("🛒 Online Electronics Store")

    # Initialize store and cart in session state
    if "store" not in st.session_state:
        st.session_state.store = Store()
    if "cart" not in st.session_state:
        st.session_state.cart = Cart()

    menu = st.sidebar.selectbox("Menu", ["Browse Products", "View Cart", "Checkout"])

    if menu == "Browse Products":
        browse_products(st.session_state.store, st.session_state.cart)
    elif menu == "View Cart":
        view_cart(st.session_state.cart)
    elif menu == "Checkout":
        checkout(st.session_state.cart)

def browse_products(store, cart):
    st.header("Browse Products")

    products = store.list_products()

    for product in products:
        st.subheader(f"{product.name} (Category: {product.category})")
        st.write(f"Price: ${product.price:.2f} | Stock: {product.stock}")

        qty = st.number_input(f"Quantity for {product.name}", min_value=0, max_value=product.stock, value=0, key=f"qty_{product.product_id}")

        if st.button(f"Add to Cart - {product.name}", key=f"add_{product.product_id}"):
            if qty > 0:
                if product.stock >= qty:
                    cart.add_item(product, qty)
                    product.reduce_stock(qty)
                    st.success(f"Added {qty} x {product.name} to cart.")
                else:
                    st.error("Not enough stock available.")
            else:
                st.warning("Please select a quantity greater than zero.")

def view_cart(cart):
    st.header("Your Cart")

    if not cart.items:
        st.info("Your cart is empty.")
        return

    for item in cart.items:
        col1, col2, col3, col4 = st.columns([4, 2, 2, 2])
        with col1:
            st.write(f"**{item.product.name}**")
        with col2:
            new_qty = st.number_input(f"Quantity for {item.product.name}", min_value=0, max_value=item.product.stock + item.quantity, value=item.quantity, key=f"cart_qty_{item.product.product_id}")
        with col3:
            st.write(f"${item.total_price():.2f}")
        with col4:
            if st.button(f"Remove {item.product.name}", key=f"remove_{item.product.product_id}"):
                # Return stock back before removing
                item.product.increase_stock(item.quantity)
                cart.remove_item(item.product.product_id)
                st.experimental_rerun()

        if new_qty != item.quantity:
            if new_qty > item.quantity:
                diff = new_qty - item.quantity
                if item.product.stock >= diff:
                    item.product.reduce_stock(diff)
                    cart.update_quantity(item.product.product_id, new_qty)
                else:
                    st.error("Not enough stock to increase quantity.")
            else:
                diff = item.quantity - new_qty
                item.product.increase_stock(diff)
                cart.update_quantity(item.product.product_id, new_qty)
            st.experimental_rerun()

    st.write(f"### Total: ${cart.total_cost():.2f}")

    if st.button("Clear Cart"):
        # Restore all stock
        for item in cart.items:
            item.product.increase_stock(item.quantity)
        cart.clear()
        st.experimental_rerun()

def checkout(cart):
    st.header("Checkout")

    if not cart.items:
        st.info("Your cart is empty, add products before checkout.")
        return

    st.write(f"Your total is: **${cart.total_cost():.2f}**")

    with st.form("checkout_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        address = st.text_area("Shipping Address")
        submit = st.form_submit_button("Place Order")

    if submit:
        if not name.strip():
            st.error("Name cannot be empty.")
            return
        if "@" not in email or not email.strip():
            st.error("Please enter a valid email.")
            return
        if not address.strip():
            st.error("Address cannot be empty.")
            return

        # Here we "process" the order
        st.success(f"Thank you {name}! Your order has been placed successfully.")
        cart.clear()
        # Optionally reset stock - for demo, not doing here
        st.balloons()

if __name__ == "__main__":
    main()
