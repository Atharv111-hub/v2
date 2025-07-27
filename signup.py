# signup.py
import streamlit as st
from utils import Validator, User, StreamlitHelper

class SignupPage:
    def __init__(self):
        self.username = ""
        self.email = ""
        self.password = ""
        self.user_data = st.session_state.get("user_data") or User.load_users()
        st.session_state["user_data"] = self.user_data
        self.errors = []

    def render(self):
        # Custom CSS for professional styling
        st.markdown("""
        <style>
        .main-header {
            text-align: center;
            color: #1f2937;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .subtitle {
            text-align: center;
            color: #6b7280;
            font-size: 1.1rem;
            margin-bottom: 2rem;
            font-weight: 400;
        }
        
        .form-container {
            background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
            padding: 2.5rem;
            border-radius: 20px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            border: 1px solid #e5e7eb;
            margin: 1rem 0;
        }
        
        .input-label {
            color: #374151;
            font-weight: 600;
            margin-bottom: 0.5rem;
            font-size: 0.95rem;
        }
        
        .stTextInput > div > div > input {
            border-radius: 12px;
            border: 2px solid #e5e7eb;
            padding: 0.75rem 1rem;
            font-size: 1rem;
            transition: all 0.3s ease;
            background-color: #ffffff;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            outline: none;
        }
        
        .signup-button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.75rem 2rem;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
            margin-top: 1rem;
        }
        
        .signup-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        .error-message {
            background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
            border: 1px solid #f87171;
            border-radius: 8px;
            padding: 0.75rem 1rem;
            margin: 0.5rem 0;
            color: #dc2626;
            font-weight: 500;
        }
        
        .success-message {
            background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
            border: 1px solid #34d399;
            border-radius: 8px;
            padding: 0.75rem 1rem;
            margin: 0.5rem 0;
            color: #065f46;
            font-weight: 500;
        }
        
        .warning-message {
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border: 1px solid #f59e0b;
            border-radius: 8px;
            padding: 0.75rem 1rem;
            margin: 0.5rem 0;
            color: #92400e;
            font-weight: 500;
        }
        
        .feature-icon {
            font-size: 1.2rem;
            margin-right: 0.5rem;
        }
        
        .login-link {
            text-align: center;
            margin-top: 1.5rem;
            padding-top: 1.5rem;
            border-top: 1px solid #e5e7eb;
        }
        
        .login-link a {
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s ease;
        }
        
        .login-link a:hover {
            color: #764ba2;
        }
        
        .password-requirements {
            background: #f8fafc;
            border-radius: 8px;
            padding: 1rem;
            margin-top: 0.5rem;
            border-left: 4px solid #667eea;
        }
        
        .requirement-item {
            color: #6b7280;
            font-size: 0.85rem;
            margin: 0.25rem 0;
        }
        </style>
        """, unsafe_allow_html=True)

        # Header section
        st.markdown('<h1 class="main-header">🚀 Join Our Platform</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Create your account and unlock amazing features</p>', unsafe_allow_html=True)

        # Main form container
        with st.container():
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            
            with st.form("signup_form", clear_on_submit=False):
                # Form header
                st.markdown("### 👤 Account Information")
                
                # Username field
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown('<div class="input-label">👤 Username</div>', unsafe_allow_html=True)
                with col2:
                    pass
                self.username = st.text_input(
                    "Username",
                    max_chars=20,
                    placeholder="Choose a unique username",
                    label_visibility="collapsed"
                )
                
                # Email field
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown('<div class="input-label">📧 Email Address</div>', unsafe_allow_html=True)
                with col2:
                    pass
                self.email = st.text_input(
                    "Email",
                    placeholder="your.email@example.com",
                    label_visibility="collapsed"
                )
                
                # Password field
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown('<div class="input-label">🔒 Password</div>', unsafe_allow_html=True)
                with col2:
                    pass
                self.password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Create a strong password",
                    label_visibility="collapsed"
                )
                
                # Password requirements
                with st.expander("🔐 Password Requirements", expanded=False):
                    st.markdown("""
                    <div class="password-requirements">
                        <div class="requirement-item">• At least 8 characters long</div>
                        <div class="requirement-item">• Contains uppercase and lowercase letters</div>
                        <div class="requirement-item">• Includes at least one number</div>
                        <div class="requirement-item">• Contains at least one special character</div>
                    </div>
                    """, unsafe_allow_html=True)

                # Validate inputs and display errors
                self.validate_inputs()
                
                # Display errors with custom styling
                if self.errors:
                    st.markdown("### ⚠️ Please fix the following issues:")
                    for err in self.errors:
                        st.markdown(f'<div class="error-message">{err}</div>', unsafe_allow_html=True)

                # Submit button
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    submit_button = st.form_submit_button(
                        "🎉 Create Account",
                        use_container_width=True
                    )
                
                if submit_button:
                    self.handle_signup()
            
            st.markdown('</div>', unsafe_allow_html=True)

        # Login link
        st.markdown("""
        <div class="login-link">
            <p>Already have an account? <a href="#" onclick="return false;">Sign in here</a></p>
        </div>
        """, unsafe_allow_html=True)

        # Features section
        st.markdown("---")
        st.markdown("### ✨ What you'll get:")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div style="text-align: center; padding: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🛡️</div>
                <h4>Secure Account</h4>
                <p style="color: #6b7280;">Your data is protected with enterprise-grade security</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">⚡</div>
                <h4>Fast Access</h4>
                <p style="color: #6b7280;">Lightning-fast performance and instant access</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="text-align: center; padding: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎯</div>
                <h4>Personalized</h4>
                <p style="color: #6b7280;">Tailored experience based on your preferences</p>
            </div>
            """, unsafe_allow_html=True)

    def validate_inputs(self):
        self.errors = []  # Reset errors
        
        if self.username:
            if self.username in self.user_data:
                self.errors.append("⚠️ Username already exists. Please choose a different one.")
        
        if self.email:
            if not Validator.is_valid_email(self.email):
                self.errors.append("❌ Please enter a valid email address.")
        
        if self.password:
            valid_pwd, pwd_msg = Validator.is_valid_password(self.password)
            if not valid_pwd:
                self.errors.append(f"🔒 {pwd_msg}")

    def handle_signup(self):
        if self.username and self.email and self.password and not self.errors:
            self.user_data[self.username] = {
                "email": self.email,
                "password": self.password,
                "role": "user"
            }
            User.save_users(self.user_data)

            # Success message with custom styling
            st.markdown("""
            <div class="success-message">
                ✅ <strong>Account created successfully!</strong> Welcome aboard! You can now log in with your credentials.
            </div>
            """, unsafe_allow_html=True)
            
            st.balloons()  # Add celebration animation
            st.session_state["current_page"] = "login"
            StreamlitHelper.rerun(st)
        elif not self.username or not self.email or not self.password:
            st.markdown("""
            <div class="warning-message">
                📝 Please fill in all required fields to create your account.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="warning-message">
                🔧 Please correct the issues above before proceeding.
            </div>
            """, unsafe_allow_html=True)


# Run the signup page
if __name__ == "__main__" or st.session_state.get("current_page") == "signup":
    page = SignupPage()
    page.render()