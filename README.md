<h1 align = "center">Invoice Extraction App with Gemini</h1>

<h3>✨Key Features</h3>
	
| Feature | Description |
|---------|-------------|
| **📤 Upload Support** | Accepts .jpg, .jpeg, .png invoice/bill images |
| **🤖 Gemini API Integration **|Uses Google's Gemini 1.5 Flash to extract invoice data |
| **✅ JSON Output** |Returns a well-formatted JSON containing key fields from the invoice |
| **🔍 Data Validation** | Ensures valid types and prevents negative values using Pydantic |
|** 🕒 Time Profiling** | Shows how long Gemini takes to process each image|

<h3>🚀 Quick Start</h3>

```bash
pip install -r requirements.txt
```
Create a .env file in the root directory and add your google gemini API key
```bash
GOOGLE_API_KEY=your_gemini_api_key_here
```
**🔑 Steps For Getting Your Gemini API Key (Google AI Studio)**

1. Visit Google AI Studio.

2. Sign in with your Google account.

3. Click on "Create API Key".

4. Copy the generated key.

<h2>🛠️ Installation From Source</h2>

```bash
git clone https://github.com/your-username/invoice-extractor.git
cd invoice-extractor
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

<h2>🧪 How to Run the App</h2>
Paste this code on your terminal

```bash
streamlit run app.py
```
Now visit:  http://localhost:8501

<h2>📄 Ouput Overview</h2>

**After running "streamlit run app.py" command you will see a streamlit UI where you can upload a invoice to extract information.**

![upload](https://github.com/user-attachments/assets/53ddf299-230b-48b7-85f0-44bf3a758c04)

**Then upload a invoive and click "Tell me about this invoice" to get extracted information. Wait for a while streamlit might take few seconds to run.⏱️**

![Screenshot 2025-04-25 170647](https://github.com/user-attachments/assets/f2316ec9-fb65-4a74-b451-ef9bf1219f59)

![Screenshot 2025-04-25 170653](https://github.com/user-attachments/assets/a23515ca-4d51-40e0-b375-16971a0831ad)

**As you can see the streamlit app did provide us with information in valid json format**

<h2>⏱️ Processing Time</h2>
Average time to extract a single invoice using Gemini:
1. 3-10 seconds
2. Gemini 1.5 Flash model is used for fast response

<h2>💰 Cost Estimation</h2>

**Wondering how much it costs to process invoices with Gemini?** 

| **Volume** | **Estimated Cost** |
|---------|-------------|
| 1 invoice |  $0.0003 |
| 100 invoice| $0.03 |
| 5,00 invoice| $0.15 |
| 1,000 invoice| $0.3 |
| 10,000 invoice| $3 |
| 25,000 invoice| $7.5 |
| 50,000 invoice| $15 |

Calculation: 
Tentative price token from google AI for Developers Input: $0.075, prompts <= 128k tokens, output: $0.30, prompts <= 128k tokens
 (https://ai.google.dev/gemini-api/docs/pricing)
<em>Note: Paid Tier, per 1M tokens in USD</em>

A 1 million would not be appopratie for a company so lets begin our calculation for 1 invoice. 

<p>
Lets say a large size image takes 800 tokens: <br>
Tokens = 800 <br>
Input price: $0.075 <br>
Output price: $0.30 <br> 

So based on given data; <br>
Total price for input  = 800/10,00,000*0.075<br> 
			= 0.00006 <br>
Total price for output = 800/10,00,000*0.30 <br>
			= 0.00024 <br> 

**Total price for one invoice** = 0.0006+0.00024  <br>
				= 0.0003


</p>






