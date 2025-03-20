# importing each of the hw files to use their functionality
import collections_hw as hw2
import string_object as hw3

# creating list of dicts from second hw and assign it to a variable
ex_dict = hw2.generate_list_of_dicts()
# using this variable, generate new common dict
hw2.generate_common_dict(ex_dict)

# correcting a sentence from third hw. Use function sentence_correction and pass hw_text value from hw3 module to it
corrected = hw3.sentence_correction(hw3.hw_text)
# using one of the functions to create last sentence, creating it and assign it to a value
last_sentence = hw3.last_sentense_creation(corrected)

# creating new corrected text with the last sentance
final = corrected + last_sentence

# calculate whitespaces
hw3.whitespaces_calculation(hw3.hw_text)