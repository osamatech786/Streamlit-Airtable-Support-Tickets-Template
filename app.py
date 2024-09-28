import datetime
import streamlit as st
from pyairtable import Table
from dotenv import load_dotenv
import os
import altair as alt
import pandas as pd
import re

# Streamlit configuration
st.set_page_config(page_title="Support tickets", page_icon="🎫")
st.title("🎫 Support tickets")
st.write(
    """
    This app shows how you can build an internal tool in Streamlit. Here, we are 
    implementing a support ticket workflow. The user can create a ticket, edit 
    existing tickets, and view some statistics.
    """
)

def get_secret(key):
    try:
    # Attempt to get the secret from environment variables
        secret = os.getenv(key)
        if secret is None:
            raise ValueError("Secret not found in environment variables")
        return secret
    except (ValueError, TypeError) as e:
        # If an error occurs, fall back to Streamlit secrets
        if hasattr(st, 'secrets'):
            return st.secrets.get(key)
        # If still not found, return None or handle as needed
        return None

# List of table names
table_options = ["Team_1", "Team_2", "Another_Team"]
# Dropdown for the user to select a table
selected_table = st.selectbox("Choose a table:", table_options)

load_dotenv()
AIRTABLE_API_KEY=get_secret("PAT")
BASE_ID=get_secret("BASE_ID")
TABLE_NAME = os.getenv(selected_table)

# Initialize Airtable client. Use the selected table name
airtable_table = Table(AIRTABLE_API_KEY, BASE_ID, selected_table)

# Initialize session state for ticket_id_input
if "ticket_id_input" not in st.session_state:
    st.session_state.ticket_id_input = ""


# Initialize a placeholder for the tickets table
tickets_placeholder = st.empty()

# Function to convert date format
def format_date(date_str):
    if date_str:
        # Parse the ISO date string
        parsed_date = datetime.datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        # Format to DD-MM-YY and 12-hour clock
        return parsed_date.strftime("%d-%m-%Y %I:%M %p")
    return ""

# Custom sorting function for status and priority
def custom_sort_key(ticket):
    # Define custom order for status and priority
    status_order = {"In Progress": 0, "Open": 1, "Closed": 2}
    priority_order = {"High": 0, "Medium": 1, "Low": 2}

    # Return a tuple for sorting by status, then priority, then Ticket ID descending
    return (
        status_order.get(ticket['Status'], 3),  # Default to lowest priority if not found
        priority_order.get(ticket['Priority'], 3),
        int(ticket['Ticket ID'])  # Negative for descending order (-int)
    )

# Function to fetch tickets from Airtable
def fetch_tickets():
    records = airtable_table.all()
    tickets = [
        {
            "Ticket ID": rec['fields'].get('Ticket ID', ''),
            "Title": rec['fields'].get('Title', ''),
            "Description": rec['fields'].get('Description', ''),
            "Status": rec['fields'].get('Status', 'Open'),
            "Priority": rec['fields'].get('Priority', 'Medium'),
            "Date Submitted": format_date(rec['fields'].get('Created Date', '')),  # Format date
            "Assigned To": rec['fields'].get('Assigned To', '')
        }
        for rec in records
    ]
    # Sort the tickets using the custom sorting key
    return sorted(tickets, key=custom_sort_key)



# Function to add a new ticket to Airtable
def add_ticket(title, description, priority):
    new_ticket = {
        "Title": title,
        "Description": description,
        "Status": "Open",
        "Priority": priority,
        "Created Date": datetime.datetime.now().strftime("%Y-%m-%d"),
    }
    airtable_table.create(new_ticket)

# Function to find record by "Ticket ID"
def find_record_id(ticket_id):
    records = airtable_table.all()
    for rec in records:
        if rec['fields'].get('Ticket ID', '') == ticket_id:
            return rec['id']
    return None

# Function to update a ticket in Airtable
def update_ticket(ticket_id, updated_fields):
    record_id = find_record_id(ticket_id)
    if record_id:
        airtable_table.update(record_id, updated_fields)

# -------------------------------------------------------------------------------

# Fetch the current tickets data from Airtable
tickets_data = fetch_tickets()

# Convert to a format suitable for display
ticket_df = pd.DataFrame(tickets_data)

# Show section to add a new ticket
st.header("Add a ticket")

# Initialize session state for title and description
if "title" not in st.session_state:
    st.session_state.title = ""
if "description" not in st.session_state:
    st.session_state.description = ""

with st.form("add_ticket_form"):
    # Bind the input fields to session state
    title = st.text_input("Title of the issue", value=st.session_state.title)
    description = st.text_area("Describe the issue", value=st.session_state.description)
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    submitted = st.form_submit_button("Submit")

# Refresh the table after adding a new ticket
if submitted:
    add_ticket(title, description, priority)
    st.success("Ticket submitted successfully!")
    st.session_state.title, st.session_state.description = "", ""
    st.rerun()
    
# Show section to view and edit existing tickets
st.header("Existing tickets")
st.write(f"Number of tickets: `{len(tickets_data)}`")

# Convert to a format suitable for display
ticket_df = pd.DataFrame(tickets_data)

