import os
from flask import Flask, request
import openai
import flask
app = Flask(__name__)


@app.route("/")
def home():
    return "Hello Darkness My Old Friend!"

@app.route("/completion-engine", methods=['POST'])
def completionEngine():
    #openai body parameters
    openai.api_key=os.getenv("OPENAI_API_KEY");
    openai_engine=request.form['engine']
    openai_prompt=request.form['prompt']
    openai_temperature=request.form['temperature']
    openai_maxtokens=request.form['max_tokens']
    openai_stop=request.form['stop']
    
    #completion endpoint
    response = openai.Completion.create(
    engine=openai_engine,
    prompt=openai_prompt,
    temperature=float(openai_temperature),
    max_tokens=int(openai_maxtokens),
    stop=openai_stop
    )
    
    openai_content_to_verify = response['choices'][0]['text']
    
    filter_response = openai.Completion.create(
      engine="content-filter-alpha",
      prompt = "<|endoftext|>"+openai_content_to_verify+"\n--\nLabel:",
      temperature=0,
      max_tokens=1,
      logprobs=10
    )
    filter_output_label=filter_response['choices'][0]['text']
    return flask.jsonify({"text": response['choices'][0]['text'], "toxicity":filter_output_label})

@app.route("/completion-model", methods=['POST'])
def completionModel():
    return flask.jsonify({"success":True})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))