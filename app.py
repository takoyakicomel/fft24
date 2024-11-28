import streamlit as st

# Ticket prices by category
TICKET_PRICES = {
    "VIP": 500,
    "Premium": 300,
    "General": 100,
}

# App title and description
st.title("Concert Ticket Booking")
st.write("Welcome! Book your concert tickets here 🎵")

# Sidebar for ticket category selection
st.sidebar.header("Select Ticket Category")
category = st.sidebar.selectbox("Choose your ticket type:", list(TICKET_PRICES.keys()))

# Display ticket price
st.write(f"**Selected Ticket Category:** {category}")
st.write(f"**Price per Ticket:** RM {TICKET_PRICES[category]}")

# Quantity selection
st.write("### Select Quantity")
quantity = st.number_input("Enter quantity:", min_value=0, max_value=10, step=1, value=0)

# Calculate total amount
total_price = quantity * TICKET_PRICES[category]

# Display total amount
st.write(f"**Total Amount to Pay:** RM {total_price}")

# Confirm button
if st.button("Confirm Purchase"):
    if quantity > 0:
        st.success(f"Thank you! You've successfully purchased {quantity} {category} ticket(s) for RM {total_price}.")
    else:
        st.warning("Please select at least one ticket to proceed.")

# Footer
st.sidebar.write("---")
st.sidebar.write("Developed by Group 4 🎶")

