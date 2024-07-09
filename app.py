import streamlit as st
import hashlib
import pandas as pd

# Function to hash passwords
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Mock user database (In a real application, use a secure database)
users = {
    "user1": {"password": hash_password("password1"), "group": 1, "role": "approver"},
    "user2": {"password": hash_password("password2"), "group": 1, "role": "non-approver"},
    "user3": {"password": hash_password("password3"), "group": 1, "role": "non-approver"},
    "user4": {"password": hash_password("password4"), "group": 2, "role": "approver"},
    "user5": {"password": hash_password("password5"), "group": 2, "role": "non-approver"},
    "user6": {"password": hash_password("password6"), "group": 2, "role": "non-approver"},
    "user7": {"password": hash_password("password7"), "group": 3, "role": "approver"},
    "user8": {"password": hash_password("password8"), "group": 3, "role": "non-approver"},
    "user9": {"password": hash_password("password9"), "group": 3, "role": "non-approver"}
}

# Mock dataset to be approved
fake_data = pd.DataFrame({
    "Name": ["John Smith", "Alice Johnson", "Bob Brown", "Emily Davis", "Michael Wilson"],
    "Age": [30, 25, 35, 28, 40],
    "Email": ["john@example.com", "alice@example.com", "bob@example.com", "emily@example.com", "michael@example.com"],
    "Department": ["HR", "Marketing", "Engineering", "Sales", "Finance"],
    "Salary": [60000, 55000, 70000, 60000, 80000],
    "Approved": [False, False, False, False, False],
    "Group": [1, 2, 3, 1, 2]  # Adding a new column "Group" ranging from 1 to 3
})

# Function to validate login
def login(username: str, password: str) -> bool:
    if username in users and users[username]["password"] == hash_password(password):
        return True
    return False

# Function to get user role
def get_user_role(username: str) -> str:
    return users[username]["role"]

# Function to approve data (active only for approvers and within their group)
def approve_data(index: int):
    if st.session_state.logged_in:
        username = st.session_state.username
        user_role = get_user_role(username)
        user_group = users[username]["group"]

        if user_role == "approver":
            if "fake_data" in st.session_state:
                if st.session_state.fake_data.at[index, "Group"] == user_group:
                    # Update the Approved status in the session state and then update the DataFrame
                    st.session_state.fake_data.at[index, "Approved"] = True
                    st.experimental_rerun()
                    st.success("Data approved successfully!")
                else:
                    st.error("You can only approve data within your own group.")
            else:
                st.error("Data not initialized. Please log in again.")
        else:
            st.error("You do not have permission to approve data.")
    else:
        st.error("Please log in to approve data.")

# Login Page
def login_page():
    st.title("Login System")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            if "fake_data" not in st.session_state:
                st.session_state.fake_data = fake_data.copy()  # Initialize fake_data in session state
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

# Landing Page
def landing_page():
    st.title("Landing Page")
    st.success(f"Welcome {st.session_state.username}!")
    role = get_user_role(st.session_state.username)
    st.write(f"Your role: {role}")

    st.header("Fake Dataset to Approve")
    if "fake_data" in st.session_state:
        st.write(st.session_state.fake_data)
    else:
        st.write(fake_data)  # Show original fake_data if not initialized in session state

    if role == "approver":
        for i in range(len(fake_data)):
            if not st.session_state.fake_data.loc[i, "Approved"]:
                if st.button(f"Approve Row {i+1}"):
                    approve_data(i)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.pop("fake_data", None)  # Clear fake_data from session state
        st.experimental_rerun()

# Streamlit app
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""

    if st.session_state.logged_in:
        landing_page()
    else:
        login_page()

if __name__ == "__main__":
    main()
