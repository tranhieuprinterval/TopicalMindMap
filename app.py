from openai import OpenAI
import streamlit as st
import time


# Setting page title and header
st.set_page_config(page_title="The SEO Works Topical Mind Map Generator", 
                   page_icon="https://www.seoworks.co.uk/wp-content/themes/seoworks/assets/images/fav.png", 
                   layout="wide",initial_sidebar_state="collapsed")

#Defines custom css file
with open( "resources/style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
file_name="resources/style.css"

# custom styling to remove red bar at top
st.markdown("""
<style>
	[data-testid="stDecoration"] {
		display: none;
	}
</style>                
            """, unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
   st.header("")
   
with col2:
   st.header("")
   st.image("resources/SeoWorksLogo-Dark.png")

with col3:
   st.header("")


st.markdown('<div style="text-align: center; font-size:36px;"><strong>Topical Mind Map Generator by The SEO Works<strong></div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; font-size:22px;">Uncover all aspects of your chosen topic with a structured mind map</div>', unsafe_allow_html=True)

# Spacers for layout purposes
st.write("#")

st.markdown(
        """
        <style>
        .stMarkdownContainer p {
            font-size: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


with st.expander("How it works"):
    st.write("Struggling with a blank page when it comes to brainstorming ideas around a topic? Use our tool to spark your \
             creativity and generate a comprehensive mind map bursting with relevant ideas. Enter your top level subject to \
             reveal a hierarchical mind map of topics and semantically related sub-topics. You will also receive a vast network \
             of related nouns and predicates to give further context to your writing.")


topic = st.text_input("Enter your topic", placeholder="Add your topic")


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"]) 

#  client = OpenAI(api_key=api_key) 

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []
        
#if topic := topic:
prompt = "Act as a Topical Mind Map Generator. Your Topic is "+topic+". Please consider all relevant nouns/predicates related to the topic, such as specific products or \
categories, as well as any specific purposes, qualities, or features that are relevant. Ensure that at least 100 nouns/predicates related to the topic are provided. \
You will then generate a topical map with each category and its corresponding subtopics based on the provided nouns. Present this map in table format. To represent the \
mind map in a table format, structure the table to reflect the hierarchy of the mind map, starting from the central concept down to primary, secondary, and tertiary \
branches where applicable. Each level of the hierarchy will be represented in the table, showing the progression from general categories to more specific subtopics.\
Beneath the topical map you will create a table of nouns and semantially related keywords related to the topic."
    
with st.form("Response_form", border=False, clear_on_submit=True):
    st.session_state.messages.append({"role": "user", "content": prompt})
    #with st.chat_message("user"):
    #    st.markdown("Here are the title ideas for your content")

    submitted = st.form_submit_button("Get your topical mind map")
    if submitted:
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("assistant", avatar="https://www.seoworks.co.uk/wp-content/themes/seoworks/assets/images/fav.png"):
                    st.markdown("***Here is your topical mind map...***")
                    stream = client.chat.completions.create(
                        model=st.session_state["openai_model"],
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ],
                        stream=True,
                    )
        

            response = st.write_stream(stream)

            st.session_state.messages.append({"role": "assistant", "content": response})

st.divider()
# Spacers for layout purposes
st.write("#")

st.markdown('<div style="text-align: center; font-size:30px;"><strong>About The SEO Works<strong></div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; font-size:22px;">We are the Digital Growth Experts. As an award-winning provider of digital \
            marketing and websites to leading brands, we have worked for more than a decade with one key goal in mind - to get businesses more \
            customers online. Find out more <a href ="https://www.seoworks.co.uk/" target="_blank" > about us</a>.</div>', unsafe_allow_html=True)

st.write("#")

st.markdown('<div style="text-align: center; font-size:14px;">Check out our other <a href = "https://www.seoworks.co.uk/resources/downloads/">resources</a>.</div>', unsafe_allow_html=True)


