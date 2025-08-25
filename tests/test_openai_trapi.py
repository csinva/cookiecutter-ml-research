# Required packages
from openai import AzureOpenAI
from azure.identity import ChainedTokenCredential, AzureCliCredential, ManagedIdentityCredential, get_bearer_token_provider

#Authenticate by trying az login first, then a managed identity, if one exists on the system)
scope = "api://trapi/.default"
credential = get_bearer_token_provider(ChainedTokenCredential(
    AzureCliCredential(), # first check local
    ManagedIdentityCredential(), # then check managed identity (for cluster jobs)
), scope)


# note, should check that the deployment name is valid and matches the appropriate API version here: https://aka.ms/trapi/models
# api_version = '2024-10-21'
# deployment_name = 'gpt-4o_2024-08-06'  
# deployment_name = 'o3_2025-04-16'

api_version = '2024-12-01-preview'
deployment_name = 'gpt-5_2025-08-07'

instance = 'gcr/shared' # See https://aka.ms/trapi/models for the instance name
endpoint = f'https://trapi.research.microsoft.com/{instance}'

#Create an AzureOpenAI Client
client = AzureOpenAI(
    azure_endpoint=endpoint,
    azure_ad_token_provider=credential,
    api_version=api_version,
)

#Do a chat completion and capture the response
response = client.chat.completions.create(
    model=deployment_name,
    messages=[
        {
            "role": "user",
            "content": "Give a one word answer, what is the capital of Spain?",
        },
    ]
)

#Parse out the message and print
response_content = response.choices[0].message.content
print(response_content)