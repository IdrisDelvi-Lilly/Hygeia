import logging 

import azure.functions as func 

bp = func.Blueprint() 

@bp.route(route="ask")
def http_ask(req: func.HttpRequest) -> func.HttpResponse: 
    logging.info('Python HTTP trigger function processed a request.') 

    name = req.params.get('name') 
    if not name: 
        try: 
            req_body = req.get_json() 
        except ValueError: 
            pass 
        else: 
            name = req_body.get('name') 

    if name: 
        return func.HttpResponse( 
            f"Hello, {name}. This HTTP-triggered function " 
            f"executed successfully.") 
    else: 
        return func.HttpResponse( 
            "This HTTP-triggered function executed successfully. " 
            "Pass a name in the query string or in the request body for a" 
            " personalized response.", 
            status_code=200 
        )
        
@app.route(route='ask', auth_level='anonymous', methods=['POST'])
def main(req):

    prompt = req.params.get('prompt') 
    if not prompt: 
        try: 
            req_body = req.get_json() 
        except ValueError: 
            raise RuntimeError("prompt data must be set in POST.") 
        else: 
            prompt = req_body.get('prompt') 
            if not prompt:
                raise RuntimeError("prompt data must be set in POST.")

    # Get managed identity token and env vars
    creds = DefaultAzureCredential()
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    embedding_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    
    kernel = Kernel()

    service_id = "manuallookup"

    azure_chat_service = AzureChatCompletion(
                            service_id=service_id,
                            deployment_name=deployment,
                            endpoint=endpoint,
                            credentials=creds,
                        )

    embedding_gen = AzureTextEmbedding(service_id="embedding", deployment_name=embedding_deployment)
    kernel.add_service(azure_chat_service)
    kernel.add_service(embedding_gen)

def generate_prompt(prompt):
    capitalized_prompt = prompt.capitalize()

    # Chat
    return f'The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: {capitalized_prompt}' 

    # Classification
    #return 'The following is a list of companies and the categories they fall into:\n\nApple, Facebook, Fedex\n\nApple\nCategory: ' 

    # Natural language to Python
    #return '\"\"\"\n1. Create a list of first names\n2. Create a list of last names\n3. Combine them randomly into a list of 100 full names\n\"\"\"'
