# Paste all your notebook code here (everything except the Streamlit part)
import streamlit as st
import pandas as pd
# --- Import functions from your backend script/notebook ---
# Assume the code from Phase 1, 2, 3 is saved in a file like `backend.py`
# from backend import load_data, clean_data, merge_data, query_agent, generate_capacity_reduction_email, PROJECT_ID, REGION, BUCKET_NAME # Example
# For this example, we'll embed simplified versions or placeholders

# --- Placeholder functions/variables if not importing ---
# In a real app, replace these with imports from your backend module
PROJECT_ID = "gen-ai-rajan-labs"
REGION = "us-central1"
BUCKET_NAME = "your-gcs-bucket-name" # Replace!
df_merged = pd.DataFrame() # Placeholder
agent_available = False # Placeholder
pandas_agent_executor = None # Placeholder

def load_and_process_data():
    # This function would encapsulate steps 1-4 from Phase 1
    # For demo, create sample data or load if previously saved
    global df_merged, agent_available, pandas_agent_executor
    st.info("Loading and processing data... Please wait.")
    # --- Add actual data loading/processing code here ---
    # Simplified example: Load a pre-processed CSV if available, otherwise show error
    try:
        # In production, you'd run the full GCS load/clean/merge/agent creation here
        # For now, let's assume df_merged and agent are created elsewhere or loaded
        # df_merged = pd.read_csv("processed_carrier_data.csv") # Example loading
        # agent_available = True # Assume agent was created if data loaded
        # placeholder data:
        data = {
            'Canonical Carrier Name': ['Carrier A', 'BLARO ARGENTINA', 'Carrier C', 'Carrier D'],
            'Your Company Account Manager Name': ['AM One', 'AM One', 'AM Two', 'AM Two'],
            'Your Company Account Manager Email': ['am1@mycompany.com', 'am1@mycompany.com', 'am2@mycompany.com', 'am2@mycompany.com'],
            'Carrier Company Account Manager Name': ['Carrier AM A', 'Carrier AM B', 'Carrier AM C', 'Carrier AM D'],
            'Carrier Company Account Manager Email': ['ama@carrier.com', 'amb@carrier.com', 'amc@carrier.com', 'amd@carrier.com'],
            'Configured Capacity': [1000, 500, 2000, 800],
            'Peak Usage': [500, 150, 1500, 200],
            'Peak Usage Percentage': [50.0, 30.0, 75.0, 25.0],
            'First Line Contact Name': ['Support A', 'Support B', 'Support C', 'Support D'],
            'First Line Contact Email': ['supporta@carrier.com', 'supportb@carrier.com', 'supportc@carrier.com', 'supportd@carrier.com'],
            'Underutilized': [False, True, False, True],
            'Proposed New Capacity': [pd.NA, 250, pd.NA, 400]
        }
        df_merged = pd.DataFrame(data)
        # Simulate agent creation success for demo
        agent_available = True # Set to False to test error handling
        st.success("Data loaded and processed successfully.")
        st.dataframe(df_merged.head()) # Show a preview
        # In a real scenario, initialize the actual agent here (Phase 2 code)
    except Exception as e:
        st.error(f"Failed to load or process data: {e}")
        df_merged = pd.DataFrame()
        agent_available = False

def query_agent(query):
     # Placeholder - replace with actual agent call from Phase 2
    if agent_available:
        st.info(f"Simulating agent query for: '{query}'")
        # Simple rule-based simulation for demo
        if "underutilized" in query.lower():
             underutilized = df_merged[df_merged['Underutilized'] == True]['Canonical Carrier Name'].tolist()
             return f"The underutilized carriers are: {', '.join(underutilized)}"
        elif "capacity for" in query.lower():
             # Very basic parsing
             try:
                 name = query.split("capacity for ")[1].split('?')[0].strip("'").strip('"')
                 info = df_merged[df_merged['Canonical Carrier Name'] == name]
                 if not info.empty:
                     return f"Details for {name}:\n{info[['Configured Capacity', 'Peak Usage', 'Peak Usage Percentage']].to_string()}"
                 else:
                     return f"Sorry, I don't have capacity info for {name}."
             except:
                  return "Could not parse carrier name from query."
        else:
             return f"Simulated response: I received your query about '{query}'. In a real deployment, I would use the LLM agent to answer this based on the data."
    else:
        return "Chatbot agent is not available."

