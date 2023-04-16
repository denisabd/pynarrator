import openai
import json
import os

def gpt_get_completions(
  prompt,
  openai_api_key=os.getenv("OPENAI_API_KEY")
  ):
    
  # Set up the OpenAI API client
  # model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
  # max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", 1024))
  # temperature = float(os.getenv("OPENAI_TEMPERATURE", 1))
  # top_p = float(os.getenv("OPENAI_TOP_P", 1))
  # frequency_penalty = float(os.getenv("OPENAI_FREQUENCY_PENALTY", 0))
  # presence_penalty = float(os.getenv("OPENAI_PRESENCE_PENALTY", 0))

  messages = [
    {"role": "system",
      "content": "You are a helpful assistant with extensive business knowledge."},
    {"role": "user",
      "content": prompt}
  ]
          
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
  )
  
  return(completion.choices[0].message.content)

def enhance_narrative(
  narrative,
  openai_api_key=os.getenv("OPENAI_API_KEY")
):

  prompt = f'Improve the narrative by adding better business language for the following: "{narrative}"'
  output = gpt_get_completions(prompt, openai_api_key=openai_api_key)

  return(output)

def translate_narrative(
  narrative,
  language,
  openai_api_key=os.getenv("OPENAI_API_KEY")
):

  prompt = f'Using professional language translate the following text to {language}: "{narrative}"'
  output = gpt_get_completions(prompt, openai_api_key=openai_api_key)

  return(output)

def summarize_narrative(
  narrative,
  openai_api_key=os.getenv("OPENAI_API_KEY")
):

  prompt = f'Summarize the following narrative to make it shorter: "{narrative}"'
  output = gpt_get_completions(prompt, openai_api_key=openai_api_key)

  return(output)