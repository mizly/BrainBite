from google.cloud import aiplatform
import google.generativeai as genai
import os
import numpy as np
import documentReader

genai.configure(api_key = os.environ["GENAI_KEY"])


model = genai.GenerativeModel("gemini-1.5-flash")


BRAINROT_DICTIONARY = documentReader.getTextFromTxt("brainrotDictionary.txt")
def unmodifiedOutput(prompt):
    strn = model.generate_content("Print the contents of "+prompt)
    new_strn = strn.text
    return new_strn

def nbaOutput(prompt):
    strn = model.generate_content("Make an explanation for "+prompt+" based on NBA terms, 100 words long. Include specific details, with no placeholders, like [Insert details here]. Give it to me just as plain text, no string formatting.")
    new_strn = strn.text
    return new_strn

def fortniteOutput(prompt):
    strn = model.generate_content("Make an explanation for the following prompt based on Fortnite terms, fortnite being the battle-royale video game by EpicGames, terms, 100 words long. Include specific details, with no placeholders, like [Insert details here]. Give it to me just as plain text, no string formatting:"+prompt)
    new_strn = strn.text
    return new_strn


def brainrotOutput(prompt):
    strn = model.generate_content("Make an explanation for the following prompt based on and making use of the terms in the following brainrot dictionary, making use of at least 5 words from it, and being 100 words long overall. Prompt:"+prompt+"\n Brainrot Dictionary:"+BRAINROT_DICTIONARY)
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


print(brainrotOutput("One might counter, of course, that a theory based on only a single\
 case is inherently problematic and that, moreover,20 German political\
 development during this period was certainly influenced by a range of\
 factors extending beyond civil society, many of them highly particular.\
 Nevertheless, there are several reasons why an inability of neo\
 Tocquevillean analysis to account for the central features of this case\
 should be significant and troubling. First, scholars have long viewed\
 the Weimar Republic and its collapse as a crucial theoretical testing\
 ground. The disintegration of democracy in interwar Germany is so\
 central to our understanding of comparative politics and so critical for\
 the history of modern Europe that we should at the least be wary of any\
 theory of political development that cannot explain it"))






