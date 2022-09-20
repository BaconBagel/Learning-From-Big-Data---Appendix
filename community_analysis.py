import csv
import itertools

import nltk
import string
import copy
import time
import collections
from itertools import chain
from itertools import combinations
nltk.download('stopwords')
from nltk.corpus import stopwords
import random
num_cats = 2
comments = []
lower_limit_training = 0
upper_limit_training = 40000
lower_limit_testing = 0
upper_limit_testing = 40000
the_path = "multid3.csv"

with open(the_path, 'r+', encoding="utf-8") as file:
    reader = csv.reader(file)
    rows = list(reader)
    for row in rows[lower_limit_training:upper_limit_training]:
        if len(row) > 4:
            comments.extend([row])
    file.close()


def remove_stopwords(comment_text):
    stop_words = set(stopwords.words('english'))
    translate_table = dict((ord(char), None) for char in string.punctuation) # Removes punctuation
    comment_text = comment_text.translate(translate_table)
    comment_text = comment_text.replace('’', '')
    comment_text = comment_text.replace(',', '')
    comment_text_token = nltk.tokenize.word_tokenize(comment_text)
    filtered_sentence = []
    for current_word in comment_text_token:
        if current_word not in stop_words:
            filtered_sentence.append(current_word)
    return filtered_sentence


def categorise(comments_tosort, num_categories):
    new_list = []
    for i in comments_tosort:
        new_list.append(i[1])
    counters = collections.Counter(new_list)
    most_common = counters.most_common(num_categories)
    counters2 = list(counters.keys())
    return most_common, counters2


all_categories = categorise(comments, num_cats)[1]
teams_categories = categorise(comments, num_cats)[0]
print(all_categories)
print(teams_categories)

all_combinations = list(combinations(all_categories, 2))
print(all_combinations)
for pairings in all_combinations:
    formated_pair = [(pairings[0], 5000), (pairings[1], 5000)]
    print (formated_pair)
    comments = []
    with open(the_path, 'r+', encoding="utf-8") as file:
        reader = csv.reader(file)
        rows = list(reader)
        for row in rows[lower_limit_training:upper_limit_training][0::2]:
            if len(row) > 4:
                if row[1] == pairings[0] or row[1] == pairings[1]:
                    comments.extend([row])
                    random.shuffle(comments)
        file.close()
    print(comments)
    def sentiment(comment_list, team_cats): # Seperates by class
        sentiment_list = []
        for user_post in comment_list:
            cnt = 0
            if len(user_post) > 1:
                for cat in pairings:
                    if user_post[1] == cat:
                        sentiment_list.append([cnt, user_post[-3]])
                    cnt += 1
        return sentiment_list


    def count_words(list_with_text, text_position): #text_position ist the place the text body has in the list
        count_list = []
        count_dict = {}
        for s in list_with_text:
            count_list.extend(s[int(text_position)])
        for d in range(len(count_list)):
            count_dict[count_list[d]] = count_list.count(count_list[d])
        return count_dict


    user_sentiments = sentiment(comments, teams_categories)
    counts = count_words(user_sentiments, -1)
    word_atlas = counts.keys()
    priors_from_frequency = []
    priors_from_frequency.clear()


    def likelyhoods(raw_sentiment, n): # calculates chance of each word occuring in class x n is number of dimensions
        initials = []
        counters = []
        for x in range(n):
            initials.append(0)
            counters.append(0)
        post_counts2 = {key: initials[:] for key in word_atlas}
        post_counts = copy.deepcopy(post_counts2)
        for comnt in raw_sentiment:
            for wrd in word_atlas:
                if wrd in comnt[-1]:
                    for dim in range(n):
                        if int(comnt[0]) == dim:
                            counters[dim] += 1
                            post_counts[wrd][dim] += 1

        post_counts_old = copy.deepcopy(post_counts)
        for word in word_atlas:
            for vec in range(n):
                post_counts[word][vec] = (post_counts_old[word][vec]+1)/(sum(post_counts_old[word])+n)

        total = sum(counters)
        new_counters = [x / total for x in counters]
        priors_from_frequency.append(new_counters)
        return post_counts


    probability_dct = likelyhoods(user_sentiments, num_cats)
    preset_priors = list(chain(*priors_from_frequency))



    def posteriors(priors_input, list1): # calculates posteriors
        c1 = 0
        vectors = []
        post_1 = [a * b for a, b in zip(priors_input, list1)]
        if sum(post_1) > 0:
            for vec in range(len(post_1)):
                vectors.append(post_1[vec]/sum(post_1))
            c1 += 1
            #print("success", c1)
        else:
            for vec in range(len(post_1)):
                vectors.append(priors_from_frequency[0][vec])
            c1 -= 1
            #print("error", c1)
        return vectors


    def find_word_probs(comments_inpt, num_vecs):
        comments_probs = []
        for commt in comments_inpt:
            if len(commt) > 0:
                addition = []
                app = []
                for wrd in word_atlas:
                    if wrd in commt[-3]:
                        for v in range(num_vecs):
                            appendage = probability_dct[wrd][v]
                            app.append(appendage)
                        addition.append(app)
                comments_probs.append([addition, commt])
        return comments_probs


    new_probs = find_word_probs(comments, num_cats)


    def classifier(found_probs, num_vecs):
        final_list = []
        for sentence_probs in found_probs:
            sentence_probs2 = sentence_probs[0]
            counter = 0
            if len(sentence_probs2) > 0:
                for pair in range(len(sentence_probs2)-1):
                    if counter == 0:
                        first_pair = posteriors(preset_priors, sentence_probs2[pair][-num_vecs:])
                    first_pair = posteriors(first_pair, sentence_probs2[pair+1][-num_vecs:])
                    counter += 1
                final_list.append([first_pair, sentence_probs])
        return final_list # returns the results of the posteriors and the comment with metadata


    def check_accuracy(prediction_scores, categories):
        wrong_answers = 1
        right_answers = 1
        final_results_checker = []
        for comment in prediction_scores:
            print(comment[0])
            # make the prediction
            for x in range(len(pairings)):
                if comment[0][x] == max(comment[0]):
                    prediction = pairings[x]
            # check if it is right
            answer = comment[-1][-1][1]

            if prediction == answer:
                right_answers += 1
            else:
                wrong_answers += 1
            final_results_checker.append([prediction, answer, comment])
            print(right_answers/(right_answers + wrong_answers), right_answers, wrong_answers)

        return final_results_checker


    b = classifier(new_probs, num_cats)
    c = check_accuracy(b, teams_categories)

    comments_check = []

    with open(the_path, 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        rows = list(reader)
        for row in rows[lower_limit_testing:upper_limit_testing][1::2]:
            if len(row) > 4:
                if row[1] == pairings[0] or row[1] == pairings[1]:
                    comments_check.extend([row])
                    random.shuffle(comments_check)
        file.close()

    new_check = find_word_probs(comments_check, num_cats)
    classified = classifier(new_check, num_cats)
    accuracy = check_accuracy(classified, teams_categories)

    with open(pairings[0] + pairings[1] + "3.csv", 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        for datapoint in accuracy:
            fields = [datapoint[0], datapoint[1], datapoint[-1][-1][-1][-2]]
            print(fields)
            writer.writerow(fields)
        file.close()

