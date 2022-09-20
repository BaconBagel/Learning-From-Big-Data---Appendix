priors = [0.3333, 0.3333, 0.3333]
tech = [0.00518134, 0.00384615, 0.03975535]
car = [0.00518134, 0.07307692, 0.051987767]
lab = [0.010362694, 0.0038461538, 0.045871559]
n_cats = len(priors)
probs = [priors, tech, tech, car, lab]


def posts_recursive(list_of_lists, n_cats):
    posts_result = []
    while True:
        if len(list_of_lists) == 1:
            break
        post_1 = [a * b for a, b in zip(list_of_lists[0], list_of_lists[1])]
        if sum(post_1) > 0:
            for vec in range(n_cats):
                posts_result.append((post_1[vec]/sum(post_1)))
        list_of_lists.pop(0)
        list_of_lists[0][0:n_cats-1] = posts_result[-n_cats:][0:]
        list_of_lists[0].pop()
        posts_recursive(list_of_lists, n_cats)
    return list_of_lists


posts = posts_recursive(probs, n_cats)
print(posts)

