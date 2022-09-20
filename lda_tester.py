import csv
import nltk
comment_outcomes = []

with open("topics_found.csv", 'r+', encoding="utf-8") as file:
    lda_outcomes = []
    reader = csv.reader(file)
    rows = list(reader)
    print(len(rows))
    for row in rows:
        lda_outcomes.append(row)


def most_common(de_list):
    return max(set(de_list), key=de_list.count)

with open("f1_median2.csv", 'r+', encoding="utf-8") as file:
    reader = csv.reader(file)
    rows = list(reader)
    counter = 0
    for row in rows:
        counter += 1
        print(counter)
        maximiser_list = []
        comment = nltk.tokenize.word_tokenize(row[2])
        for word in comment:
            for outcome in lda_outcomes:
                if word in outcome[1]:
                    maximiser_list.append(outcome[0])
        if len(maximiser_list) > 0:
            comment_outcomes.append([most_common(maximiser_list), row]) # We should probably add the tuple probabilities instead of this
        else:
            comment_outcomes.append(["none", row])
with open('politics.csv', 'a+', encoding='utf-8', newline='') as file:
    for out in comment_outcomes:
        if str(out[0]) == "10":
            fields = [out[1][0], out[1][1], out[1][2], out[1][3], out[1][4]]
            writer = csv.writer(file)
            writer.writerow(fields)
    file.close()
