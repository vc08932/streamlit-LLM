import os
# Detect the existance of the OpenAI api Key
if os.path.exists(".streamlit/secrets.toml") == False:
    key = input("OpenAI Key:")
    
    if os.path.exists(".streamlit") == False: # Detect the existance of the folder
        os.makedirs(".streamlit")
        
    with open(".streamlit/secrets.toml","w") as keyfile:
        keyfile.write("openai_api =" + "'" + key + "'")
        print("OpenAI api Key is successfully configured.")
        
else:
    print("There is OpenAI api key already.")