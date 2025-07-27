# consult.py ✅

import streamlit as st
from datetime import datetime
from utils import Consultation  # this is your DB helper class from utils.py


class ConsultationPage:
    def __init__(self, username):
        self.username = username
        self.symptoms = ""
        self.preferred_time = ""

    def display_form(self):
        st.header("👨‍⚕️ Consult a Doctor")
        with st.form("consult_form"):
            self.symptoms = st.text_area("Describe your symptoms")
            self.preferred_time = st.text_input("Preferred time (e.g. Morning, Evening)")
            submitted = st.form_submit_button("Request Consultation")
            if submitted:
                self.submit()

    def submit(self):
        if not self.symptoms or not self.preferred_time:
            st.warning("⚠️ Please fill in all fields.")
            return

        record = {
            "user": self.username,
            "symptoms": self.symptoms,
            "preferred_time": self.preferred_time,
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        Consultation.save(record)
        st.success("✅ Consultation request submitted!")


class ConsultationHistory:
    def __init__(self, username):
        self.username = username
        self.consultations = []

    def display_consultations(self):
        st.header("📋 Your Consultation History")
        self.consultations = Consultation.get_user_consultations(self.username)

        if not self.consultations:
            st.info("You have no consultation history.")
            return

        for i, c in enumerate(self.consultations, 1):
            self._display_entry(i, c)

    def _display_entry(self, idx, c):
        st.write(f"### 📝 Consultation #{idx}")
        st.write(f"**Date:** {c['datetime']}")
        st.write(f"**Symptoms:** {c['symptoms']}")
        st.write(f"**Preferred Time:** {c['preferred_time']}")
        st.markdown("---")