def generate_capacity_reduction_email(carrier_name):
     # Placeholder - replace with actual function from Phase 3
    st.info(f"Simulating email generation for: '{carrier_name}'")
    if df_merged.empty:
        return "Error: Data not loaded."
    carrier_data = df_merged[df_merged['Canonical Carrier Name'] == carrier_name]
    if carrier_data.empty: return f"Error: Carrier '{carrier_name}' not found."
    carrier_info = carrier_data.iloc[0]
    if not carrier_info.get('Underutilized', False): return f"Carrier '{carrier_name}' is not underutilized."
    # Simplified email text for demo
    return f"""
--- SIMULATED EMAIL PREVIEW ---
To: {carrier_info.get('Carrier Company Account Manager Email', 'N/A')}
CC: {carrier_info.get('Your Company Account Manager Email', 'N/A')}
Subject: Planned Capacity Adjustment for {carrier_name}

Dear {carrier_info.get('Carrier Company Account Manager Name', 'Manager')},

This is a notification regarding planned capacity reduction for {carrier_name} from {carrier_info.get('Configured Capacity', 'N/A')} to {carrier_info.get('Proposed New Capacity', 'N/A')} due to low utilization ({carrier_info.get('Peak Usage Percentage', 'N/A'):.2f}%).

Please contact {carrier_info.get('Your Company Account Manager Name', 'your AM')} with questions.

Best regards,
[Your Company]
--- END PREVIEW ---
"""

# --- Streamlit App Layout ---
st.set_page_config(layout="wide")
st.title("📞 Telecom Carrier Capacity Assistant")
st.markdown(f"**Project:** `{PROJECT_ID}` | **Region:** `{REGION}` | **Data Bucket:** `{BUCKET_NAME}`")

# --- Load data on startup ---
# Use st.cache_data or st.cache_resource for efficiency in real apps
# For simplicity here, we load it directly or use a button
if 'data_loaded' not in st.session_state:
     st.session_state.data_loaded = False
     st.session_state.agent_available = False

if not st.session_state.data_loaded:
    if st.button("Load and Process Carrier Data"):
        load_and_process_data() # Load data using the function
        st.session_state.data_loaded = True
        st.session_state.agent_available = agent_available # Store agent status
        st.rerun() # Rerun the script to update the UI state
    else:
        st.warning("Please click the button above to load data.")
        st.stop() # Stop execution if data isn't loaded
elif not st.session_state.agent_available:
     st.error("Data loaded, but the Chatbot Agent could not be initialized. Please check logs/configuration.")
     st.stop()


# --- Main Interaction Area ---
col1, col2 = st.columns([2, 1]) # Chat area, Control Panel

with col1:
    st.subheader("Chat with Carrier Data")
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hi! How can I help you with the carrier data today?"}]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Ask a question about carriers, usage, or contacts..."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get assistant response
        with st.spinner("Thinking..."):
             # Use the actual query_agent function here
            response = query_agent(prompt)
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

with col2:
    st.subheader("Actions")
    st.markdown("Identify underutilized carriers and generate notification emails.")

    if not df_merged.empty and 'Underutilized' in df_merged.columns:
        underutilized_carriers = df_merged[df_merged['Underutilized'] == True]['Canonical Carrier Name'].tolist()

        if underutilized_carriers:
            st.success(f"Found {len(underutilized_carriers)} underutilized carriers.")
            selected_carrier = st.selectbox(
                "Select underutilized carrier for email:",
                options=underutilized_carriers,
                index=None, # Nothing selected by default
                placeholder="Choose a carrier..."
            )

            if selected_carrier and st.button(f"Generate Email for {selected_carrier}"):
                 with st.spinner("Generating email text..."):
                     # Use the actual email generation function here
                     email_text = generate_capacity_reduction_email(selected_carrier)
                     st.text_area("Generated Email Text:", email_text, height=400)
                     st.info("Please review the generated text carefully before sending.")
            elif selected_carrier:
                st.write("") # Just to add some space if a carrier is selected but button not clicked
        else:
            st.info("No carriers currently meet the criteria for underutilization (<40%).")
    else:
        st.warning("Carrier data not loaded or processed correctly for action panel.")
