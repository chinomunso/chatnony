import streamlit as st
from google import genai
from google.genai import types
from datetime import datetime


st.set_page_config(

    page_title="NONY-AI",
    page_icon="Asset 2.png",
    layout="wide",
   
)
st.title("NONY AI")
with st.sidebar:
    st.image("Asset 2.png",width=150)
    st.title("NONY TECHS")
    st.markdown("----")

api_key=st.secrets["api_key"]
model_name="gemini-3-flash-preview"
if "history" not in st.session_state:
    st.session_state.history=[]
if "message" not in st.session_state:
    st.session_state.message=[]
if prompt:=st.chat_input("ASK NONY"):
    timestamp=datetime.now().strftime("%y-%m-%d %H:%M:%S")
    st.session_state.message.append({

        "role":"user",
        "contents":prompt,
        "timestamp":timestamp
    })
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(f"*{timestamp}*")
    with st.chat_message("assistant"):
        try:
            contents=[] 
            for msg in st.session_state.message:
                role="model" if msg['role']=="assistant" else "user" 
                contents.append({

                    "role":role,
                    "parts":[{'text':msg['contents']}]
                }) 
            client=genai.Client(api_key=api_key)
            respond_stream=client.models.generate_content_stream(

                model=model_name,
                contents=contents
            )
            respond_placeholder=st.empty()
            full_respond=""
            for chunk in respond_stream:
                if hasattr(chunk,'text') and chunk.text:
                    full_respond+=chunk.text
                    respond_placeholder.markdown(full_respond )
            st.session_state.history.append({"role":"model","text":full_respond})
            respond_placeholder.markdown(full_respond)
            response_timestamp=datetime.now().strftime("%y-%m-%D  %H:%M:%S")
            st.session_state.message.append({
                "role":"assistant",
                "contents":full_respond,
                "timestamp":response_timestamp
            })
        
        except Exception as e:
            st.error(f"error:{str(e)}")
    




