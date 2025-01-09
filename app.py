import streamlit as st
import datetime

class Subscription:
    def __init__(self, user_name, plan_type):
        self.user_name = user_name
        self.plan_type = plan_type
        self.start_date = datetime.datetime.now()
        self.end_date = self.calculate_end_date()
        self.is_active = True

    def calculate_end_date(self):
        if self.plan_type == "monthly":
            return self.start_date + datetime.timedelta(days=30)
        elif self.plan_type == "yearly":
            return self.start_date + datetime.timedelta(days=365)
        else:
            raise ValueError("Plan type must be 'monthly' or 'yearly'")

    def renew_subscription(self):
        if not self.is_active:
            st.warning(f"Subscription for {self.user_name} is expired. Please renew.")
            return
        if self.plan_type == "monthly":
            self.end_date = self.end_date + datetime.timedelta(days=30)
        elif self.plan_type == "yearly":
            self.end_date = self.end_date + datetime.timedelta(days=365)
        st.success(f"Subscription renewed for {self.user_name}. New end date: {self.end_date}")

    def check_status(self):
        today = datetime.datetime.now()
        if today > self.end_date:
            self.is_active = False
            st.error(f"Subscription for {self.user_name} has expired on {self.end_date}.")
        else:
            st.info(f"Subscription for {self.user_name} is active until {self.end_date}.")

    def change_plan(self, new_plan):
        self.plan_type = new_plan
        self.end_date = self.calculate_end_date()
        st.success(f"Subscription plan changed to {new_plan} for {self.user_name}. New end date: {self.end_date}")

    def cancel_subscription(self):
        self.is_active = False
        self.end_date = datetime.datetime.now()
        st.success(f"Subscription for {self.user_name} has been cancelled.")

def main():
    st.title("Subscription Management System")

    # Input pengguna
    user_name = st.text_input("Enter your name:")

    if 'subscription' not in st.session_state:
        st.session_state['subscription'] = None

    if user_name:
        # Jika langganan sudah ada
        if st.session_state['subscription']:
            subscription = st.session_state['subscription']
            subscription.check_status()
            
            # Mengubah paket
            new_plan = st.radio("Change your plan to:", ("monthly", "yearly"))
            if st.button(f"Change to {new_plan} plan"):
                subscription.change_plan(new_plan)
                st.session_state['subscription'] = subscription  # Simpan perubahan

            # Pembatalan langganan
            if st.button("Cancel Subscription"):
                subscription.cancel_subscription()
                st.session_state['subscription'] = None  # Menghapus langganan yang dibatalkan
        else:
            # Membuat langganan baru
            plan_type = st.radio("Choose your plan type:", ("monthly", "yearly"))

            if st.button("Create Subscription"):
                # Membuat langganan baru
                subscription = Subscription(user_name, plan_type)
                st.session_state['subscription'] = subscription  # Menyimpan langganan ke session state
                st.success(f"Subscription created for {user_name} with {plan_type} plan.")
                subscription.check_status()

    else:
        st.warning("Please enter your name to manage your subscription.")

if __name__ == "__main__":
    main()
