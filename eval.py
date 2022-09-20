import csv
list1 = [['rickandmorty', 'breakingbad'], ['rickandmorty', 'ozark'], ['rickandmorty', 'bettercallsaul'],
         ['rickandmorty', 'theboys'], ['rickandmorty', 'invincible'], ['rickandmorty', '90DayFiance'],
         ['rickandmorty', 'iasip'], ['breakingbad', 'ozark'], ['breakingbad', 'bettercallsaul'],
         ['breakingbad', 'theboys'], ['breakingbad', 'invincible'], ['breakingbad', '90DayFiance'],
         ['breakingbad', 'iasip'], ['ozark', 'bettercallsaul'], ['ozark', 'theboys'],
         ['ozark', 'invincible'], ['ozark', '90DayFiance'], ['ozark', 'iasip'],
         ['bettercallsaul', 'theboys'], ['bettercallsaul', 'invincible'], ['bettercallsaul', '90DayFiance'], ['bettercallsaul', 'iasip'], ['theboys', 'invincible'], ['theboys', '90DayFiance'], ['theboys', 'iasip'], ['invincible', '90DayFiance'], ['invincible', 'iasip'], ['90DayFiance', 'iasip']]
list_of_pairs = [('bettercallsaul', 'theboys'), ('bettercallsaul', 'invincible'), ('bettercallsaul', '90DayFiance'), ('bettercallsaul', 'iasip'), ('theboys', 'invincible'), ('theboys', '90DayFiance'), ('theboys', 'iasip'), ('invincible', '90DayFiance'), ('invincible', 'iasip'), ('90DayFiance', 'iasip')]

for file_name in list1:
    pathname = file_name[0] + file_name[1] + ".csv"
    correct_answer = 1
    wrong_answers = 1
    try:
        with open(pathname, 'r+', encoding="utf-8") as file:
            reader = csv.reader(file)
            rows = list(reader)
            for row in rows:
                if len(row) > 0:
                    if row[0] == row[1]:
                        correct_answer += 1
                    else:
                        wrong_answers += 1
            file.close()
    except FileNotFoundError:

    print(file_name, correct_answer/(correct_answer+wrong_answers))
