
import tkinter as tk
from tkinter import messagebox, simpledialog
from classes.ecommerce_platform import ECommercePlatform

class ECommerceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("E-Commerce App")
        self.root.geometry("400x400")

        self.platform = ECommercePlatform()
        self.logged_in_user = None

        self.create_login_register_screen()

    def create_login_register_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Username").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Register", command=self.register).pack(pady=5)
        tk.Button(self.root, text="Login", command=self.login).pack(pady=5)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "" or password == "":
            messagebox.showerror("Error", "Username and password cannot be empty")
            return
        if self.platform.register_user(username, password):
            messagebox.showinfo("Success", "Registered successfully! Please login.")
        else:
            messagebox.showerror("Error", "Username already exists.")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = self.platform.login_user(username, password)
        if user:
            self.logged_in_user = username
            messagebox.showinfo("Success", "Login successful!")
            self.create_main_screen()
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    def create_main_screen(self):
        self.clear_screen()

        tk.Label(self.root, text=f"Welcome, {self.logged_in_user}!").pack(pady=5)

        self.product_listbox = tk.Listbox(self.root, height=10)
        self.product_listbox.pack(pady=5)

        self.products = self.platform.get_products()
        for product in self.products:
            self.product_listbox.insert(tk.END, f"{product.id}: {product.name} - ${product.price}")

        tk.Button(self.root, text="Add to Cart", command=self.add_to_cart).pack(pady=5)
        tk.Button(self.root, text="View Cart", command=self.view_cart).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=5)

    def add_to_cart(self):
        try:
            selection = self.product_listbox.curselection()
            if not selection:
                messagebox.showerror("Error", "Please select a product to add.")
                return
            index = selection[0]
            product_id = self.products[index].id
            if self.platform.add_to_cart(self.logged_in_user, product_id):
                messagebox.showinfo("Success", "Product added to cart!")
            else:
                messagebox.showerror("Error", "Failed to add product.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def view_cart(self):
        items = self.platform.get_cart_items(self.logged_in_user)
        total = self.platform.get_cart_total(self.logged_in_user)
        if not items:
            messagebox.showinfo("Cart", "Your cart is empty.")
            return
        cart_str = "\n".join([f"{item.name} - ${item.price}" for item in items])
        cart_str += f"\n\nTotal Price: ${total:.2f}"
        messagebox.showinfo("Cart Summary", cart_str)

    def logout(self):
        self.logged_in_user = None
        self.create_login_register_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ECommerceGUI(root)
    root.mainloop()