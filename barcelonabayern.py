import praw
import csv
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
comment_list = []


reddit = praw.Reddit(
    client_id="zoGt96DIEzfn-B4qWZnszA",
    client_secret="ytLy-JztH2eLSJcNPohnyAEFEZP0_w",
    user_agent="/u/snoopdrug - Naive Bayesian classifier attempt",
)

def getSubComments(comment, allComments, verbose=True):
    allComments.append(comment)
    if not hasattr(comment, "replies"):
        replies = comment.comments()
    if verbose:
        print("fetching (" + str(len(allComments)) + " comments fetched total)")
    else:
        replies = comment.replies
    for child in replies:
        getSubComments(child, allComments, verbose=verbose)


def getAll(r, submissionId, verbose=True):
    submission = r.submission(submissionId)
    comments = submission.comments.list()


def remove_stopwords(comment_text):
    stop_words = set(stopwords.words('english'))
    from nltk.tokenize import RegexpTokenizer
    tokenizer = RegexpTokenizer(r'\w+')
    comment_text_token = tokenizer.tokenize(comment_text)
    filtered_sentence = []
    for current_word in comment_text_token:
        if current_word not in stop_words:
            filtered_sentence.append(current_word)
    filtered_sentence = (" ").join(filtered_sentence)
    return filtered_sentence


for submission in reddit.subreddit("shitposting").top(time_filter="year", limit=None):
    all_comments = submission.comments.list()
    for comment in all_comments:
        if hasattr(comment, "author_flair_text"):
            if comment.body is not None:
                body = comment.body
                body = remove_stopwords(body)
                upvotes = comment.score
                flair = comment.author_flair_text
                comment_id = comment.id
                comment_time = comment.created_utc
                print(str(comment_id), flair, str(body), str(upvotes), comment_time)
                with open('shitpostingvspolitics.csv', 'a+', encoding='utf-8', newline='') as file:
                    fields = [str(comment_id), "shitposting", str(body), str(upvotes), str(comment_time)]
                    writer = csv.writer(file)
                    writer.writerow(fields)
                    file.close()






