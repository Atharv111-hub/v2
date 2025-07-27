import streamlit as st
import time
from utils import StreamlitHelper, User  # ✅ fixed OOP imports

class LoginPage:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.user_data = {}
        self.max_login_attempts = 3
        self.lockout_duration = 300  # 5 minutes in seconds

    def render(self):
        # Custom CSS for professional styling
        self.inject_custom_css()
        
        # Header with logo and branding
        self.show_header()
        
        # Main login form
        self.show_form()
        
        # Footer with additional options
        self.show_footer()

    def inject_custom_css(self):
        st.markdown("""
        <style>
        .main-header {
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: -1rem -1rem 2rem -1rem;
            color: white;
            border-radius: 0 0 20px 20px;
        }
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            border: 1px solid #e1e5e9;
        }
        .login-title {
            color: #2c3e50;
            font-size: 1.8rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            text-align: center;
        }
        .footer-links {
            text-align: center;
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid #eee;
        }
        .security-badge {
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 1rem 0;
            font-size: 0.9rem;
            color: #27ae60;
        }
        .stButton > button {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 0.75rem;
            border-radius: 8px;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .alert-info {
            background-color: #e8f4fd;
            border-left: 4px solid #3498db;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 5px;
        }
        </style>
        """, unsafe_allow_html=True)

    def show_header(self):
        st.markdown("""
        <div class="main-header">
            <h1>🏥 Medicare Plus</h1>
            <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">Your Trusted Medicine Delivery Partner</p>
        </div>
        """, unsafe_allow_html=True)

    def show_form(self):
        # Center the login form
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            st.markdown('<h2 class="login-title">🔐 Secure Login</h2>', unsafe_allow_html=True)
            
            # Security badge
            st.markdown("""
            <div class="security-badge">
                🛡️ SSL Secured & HIPAA Compliant
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("login_form", clear_on_submit=False):
                # Username field with icon
                self.username = st.text_input(
                    "👤 Username/Email",
                    placeholder="Enter your username or email",
                    max_chars=50,
                    key="username_input"
                )
                
                # Password field with icon
                self.password = st.text_input(
                    "🔒 Password",
                    type="password",
                    placeholder="Enter your password",
                    key="login_password"
                )
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Login button
                login_button = st.form_submit_button("🚀 Login to Medicare Plus")
                
                # Load users from DB → Session
                if "user_data" not in st.session_state:
                    st.session_state["user_data"] = User.load_users()
                self.user_data = st.session_state["user_data"]

                if login_button:
                    self.handle_login()
            
            st.markdown('</div>', unsafe_allow_html=True)

    def handle_login(self):
        # Initialize session state for login attempts if not exists
        if "login_attempts" not in st.session_state:
            st.session_state["login_attempts"] = 0
            st.session_state["last_attempt_time"] = 0

        # Check if account is locked
        if self.is_account_locked():
            remaining_time = self.get_remaining_lockout_time()
            st.error(f"🔒 Account temporarily locked. Try again in {remaining_time} minutes.")
            return

        # Validate input
        validation_error = self.validate_input()
        if validation_error:
            st.warning(f"⚠️ {validation_error}")
            return

        # Authenticate user
        auth_result = self.authenticate_user()
        
        if auth_result["success"]:
            # Reset login attempts on successful login
            st.session_state["login_attempts"] = 0
            
            user_info = auth_result["user_info"]
            st.success(f"✅ Welcome back, {user_info.get('full_name', self.username)}!")
            
            # Set session state
            self.set_session_state(user_info)
            
            # Add a small delay for better UX
            time.sleep(1)
            StreamlitHelper.rerun(st)
        else:
            # Increment failed attempts
            st.session_state["login_attempts"] += 1
            st.session_state["last_attempt_time"] = time.time()
            
            remaining_attempts = self.max_login_attempts - st.session_state["login_attempts"]
            
            if remaining_attempts > 0:
                st.error(f"❌ {auth_result['message']} ({remaining_attempts} attempts remaining)")
            else:
                st.error("🔒 Account locked due to multiple failed attempts. Please try again later.")

    def validate_input(self):
        if not self.username or not self.password:
            return "Please enter both username/email and password."
        
        if len(self.username) < 3:
            return "Username must be at least 3 characters long."
        
        if len(self.password) < 6:
            return "Password must be at least 6 characters long."
        
        # Email validation if username contains @
        if "@" in self.username:
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, self.username):
                return "Please enter a valid email address."
        
        return None

    def authenticate_user(self):
        # Check if user exists (by username or email)
        user_key = None
        for key, user_info in self.user_data.items():
            if (key.lower() == self.username.lower() or 
                user_info.get("email", "").lower() == self.username.lower()):
                user_key = key
                break
        
        if not user_key:
            return {"success": False, "message": "User not found. Please check your credentials."}
        
        user_info = self.user_data[user_key]
        
        # Check if account is active
        if user_info.get("status") == "inactive":
            return {"success": False, "message": "Account is deactivated. Please contact support."}
        
        # Verify password
        if user_info["password"] != self.password:
            return {"success": False, "message": "Incorrect password."}
        
        return {"success": True, "user_info": user_info, "username": user_key}

    def is_account_locked(self):
        if st.session_state["login_attempts"] >= self.max_login_attempts:
            time_since_last_attempt = time.time() - st.session_state["last_attempt_time"]
            return time_since_last_attempt < self.lockout_duration
        return False

    def get_remaining_lockout_time(self):
        time_since_last_attempt = time.time() - st.session_state["last_attempt_time"]
        remaining_seconds = self.lockout_duration - time_since_last_attempt
        return max(0, int(remaining_seconds / 60))

    def set_session_state(self, user_info):
        st.session_state["is_logged_in"] = True
        st.session_state["current_user"] = self.username
        st.session_state["current_role"] = user_info.get("role", "customer")
        st.session_state["user_profile"] = {
            "full_name": user_info.get("full_name", ""),
            "email": user_info.get("email", ""),
            "phone": user_info.get("phone", ""),
            "address": user_info.get("address", ""),
            "membership_type": user_info.get("membership_type", "standard")
        }
        st.session_state["login_time"] = time.time()
        st.session_state["current_page"] = "dashboard"

    def show_footer(self):
        st.markdown("""
        <div class="footer-links">
        </div>
        """, unsafe_allow_html=True)