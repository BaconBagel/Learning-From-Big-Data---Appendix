import praw
import csv
import nltk
import statistics
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
    user_agent="/u/snoopdrug - Naive Bayesian classifier attempt for F1 comments",
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


sub = "montreal"

races = ["uva93o", "uvcbkb", "uaw33k", "uau1dt", "tip2w4", "vg2umq", "xbhnfv", "w6utzt", "v0ag4v", "wzunih", "wcnwid", "vvqqtf", "tppwp7", "u0aaoo", "x5m54t"]

counter = 0


def iter_top_level(comments):
    for top_level_comment in comments:
        if isinstance(top_level_comment, praw.models.MoreComments):
            yield from iter_top_level(top_level_comment.comments())
        else:
            yield top_level_comment

            
for submission in reddit.subreddit("formula1").top(time_filter="year", limit=None):
    print(submission)
    if hasattr(submission, "link_flair_text"):
        all_comments = iter_top_level(submission.comments)
        votes = []
        for comment in all_comments:
            print(comment, comment.body)
            if hasattr(comment, "body"):
                if comment.body is not None:
                        votes.append(comment.score)
        threshold = statistics.median(votes)

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
                        print(str(comment_id), "race", str(body), str(upvotes), comment_time)
                        counter += 1
                        if upvotes > threshold:
                            with open('f1_year_parents_only3.csv', 'a+', encoding='utf-8', newline='') as file:
                                fields = [str(comment_id), "upvoted", str(body), str(upvotes), str(comment_time)]
                                writer = csv.writer(file)
                                writer.writerow(fields)
                                file.close()
                        elif upvotes <= threshold:
                            with open('f1_year_parents_only3.csv', 'a+', encoding='utf-8', newline='') as file:
                                fields = [str(comment_id), "downvoted", str(body), str(upvotes), str(comment_time)]
                                writer = csv.writer(file)
                                writer.writerow(fields)
                                file.close()



