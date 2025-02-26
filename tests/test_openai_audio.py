from openai import OpenAI
import requests
import base64
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider, AzureCliCredential

azure_credential = AzureCliCredential()
token_provider = get_bearer_token_provider(
    azure_credential,
    "https://cognitiveservices.azure.com/.default"
)


client = AzureOpenAI(
    api_version="2025-01-01-preview",
    azure_endpoint="https://neuroaiservice.cognitiveservices.azure.com/openai/deployments/gpt-4o-audio-preview/chat/completions?api-version=2025-01-01-preview",
    azure_ad_token_provider=token_provider,
)


# read in audio file
wav_file = "fklc1_si2308.wav"
with open(wav_file, "rb") as wav_file:
    wav_data = wav_file.read()
encoded_string = base64.b64encode(wav_data).decode('utf-8')

completion = client.chat.completions.create(
    model="gpt-4o-audio-preview",
    modalities=["text", "audio"],
    audio={"voice": "alloy", "format": "wav"},
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What text is in this recording?"
                },
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": encoded_string,
                        "format": "wav"
                    }
                }
            ]
        },
    ]
)

print(completion.choices[0].message)
print()
