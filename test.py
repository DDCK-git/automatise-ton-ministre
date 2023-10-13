import gradio as gr
import openai
import os
openai.api_key = os.getenv('openapi_key')

def gpt3(prompt):
    system_prompt = f"test prompt" 

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ])
    return response.choices[0].message['content']

iface = gr.Interface(fn=gpt3, inputs="text", outputs="text")
iface.launch()