with open("lda_outcomes.csv", 'r+', encoding="utf-8") as file:
    lda_outcomes = []
    reader = csv.reader(file)
    rows = list(reader)
    print(len(rows))
    for row in rows:
        lda_outcomes.append(row)
