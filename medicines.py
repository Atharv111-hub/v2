# medicines.py

import streamlit as st
from datetime import datetime
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from utils import DBHelper  # ✅ FIXED import to match OOP utils.py

ITEMS_PER_PAGE = 20


@dataclass
class Medicine:
    id: str
    name: str
    description: str
    category: str
    price: float
    stock: int
    expiry_date: Optional[str] = None
    manufacturer: Optional[str] = None
    requires_prescription: bool = False


class MedicineManager:
    def get_all_medicines(self) -> List[Dict[str, Any]]:
        return DBHelper.fetch_all("SELECT * FROM medicines")

    def is_expired(self, med: Dict[str, Any], today: Optional[datetime.date] = None) -> bool:
        today = today or datetime.today().date()
        try:
            expiry = datetime.strptime(str(med["expiry_date"]), "%Y-%m-%d").date()
            return expiry < today
        except Exception:
            return False

    def filter_medicines(
        self,
        medicines: List[Dict[str, Any]],
        search_term: str = "",
        category: str = "All",
        in_stock_only: bool = True
    ) -> List[Dict[str, Any]]:
        result = []
        for med in medicines:
            if search_term.lower() not in med.get('name', "").lower():
                continue
            if category != "All" and med.get("category") != category:
                continue
            if in_stock_only and med.get("stock", 0) <= 0:
                continue
            result.append(med)
        return result


class MedicineUI:
    def __init__(self, show_expiry=False):
        self.manager = MedicineManager()
        self.medicines = self.manager.get_all_medicines()
        self.filtered: List[Dict[str, Any]] = []
        self.page = 0
        self.search_term = ""
        self.category = "All"
        self.in_stock_only = True
        self.sort_by = "Name"
        self.show_expiry = show_expiry

    def draw_filters(self):
        st.header("📋 Browse Medicines")
        col1, col2 = st.columns([3, 1])
        with col1:
            self.search_term = st.text_input("Search Medicines", key="search_term")
        with col2:
            st.button("🔄 Refresh")

        categories = sorted({med.get("category", "Other") for med in self.medicines})
        col1, col2, col3 = st.columns(3)
        with col1:
            self.category = st.selectbox("Category", ["All"] + categories)
        with col2:
            self.in_stock_only = st.checkbox("In Stock Only", True)
        with col3:
            self.sort_by = st.selectbox("Sort By", ["Name", "Price", "Stock"])

    def apply_filters_and_sorting(self):
        self.filtered = self.manager.filter_medicines(
            self.medicines,
            search_term=self.search_term,
            category=self.category,
            in_stock_only=self.in_stock_only
        )
        if self.sort_by == "Price":
            self.filtered.sort(key=lambda m: m.get("price", 0))
        elif self.sort_by == "Stock":
            self.filtered.sort(key=lambda m: m.get("stock", 0), reverse=True)
        else:
            self.filtered.sort(key=lambda m: m.get("name", ""))

    def display_pagination(self):
        st.markdown(f"**{len(self.filtered)} medicine(s) found**")
        if not self.filtered:
            st.info("No matching results.")
            return []

        total_pages = (len(self.filtered) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
        self.page = st.selectbox("Page", range(1, total_pages + 1), index=0) - 1
        return self.filtered[self.page * ITEMS_PER_PAGE:(self.page + 1) * ITEMS_PER_PAGE]

    def draw_medicine_card(self, med: Dict[str, Any]):
        expired = self.manager.is_expired(med)
        key = f"qty_{med.get('id', med.get('name', 'unknown'))}"
        default_qty = st.session_state.get("cart_quantities", {}).get(key, 0)

        st.subheader(f"{med['name']} {'(Expired)' if expired else ''}")
        st.caption(f"Category: {med.get('category', 'Other')}")
        st.write(med.get("description", "No description provided."))
        if med.get("manufacturer"):
            st.write(f"🏭 Manufacturer: {med['manufacturer']}")

        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            st.write(f"💰 ₹{med.get('price', 0):.2f} per unit")
        with col2:
            stock = med.get("stock", 0)
            stock_text = "Out of Stock" if stock == 0 else f"In Stock: {stock}"
            st.write(f"📦 {stock_text}")
        with col3:
            if expired:
                st.warning("❌ Not available")
            elif stock > 0:
                qty = st.number_input("Quantity", min_value=0, max_value=stock, value=default_qty, key=key)
                st.session_state.setdefault("cart_quantities", {})[key] = qty

        if med.get("requires_prescription"):
            st.warning("⚠️ Requires prescription")

        expiry_string = med.get("expiry_date", "N/A")
        try:
            expiry = datetime.strptime(expiry_string, "%Y-%m-%d").date()
            days_left = (expiry - datetime.today().date()).days
            if expired:
                st.error("❌ Medicine not available")
            elif self.show_expiry or days_left <= 30:
                st.warning(f"⚠️ Expires in {days_left} days ({expiry})")
            else:
                st.caption(f"Expiry: {expiry}")
        except Exception:
            st.caption(f"Expiry: {expiry_string}")

        st.markdown("---")

    def add_selected_to_cart(self, medicines: List[Dict[str, Any]]):
        added_items = []
        today = datetime.today().date()
        for med in medicines:
            key = f"qty_{med.get('id', med.get('name', 'unknown'))}"
            qty = st.session_state.get("cart_quantities", {}).get(key, 0)
            if qty > 0 and not self.manager.is_expired(med, today):
                added_items.append({
                    "id": med.get("id"),
                    "name": med.get("name"),
                    "price": med.get("price"),
                    "qty": qty,
                    "category": med.get("category"),
                    "expiry_date": med.get("expiry_date")
                })

        if added_items:
            st.session_state.setdefault("cart", []).extend(added_items)
            st.success(f"🛒 Added {len(added_items)} item(s) to cart!")
        else:
            st.warning("⚠️ Please select at least one item with quantity.")

    def clear_selections(self, medicines: List[Dict[str, Any]]):
        for med in medicines:
            key = f"qty_{med.get('id', med.get('name', 'unknown'))}"
            st.session_state.get("cart_quantities", {}).pop(key, None)
        st.experimental_rerun()

    def show(self):
        if not self.medicines:
            st.warning("No medicines available.")
            return

        self.draw_filters()
        self.apply_filters_and_sorting()
        meds_page = self.display_pagination()

        for med in meds_page:
            self.draw_medicine_card(med)

        with st.container():
            col1, col2 = st.columns([3, 2])
            with col1:
                if st.button("🛒 Add Selected to Cart"):
                    self.add_selected_to_cart(meds_page)
            with col2:
                if st.button("🗑️ Clear Selections"):
                    self.clear_selections(meds_page)


# Usage
if __name__ == "__main__" or st.session_state.get("current_page") == "medicines":
    ui = MedicineUI(show_expiry=False)
    ui.show()

elif st.session_state.get("current_page") == "enhanced_medicines":
    ui = MedicineUI(show_expiry=True)
    ui.show()
