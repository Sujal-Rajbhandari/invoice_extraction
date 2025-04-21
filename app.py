from dotenv import load_dotenv
import json 
load_dotenv()
import streamlit as st 
import os 
from PIL import Image
import google.generativeai as genai
import re 

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def invoice_info(image): 
    prompt = """
    You need to extract key information from given image.
    From the invoice/bill image that it provided extract and return the following field in valid JSON format only
    {
    "Invoice_Date": "...",
    "Invoice_Number": "...",
    "Invoice_Amount": "..." ,
    "Items": [
        {
            "name": "...",
            "description": "...",
            "quantity": "...",
            "unit_price": "...", 
        }
        ]
    } 
    If a field is not found then return keep it as none value
    Do not include explanations, markdown formatting, or anything else. Only return raw JSON.
    """
    response = model.generate_content([image[0],prompt])
    return response.text
    
# def get_gemini_reponse(input,image,prompt):
#     reponse = model.generate_content([input,image[0],prompt])
#     return reponse.text

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
    
st.set_page_config(page_title = "Invoice extraction")
st.header("Information Extraction from Invoice")

# input = st.text_input("Enter your prompt: ", key = "input")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
# image = ""


if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width = True)
    
    if st.button("Tell me about the invoice"):
# converting upload image into gemini format
        image_data = input_image_details(uploaded_file)
        try:
            response_text = invoice_info(image_data) #sned image to gemini
            if not response_text.strip(): #no reponse then error 
                raise ValueError("Empty response from Gemini")

            json_str = re.search(r"\{.*\}", response_text, re.DOTALL).group() #extracting all the key inforamtion from the function prompt all informatiion inside {} 
            response_json = json.loads(json_str)
            st.subheader("Extracted Invoice Data:")
            st.json(response_json)

        except Exception as e:
            st.error(" Failed to extract valid JSON from model's response.")
            if 'response_text' in locals():
                st.subheader("Raw Gemini Response:")
                st.code(response_text)
            st.exception(e)
