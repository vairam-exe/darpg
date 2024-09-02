import os
import yaml
import google.generativeai as genai
import base64
import pandas as pd
import numpy as np
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import OpenAI 
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from st_aggrid import AgGrid, GridOptionsBuilder

def initialize_ai_env():
    with open("geminiapi/api.yaml", "r") as f:
        config = yaml.full_load(f)
        apikey = config['gemini']['api_key']
        os.environ['GOOGLE_API_KEY'] = apikey
        genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

class grievanceRedressal:
    llm_resp=''
    chat_history=''
    inp_query=''
    department=''
    def __init__(self,st_obj):
        self.st_obj=st_obj
    
    def add_bg_from_local(self,image_file):

        with open(image_file, "rb") as image_file:
            
           encoded_string = base64.b64encode(image_file.read())
           st.markdown(f"""<style>.stApp {{background-image: url(data:image/{"png"};base64,{encoded_string.decode()});background-size: cover}}</style>""",unsafe_allow_html=True)

    def initialize_ui_sidebar(self):
        with self.st_obj.sidebar:    
           "**DARPG Grievances Chatbot**"
           self.st_obj.text_area(label="**Objective**",value="1. What are the contact details of the Department of Administrative Reforms and Public Grievances?\n\n Department of Administrative Reforms and Public Grievances, 5th floor, Sardar Patel Bhavan, Sansad Marg, New Delhi – 110001 Website:: www.darpg.gov.in Tele fax : 23741006 \n\n2. Where can the grievances be sent?\n\n The grievances can be sent to :\nThe Department of Administrative Reforms and Public Grievances. (pgportal.gov.in)\nThe Department of Pensions and Pensioners’ Welfare.(DP&PW) (pgportal.gov.in/pension/)\nThe above nodal agencies receive grievances online through pgportal.gov.in as well as by post or by hand in person, from the public.\n\n3. How do I lodge the grievance?\n\nThe grievances can be lodged online on . In cases where internet facility is not available or even otherwise, the citizen is free to send her/his grievance by Post. There is no prescribed format.The grievance may be written on any plain sheet of paper or on a Postcard / Inland letter and addressed to the Department. The grievance can also be filled through Common Service Centre.\n\n4. What happens when I lodge the grievance? \n\nThe grievance is acknowledged online or by post. A unique registration number is given to each grievance.\n\n5. How do I track my grievance?\n\n It may be tracked on the pgportal using view status link and after providing unique registration number.\n\n6.What happens to the grievances? How are the grievances dealt with in Central Ministries/Departments?\n\n Every Central Ministry / Department has designated a Joint Secretary or a Director / Deputy Secretary, as its ‘Director of Grievances’. He / She is the nodal officer for redress of grievances on work areas allocated to that particular Ministry / Department.\n\n7. After redress, can the grievance be re-opened for further correspondence about it having been closed without details etc.?\n\nNo. In such situations, the citizen will have to lodge a fresh grievance drawing reference to the closed grievance, and call for details. Sometimes, the details are sent by post and mentioned in the final report. The postal delivery may be awaited before lodging a fresh grievance\n\n8. What are the contact details of the Nodal Officers of Public Grievances in Ministries/Departments?\n\nThe list is accessible on the Department’s website at In addition to this, it is also available in the Citizen’s Charter of the Ministries/Departments hosted on their websites.\n\n9. What is the system of granting personal hearing on grievances?\n\nEvery Wednesday of the week has been earmarked for receiving and hearing of grievances by the Director of Public Grievances in person.\n\n10. What are the types of grievances which are not taken up for redress by the Department?\n\nSubjudice cases or any matter concerning judgment given by any court.\nPersonal and family disputes\nRTI matters\nAnything that impacts upon territorial integrity of the country or friendly relations with other countries\n\n11. What is the role of Department of Administrative Reforms and Public Grievances (DARPG) with reference to the grievances concerning Central Ministries/Departments/ Organizations?\n\nThe Department of Administrative Reforms & Public Grievances is the chief policy making, monitoring and coordinating Department for public grievances arising from the work of Ministries/Departments/Organizations of the Government of India. The grievances received in the department are forwarded to the Ministries/Departments concerned. Redressal of grievances is done by respective Ministries/Departments in a decentralized manner. The Department periodically reviews the status of redressal of public grievances under CPGRAMS of Ministries/Departments for speedy disposal of grievances / complaints.\n\n12. What is the role of Department of Administrative Reforms and Public Grievances (DARPG) with reference to the grievances concerning State Government?\n\nAll grievances relating to State Governments / Union Territory Administrations and Government of NCT Region of Delhi, are sent to the State/ UT/ NCT Government concerned. Citizens may take up matter regarding pendency of their grievances directly with the State Government concerned also.\n\n13. What is the time limit for redress of grievance?\n\nThirty (30) days. In case of delay an interim reply with reasons for delay is required to be given.\n\n14. What action can be taken by me in case of non-redress of my grievance within the prescribed time?\n\nYou may take up the matter with the Director of Public Grievances of the Ministry/Department concerned whose details are available on the pgportal.\n\n15. What can a citizen do if he is not satisfied with the redressal of his grievance?\n\nAn Appeal provision has been made for redressal of dis-satisfied grievances in respect of Central Ministry/Department identified through a mandatory feedback ratting to be given by the Citizen on disposal of the grievance by the Nodal Grievance Officers. The appeal needs to be filed by the applicant within 30 days.\n\n16. How to deactivate CPGRAMS account?\n\nThe request for deactivation of a user account can be made through email to the CPGRAMS helpdesk (cpgrams-darpg@nic.in). The email should be sent from the registered email id only.\nIn case of deactivation, the user can not create an account with the same email-id/mobile but the user can make a request again to activate the same account.\n\n17. How to change the details of the Nodal Grievance Officer and Nodal Appellate Authority in the portal?\n\nThe concerned organisation (Ministries/Department/State Govt) can change the details with their log in credentials.\n\n18. Whether the Department has operated any feedback call centre?\n\nYes. Department has established Feedback call centre to get the feedback from the citizen on disposed grievance in case the feedback is not received through the portal. The call centre also assists in filling the appeal.", height=600)
    
    def initialize_ui_categories(self):
        df = pd.read_csv('data/Complaint_Category.csv')
        #print(df.columns)
        required_df = df[["Category","ParentCategory","OrgCode"]].sort_values(by=['Category'])
        new_row=["All",np.nan,"ALL"]
        required_df.loc[len(required_df)]=new_row
        new_row1=["All","All","ALL"]
        required_df.loc[len(required_df)]=new_row1
        required_df_1=required_df[required_df['ParentCategory'].isna()].sort_values(by=['Category'])
        #print(required_df_1)

        # Create the primary dropdown for Category and selected value is assigned to var
        selected_category = self.st_obj.selectbox("Department/Ministry", required_df_1['Category'].unique())
        
        # Filter the dataframe based on the selected category
        filtered_df = required_df[required_df['ParentCategory'] == selected_category]
        selected_org_code=filtered_df["OrgCode"].unique()[0]
        #print(selected_org_code)
        self.department=selected_category
        selected_sub_category=self.st_obj.selectbox("Categories"+self.department, filtered_df['Category'].unique())
        #print(selected_sub_category)
        sub_category_df=required_df[(required_df['ParentCategory']==selected_sub_category) &(required_df["Category"]!=selected_sub_category) & (required_df["OrgCode"]==selected_org_code)]
        sub_category_df=sub_category_df[["Category","ParentCategory"]]
       

    def get_input_query(self):
        user_question = self.st_obj.text_input("**YOUR QUERIES**")
        
        self.inp_query=user_question

    def initialize_ui(self):
        self.st_obj.set_page_config("DARPG Chatbot")
        self.st_obj.header("DARPG Grievances Chatbot") 
        self.initialize_ui_categories()
        self.initialize_ui_sidebar()
    def return_out(self):   

        if self.department !='All':
            prompt = PromptTemplate(input_variables=["concept"], template="Answer to the ask {concept} from "+self.department+" Department")
        else:
            prompt = PromptTemplate(input_variables=["concept"], template="Answer the {concept} from all DARPG Departments")
     
    
        llm = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.0)
        chain = LLMChain(llm=llm, prompt=prompt)

        #concatenate history
        self.chat_history +="**You asked :**"
        self.chat_history +=self.inp_query
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []
        st.session_state['chat_history'].append(("**Queried**", self.inp_query))


        #output = chain.invoke(self.inp_query)
        print(self.chat_history)
        output = chain.invoke(self.chat_history)
        
        #capture response in history text
        self.chat_history +="**Bot's answer:**"
        self.chat_history +=output["text"]
        print(self.chat_history)

        return output["text"]

    def process(self):
        if self.st_obj.button("Retreive Information"):

            with self.st_obj.spinner("Retrieving Information..."):
                llm_resp = self.return_out()
                self.st_obj.session_state['chat_history'].append(("**Bot's answer**", llm_resp))
                self.st_obj.write(llm_resp)

            

def main():
    initialize_ai_env()
    grievanceRedressal_obj=grievanceRedressal(st)
    grievanceRedressal_obj.initialize_ui()
    grievanceRedressal_obj.get_input_query()
    grievanceRedressal_obj.process()
    


if __name__=="__main__":
    main()