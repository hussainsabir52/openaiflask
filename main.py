import os
from flask import Flask, request
import openai
import flask
import random

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello Darkness My Old Friend!"

@app.route("/completion-engine", methods=['POST'])
def completionEngine():
    request_data = request.get_json()
    # #openai body parameters
    openai.api_key=request.headers.get('api_key');
    openai.organization=request.headers.get('organization')
    openai_engine=request_data['engine']
    openai_prompt=request_data['prompt']
    openai_temperature=request_data['temperature']
    openai_maxtokens=request_data['max_tokens']
    openai_stop=request_data['stop']
    
    ## Completion Request
    response = openai.Completion.create(
    engine=openai_engine,
    prompt=openai_prompt,
    temperature=float(openai_temperature),
    max_tokens=int(openai_maxtokens),
    stop=openai_stop,
    user=str(random.getrandbits(32))
    )
    
    text=response['choices'][0]['text']
    token_count=(len(text)/4)
    openai_content_to_verify = response['choices'][0]['text']
    
    ## Toxicity Check
    filter_response = openai.Completion.create(
      engine="content-filter-alpha",
      prompt = "<|endoftext|>"+openai_content_to_verify+"\n--\nLabel:",
      temperature=0,
      max_tokens=1,
      logprobs=10
    )
    
    ## Toxicity Result Label
    filter_output_label=filter_response['choices'][0]['text']
    return flask.jsonify({"completion":response['choices'][0]['text'], "token_length":token_count,"toxicity":filter_output_label})

@app.route("/completion-model", methods=['POST'])
def completionModel():
    request_data = request.get_json()
    print(request_data)
    ## Openai body parameters
    openai.api_key=request.headers.get('api_key');
    openai.organization=request.headers.get('organization')
    openai_model=request_data['model']
    openai_prompt=request_data['prompt']
    openai_temperature=request_data['temperature']
    openai_maxtokens=request_data['max_tokens']
    openai_stop=request_data['stop']
    
    ## Completion Request
    response = openai.Completion.create(
    model=openai_model,
    prompt=openai_prompt,
    temperature=float(openai_temperature),
    max_tokens=int(openai_maxtokens),
    stop=openai_stop,
    user=str(random.getrandbits(32))
    )
    text=response['choices'][0]['text']
    token_count=(len(text)/4)
    openai_content_to_verify = response['choices'][0]['text']
    
    ## Toxicity Check
    filter_response = openai.Completion.create(
      engine="content-filter-alpha",
      prompt = "<|endoftext|>"+openai_content_to_verify+"\n--\nLabel:",
      temperature=0,
      max_tokens=1,
      logprobs=10
    )
    
    ## Toxicity Result Label
    filter_output_label=filter_response['choices'][0]['text']
    return flask.jsonify({"completion":response['choices'][0]['text'], "token_length":token_count, "toxicity":filter_output_label})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))