# main.py

import streamlit as st

from utils import User, StreamlitHelper
from landing import LandingPage
from signup import SignupPage
from login import LoginPage
from dashboard import welcome_page
from orders import OrderUI  # ✅ FIX: replaced 'place_order' with correct class import

class SessionManager:
    def __init__(self):
        self.defaults = {
            "user_data": User.load_users(),
            "is_logged_in": False,
            "current_user": "",
            "current_page": "landing",
            "dashboard_menu_selected": 0,
            "cart": [],
            "cart_quantities": {},
            "address": ""
        }

    def initialize(self):
        for key, value in self.defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value

class AppController:
    def __init__(self):
        self.session = SessionManager()
        self.session.initialize()
        self.page = st.session_state.get("current_page", "landing")
        self.logged_in = st.session_state.get("is_logged_in", False)

    def route(self):
        if self.logged_in:
            self.handle_logged_in_flow()
        else:
            self.handle_guest_flow()

    def handle_logged_in_flow(self):
        if self.page == "order":
            username = st.session_state.get("current_user", "guest")
            OrderUI(username).place_order_page()  # ✅ FIX: use object method call
        else:
            welcome_page()

    def handle_guest_flow(self):
        if self.page == "landing":
            LandingPage().show()
        elif self.page == "login":
            LoginPage().render()
            self._page_switcher("signup", "Don’t have an account? Sign Up below 👇", "Go to Sign Up")
        elif self.page == "signup":
            SignupPage().render()
            self._page_switcher("login", "Already have an account? Login below 🔑", "Go to Login")
        else:
            st.session_state["current_page"] = "landing"
            LandingPage().show()

    def _page_switcher(self, new_page: str, message: str, button_label: str):
        st.info(message)
        if st.button(button_label):
            st.session_state["current_page"] = new_page
            StreamlitHelper.rerun(st)

# ⛳ Entry Point
if __name__ == "__main__":
    app = AppController()
    app.route()
