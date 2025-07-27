# orders.py
import streamlit as st
from datetime import datetime
from utils import Order as OrderManager

class OrderUI:
    def __init__(self, username):
        self.username = username
        self.cart = st.session_state.get("cart", [])
        self.total = 0
        self.address = st.session_state.get("address", "")

    def is_cart_empty(self):
        return not self.cart

    def show_empty_cart_message(self):
        st.info("🛍️ Your cart is empty. Cannot place an order.")
        if st.button("Go to Medicines", type="primary"):
            st.session_state["dashboard_menu_selected"] = 0
            st.session_state["current_page"] = "dashboard"
            st.rerun()

    def render_order_summary(self):
        st.subheader("🧾 Order Summary")
        self.total = sum(item["price"] * item["qty"] for item in self.cart)
        for item in self.cart:
            st.write(
                f"- {item['name']} (x{item['qty']} @ ₹{item['price']}/unit) = ₹{item['qty'] * item['price']}"
            )
        st.write(f"**Total: ₹{self.total}**")

    def ask_for_address(self):
        st.subheader("🚚 Delivery Details")
        self.address = st.text_area("Delivery Address", value=self.address)
        st.session_state["address"] = self.address  # Save/update for reuse

    def handle_order_submission(self):
        if not self.address.strip():
            st.warning("⚠️ Address is required.")
            return

        order = {
            "user": self.username,
            "address": self.address.strip(),
            "total": self.total,
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": self.cart
        }

        order_id = OrderManager.insert_order(order)
        if order_id:
            st.success(f"✅ Order #{order_id} placed successfully!")
            st.session_state["cart"] = []
            st.session_state["cart_quantities"] = {}
            st.session_state["dashboard_menu_selected"] = 2
            st.session_state["current_page"] = "dashboard"
            st.rerun()
        else:
            st.error("❌ Failed to place order. Please try again later.")

    def place_order_page(self):
        if self.is_cart_empty():
            self.show_empty_cart_message()
            return

        st.header("🛒 Place Your Order")
        self.render_order_summary()
        self.ask_for_address()

        if st.button("🛒 Place Order", use_container_width=True, type="primary"):
            self.handle_order_submission()

    @staticmethod
    def show_user_orders(username):
        orders = OrderManager.get_user_orders(username)
        st.header("📦 Your Orders")

        if not orders:
            st.info("🛍️ You have no orders yet.")
            return

        for i, order in enumerate(orders, 1):
            st.subheader(f"📌 Order #{order['id']} — {order['datetime']}")
            st.write(f"🏠 Address: {order['address']}")
            st.write(f"💵 Total: ₹{order['total']:.2f}")
            st.markdown("---")


# 👇 Example usage
if __name__ == "__main__" or st.session_state.get("current_page") in ("order", "orders"):
    username = st.session_state.get("username", "guest")

    # If ordering page
    if st.session_state.get("current_page") == "order":
        order_ui = OrderUI(username)
        order_ui.place_order_page()

    # If viewing previous orders
    elif st.session_state.get("current_page") == "orders":
        OrderUI.show_user_orders(username)
