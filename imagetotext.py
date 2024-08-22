import requests
import streamlit as st

API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
headers = {"Authorization": "Bearer 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"}


def query(image_file):
    data = image_file.read()
    response = requests.post(API_URL, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"API request failed with status code {response.status_code}"}


st.title("Image to text")

image_file = st.file_uploader("Upload an Image", type="jpg")

if st.button("Generate Caption"):
    if image_file is not None:
        with st.spinner("Generating caption..."):
            output = query(image_file)
            if 'error' in output:
                st.error(output['error'])
            else:
                # Print the output for debugging purposes
                st.write("Raw output:", output)

                # Check if output is a list and handle accordingly
                if isinstance(output, list) and len(output) > 0:
                    caption = output[0].get('caption', 'No caption returned') if isinstance(output[0],
                                                                                            dict) else 'No caption returned'
                    st.write("Caption:", caption)
                else:
                    st.write("Caption:", 'No caption returned or unexpected response format')
    else:
        st.error("Please upload an image first.")
