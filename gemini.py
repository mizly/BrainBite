from google.cloud import aiplatform
import google.generativeai as genai
import os
import numpy as np
import documentReader
gen_ai_key = os.environ.get('GENAI_KEY')
genai.configure(api_key = gen_ai_key)

model = genai.GenerativeModel("gemini-1.5-flash")


BRAINROT_DICTIONARY = documentReader.getTextFromTxt("brainrotDictionary.txt")
def unmodifiedOutput(prompt):
    return prompt

def nbaOutput(prompt):
    strn = model.generate_content("Make an explanation for "+prompt+" based on NBA terms, 100 words long. Include specific details, with no placeholders, like [Insert details here]. Give it to me just as plain text, no string formatting.")
    new_strn = strn.text
    return new_strn

def fortniteOutput(prompt):
    strn = model.generate_content("Make an explanation for the following prompt based on Fortnite terms, fortnite being the battle-royale video game by EpicGames, terms, 100 words long. Include specific details, with no placeholders, like [Insert details here]. Give it to me just as plain text, no string formatting:"+prompt)
    new_strn = strn.text
    return new_strn


def brainrotOutput(prompt):
    strn = model.generate_content("Return in text and punctuation only. Make an explanation for the following prompt based on and making use of the terms in the following brainrot dictionary, making use of at least 5 words from it, and being 100 words long overall. DO NOT HIGHLIGHT THE WORDS THAT YOU USED IN ANYWAY. Prompt:"+prompt+"\n Brainrot Dictionary:"+BRAINROT_DICTIONARY+".")
    new_strn = strn.text
    return new_strn
    

def redditOutput(prompt):
    strn = model.generate_content("Create a reddit post for "+prompt+ " based on the AITA posts on reddit, 100 words long. Include specific details, with no placeholders, like [Insert details here]. Give it to me just as plain text, no string formatting.")
    new_strn = strn.text
    return new_strn

def eli5Output(prompt):
    strn = model.generate_content("Explain "+prompt+" to me like I am 5, 100 words long. Include specific details, with no placeholders, like [Insert details here]. Give it to me just as plain text, no string formatting.")
    new_strn = strn.text
    return new_strn









