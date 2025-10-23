import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/query"

st.set_page_config(page_title="Document Query App", layout="centered")

st.title("Chat with your Doc")

st.text("")

st.markdown("Ask something about your documents!")

st.write("")

query = st.text_input("Enter your question about the documents:", placeholder="Don't ask hard questions !!!!!")

st.text("")

if st.button("Ask"):
    if query.strip() == "":
        st.warning("Please enter a valid question.")
    else:
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json={"question": query})
                if(response.status_code == 200):
                    data = response.json()
                    st.subheader("Response...")
                    st.write(data["response"])

                    if(data["sources"]):
                        st.markdown("**Sources:**")
                        st.subheader("Sources...")
                        for src in data["sources"]:
                            st.markdown(f"- {src}")
                else:
                    st.error(f"error - {response.status_code} : {response.text}")
            except Exception as e:
                st.error(f"An error occured: {e}")