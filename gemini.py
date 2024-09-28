from google.cloud import aiplatform
import google.generativeai as genai
import os
import numpy as np
    

genai.configure(api_key = os.environ["GENAI_KEY"])

PROJECT_ID = 647051127337  # @param {type:"string"} ENV VARIABLE
LOCATION = "us-central1"  # @param {type:"string"}


'''
from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
    HarmCategory,
    HarmBlockThreshold,
    Part,
)
'''
model = genai.GenerativeModel("gemini-1.5-flash")
system_instruction = "You are a redditor"



def produceOutput(prompt, storyStyle):
    
    strn = model.generate_content("Create a reddit post for "+prompt+ " based on the "+storyStyle+ " posts on reddit, 100 words long. Include specific details, with no placeholders, like [Insert details here]")
    return strn

def main():
    print(produceOutput("duke dennis rizz battle lore","AITA"))

main()