import random
import uuid

def generateRandomEntries(n=100, m=5, t=3, q = 20, p_lower = 7, p_upper = 27):
    with open('./random_data/foods.txt') as f:
        foods = f.readlines()
    with open('./random_data/names.txt') as f:
        names = f.readlines()
    with open('./random_data/countries.txt') as f:
        countries = f.readlines()
    
    original_product_names = list(map(lambda x: x[:len(x)-1],foods))
    product_names = random.sample(original_product_names,n)
    human_names = list(map(lambda x: x[:len(x)-1],names))
    human_names = random.sample(human_names, m)
    country_names = list(map(lambda x: x[:len(x)-1], countries))
    country_names = random.sample(country_names,t)
    quantity_range = list(range(q+1))
    price_range = list(range(p_lower,p_upper))
    number_of_tags_range = list(range(t))

    rsf = []
    for product in product_names:
        current_product = {}
        number_of_tags = random.choice(number_of_tags_range)
        countries = random.sample(country_names, number_of_tags)
        current_product['tags'] = random.sample(country_names, number_of_tags)
        current_product['id'] = uuid.uuid4().hex
        current_product['name'] = (current_product['tags'][0] \
             if len(current_product['tags']) else "") \
            + " " + product + " " + \
                random.choice(original_product_names)
        current_product['user'] = random.choice(human_names)
        current_product['quantity'] = random.choice(quantity_range)
        current_product['price'] = random.choice(price_range)


        rsf.append(current_product)
    return rsf

result = generateRandomEntries(n=150)
print(result)
print(len(result))
assert len(result) == 150

# TODO idea: to simulate shop transactions over some n number of days, I could
# use a stochastic transition matrix over markov chain