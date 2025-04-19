from dotenv import load_dotenv
load_dotenv() 
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_reponse(input,image,prompt):
    reponse = model.generate_content([input,image[0],prompt])
    return reponse.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{
            "mime_type": uploaded_file.type,
            "data": bytes_data}
        ]
        return image_parts
    else:
        return FileNotFoundError("No file uploaded")
    
st.set_page_config(page_title = "Inice extraction")
st.header("Gemini Application")
input = st.text_input("Enter your prompt: ", key = "input")
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
submit_button = st.button("Tell me about the invoice")
input_prompt = """
You are an expert in invoice extraction.
You are given an image of an invoice. We will upload a image as invoice and you will have to answer any questions based on the uploaded image
"""
if submit_button:
    image_data = input_image_details(uploaded_file)
    reponse = get_gemini_reponse(input,image_data,input_prompt)
    st.subheader("The response is: ")
    st.write(reponse)

