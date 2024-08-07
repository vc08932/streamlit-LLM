import os

# Detect the existance of the OpenAI api Key
if os.path.exists(".streamlit/secrets.toml") == False:
    key = input("OpenAI API Key: ")
    print("---\nInput a login password to prevent unanticipated access")
    
    password = input("Password: ")
    print("---\n(Opinional) If you need to use a proxy or service emulator only")
    base_url = input("Base_url (Press enter when unneccessary):").rstrip()
    
    if os.path.exists(".streamlit") == False: # Detect the existance of the folder
        os.makedirs(".streamlit")
        
    with open(".streamlit/secrets.toml","w") as keyfile:
        keyfile.write(f'openai_api = "{key}"')
        keyfile.write(f'\nlogin = "{password}"')
        keyfile.write(f'\nbase_url = "{base_url}"')
        print("OpenAI API Key and password is successfully configured.")
        
else:
    print("There are OpenAI API key and login password already.")