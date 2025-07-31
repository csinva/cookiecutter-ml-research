from openai import AzureOpenAI
import os
from azure.identity import ChainedTokenCredential, AzureCliCredential, ManagedIdentityCredential, get_bearer_token_provider
client_id = os.environ.get("AZURE_CLIENT_ID")

scope = "https://cognitiveservices.azure.com/.default"
credential = get_bearer_token_provider(ChainedTokenCredential(
    # AzureCliCredential(), # first check local
    ManagedIdentityCredential(client_id=client_id)
), scope)



if __name__ == '__main__':
    client = AzureOpenAI(
        api_version="2025-01-01-preview",
        azure_endpoint="https://dl-openai-1.openai.azure.com/",
        azure_ad_token_provider=credential,
    )

    response = client.chat.completions.create(  # replace this value with the deployment name you chose when you deployed the associated model.
        # model='gpt-4o',
        # model='gpt-4o-mini',
        # model='gpt-4.1',
        model='o4-mini',
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "2+3="}
        ],
        # temperature=0,
    )
    print(response.choices[0].message.content)
