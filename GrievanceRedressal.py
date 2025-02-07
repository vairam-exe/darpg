import os
import yaml
import base64
import pandas as pd
import numpy as np
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI

def initialize_ai_env():
    """Load Google API key and configure the environment for Google Generative AI."""
    with open("geminiapi/api.yaml", "r") as f:
        config = yaml.full_load(f)
        api_key = config['gemini']['api_key']
        os.environ['GOOGLE_API_KEY'] = api_key
        genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

class GrievanceRedressal:
    """Class to handle the grievance redressal chatbot functionality."""
    
    def __init__(self, st_obj):
        self.st_obj = st_obj
        self.chat_history = ""
        self.inp_query = ""
        self.department = ""

    def add_background_image(self, image_file):
        """Add a background image to the Streamlit app."""
        with open(image_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            st.markdown(f"""<style>.stApp {{background-image: url(data:image/png;base64,{encoded_string.decode()});background-size: cover}}</style>""", unsafe_allow_html=True)

    def initialize_ui_sidebar(self):
        """Initialize the sidebar with information about the chatbot."""
        with self.st_obj.sidebar:    
            st.markdown("**DARPG Grievances Chatbot**")
            st.text_area(label="**Objective**", value=self.get_objective_text(), height=600)

    def get_objective_text(self):
        """Return the objective text for the sidebar."""
        return """1. What are the contact details of the Department of Administrative Reforms and Public Grievances?
        ...
        17. How to change the details of the Nodal Grievance Officer and Nodal Appellate Authority in the portal?
        ...
        18. Whether the Department has operated any feedback call centre?
        ...
        """

    def initialize_ui_categories(self):
        """Initialize the dropdowns for selecting categories and departments."""
        df = pd.read_csv('data/Complaint_Category.csv')
        required_df = df[["Category", "ParentCategory", "OrgCode"]].sort_values(by=['Category'])
        
        # Add "All" options to the DataFrame
        required_df.loc[len(required_df)] = ["All", np.nan, "ALL"]
        required_df.loc[len(required_df)] = ["All", "All", "ALL"]
        
        # Filter for parent categories
        parent_categories = required_df[required_df['ParentCategory'].isna()].sort_values(by=['Category'])

        # Create the primary dropdown for Category
        selected_category = self.st_obj.selectbox("Department/Ministry", parent_categories['Category'].unique())
        
        # Filter the DataFrame based on the selected category
        filtered_df = required_df[required_df['ParentCategory'] == selected_category]
        selected_org_code = filtered_df["OrgCode"].unique()[0]
        
        self.department = selected_category
        selected_sub_category = self.st_obj.selectbox("Categories in " + self.department, filtered_df['Category'].unique())

    def get_input_query(self):
        """Get the user's input query."""
        self.inp_query = self.st_obj.text_input("**YOUR QUERIES**")

    def initialize_ui(self):
        """Set up the main UI components of the Streamlit app."""
        self.st_obj.set_page_config("DARPG Chatbot")
        self.st_obj.header("DARPG Grievances Chatbot") 
        self.initialize_ui_categories()
        self.initialize_ui_sidebar()

    def return_output(self):   
        """Generate a response based on the user's query and selected department."""
        prompt_template = PromptTemplate(
            input_variables=["concept"],
            template=f"Answer to the ask {{concept}} from {self.department} Department" if self.department != 'All' else "Answer the {{concept}} from all DARPG Departments"
        )

        llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.0)
        chain = LLMChain(llm=llm, prompt=prompt_template)

        # Concatenate chat history
        self.chat_history += f"**You asked:** {self.inp_query}\n"
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []
        st.session_state['chat_history'].append(("**Queried**", self.inp_query))

        # Generate output from the chain
        output = chain.invoke(self.chat_history)

        # Capture response in history text
        self.chat_history += f"**Bot's answer:** {output['text']}\n"
        return output["text"]

    def process(self):
        """Process the user's input and retrieve information."""
        if self.st_obj.button("Retrieve Information"):
            with self.st_obj.spinner("Retrieving Information..."):
                llm_resp = self.return_output()
                st.session_state['chat_history'].append(("**Bot's answer**", llm_resp))
                self.st_obj.write(llm_resp)

def main():
    """Main function to run the Streamlit app."""
    initialize_ai_env()
    grievance_redressal_obj = GrievanceRedressal(st)
    grievance_redressal_obj.initialize_ui()
    grievance_redressal_obj.get_input_query()
    grievance_redressal_obj.process()

if __name__ == "__main__":
    main()
