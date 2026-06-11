from google import genai

client = genai.Client(
    api_key="AIzaSyAtffjqt53lzeFcxoTD-f0o0wzb_w5ufe0"
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hello"
)

print(response.text)