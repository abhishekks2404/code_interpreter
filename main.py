import os
import asyncio
import streamlit as st
from codeinterpreterapi import CodeInterpreterSession, File
import uuid
from dotenv import load_dotenv

# load_dotenv()


# deployment_name: str = "gpt-3.5-turbo-16k"
# openai_api_type: str = "azure"
# openai_api_base: str = os.getenv("OPENAI_ENDPOINT")
# openai_api_version: str = "2023-03-15-preview"
# openai_api_key: str = st.secrets["OPENAI_API_KEY"]

# Set verbose mode to display more information
os.environ["VERBOSE"] = "True"
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": """Hello! How may I assist you?""" }]

if "images" not in st.session_state:
    st.session_state.images = []
images = []
def main():
    st.title("Code Interpreter")
    


    with st.sidebar:
        st.subheader("Upload File to Chat")
        uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True,type=[".csv",".txt",".py",".json"])

        uploaded_files_list = []
        for uploaded_file in uploaded_files:
            bytes_data = uploaded_file.read()
            uploaded_files_list.append(File.from_bytes(name=uploaded_file.name,
                                                content=bytes_data))
            
        if st.session_state.images:
            st.header("Extracted Images:")
            count = 1
            for image in st.session_state.images:
                
                st.image(image, caption=f'Image : {count}', use_column_width=True)
                count = count +1
            

                
    for message in st.session_state.messages:
        st.chat_message(message["role"]).markdown(message["content"])                
    # if(st.session_state.bool):
    #     if(st.session_state.name):
    #             with st.spinner("Thinking..."):

    #st.chat_message("assistant").markdown(f"""Hello! How may I assist you? """)
    
                    
 
    if prompt :=  st.chat_input("Ask me anything"):
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            async def run_code_interpreter():
                with st.spinner("Thinking..."):
                
                    async with CodeInterpreterSession(model='gpt-3.5-turbo-16k') as session:
                        response = await session.generate_response(prompt, files=uploaded_files_list)
                
                        
                        st.chat_message("assistant").markdown(response.content)
                
                    for file in response.files:
                    # Display the image content as bytes
                        st.image(file.content,use_column_width=True, caption=file.name)

                        st.session_state.images.append(file.content)
                        

                    
                    st.session_state.messages.append({"role": "assistant", "content": response.content})
            asyncio.run(run_code_interpreter())
        
    # User input for the prompt
    #prompt = st.text_input("Enter Prompt")
    

    # Button to submit the request
    #button = st.button("Submit")

    # Check if the button was clicked
    # if button and prompt:
    #     async def run_code_interpreter():
    #         async with CodeInterpreterSession(model='gpt-3.5-turbo-16k') as session:
    #             response = await session.generate_response(prompt, files=uploaded_files_list)
                
    #             st.write("AI Output:")
    #             st.write(response.content)
                
    #             for file in response.files:
    #                 # Display the image content as bytes
    #                 st.image(file.content,use_column_width=True, caption=file.name)
                    
    #     # Run the asyncio event loop
    #     asyncio.run(run_code_interpreter())

if __name__ == "__main__":
    with open("style.css") as source_des:
        st.markdown(f"<style>{source_des.read()}</style>", unsafe_allow_html=True)

    main()