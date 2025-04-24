from dotenv import load_dotenv
import json 
import streamlit as st 
import os 
from PIL import Image
import google.generativeai as genai
import re 
import time 
from typing import List, Optional
from pydantic import BaseModel, ValidationError, validator

load_dotenv()
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

#validation
class ItemModel(BaseModel):
    name: Optional[str] = None 
    description: Optional[str] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None

class InvoiceModel(BaseModel):
    Invoice_Date: Optional[str]
    Invoice_Number: Optional[int] 
    Invoice_Amount: Optional[float] 
    Items: List[ItemModel]

#sending prompt to gemini 
def invoice_info(image): 
    response = model.generate_content([image[0],prompt])
    return response.text

#conver invoice into gemini format 
def input_image_details(uploaded_file):
        bytes_data = uploaded_file.getvalue()
        return  [{
            "mime_type": uploaded_file.type,
            "data": bytes_data}]

#streamlit application
st.set_page_config(page_title = "Invoice extraction")
st.header("Information Extraction from Invoice")

#form to upload image and extract only after submission  
with st.form("invoice_form"):
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    submitted = st.form_submit_button("Tell me about this invoice")

if submitted and uploaded_file:
    st.image(Image.open(uploaded_file), caption="Uploaded Image", use_container_width = True)

#time taken for gemini to extract information 
    image_data = input_image_details(uploaded_file)  # converting upload image into gemini format
    start_time = time.time()
    response_text = invoice_info(image_data) #sned image to gemini
    end_time = time.time()
    processing_time = end_time - start_time
    st.success(f"Processing time: {processing_time: .2f} seconds")

    if not response_text.strip(): 
        st.error("Empty ressponse from gemini")
    else:
        try: 
            match = re.search(r"```json(.*?)```", response_text, re.DOTALL)
            json_str = match.group(1).strip() if match else re.search(r"\{.*\}", response_text, re.DOTALL).group()
            parsed_data = json.loads(json_str)
            invoice = InvoiceModel(**parsed_data)
            st.subheader("Extracted Invoice Information:")
            st.json(invoice.dict())
        except (ValidationError, json.JSONDecodeError) as e:
            st.error("Failed to validate or parse the response.")
            st.code(response_text)
            st.exception(e)


