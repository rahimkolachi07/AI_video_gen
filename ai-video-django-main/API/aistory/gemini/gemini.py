import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

import os
os.environ['GOOGLE_API_KEY']="AIzaSyAmkjiWkiTRY0QBJwsNvCscd3-HAqtXZF4"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    pass
def g_model(text):
  try:
    os.environ['GOOGLE_API_KEY']="AIzaSyCMlyvJiFRkunaFHmEhuZYzG8ei5RVU3qM"
    genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
    for m in genai.list_models():
      if 'generateContent' in m.supported_generation_methods:
        pass
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(text)
    return response.text
  except:
    try:
      os.environ['GOOGLE_API_KEY']="AIzaSyDYfGn8RMp85kuUikHoVNqkkjhC1P9wHZk"
      genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
      for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
          pass
      model = genai.GenerativeModel('gemini-pro')
      response = model.generate_content(text)
      return response.text
    except:
      try:
        os.environ['GOOGLE_API_KEY']="AIzaSyCMAWxf99ou5JwIJgJTmSbojM8XzyBvnMo"
        genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
        for m in genai.list_models():
          if 'generateContent' in m.supported_generation_methods:
            pass
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(text)
        return response.text
      except:
        try:
          os.environ['GOOGLE_API_KEY']="AIzaSyCkpcSTKFNA2t5xoMJ89A1OJW1xctj4pRs"
          genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
          for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
              pass
          model = genai.GenerativeModel('gemini-pro')
          response = model.generate_content(text)
          return response.text
        except:
          os.environ['GOOGLE_API_KEY']="AIzaSyAwZ6_dfUJhYCzKUWN4I3JOmbl6Ihjn36U"
          genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
          for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
              pass
          model = genai.GenerativeModel('gemini-pro')
          response = model.generate_content(text)
          return response.text
