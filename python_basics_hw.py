# --------------------- Task 1 ---------------------
# importing randint method from random module to create list of 100 random values from 0 to 1000
from random import randint

# creating a list "l" using list comprehension structure (using for loop and range keyword to create list of 100 values)
l = [randint(0, 1000) for i in range(100)]


# --------------------- Task 2 ---------------------
# creating sorting function with clear name
def list_sorting(lst):
    # initializing an iterator
    i = 0
    # crearing a loop that will step over each element of the list (iterating by indexes)
    while i < len(lst) - 1:
        # checking if the next element is smaller then the previous
        if lst[i + 1] < lst[i]:
            # if so, changing the order for these two elements by inserting the smaller one before
            lst.insert(i, lst[i + 1])
            # and we should delete the originak element from the list
            del lst[i + 2]
            # To be sure that all list was sorted we step back to recheck the previous element
            i = max(0, i - 1)
        # using keywork "else" describe what should be done for another hand
        else:
            # if elements are in the right order, increase the iterator by one
            i += 1
            # return sorted list with the return keyword
    return lst


# --------------------- Task 3 ---------------------
def even_odd_average(lst):
    # creating lists "even_list" and "odd_list" using list comprehension structure 
    # (using operators % and ==/!= to identify if the number is odd or even)
    even_list = [i for i in lst if i % 2 == 0]
    odd_list = [i for i in lst if i % 2 != 0]
    # calculating sum for these two lists
    even_sum = sum(even_list)
    odd_sum = sum(odd_list)
    # in return section calculating each of average numbers using formula
    return even_sum / len(even_list), odd_sum / len(odd_list)

# using print keyword to print both values in console 
print('Even average: ', even_odd_average(l)[0], '\nOdd average: ', even_odd_average(l)[1])