from dotenv import load_dotenv
import json 
load_dotenv()
import streamlit as st 
import os 
from PIL import Image
import google.generativeai as genai
import re 
import time 

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash", 
                                generation_config = {"response_mime_type":"application/json"})

prompt = """
    You need to extract key information from given image.
    From the invoice/bill image that it provided extract information and strctly return the following field in valid JSON format only
    {
    "Invoice_Date": "YYYY-MM-DD",
    "Invoice_Number": "integer",
    "Invoice_Amount": "float" ,
    "Items": [
        {
            "name": "string",
            "description": "string or null",
            "quantity": "integer",
            "unit_price": "float", 
        }
        ]
    } 
    If a field is not found then return keep it as none value
    Do not include explanations, markdown formatting or anything else. Only return raw JSON.
    """

def invoice_info(image): 
    response = model.generate_content([image[0],prompt])
    return response.text
    
def cost(input_token, output_token): 
    input_cost = (input_token/100000) * 0.075 
    output_cost = (output_token/100000) * 0.30
    total = input_cost + output_cost
    return total

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

def validation(data): 
    items = data.get("Items", [])
    for item in items:
        try:  
            quantity = int(item["quantity"])
            unit_price = float(item["unit_price"])
        except (ValueError, TypeError):
            return False, "Invalid quantity or unit price in the invoice."
    return True, ""


st.set_page_config(page_title = "Invoice extraction")
st.header("Information Extraction from Invoice")


uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])


if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width = True)
    
    if st.button("Tell me about the invoice"):
# converting upload image into gemini format
        image_data = input_image_details(uploaded_file)
        try:
            start_time = time.time()
            response_text = invoice_info(image_data) #sned image to gemini
            end_time = time.time()
            processing_time = end_time - start_time
            st.success(f"Processing time: {processing_time:.2f} seconds")

            input_token_estimate = len(prompt)//4 #estimating the token for input
            output_token_estimate = len(response_text)// 4 
            cost_estimate = cost(input_token_estimate, output_token_estimate) 
            st.success(f"Price for this image: ${cost_estimate:.6f} ")

            if not response_text.strip(): #no reponse then error 
                raise ValueError("Empty response from Gemini")
        
            match = re.search(r"```json(.*?)```", response_text, re.DOTALL)
            if match:
                json_str = match.group(1).strip()
            else:
                json_str = re.search(r"\{.*\}", response_text, re.DOTALL).group()
                
            response_json = json.loads(json_str)


            valid, error_msg = validation(response_json)
            if not valid:
                st.error(f"Validation Error: {error_msg}")
                st.subheader("Raw Gemini Response:")
                st.code(response_text)
            else:
                st.subheader("Extracted Invoice Data:")
                st.json(response_json)

            response_json = json.loads(json_str)
                
        except Exception as e:
            st.error(" Failed to extract valid JSON from model's response.")
            if 'response_text' in locals():
                st.subheader("Raw Gemini Response:")
                st.code(response_text)
            st.exception(e)

