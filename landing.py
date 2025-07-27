# landing.py
import streamlit as st
from utils import StreamlitHelper  


class LandingPage:
    def __init__(self):
        self.set_page_config()
        self.inject_custom_css()

    def set_page_config(self):
        st.set_page_config(
            page_title="Medicare Plus - Professional Healthcare Platform",
            page_icon="⚕️",
            layout="wide",
            initial_sidebar_state="collapsed"
        )

    def inject_custom_css(self):
        st.markdown("""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Global Styling */
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Inter', sans-serif;
        }
        
        /* Main container */
        .main .block-container {
            padding-top: 2rem;
            max-width: 1200px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
            margin: 2rem auto;
        }
        
        /* Hero Section */
        .hero-title {
            font-size: 3.5rem !important;
            font-weight: 700 !important;
            color: #1e293b !important;
            text-align: center;
            margin-bottom: 0.5rem !important;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .hero-subtitle {
            font-size: 1.3rem !important;
            color: #000000 !important;
            text-align: center;
            font-weight: 700 !important;
            margin-bottom: 2rem !important;
        }
        
        .hero-stats {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            padding: 1rem;
            border-radius: 15px;
            text-align: center;
            font-weight: 600;
            color: #1e293b;
            border: 2px solid #e2e8f0;
        }
        
        .hero-description {
            font-size: 1.4rem !important;
            color: #374151 !important;
            text-align: center;
            line-height: 1.6 !important;
            margin: 2rem 0 !important;
            font-weight: 400;
        }
        
        /* Custom Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 25px !important;
            padding: 0.75rem 2rem !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3) !important;
            width: 100% !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4) !important;
            background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        }
        
        /* Secondary buttons */
        .secondary-btn button {
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
        }
        
        .secondary-btn button:hover {
            background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important;
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4) !important;
        }
        
        /* Statistics Cards */
        [data-testid="metric-container"] {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border: 2px solid #e2e8f0;
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }
        
        [data-testid="metric-container"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            border-color: #10b981;
        }
        
        [data-testid="metric-container"] > div {
            text-align: center;
        }
        
        [data-testid="metric-container"] [data-testid="metric-value"] {
            font-size: 2.5rem !important;
            font-weight: 700 !important;
            color: #10b981 !important;
        }
        
        [data-testid="metric-container"] [data-testid="metric-label"] {
            font-size: 1rem !important;
            color: #6b7280 !important;
            font-weight: 500 !important;
        }
        
        /* Feature Cards */
        .feature-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            padding: 2rem;
            border-radius: 15px;
            border: 2px solid #e2e8f0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            margin: 1rem 0;
            transition: all 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            border-color: #3b82f6;
        }
        
        /* Trust Section */
        .trust-badges {
            background: linear-gradient(135deg, #fef3c7 0%, #fcd34d 100%);
            padding: 1rem;
            border-radius: 15px;
            text-align: center;
            font-weight: 600;
            color: #92400e;
            border: 2px solid #fbbf24;
            margin: 1rem 0;
        }
        
        .trust-card {
            background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
            padding: 1.5rem;
            border-radius: 15px;
            border: 2px solid #bfdbfe;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .trust-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.1);
        }
        
        /* CTA Section */
        .cta-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 3rem 2rem;
            border-radius: 20px;
            text-align: center;
            margin: 2rem 0;
        }
        
        .cta-section h3 {
            color: white !important;
            font-size: 2.2rem !important;
            margin-bottom: 1rem !important;
        }
        
        .cta-section p {
            font-size: 1.2rem !important;
            opacity: 0.9;
            margin-bottom: 2rem !important;
        }
        
        /* Footer */
        .footer-section {
            background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            margin-top: 2rem;
        }
        
        .footer-section h4 {
            color: #10b981 !important;
        }
        
        /* Dividers */
        .stDivider > div {
            background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
            height: 2px;
        }
        
        /* Subheaders */
        h3 {
            color: #1e293b !important;
            font-weight: 600 !important;
            margin-bottom: 1rem !important;
        }
        
        h4 {
            color: #374151 !important;
            font-weight: 600 !important;
        }
        
        /* Text styling */
        p {
            line-height: 1.6 !important;
            color: #4b5563 !important;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            border-radius: 10px;
            border: 2px solid #e2e8f0;
        }
        
        /* Mobile responsive */
        @media (max-width: 768px) {
            .hero-title {
                font-size: 2.5rem !important;
            }
            
            .hero-description {
                font-size: 1.2rem !important;
            }
            
            .main .block-container {
                margin: 1rem;
                border-radius: 15px;
            }
        }
        </style>
        """, unsafe_allow_html=True)

    def show(self):
        self.show_hero_section()
        self.show_statistics()
        self.show_features()
        self.show_trust_section()
        self.show_cta()
        self.show_footer()

    def show_hero_section(self):
        # Hero Section
        st.markdown('<h1 class="hero-title">⚕️ Medicare Plus</h1>', unsafe_allow_html=True)
        st.markdown('<p class="hero-subtitle">Your trusted healthcare partner at your fingertips</p>', unsafe_allow_html=True)
        
        # Trust indicator
        st.markdown('<div class="hero-stats">📈 Trusted by 50,000+ patients nationwide</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Main headline
        st.markdown("## Healthcare Made Simple & Accessible")
        st.markdown(
            '<p class="hero-description">Connect with certified doctors and order prescription medicines '
            'from the comfort of your home. Available 24/7 across India.</p>',
            unsafe_allow_html=True
        )

        # Hero CTA
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Start Your Healthcare Journey", key="start"):
                st.session_state["current_page"] = "login"
                StreamlitHelper.rerun(st)

    def show_statistics(self):
        st.markdown("---")
        st.markdown("### 📊 Our Impact in Numbers")
        
        cols = st.columns(4)
        stats = [
            ("50,000+", "Happy Patients"),
            ("500+", "Expert Doctors"),
            ("15,000+", "Medicines Available"),
            ("24/7", "Customer Support")
        ]
        
        for col, (number, label) in zip(cols, stats):
            col.metric(label, number)

    def show_features(self):
        st.markdown("---")
        st.markdown("### 🧰 Complete Healthcare Solutions")
        st.markdown("Everything you need for your health and wellness, delivered with care and precision.")

        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h4>🩺 Online Doctor Consultations</h4>
                <p>Connect with certified doctors via video, voice or chat. Get expert medical advice from the comfort of your home.</p>
                <ul>
                    <li>🔥 Instant consultations available</li>
                    <li>👨‍⚕️ 500+ certified doctors</li>
                    <li>💬 Multiple communication options</li>
                    <li>📋 Digital prescriptions</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
            if st.button("📅 Book Consultation", key="goto_login_consult"):
                st.session_state["current_page"] = "login"
                StreamlitHelper.rerun(st)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="feature-card">
                <h4>💊 Prescription Medicine Delivery</h4>
                <p>Upload and verify your prescription with our pharmacists. Get genuine medicines delivered to your doorstep.</p>
                <ul>
                    <li>🚚 Same-day delivery available</li>
                    <li>✅ Verified by licensed pharmacists</li>
                    <li>💰 Competitive pricing</li>
                    <li>🔒 100% genuine medicines</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
            if st.button("🛒 Order Medicines", key="goto_login_order"):
                st.session_state["current_page"] = "login"
                StreamlitHelper.rerun(st)
            st.markdown('</div>', unsafe_allow_html=True)

    def show_trust_section(self):
        st.markdown("---")
        st.markdown("### 🔐 Trusted & Certified")
        st.markdown("We follow national and international standards to ensure your data and health are protected.")

        # Trust badges
        st.markdown('<div class="trust-badges">🏛️ MCI Certified | 🛡️ ISO 27001 | ⚖️ HIPAA Compliant | 🔒 SSL Secured</div>', unsafe_allow_html=True)

        st.markdown("#### Why Trust Us?")
        cols = st.columns(3)
        
        with cols[0]:
            st.markdown("""
            <div class="trust-card">
                <h4>🛡️ Secure & Confidential</h4>
                <p>Your data is encrypted and stored with enterprise-grade security. We never share your personal information.</p>
            </div>
            """, unsafe_allow_html=True)
            
        with cols[1]:
            st.markdown("""
            <div class="trust-card">
                <h4>✅ Licensed Professionals</h4>
                <p>All doctors and pharmacists are verified, licensed professionals with years of experience.</p>
            </div>
            """, unsafe_allow_html=True)
            
        with cols[2]:
            st.markdown("""
            <div class="trust-card">
                <h4>🚚 Fast Delivery</h4>
                <p>Same-day delivery available in major cities. Express delivery options for urgent medicines.</p>
            </div>
            """, unsafe_allow_html=True)

    def show_cta(self):
        st.markdown("---")
        
        # CTA Section with gradient background
        st.markdown("""
        <div class="cta-section">
            <h3>🎯 Ready to Transform Your Healthcare Experience?</h3>
            <p>Join thousands of patients who trust Medicare Plus for their healthcare needs. Start your journey toward better health today.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # CTA Button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🧭 Let's Get Started", key="get_started"):
                st.session_state["current_page"] = "login"
                StreamlitHelper.rerun(st)

    def show_footer(self):
        st.markdown("---")
        
        # Contact section
        with st.expander("📞 Contact & Support", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **📞 Contact Information:**
                - Phone: +91 1800-123-4567
                - Email: support@medicareplus.com
                - Emergency: Available 24/7
                """)
                
            with col2:
                st.markdown("""
                **🌍 Service Areas:**
                - Available across India
                - Same-day delivery in major cities
                - Express delivery nationwide
                """)
        
        # Footer
        st.markdown("""
        <div class="footer-section">
            <div style="text-align: center;">
                <h4>Medicare Plus - Your Health, Our Priority</h4>
                <p>© 2024 Medicare Plus. All rights reserved. | Privacy Policy | Terms of Service</p>
                <p>🏥 Transforming healthcare delivery across India</p>
            </div>
        </div>
        """, unsafe_allow_html=True)