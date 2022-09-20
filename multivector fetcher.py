import praw
import csv
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
comment_list = []



reddit = praw.Reddit(
    client_id="zoGt96DIEzfn-B4qWZnszA",
    client_secret="ytLy-JztH2eLSJcNPohnyAEFEZP0_w",
    user_agent="/u/snoopdrug - Naive Bayesian classifier attempt",
)


def remove_stopwords(comment_text):
    comment_text = comment_text.lower()
    stop_words = set(stopwords.words('english'))
    from nltk.tokenize import RegexpTokenizer
    tokenizer = RegexpTokenizer(r'\w+')
    comment_text_token = tokenizer.tokenize(comment_text)
    filtered_sentence = []
    lemmatizer = WordNetLemmatizer()
    for current_word in comment_text_token:
        if current_word not in stop_words:
            filtered_sentence.append(lemmatizer.lemmatize(current_word))
    filtered_sentence = (" ").join(filtered_sentence)
    return filtered_sentence


subs = ["sub1", "sub2"]
fetch_limit = 100000
sub_limit = 2

for sub in subs:
    counter = 0
    for submission in reddit.subreddit(sub).top(time_filter="year", limit=None):
        all_comments = submission.comments.list()
        for comment in all_comments:
            if hasattr(comment, "author_flair_text"):
                if comment.body is not None:
                    if len(comment.body) > 10:
                        body = comment.body
                        body = remove_stopwords(body)
                        upvotes = comment.score
                        flair = comment.author_flair_text
                        comment_id = comment.id
                        comment_time = comment.created_utc
                        print(str(comment_id), sub, str(body), str(upvotes), comment_time)
                        counter += 1
                        with open('opinions.csv', 'a+', encoding='utf-8', newline='') as file:
                            fields = [str(comment_id), sub, str(body), str(upvotes), str(comment_time)]
                            writer = csv.writer(file)
                            writer.writerow(fields)
                            file.close()
            if counter > fetch_limit:
                break
        if counter > sub_limit:
            break




