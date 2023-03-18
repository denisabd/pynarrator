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
       "content": "You are a helpful assistant with extensive knowledge of Python programming."},
      {"role": "user",
       "content": prompt}
  ]
          
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
  )
  
  return(completion.choices[0].message.content)
