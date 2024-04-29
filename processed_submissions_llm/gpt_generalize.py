import pandas as pd
import os
from openai import OpenAI
import time

# initialize the OpenAI client with API key
client = OpenAI(api_key="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")


def generalize_topic(text, topic):
    # use ChatGPT to generalize a single topic
    prompt_text = (
        f"You are a helpful assistant trained to provide structured responses."
        f"I have a post and its detailed topic that needs to be simplified into a more general category. "
        f"The post is: {text}\n\n"
        f"The topic is: {topic}\n\n"
        f'Please provide more general categories for this post as a simple list separated by commas. Each category should be 1 word long.'
    )
    try:
        # send the prompt to the OpenAI API and get the response
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt_text,
            temperature=0.1,
            max_tokens=100,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        generalized_topic = response.choices[0].text.strip()
        return generalized_topic
    except Exception as e:
        print(f"Error during API call: {e}")
        return "Error"

def process_csv_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path)
            print(file_path)

            # apply the generalization to each topic in the dataFrame
            df['generalized_topic'] = df.apply(lambda x: generalize_topic(x['text'], x['topic']), axis=1)

            # save the updated DataFrame
            output_filename = os.path.splitext(filename)[0] + "_generalized.csv"
            output_path = os.path.join(directory, output_filename)
            df.to_csv(output_path, index=False)
            print(f"Updated file saved to {output_path}")

# run the process
process_csv_files(os.getcwd())