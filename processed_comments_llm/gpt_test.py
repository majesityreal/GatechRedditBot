import json
import pandas as pd
from openai import OpenAI
from datetime import datetime
import os

# initialize OpenAI client with API key
# client = OpenAI(api_key="#apikey")
# dummy api key here for data privacy.
client = OpenAI(api_key="#apikey")


def analyze_text(text):
    # analyzes the text to determine its sentiment and main topic
    try:
        prompt_text = (
            f"You are a helpful assistant trained to provide structured responses."
            f"Please analyze the following text and provide the sentiment (positive, negative, neutral) and the topic categories."
            f"Please provide more general categories for this comment as a simple list separated by commas. Each category should be 1 word long."
            f"Format your response as 'Sentiment: [sentiment]. Topic: [topic]':\n\n\"{text}\""
        )
        # send the prompt to the OpenAI API and get the response
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt_text,
            temperature=0.1,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        # access the response
        response_text = response.choices[0].text.strip()
        # parse the structured response
        parts = response_text.split(". ")
        sentiment = parts[0].replace("Sentiment: ", "").strip()
        topic = parts[1].replace("Topic: ", "").strip() if len(parts) > 1 else "Error"
        return sentiment, topic
    except Exception as e:
        print(f"Error during API call: {e}")
        return "Error", "Error"

def process_json_lines(file_path, output_path):
    #process each line of a JSON file to analyze comments for sentiment and topic
    processed_data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        x = 0
        for line in file:
            try:
                comment = json.loads(line)
                comment_text = comment.get('body', '')
                # skip deleted or removed comments
                if comment_text in ['[deleted]', '[removed]']:
                    continue
                created_utc = comment['created_utc']
                created_date = datetime.fromtimestamp(created_utc).strftime('%Y-%m-%d')
                sentiment, topic = analyze_text(comment_text)
                processed_data.append({
                    'type': 'comment',
                    'text': comment_text,
                    'sentiment': sentiment,
                    'topic': topic,
                    'score': comment['score'],
                    'date': created_date
                })
                x += 1
                if x%250 == 0:
                    print(x)
            except json.JSONDecodeError as e:
                print(f"failed to decode JSON from line: {line} with error: {e}")

    df = pd.DataFrame(processed_data)
    df.to_csv(output_path, index=False)
    print(f"Analysis completed. Results saved to {output_path}.")

current_directory = "batch8"
print("batch8")
for filename in os.listdir(current_directory):
    if filename.endswith('.txt'):
        file_path = os.path.join(current_directory, filename)
        output_path = os.path.join(current_directory, filename.replace('.txt', '.csv'))
        process_json_lines(file_path, output_path)
        
# Note, there can be Errors