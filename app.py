import streamlit as st

# Ticket categories and prices (in RM)
ticket_prices = {
    "Meet & Greet (Ultimate Fan Experience)": 1000,
    "VIP (Front Row)": 500,
    "Premium (Middle Section)": 300,
    "Regular (Back Row)": 100,
}

ticket_descriptions = {
    "Meet & Greet (Ultimate Fan Experience)": "Exclusive access to meet the artists backstage.",
    "VIP (Front Row)": "Enjoy front-row seats for the best view of the concert.",
    "Premium (Middle Section)": "Perfect view from the middle section of the stadium.",
    "Regular (Back Row)": "Affordable seats with a great atmosphere at the back.",
}

# Initialize session state for ticket quantities
if "ticket_quantities" not in st.session_state:
    st.session_state["ticket_quantities"] = {category: 0 for category in ticket_prices}
if "user_name" not in st.session_state:
    st.session_state["user_name"] = ""

# Function to reset ticket quantities
def reset_tickets():
    for category in st.session_state["ticket_quantities"]:
        st.session_state["ticket_quantities"][category] = 0

# Title and introduction
st.title("🎶 Anugerah Malaysia Live 2024")
st.subheader("Featuring Siti Nurhaliza, Yuna, and Faizal Tahir")
st.write("""
**📅 Date**: 25th December 2024  
**📍 Venue**: Bukit Jalil National Stadium  
Secure your spot for this unforgettable concert! Choose your ticket category below and book now!  
""")

# Add a smaller image of the concert
st.image("https://i.imgflip.com/41aizo.jpg", use_column_width=False, width=400)  # Adjust width to 400 for a smaller image

# Add space after the image
st.write("\n")  # Adds a newline for spacing

# Keep the same header for ticket selection
st.header("🎟 Select Your Tickets Below:")

# Create a collapsible section for ticket categories
with st.expander("🎫 Ticket Categories and Prices (Click to View Details)"):
    for category, price in ticket_prices.items():
        st.write(f"**{category}**: RM {price} per ticket")
        st.write(f"🔎 *{ticket_descriptions[category]}*")

# Interactive ticket selection (no numbers in the main section)
for category in ticket_prices:
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.write(f"**{category}**")
    with col2:
        if st.button(f"➖ {category}", key=f"decrease_{category}"):
            if st.session_state["ticket_quantities"][category] > 0:
                st.session_state["ticket_quantities"][category] -= 1
    with col3:
        if st.button(f"➕ {category}", key=f"increase_{category}"):
            st.session_state["ticket_quantities"][category] += 1

# Sidebar: Booking Summary and Total Amount
st.sidebar.title("📊 Booking Summary")
total_tickets = sum(st.session_state["ticket_quantities"].values())
total_amount = sum(
    st.session_state["ticket_quantities"][category] * price
    for category, price in ticket_prices.items()
)
if total_tickets > 0:
    st.sidebar.write(f"**Total Tickets Selected**: {total_tickets}")
    st.sidebar.write("**Breakdown by Category:**")
    for category, quantity in st.session_state["ticket_quantities"].items():
        if quantity > 0:
            st.sidebar.write(f"{category}: {quantity} tickets")
    st.sidebar.write(f"**Total Amount to Pay**: RM {total_amount}")
else:
    st.sidebar.write("No tickets selected yet.")

# Ask for name if user proceeds to checkout
if total_tickets > 0:
    st.header("Please enter your name before proceeding to checkout:")
    st.text_input("Your Name", key="user_name", value=st.session_state["user_name"])
    
    # Checkout button in the main section
    if st.button("Proceed to Checkout"):
        user_name = st.session_state["user_name"]
        if user_name:
            # Display the new meme image before thank you message
            st.image("https://i.imgflip.com/5563ph.jpg", width=200)  # New meme, smaller size

            # Prepare ticket summary for the user
            ticket_summary = []
            for category, quantity in st.session_state["ticket_quantities"].items():
                if quantity > 0:
                    ticket_summary.append(f"{category}: {quantity} tickets")
            
            # Display the confirmation message with ticket details
            st.write("...")  # Adds some space before showing the thank you message
            st.write(f"🎉 Thank you for your booking, {user_name}!")
            st.write(f"Your total amount is **RM {total_amount}**.")
            st.write("You have selected the following tickets:")
            for item in ticket_summary:
                st.write(f"- {item}")
            st.write("We look forward to seeing you at Anugerah Malaysia Live 2024!")
            st.write("Feel free to share your excitement on social media!")
            st.balloons()

            # Button for downloading a 'ticket' (dummy text file for now)
            st.download_button(
                label="Download Your Ticket",
                data=f"Name: {user_name}\nTickets: {', '.join(ticket_summary)}\nTotal: RM {total_amount}",
                file_name=f"{user_name}_ticket.txt",
                mime="text/plain"
            )
        else:
            st.warning("Please enter your name to proceed.")
else:
    st.warning("Please select at least one ticket to proceed.")

# Reset and Checkout buttons in the main section
st.header("🔧 Actions")
col1, col2 = st.columns(2)
with col1:
    if st.button("Reset Tickets"):
        reset_tickets()
        st.success("All selections have been reset!")
