# creating a list of all letters, we will use it in dictionaries creation
alphabet_list = [chr(i) for i in range(ord('a'), ord('z') + 1)]
# importing randint method from tandom module
from random import randint

# --------------------- Task 1 ---------------------
# use clear function naming - with this function we will create one dict with random number of elements
def generate_dict():
    # defining the future keys in here
    keys_list = []
    # creating a copy of alphabet_list cause we will change it in this process. Not to bother initial list
    alphabet_list_copy = alphabet_list.copy()
    # we will go with random number of elements from 1 to 10. We use "_" in this loop cause we just need to repeat some times
    for _ in range(randint(1, 10)):
        # we take random letter from alphabet_list
        char = alphabet_list_copy[randint(0, len(alphabet_list_copy) - 1)]
        # and then add it to our list of keys
        keys_list.append(char)
        # to avoid repetition of letters, removes used letter from the copied list of letters
        alphabet_list_copy.remove(char)
    # using fromkeys method we create dict with defined keys with value 0
    dict_ = dict.fromkeys(keys_list, 0)
    # after that we go through all of the keys and assign random integer to it 
    for key in dict_.keys():
        # this integer could be from 0 to 100 including both end points
        dict_[key] = randint(0, 100)
    # return this created dict to work with it 
    return dict_

# in this function we will create list of random number of random dicts 
def generate_list_of_dicts():
    # create empty list
    list_of_dicts = []
    # and then create from 2 to 10 dictionaries in it 
    for _ in range(randint(2, 10)):
        # use previous function and append function
        list_of_dicts.append(generate_dict())
    # return this list to work with it in the next task
    return(list_of_dicts)

# create an example of this list and assign it to a value to save it
ex_dict = generate_list_of_dicts()
# display this list
# print(ex_dict)


# --------------------- Task 2 ---------------------
# in this function we will create common dictionary from list of dictionaries (with defined rules)
def generate_common_dict(list_of_dicts):
    # create empty list of keys and common dict - final dict
    keys_list = []
    common_dict = {}
    # iterating through dicts in list of dicts
    for d in list_of_dicts:
        # end then through keys in this dict
        for key in d.keys():
            # filling our list of keys
            keys_list.append(key)
    # then create new dict with those keys end all of the values are empty dicts
    common_dict_full = {key: {} for key in keys_list}
    # then again iterate through dicts in list of dicts and then through items in this particular dict
    for d in list_of_dicts:
        for key, value in d.items():
            # in this inner dict we create elements that will contain key as number of dictionary 
            # and value as value with defined key in this dict
            common_dict_full[key][list_of_dicts.index(d) + 1] = value
    # then we will work with this created full dict and will iterate throught outer elements - letter and inner dict
    for letter, dict_ in common_dict_full.items():
        # define max value in thid inner dict
        max_value = max(dict_.values())
        # and it's appropriate key in this inner dict
        max_key = max(dict_, key=dict_.get)
        # then we will check if the inner dict has more then 1 element
        if len(dict_.keys()) > 1:
            # and if does, we will change the key in a propriate way
            new_key = letter + '_' + str(max_key)
        # if doesn't, just leave it as it was
        else:
            new_key = letter
        # and add new element to our final dictioanry with appropriate keys and values
        common_dict[new_key] = max_value
    return common_dict

# check with previously saved list
# print(generate_common_dict(ex_dict))
