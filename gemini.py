from google.cloud import aiplatform
import google.generativeai as genai
import os
import numpy as np
import documentReader
import json
gen_ai_key = os.environ.get('GENAI_KEY')
genai.configure(api_key = gen_ai_key)

model = genai.GenerativeModel("gemini-1.5-pro-latest")
prompt_schema = "Use this JSON schema:\nResponse = {\"Explanation\":str, \"Quiz\":[[]]}\n"


BRAINROT_DICTIONARY = documentReader.getTextFromTxt("brainrotDictionary.txt")
def unmodifiedOutput(prompt):
    strn = model.generate_content("Return the prompt as is, IN PLAIN TEXT WITH NO FORMATTING. Additionally, output a quiz based on the prompt. Do this in a JSON format, where the value for the Quiz key is a 2d array of 5 elements, each representing a question. Each question is an array of size 6, with the 0th element being the question as a string, the next 4 elements are options, and the last element gives the exact index of the correct answer option, including the 0th index. Make sure to give EVERYTHING in plain text. Here is the format:"+prompt_schema+". Put the unmodified explanation in the explanation section of this json ONLY. Here is the prompt:"+prompt)
    strn_dict = json.loads(strn.text)
    return strn_dict

def nbaOutput(prompt):
    strn = model.generate_content("Make an explanation for the given prompt based on NBA terms, 100 words long. Include specific details, with no placeholders, like [Insert details here]. Give it to me just as plain text, no string formatting. Additionally, output a quiz based on the prompt, NOT IN NBA TERMS. Do this in a JSON format, where the value for the Quiz key is a 2d array of 5 elements, each representing a question. Each question is an array of size 6, with the 0th element being the question as a string, the next 4 elements are options, and the last element gives the exact index of the correct answer option, including the 0th index. Make sure to give EVERYTHING in plain text. Here is the format:"+prompt_schema+". Put the NBA explanation in the explanation section of this json ONLYHere is the prompt:"+prompt)
    strn_dict = json.loads(strn.text)
    return strn_dict

def fortniteOutput(prompt):
    strn = model.generate_content("Make an explanation for the following prompt based on Fortnite terms, fortnite being the battle-royale video game by EpicGames, terms, 100 words long. Include specific details, with no placeholders, like [Insert details here]. Give it to me just as plain text, no string formatting. Additionally, output a quiz based on the prompt, NOT IN FORTNITE TERMS. Do this in a JSON format, where the value for the Quiz key is a 2d array of 5 elements, each representing a question. Each question is an array of size 6, with the 0th element being the question as a string, the next 4 elements are options, and the last element gives the exact index of the correct answer option, including the 0th index. Make sure to give EVERYTHING in plain text. Here is the format:"+prompt_schema+". Put the fortnite explanation in the explanation section of this json ONLY. Here is the prompt:"+prompt)
    strn_dict = json.loads(strn.text)
    return strn_dict


def brainrotOutput(prompt):
    strn = model.generate_content("Return in text and punctuation only. Make an explanation for the following prompt based on and making use of the terms in the following brainrot dictionary, making use of at least 8 words from it, and being 100 words long overall. DO NOT HIGHLIGHT THE WORDS THAT YOU USED IN ANYWAY, INCLUDING **. Here is the Brainrot Dictionary:"+BRAINROT_DICTIONARY+". Additionally, output a quiz based on the prompt, NOT IN BRAINROT TERMS. Do this in a JSON format, where the value for the Quiz key is a 2d array of 5 elements, each representing a question. Each question is an array of size 6, with the 0th element being the question as a string, the next 4 elements are options, and the last element gives the exact index of the correct answer option, including the 0th element. Make sure to give EVERYTHING in plain text. Here is the format:"+prompt_schema+". Put the brainrot explanation in the explanation section of this json only. Here is the prompt:"+prompt)
    strn_dict = json.loads(strn.text)
    return strn_dict
    

def redditOutput(prompt):
    strn = model.generate_content("Create a reddit post for "+prompt+ " based on the AITA posts on reddit, 100 words long. Include specific details, with no placeholders, like [Insert details here]. Give it to me just as plain text, no string formatting. Additionally, output a quiz based on the prompt, NOT IN REDDIT TERMS. Do this in a JSON format, where the value for the Quiz key is a 2d array of 5 elements, each representing a question. Each question is an array of size 6, with the 0th element being the question as a string, the next 4 elements are options, and the last element gives the exact index of the correct answer option, including the 0th index. Make sure to give EVERYTHING in plain text. Here is the format:"+prompt_schema+". Put the reddit post in the explanation section of this json. Here is the prompt:"+prompt)
    strn_dict = json.loads(strn.text)
    return strn_dict

def eli5Output(prompt):
    strn = model.generate_content("Explain "+prompt+" to me like I am 5, 100 words long. Include specific details, with no placeholders, like [Insert details here]. Give it to me just as plain text, no string formatting. Additionally, output a quiz based on the prompt, NOT IN ELI5 TERMS. Do this in a JSON format, where the value for the Quiz key is a 2d array of 5 elements, each representing a question. Each question is an array of size 6, with the 0th element being the question as a string, the next 4 elements are options, and the last element gives the exact index of the correct option,including the 0th index. Make sure to give EVERYTHING in plain text. Here is the format:"+prompt_schema+". Put the eli5 explanation in the Explanation section of the json ONLY. Here is the prompt:"+prompt)
    strn_dict = json.loads(strn.text)
    return strn_dict



output =    unmodifiedOutput("The War of 1812 was fought by the United States and its allies against the United Kingdom and its allies in North America. It began when the United States declared war on Britain on 18 June 1812. Although peace terms were agreed upon in the December 1814 Treaty of Ghent, the war did not officially end until the peace treaty was ratified by the United States Congress on 17 February 1815.")

print(output)






