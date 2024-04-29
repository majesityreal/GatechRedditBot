import re
from nltk.corpus import stopwords

def preprocess_text_VADER(text):
    # remove urls
    processed_text = re.sub(r'http\S+', '', text)

    return processed_text

def preprocess_text_TextBlob(text):
    # convert to lower case
    lower_text = text.lower()
    
    # remove urls
    lower_text = re.sub(r'http\S+', '', lower_text)

    # remove emails
    lower_text = re.sub(r'\S*@\S*\s?', "", lower_text)
    
    # tokenize as the function CountVectorizer()
    tokens = re.findall(r"(?u)\b\w\w+\b", lower_text)
    
    # stop word
    processed_text = [d for d in tokens if d not in stopwords.words('english')]

    return ' '.join(processed_text)

# sample_text = "Still holding out for a Single Payer health system? While you wait - please consider signing up for our new Grad SGA initiative focus groups on Health Insurance here at Georgia Tech.\n\nSign-up here: https:\/\/goo.gl\/forms\/OwHugOjggSysUdQT2\n\nFor questions, please feel free to email grad.studentlife@sga.gatech.edu"
# print(sample_text)
# print(preprocess_text_VADER(sample_text))
# print(preprocess_text_TextBlob(sample_text))