# Make the DataFrame editable
if not ticket_df.empty:
    st.write("### Existing Tickets Table")
    
    # Use st.data_editor for editable table, allowing editing of Title, Description, Status, Priority
    edited_df = st.data_editor(
        ticket_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Status": st.column_config.SelectboxColumn(
                "Status",
                help="Ticket status",
                options=["Open", "In Progress", "Closed"],
                required=True,
            ),
            "Priority": st.column_config.SelectboxColumn(
                "Priority",
                help="Priority",
                options=["High", "Medium", "Low"],
                required=True,
            ),
        },
        disabled=["Ticket ID", "Date Submitted"],  # Disable editing of these columns
    )

    # Compare the original and edited dataframes to detect changes
    if not ticket_df.equals(edited_df):
        for i, row in edited_df.iterrows():
            ticket_id = row['Ticket ID']
            updated_fields = {
                "Title": row['Title'],
                "Description": row['Description'],
                "Status": row['Status'],
                "Priority": row['Priority']
            }
            # Update the Airtable record
            update_ticket(ticket_id, updated_fields)
        st.success("Changes saved successfully!")

    st.write('-----------------------------------')
    # Display statistics and plots as before
    st.header("Statistics")
    col1, col2, col3 = st.columns(3)
    num_open_tickets = len(ticket_df[ticket_df["Status"] == "Open"])
    col1.metric(label="Number of open tickets", value=num_open_tickets, delta=10)
    col2.metric(label="First response time (hours)", value=5.2, delta=-1.5)
    col3.metric(label="Average resolution time (hours)", value=16, delta=2)

    st.write("")
    st.write("##### Ticket status per month")
    status_plot = (
        alt.Chart(ticket_df)
        .mark_bar()
        .encode(
            x="month(Date Submitted):O",
            y="count():Q",
            xOffset="Status:N",
            color="Status:N",
        )
        .configure_legend(
            orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
        )
    )
    st.altair_chart(status_plot, use_container_width=True, theme="streamlit")

    st.write("##### Current ticket priorities")
    priority_plot = (
        alt.Chart(ticket_df)
        .mark_arc()
        .encode(theta="count():Q", color="Priority:N")
        .properties(height=300)
        .configure_legend(
            orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
        )
    )
    st.altair_chart(priority_plot, use_container_width=True, theme="streamlit")
else:
    st.write("No tickets found.")

# ---------------------------------------

# Delete Logic
st.write('----------------------------------')
st.subheader('Delete Tickets')
st.write('Please enter Ticket IDs separated by commas if multiple IDs need to be deleted. e.g., 2, 3, 5, 7')
st.write('Please enter Ticket IDs by range to delete e.g., 1-5')

# Take input for Ticket IDs
ticket_id_input = st.text_input("Enter Ticket IDs to delete", value=st.session_state.ticket_id_input, key="delete_input")

# Function to process the input string and extract Ticket IDs
def parse_ticket_ids(input_str):
    input_str = input_str.strip()  # Remove leading and trailing spaces
    
    # Validate the input (only numbers, commas, and a single dash for range)
    if not re.match(r'^[\d\s,-]+$', input_str):
        st.error("Invalid input format. Only numbers, commas, and dashes are allowed.")
        return []

    input_str = re.sub(r'\s+', '', input_str)  # Remove all whitespace
    ticket_ids = set()  # Use a set to prevent duplicate IDs

    # Check if input contains a dash for range processing
    if '-' in input_str:
        try:
            range_parts = input_str.split('-')
            if len(range_parts) == 2:
                start, end = int(range_parts[0]), int(range_parts[1])
                if start <= end:
                    ticket_ids.update(range(start, end + 1))
                else:
                    st.error("Invalid range. Start of range should be less than or equal to end.")
                    return []
            else:
                st.error("Invalid range format. Use a single dash (e.g., 1-5).")
                return []
        except ValueError:
            st.error("Invalid range input. Please enter valid numbers.")
            return []
    
    # Check if input contains commas for individual ticket processing
    else:
        try:
            individual_ids = [int(x) for x in input_str.split(',')]
            ticket_ids.update(individual_ids)
        except ValueError:
            st.error("Invalid input. Please ensure all Ticket IDs are numbers.")
            return []

    return sorted(ticket_ids)

# Function to find and delete a ticket by its ID
def delete_ticket(ticket_id):
    # Fetch all records and match by "Ticket ID"
    records = airtable_table.all()
    record_to_delete = None
    
    for rec in records:
        # Check if "Ticket ID" matches the given ID
        if rec['fields'].get('Ticket ID') == ticket_id:
            record_to_delete = rec['id']
            break

    # If a matching record is found, delete it
    if record_to_delete:
        airtable_table.delete(record_to_delete)
        return True
    return False

# Processing ticket deletions
if st.button("Delete Tickets"):
    ticket_ids_to_delete = parse_ticket_ids(ticket_id_input)
    if ticket_ids_to_delete:
        deleted_ids = []
        non_existing_ids = []

        for ticket_id in ticket_ids_to_delete:
            if delete_ticket(ticket_id):
                deleted_ids.append(ticket_id)
            else:
                non_existing_ids.append(ticket_id)

        if deleted_ids:
            st.success(f"Deleted tickets with IDs: {deleted_ids}")
        if non_existing_ids:
            st.warning(f"Ticket IDs not found or already deleted: {non_existing_ids}")

        st.session_state.ticket_id_input = ""
        st.rerun()
