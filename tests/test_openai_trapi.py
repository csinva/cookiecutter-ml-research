# Required packages
from openai import AzureOpenAI
from azure.identity import ChainedTokenCredential, AzureCliCredential, ManagedIdentityCredential, get_bearer_token_provider

#Authenticate by trying az login first, then a managed identity, if one exists on the system)
scope = "api://trapi/.default"
credential = get_bearer_token_provider(ChainedTokenCredential(
    AzureCliCredential(),
    ManagedIdentityCredential(),
), scope)

api_version = '2024-12-01-preview'  # Ensure this is a valid API version see: https://learn.microsoft.com/en-us/azure/ai-services/openai/api-version-deprecation#latest-ga-api-release
deployment_name = 'gpt-4o_2024-08-06'  # Ensure this is a valid deployment name see https://aka.ms/trapi/models for the deployment name
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
            "content": "Give a one word answer, what is the capital of France?",
        },
    ]
)

#Parse out the message and print
response_content = response.choices[0].message.content
print(response_content)