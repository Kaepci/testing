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

def main():
    st.title("Subscription Management System")

    # Input pengguna
    user_name = st.text_input("Enter your name:")

    plan_type = st.radio("Choose your plan type:", ("monthly", "yearly"))

    if st.button("Create Subscription"):
        if user_name:
            # Membuat langganan baru
            subscription = Subscription(user_name, plan_type)

            # Menampilkan status langganan
            subscription.check_status()

            # Pilihan untuk memperbarui langganan
            if st.button("Renew Subscription"):
                subscription.renew_subscription()
        else:
            st.warning("Please enter your name before creating a subscription.")

if __name__ == "__main__":
    main()
