import os
# Detect the existance of the OpenAI api Key
if os.path.exists(".streamlit/secrets.toml") == False:
    key = input("OpenAI Key: ")
    print("---\nInput a login password to prevent unexpected access")
    password = input("Password: ")
    
    if os.path.exists(".streamlit") == False: # Detect image.pngthe existance of the folder
        os.makedirs(".streamlit")
        
    with open(".streamlit/secrets.toml","w") as keyfile:
        keyfile.write("openai_api =" + "'" + key + "'")
        keyfile.write("\nlogin =" + "'" + password + "'")
        print("OpenAI api Key and password is successfully configured.")
        
else:
    print("There are OpenAI api key and login password already.")