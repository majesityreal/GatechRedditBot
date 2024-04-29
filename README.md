### Gatech Subreddit Vibe Analysis
Code for data processing, performing sentiment analysis, and metrics evaluation using various methods

### Code Structure

preprocess_data.py: perform data preprocessing

extract_processed_comments.py, extract_processed_submissions.py: perform textblob and vader sentiment analysis

sa_metrics.py: generate various metrics from our result

/analysis: confusion matrix plots
/analysis/comments/confusion_matrix.py: generate confusion matrix from our llm result
/analysis/posts_updated/confusion_matrix.py: generate confusion matrix from our llm result

/processed_comments: processed comments data
/processed_submissions: processed posts data

/processed_comments_SA_result: completed sentiment anlaysis for comments
/processed_posts_SA_result: completed sentiment anlaysis for posts
/SA_plots: plots from traditional sentiment analysis results 

/processed_comments_llm/fix_lists.py, gpt_test.py, popular_topics_all.py, popular_topics_each.py: openai gpt analysis for comments
/processed_submissions_llm/fix_lists.py, gpt_test.py, popular_topics_all.py, popular_topics_each.py: openai gpt analysis for posts
