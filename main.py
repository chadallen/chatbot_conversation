#https://replit.com/@chadallen/chatbotconversation

import openai
import os
from flask import Flask, request, render_template, jsonify

openai.api_key = os.environ['api_key']

def chat_simulation(iterations, temperature, max_tokens, chatbot1_name, chatbot1_personality, chatbot2_name, chatbot2_personality, initial_conversation_text):


    conversation_history = f"{chatbot1_name}   {chatbot1_personality} and {chatbot2_name} {chatbot2_personality}. {chatbot1_name} and {chatbot2_name}, are having a conversation about {initial_conversation_text}.\n\n"
  
    results = []

    for i in range(iterations):
        print(conversation_history)
        response = chat_gpt(conversation_history + f"{chatbot1_name}: ", temperature, max_tokens)
        conversation_history += f"{chatbot1_name}: " + response + "\n"
        results.append(f"{chatbot1_name}: " + response + "\n")
       # if i > 0:
        response = chat_gpt(conversation_history + f"{chatbot2_name}: ", temperature, max_tokens)
        conversation_history += f"{chatbot2_name}: " + response + "\n"
        results.append(f"{chatbot2_name}: " + response + "\n")  
    
        print(results)
        print(i)

    return results

def chat_gpt(prompt, temperature, max_tokens):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop = "\n"
    )
    return response.choices[0].text.strip()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        iterations = int(request.form.get('iterations', 0))
        temperature = float(request.form.get('temperature', 0))
        max_tokens = int(request.form.get('max_tokens', 0))
        chatbot1_name= str(request.form.get('chatbot1_name', '0'))
        chatbot2_name = str(request.form.get('chatbot2_name', '0'))
        chatbot1_personality = str(request.form.get('chatbot1_personality', ''))
        chatbot2_personality = str(request.form.get('chatbot2_personality', ''))
        initial_conversation_text = str(request.form.get('initial_conversation_text', ' '))

        return jsonify(chat_simulation(iterations, temperature, max_tokens, chatbot1_name, chatbot1_personality, chatbot2_name, chatbot2_personality, initial_conversation_text))
    else:
        return render_template('index.html')

app.run(host='0.0.0.0', port=81)
