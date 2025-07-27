# cart.py
import streamlit as st
import datetime


class CartUtils:
    @staticmethod
    def get_expiry_status(expiry_date_str: str) -> str:
        try:
            expiry_parts = expiry_date_str.split('-')
            if len(expiry_parts) == 3:
                expiry_date = datetime.datetime(
                    int(expiry_parts[0]),
                    int(expiry_parts[1]),
                    int(expiry_parts[2])
                )
                days_until_expiry = (expiry_date - datetime.datetime.now()).days
                if days_until_expiry < 0:
                    return "⚠️ EXPIRED"
                elif days_until_expiry <= 30:
                    return f"⏰ Expires in {days_until_expiry} days"
                else:
                    return "✅ Fresh"
        except Exception:
            return "📅 Date format invalid"
        return "📅 Unknown"


class CartPage:
    def __init__(self):
        self.cart = st.session_state.get("cart", [])
        self.cart_quantities = st.session_state.get("cart_quantities", {})

    def show(self) -> bool:
        self.show_top_bar()
        st.title("🛒 Your Cart")

        if not self.cart:
            return self.render_empty_cart()

        self.show_summary()
        st.divider()
        self.render_cart_items()
        st.divider()
        self.render_action_buttons()
        return True

    def show_top_bar(self):
        st.header("🏥 MediCare Delivery System")

    def render_empty_cart(self) -> bool:
        st.info("🛍️ Your cart is empty. Start shopping to add medicines!")
        if st.button("Browse Medicines", key="browse_meds", type="primary", use_container_width=True):
            st.session_state["dashboard_menu_selected"] = 0
            st.rerun()
        return False

    def show_summary(self):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Items in Cart", len(self.cart))
        with col2:
            total_qty = sum(item['qty'] for item in self.cart)
            st.metric("Total Quantity", total_qty)
        with col3:
            total_amount = self.get_total_amount()
            st.metric("Total Amount", f"₹{total_amount}")

    def render_cart_items(self):
        for i, item in enumerate(self.cart):
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                with col1:
                    st.write(f"**{item['name']}**")
                    st.write(f"Price: ₹{item['price']} per unit")
                    expiry_text = CartUtils.get_expiry_status(item.get('expiry_date', 'Not specified'))
                    st.write(f"Expiry: {expiry_text}")
                with col2:
                    new_qty = st.number_input("Qty", min_value=1, max_value=99, value=item['qty'], key=f"qty_{i}")
                    if new_qty != item['qty']:
                        self.cart[i]['qty'] = new_qty
                        st.session_state["cart"] = self.cart
                        st.rerun()
                with col3:
                    subtotal = item['price'] * item['qty']
                    st.write(f"**₹{subtotal}**")
                with col4:
                    if st.button("Remove", key=f"remove_{i}", type="secondary"):
                        self.cart.pop(i)
                        st.session_state["cart"] = self.cart
                        st.rerun()
            st.divider()

    def render_action_buttons(self):
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Continue Shopping", key="continue_shopping", use_container_width=True):
                st.session_state["dashboard_menu_selected"] = 0
                st.rerun()
        with col2:
            if st.button("Clear Cart", use_container_width=True, type="secondary"):
                st.session_state["cart"] = []
                st.session_state["cart_quantities"] = {}
                st.rerun()
        with col3:
            if st.button("Order Now", key="order_now", use_container_width=True, type="primary"):
                st.session_state["current_page"] = "order"
                st.rerun()

        st.success(f"**Total Amount: ₹{self.get_total_amount()}**")

    def get_total_amount(self) -> float:
        return sum(item['price'] * item['qty'] for item in self.cart)
