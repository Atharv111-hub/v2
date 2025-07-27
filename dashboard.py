import streamlit as st
import logging

from utils import StreamlitHelper
from medicines import MedicineUI
from orders import OrderUI
from consult import ConsultationPage, ConsultationHistory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DashboardSessionManager:
    def initialize(self):
        defaults = {
            "is_logged_in": False,
            "current_user": "",
            "cart": [],
            "cart_quantities": {},
            "current_page": "landing",
            "user_preferences": {},
            "last_activity": None,
            "dashboard_menu_selected": 0
        }
        for key, default_value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = default_value

    def clear(self):
        keys = ["is_logged_in", "current_user", "cart", "cart_quantities", "user_preferences", "dashboard_menu_selected"]
        for key in keys:
            st.session_state[key] = {} if key in ["cart", "cart_quantities", "user_preferences"] else \
                False if key == "is_logged_in" else \
                0 if key == "dashboard_menu_selected" else ""
        st.session_state["current_page"] = "landing"

class DashboardUI:
    def __init__(self):
        self.username = st.session_state.get("current_user", "Guest")
        self.apply_custom_css()

    def apply_custom_css(self):
        st.markdown("""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Professional Medical Background Pattern */
        .medicine-background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            overflow: hidden;
            pointer-events: none;
            background: 
                radial-gradient(circle at 20% 20%, rgba(59, 130, 246, 0.02) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(16, 185, 129, 0.02) 0%, transparent 50%);
        }
        
        .medicine-icon {
            position: absolute;
            opacity: 0.03;
            animation: professionalFloat 45s infinite linear;
            font-size: 1.2rem;
            color: #64748b;
            filter: blur(0.5px);
        }
        
        .medicine-icon:nth-child(1) { left: 8%; top: 10%; animation-delay: 0s; }
        .medicine-icon:nth-child(2) { left: 25%; top: 25%; animation-delay: 8s; }
        .medicine-icon:nth-child(3) { left: 42%; top: 15%; animation-delay: 16s; }
        .medicine-icon:nth-child(4) { left: 58%; top: 30%; animation-delay: 24s; }
        .medicine-icon:nth-child(5) { left: 75%; top: 20%; animation-delay: 32s; }
        .medicine-icon:nth-child(6) { left: 92%; top: 35%; animation-delay: 40s; }
        .medicine-icon:nth-child(7) { left: 15%; top: 60%; animation-delay: 5s; }
        .medicine-icon:nth-child(8) { left: 35%; top: 70%; animation-delay: 13s; }
        .medicine-icon:nth-child(9) { left: 65%; top: 65%; animation-delay: 21s; }
        .medicine-icon:nth-child(10) { left: 85%; top: 75%; animation-delay: 29s; }
        
        @keyframes professionalFloat {
            0%, 100% {
                transform: translateY(0px) rotate(0deg);
                opacity: 0.03;
            }
            50% {
                transform: translateY(-15px) rotate(5deg);
                opacity: 0.02;
            }
        }
        
        /* Professional Global Styles */
        .stApp {
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 50%, #e2e8f0 100%);
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            position: relative;
        }
        
        .stApp::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                linear-gradient(135deg, rgba(59, 130, 246, 0.01) 0%, transparent 50%),
                linear-gradient(45deg, rgba(16, 185, 129, 0.01) 0%, transparent 50%);
            z-index: -2;
            pointer-events: none;
        }
        
        /* Professional Main Content Area */
        .main .block-container {
            padding: 2rem 3rem;
            background: rgba(255, 255, 255, 0.98);
            border-radius: 12px;
            margin: 1rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.9);
            position: relative;
            z-index: 1;
        }
        
        /* Professional Header Styling */
        .main-header {
            text-align: center;
            padding: 2.5rem 0;
            background: linear-gradient(135deg, #1e40af 0%, #1d4ed8 100%);
            border-radius: 12px;
            margin-bottom: 2rem;
            color: white;
            box-shadow: 0 4px 20px rgba(59, 130, 246, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.1);
            position: relative;
            overflow: hidden;
        }
        
        .main-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, transparent 40%, rgba(255, 255, 255, 0.03) 50%, transparent 60%);
            animation: professionalShimmer 8s linear infinite;
        }
        
        @keyframes professionalShimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        .main-header h1 {
            font-size: 2.8rem;
            font-weight: 600;
            margin: 0;
            text-shadow: none;
            position: relative;
            z-index: 2;
            letter-spacing: -0.02em;
        }
        
        .main-header .subtitle {
            font-size: 1.1rem;
            opacity: 0.85;
            margin: 0.8rem 0;
            font-weight: 400;
            position: relative;
            z-index: 2;
        }
        
        .features-badge {
            display: inline-block;
            background: rgba(255, 255, 255, 0.15);
            padding: 0.6rem 1.2rem;
            border-radius: 25px;
            margin: 1rem 0;
            font-weight: 500;
            backdrop-filter: blur(10px);
            position: relative;
            z-index: 2;
            font-size: 0.95rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .welcome-message {
            background: linear-gradient(135deg, #059669 0%, #047857 100%);
            color: white;
            padding: 1.2rem 2rem;
            border-radius: 8px;
            text-align: center;
            font-weight: 500;
            font-size: 1rem;
            margin: 1.5rem 0;
            box-shadow: 0 2px 10px rgba(16, 185, 129, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.1);
            position: relative;
            z-index: 1;
        }
        
        /* Sidebar Styling */
        .css-1d391kg, .css-1cypcdb {
            background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
            position: relative;
            z-index: 10;
        }
        
        .css-17eq0hr, .css-1lcbmhc {
            background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
            color: white;
            position: relative;
            z-index: 10;
        }
        
        .sidebar .block-container {
            padding: 1.5rem 1rem;
            background: transparent;
            position: relative;
            z-index: 10;
        }
        
        .sidebar-header {
            text-align: center;
            padding: 1rem 0;
            color: white;
            border-bottom: 2px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 1.5rem;
        }
        
        .sidebar-header h2 {
            color: #93c5fd;
            font-size: 1.4rem;
            font-weight: 500;
            margin: 0;
        }
        
        .user-info {
            background: rgba(147, 197, 253, 0.12);
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            border-left: 3px solid #93c5fd;
            color: white;
        }
        
        .cart-info {
            background: rgba(248, 113, 113, 0.12);
            padding: 0.8rem;
            border-radius: 8px;
            margin: 0.5rem 0;
            border-left: 3px solid #f87171;
            color: white;
        }
        
        /* Menu Items */
        .stRadio > div {
            background: transparent;
        }
        
        .stRadio > div > label {
            background: rgba(255, 255, 255, 0.1);
            margin: 0.3rem 0;
            padding: 0.8rem 1rem;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            transition: all 0.3s ease;
            cursor: pointer;
            border: 1px solid transparent;
        }
        
        .stRadio > div > label:hover {
            background: rgba(96, 165, 250, 0.25);
            border-color: #60a5fa;
            transform: translateX(5px);
        }
        
        .stRadio > div > label[data-checked="true"] {
            background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
            border-color: #60a5fa;
            box-shadow: 0 5px 15px rgba(96, 165, 250, 0.3);
        }
        
        /* Logout Button */
        .logout-btn {
            width: 100%;
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            color: white;
            border: none;
            padding: 0.8rem 1rem;
            border-radius: 8px;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 1rem;
        }
        
        .logout-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(239, 68, 68, 0.4);
        }
        
        /* Professional Content Cards */
        .content-card {
            background: rgba(255, 255, 255, 0.98);
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 2px 15px rgba(0, 0, 0, 0.04);
            margin: 1rem 0;
            border: 1px solid rgba(0, 0, 0, 0.02);
            position: relative;
            z-index: 1;
            backdrop-filter: blur(5px);
        }
        
        /* Loading Spinner */
        .stSpinner > div {
            border-color: #60a5fa;
        }
        
        /* Success/Error Messages */
        .stSuccess {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            border: none;
            border-radius: 10px;
            color: white;
            position: relative;
            z-index: 1;
        }
        
        .stError {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            border: none;
            border-radius: 10px;
            color: white;
            position: relative;
            z-index: 1;
        }
        
        /* Divider */
        hr {
            border: none;
            height: 2px;
            background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
            border-radius: 2px;
            margin: 2rem 0;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Custom animations */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .animated-card {
            animation: fadeInUp 0.6s ease-out;
        }
        
        /* Floating medicine icons in content areas */
        .content-medicine-icon {
            position: absolute;
            opacity: 0.03;
            font-size: 1.5rem;
            color: #3b82f6;
            animation: contentFloat 12s infinite ease-in-out;
            pointer-events: none;
        }
        
        @keyframes contentFloat {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .main .block-container {
                padding: 1rem;
                margin: 0.5rem;
            }
            
            .main-header h1 {
                font-size: 2rem;
            }
            
            .medicine-icon {
                font-size: 1.5rem;
                opacity: 0.05;
            }
        }
        </style>
        """, unsafe_allow_html=True)

    def add_medicine_background(self):
        """Add subtle professional medicine icons to the background"""
        medicine_icons = ["⚕️", "🩺", "💊", "🏥", "🔬", "🧬", "⚕️", "🩺", "💊", "🏥"]
        
        background_html = '<div class="medicine-background">'
        for icon in medicine_icons:
            background_html += f'<div class="medicine-icon">{icon}</div>'
        background_html += '</div>'
        
        st.markdown(background_html, unsafe_allow_html=True)

    def setup_page(self):
        try:
            st.set_page_config(
                page_title="MediCare Plus - Dashboard",
                page_icon="🏥",
                layout="wide",
                initial_sidebar_state="expanded"
            )
        except Exception as e:
            logger.warning("Streamlit page config already set.")
        
        # Add animated background immediately after page setup
        self.add_medicine_background()

    def header(self):
        st.markdown("""
        <div class="main-header animated-card">
            <h1>🏥 MediCare Plus</h1>
            <div class="subtitle">Your trusted medicine delivery service</div>
            <div class="features-badge">💊 Fast Delivery • 👨⚕️ Expert Consultation • 🚚 24/7 Service</div>
        </div>
        """, unsafe_allow_html=True)
        
        if self.username:
            st.markdown(f"""
            <div class="welcome-message animated-card">
                👋 Welcome back, <strong>{self.username}</strong>! Ready to take care of your health?
            </div>
            """, unsafe_allow_html=True)

    def sidebar_menu(self) -> str:
        # Sidebar header
        st.sidebar.markdown("""
        <div class="sidebar-header">
            <h2>📋 Dashboard Menu</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # User info
        cart_count = len(st.session_state.get("cart", []))
        st.sidebar.markdown(f"""
        <div class="user-info">
            <strong>🧑💻 {self.username}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        if cart_count > 0:
            st.sidebar.markdown(f"""
            <div class="cart-info">
                🛒 <strong>{cart_count}</strong> items in cart
            </div>
            """, unsafe_allow_html=True)
        
        # Menu options
        menu_options = [
            ("🏪 Browse Medicines", "Medicines"),
            ("🛒 Cart & Order", "Cart"),
            ("📦 Order History", "Orders"),
            ("👨⚕️ Consult Doctor", "Consult Doctor"),
            ("📋 Consultation History", "Consult History"),
        ]
        
        menu_labels, menu_values = zip(*menu_options)
        
        st.sidebar.markdown("### 📂 Navigation")
        selected_index = st.sidebar.radio(
            "",
            range(len(menu_options)),
            format_func=lambda i: menu_labels[i],
            index=st.session_state.get("dashboard_menu_selected", 0),
            key="dashboard_menu_radio"
        )
        
        st.session_state["dashboard_menu_selected"] = selected_index
        
        st.sidebar.markdown("---")
        
        # Logout button
        if st.sidebar.button("🚪 Logout", key="logout_btn"):
            DashboardSessionManager().clear()
            st.success("✅ Successfully logged out. Redirecting...")
            StreamlitHelper.rerun(st)
        
        return menu_values[selected_index]

class DashboardController:
    def __init__(self):
        self.session = DashboardSessionManager()
        self.ui = DashboardUI()

    def run(self):
        self.session.initialize()
        self.ui.setup_page()
        
        if not st.session_state.get("is_logged_in", False):
            st.markdown("""
            <div class="content-card animated-card" style="text-align: center;">
                <h2 style="color: #ff6b6b;">🔒 Access Restricted</h2>
                <p>Please log in first to access your dashboard.</p>
            </div>
            """, unsafe_allow_html=True)
            return

        username = st.session_state.get("current_user", "")
        if username == "":
            st.markdown("""
            <div class="content-card animated-card" style="text-align: center;">
                <h2 style="color: #ff6b6b;">⚠️ Session Expired</h2>
                <p>Your session has expired. Please log in again.</p>
            </div>
            """, unsafe_allow_html=True)
            return

        self.ui.header()
        selected_menu = self.ui.sidebar_menu()
        self.handle_menu(selected_menu, username)

    def handle_menu(self, selected: str, username: str):
        st.markdown("<hr>", unsafe_allow_html=True)
        
        try:
            if selected == "Medicines":
                with st.spinner("🔍 Loading medicines..."):
                    st.markdown('<div class="content-card animated-card">', unsafe_allow_html=True)
                    MedicineUI(show_expiry=True).show()
                    st.markdown('</div>', unsafe_allow_html=True)
                    
            elif selected == "Cart":
                with st.spinner("🛒 Loading your cart..."):
                    st.markdown('<div class="content-card animated-card">', unsafe_allow_html=True)
                    from cart import CartPage
                    CartPage().show()
                    st.markdown('</div>', unsafe_allow_html=True)
                    
            elif selected == "Orders":
                with st.spinner("📦 Retrieving your orders..."):
                    st.markdown('<div class="content-card animated-card">', unsafe_allow_html=True)
                    OrderUI.show_user_orders(username)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
            elif selected == "Consult Doctor":
                with st.spinner("💬 Preparing consultation..."):
                    st.markdown('<div class="content-card animated-card">', unsafe_allow_html=True)
                    ConsultationPage(username).display_form()
                    st.markdown('</div>', unsafe_allow_html=True)
                    
            elif selected == "Consult History":
                with st.spinner("📋 Fetching consultation history..."):
                    st.markdown('<div class="content-card animated-card">', unsafe_allow_html=True)
                    ConsultationHistory(username).display_consultations()
                    st.markdown('</div>', unsafe_allow_html=True)
                    
            else:
                st.markdown("""
                <div class="content-card animated-card" style="text-align: center;">
                    <h2 style="color: #ff6b6b;">❌ Invalid Selection</h2>
                    <p>Please select a valid menu option.</p>
                </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            st.markdown("""
            <div class="content-card animated-card" style="text-align: center;">
                <h2 style="color: #ff6b6b;">⚠️ Something went wrong</h2>
                <p>We're experiencing technical difficulties. Please try again.</p>
            </div>
            """, unsafe_allow_html=True)
            logger.exception(f"Error handling menu {selected}: {e}")
        
        st.markdown("<hr>", unsafe_allow_html=True)

def welcome_page():
    DashboardController().run()