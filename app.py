import streamlit as st
import pandas as pd
from datetime import datetime

# Optional: For user authentication (e.g., Streamlit-Authenticator)
# import streamlit_authenticator as stauth

# Define the approval groups
approval_groups = {
    "Group 1": {"approved": False, "approver": None, "timestamp": None},
    "Group 2": {"approved": False, "approver": None, "timestamp": None},
    "Group 3": {"approved": False, "approver": None, "timestamp": None},
}

# Function to check if all groups have approved
def all_approved(approval_groups):
    return all(group["approved"] for group in approval_groups.values())

def main():
    st.title("File Approval Management")

    # Display the approval status
    st.subheader("Approval Status")
    status_df = pd.DataFrame(approval_groups).T
    st.table(status_df)

    # Select the group to approve
    group = st.selectbox("Select your group", list(approval_groups.keys()))

    if st.button("Approve File"):
        approval_groups[group]["approved"] = True
        approval_groups[group]["approver"] = st.text_input("Enter your name")
        approval_groups[group]["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.success(f"{group} has approved the file.")

    # Check if all groups have approved
    if all_approved(approval_groups):
        st.success("The file has been approved by all groups!")

if __name__ == "__main__":
    main()
