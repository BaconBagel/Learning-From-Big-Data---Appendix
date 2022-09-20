import praw
import csv

comment_list = []


reddit = praw.Reddit(
    client_id="zoGt96DIEzfn-B4qWZnszA",
    client_secret="ytLy-JztH2eLSJcNPohnyAEFEZP0_w",
    user_agent="/u/snoopdrug - Naive Bayesian classifier attempt",
)

reddit.read_only = True

for submission in reddit.subreddit("science").top(time_filter="all", limit=None):
    all_comments = submission.comments.list()
    for comment in all_comments:
        if hasattr(comment, "author_flair_text"):
            if comment.author_flair_text is not None:
                matches_1 = ["eclerc", "errari", "sainz"]
                matches_2 = ["erstappen", "erez", "Bull", "bull"]
                matches_3 = ["amilton", "ercedes" "ussel", "Merc"]
                if any(x in comment.author_flair_text for x in matches_1):
                    body = comment.body
                    flair = comment.author_flair_text
                    upvotes = comment.score
                    comment_id = comment.id
                    comment_time = comment.created_utc
                    with open('3teamsandother.csv', 'a+', encoding='utf-8', newline='') as file:
                        fields = [str(comment_id), str(flair), str(body), str(upvotes), comment_time]
                        writer = csv.writer(file)
                        writer.writerow(fields)
                        file.close()
                elif any(x in comment.author_flair_text for x in matches_2):
                    body = comment.body
                    flair = comment.author_flair_text
                    upvotes = comment.score
                    comment_id = comment.id
                    comment_time = comment.created_utc
                    with open('3teamsandother.csv', 'a+', encoding='utf-8', newline='') as file:
                        fields = [str(comment_id), str(flair), str(body), str(upvotes), comment_time]
                        writer = csv.writer(file)
                        writer.writerow(fields)
                        file.close()
                elif any(x in comment.author_flair_text for x in matches_3):
                    body = comment.body
                    flair = comment.author_flair_text
                    upvotes = comment.score
                    comment_id = comment.id
                    comment_time = comment.created_utc
                    with open('3teamsandother.csv', 'a+', encoding='utf-8', newline='') as file:
                        fields = [str(comment_id), str(flair), str(body), str(upvotes), comment_time]
                        writer = csv.writer(file)
                        writer.writerow(fields)
                        file.close()
                else:
                    body = comment.body
                    flair = comment.author_flair_text
                    upvotes = comment.score
                    comment_id = comment.id
                    comment_time = comment.created_utc
                    with open('3teamsandother.csv', 'a+', encoding='utf-8', newline='') as file:
                        fields = [str(comment_id), str(flair), str(body), str(upvotes), comment_time]
                        writer = csv.writer(file)
                        writer.writerow(fields)
                        file.close()





