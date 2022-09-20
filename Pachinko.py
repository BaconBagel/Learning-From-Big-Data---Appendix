
import csv
import tomotopy as tp
mdl = tp.PAModel(k1=5, k2=100, min_cf=20)
the_path = "f1_titles.csv"

with open(the_path, 'r+', encoding="utf-8") as file:
    reader = csv.reader(file)
    rows = list(reader)
    print(len(rows))
    for row in rows:
        mdl.add_doc(row[0].strip().split())
    file.close()

print('Starting training model')
iterations = 10
for i in range(0, 100, iterations):
    mdl.train(iterations)
    print('Iteration: {}\tLog-likelihood: {}'.format(i, mdl.ll_per_word))

for k in range(mdl.k1):
    subtopics = mdl.get_sub_topics(k)
    print('\n\nSubtopics of topic #%s' % k)
    for subtopic, probability in subtopics:
        print('    Top 10 words of subtopic topic #%s: probability in supertopic #%s: %r' % (subtopic, k, probability))
        print('    %r' % mdl.get_topic_words(subtopic, top_n=20))