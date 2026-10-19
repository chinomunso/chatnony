import streamlit as st
from openai import OpenAI
from datetime import datetime
from PIL import Image
import base64
from io import BytesIO

st.set_page_config(

    page_title="NONY-AI",
    page_icon="Asset 2.png",
    layout="wide",
   
)

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
      
    upload_image=st.file_uploader("image",type=["png","jpeg","jpg","webp"]) 
    camera_image=st.camera_input("photo")
    
    st.markdown("----")
    st.caption(f"Total message:{len(st.session_state.get('message',[]))}")
current_date=datetime.now().strftime("%y-%m-%D")
current_year=datetime.now().year




final_image=None
if upload_image:
    final_image=Image.open(upload_image)
    st.image(final_image,caption="preview")
if camera_image:
    final_image=Image.open(camera_image)
    st.image(final_image,caption="preview")



def encode_image(image):
    buffered=BytesIO()
    img.save(buffered,format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

api_key=st.secrets["OPENROUTER_API_KEY"]
if "history" not in st.session_state:
    st.session_state.history=[]
if "message" not in st.session_state:
    st.session_state.message=[]



            
for msg in st.session_state.message:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "image_data" in msg:
            st.image(msg["image_data"],width=300)
            st.markdown(msg["content"])
        if "timestamp" in msg:
            st.caption(msg["timestamp"])



if prompt:=st.chat_input("ASK NONY"):
    timestamp=datetime.now().strftime("%y-%m-%D %H:%M:%S")
    st.session_state.message.append({

        "role":"user",
        "contents":prompt,
        "timestamp":timestamp
    })
    with st.chat_message("user"):
        if final_image:
            st.image(final_image,width=250)
        st.markdown(prompt)
        user_content={"role":"user","content":prompt}
        if final_image:
            user_content["image_data"]=final_image
            st.session_state.message.append(user_content)
        st.caption(f"*{timestamp}*")
    with st.chat_message("assistant"):
        st.spinner("Nony AI is thinking.......")
        try:
            if final_image:
                base64_img=encode_image(final_image)
                respond_strem=client.chats.completions.create(
                    model="gpt-4o",
                    messages=[{
                                "role":"user",
                                "content":[
                                    {"type":"text","text":prompt},
                                    {
                                        "type":"image_url",
                                        "image_url":{
                                            "url":f"data:image/png;base64,{base64_img}"
                                        }
                                    }
                                ]
                        
                    }],
    
                    max_tokens=500                )
        
                
            messages=[] 
            for msg in st.session_state.message:
                role="assistant" if msg['role']=="assistant" else "user" 
                messages.append({

                    "role":role,
                    "content":msg['contents']
                })
            model_name="openrouter/free"
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
    




