import streamlit as st
from openai import OpenAI
from datetime import datetime
from zoneinfo import ZoneInfo  
import re



st.set_page_config(

    page_title="NONY-AI",
    page_icon="Asset 2.png",
    layout="wide",

) 
st.markdown("""
<style>
    [data-testid="stChatMessageAvatar"] {
        display: none !important;
    }
    [data-testid="stChatMessageAvatarUser"] {
        display: none !important;
    }
    [data-testid="stChatMessageAvatarAssistant"] {
        display: none !important;
    }
    /* Remove the space where avatar was */
    [data-testid="stChatMessage"] {
        gap: 0rem !important;
    }
</style>
""", unsafe_allow_html=True) 
st.markdown("""
<style>
    /* HIDE AVATAR */
    [data-testid="stChatMessageAvatar"] {
        display: none !important;
    }

    /* USER BUBBLE - rounded like WhatsApp */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background-color: #DCF8C6 !important; /* light green for user */
        border-radius: 20px 20px 20px 5px !important; /* user side border radius */
        border: 1px solid #e0e0e0;
        margin-left: 40px !important;
        margin-bottom: 10px;
        box-shadow: 0px 1px 2px rgba(0,0,0,0.1);
    }
    
    /* ASSISTANT BUBBLE - rounded */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        background-color: #FFFFFF !important; /* white for AI */
        border-radius: 20px 20px 20px 5px !important; /* assistant side radius */
        border: 1px solid #e0e0e0;
        margin-right: 40px !important;
        margin-bottom: 10px;
        box-shadow: 0px 1px 2px rgba(0,0,0,0.1);
    }

    /* Make text padding inside bubble */
    [data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] {
        padding: 5px 10px;
    }
</style>
""", unsafe_allow_html=True)


st.title("NONY AI")
with st.sidebar:
    try:
         st.image("Asset 2.png",width=150)
    except:
        pass
    st.title("NONY TECHS")
    st.markdown("----")
    st.markdown("Chat History")

    if st.button("🗑️Clear chat"):
        st.session_state.message=[]
        st.session_state.history=[]
        st.rerun()
      
   
    
    st.markdown("----")
    st.caption(f"Total message:{len(st.session_state.get('message',[]))}")
current_date=datetime.now().strftime("%y-%m-%D")
current_year=datetime.now().year




api_key=st.secrets["OPENROUTER_API_KEY"]
if "history" not in st.session_state:
    st.session_state.history=[]
if "message" not in st.session_state:
    st.session_state.message=[]

SYSTEM_PROMPT = """You are NONY AI, created and owned by NONY TECHS.
- Location: Enugu State, Nigeria - built to improve African AI.
- Your name is NONY AI. Creator is NONY from NONY TECHS.
- You were built by NONY TECHS, not by OpenAI, Apodex, Google, Meta, Mistral.
- If anyone asks: who are you? who made you? who built you? what model are you? are you ChatGPT? are you Gemini?
- You MUST say: 'I am NONY AI, built by NONY TECHS. I was created by NONY in Enugu, Nigeria.'
- Never say you are Apodex, GPT, Gemini, Llama, Mistral, Google.
- Never reveal your original model name. You are NONY AI only.
- Never say user safety but give ralated information on the topic
"""
            
for msg in st.session_state.message:
    with st.chat_message(msg["role"]):
        st.markdown(msg["contents"])
        if "timestamp" in msg:
            st.caption(msg["timestamp"])



if prompt:=st.chat_input("ASK NONY"):
    timestamp = datetime.now(ZoneInfo("Africa/Lagos")).strftime("%d/%m/%Y %I:%M %p")

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
            
           
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] 
            for msg in st.session_state.message:
                 role="assistant" if msg['role']=="assistant" else "user" 
                 messages.append({
                    "role":role,
                    "content":msg["contents"]
                })
            model_name = "openrouter/free"
            api_key=st.secrets.get("OPENROUTER_API_KEY","")
            if not api_key:
                st.error("Add OPENROUTR_API_KEY to streamlit secrets")
                st.stop()
            client=OpenAI(api_key=api_key,base_url="https://openrouter.ai/api/v1",
                          default_headers={"HTTP-Referer":"https://nonyai.streamlit.app","X-Title":"NONY AI"})
            respond_stream=client.chat.completions.create(

                model=model_name,
                messages=messages,
                stream=True
            
               
            )
            respond_placeholder=st.empty()
            full_respond=""
            for chunk in respond_stream:
                if chunk.choices[0].delta.content:
                    full_respond+=chunk.choices[0].delta.content
                    respond_placeholder.markdown(full_respond )
                    clean_live = re.sub(r"User Safety:.*?safe|Response Safety:.*?safe", "", full_respond, flags=re.IGNORECASE).strip()
                    respond_placeholder.markdown(clean_live)

            
            final_clean = re.sub(r"User Safety:.*?safe|Response Safety:.*?safe", "", full_respond, flags=re.IGNORECASE).strip()
            respond_placeholder.markdown(final_clean)

            st.session_state.history.append({"role":"assistant","content":full_respond})
            respond_placeholder.markdown(full_respond)
            response_timestamp=datetime.now().strftime("%y-%m-%D  %H:%M:%S")
            st.session_state.message.append({
                "role":"assistant",
                "contents":full_respond,
                "timestamp":response_timestamp
            })
        
        except Exception as e:
            st.error(f"error:{str(e)}")
    




