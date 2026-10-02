from numpy import base_repr
from random import randint, choices, choice, shuffle, sample
from math import ceil
from time import time
import copy
from num2words import num2words
from six.moves import input
from numberlists import *

max_nums = [100, 100, 1000, 1000, 10_000, 10_000, 10_000, 10_000, 10_000, 10_000, 20_000]
max_num = 100
min_nums = [0, 0, 10, 10, 100, 1000, 1000, 1000, 1000, 2000, 2000]
num_rules = 3
levelup_table = [-1, 50, 150, 400, 1000, 2000, 3500, 5000, 7000, 10_000]
starting_lives = 3
game_time = 0
question_number = 0
cyclops_count = 0
cyclops_trigger = False
#                       0  1    2   3   4   5  6  7  8  9  10 11 12
solutions_per_level = [-1, 100, 50, 25, 13, 8, 5, 4, 3, 2, 2, 2, 2]
min_sol_per_level =   [-1, 1,   1,  1,  1,  1, 2, 2, 2, 2, 2, 2, 2]
max_solutions = 2
debug = False
needed_sols = 1
buffer_points = 0
prev_answers = []

#GLOBALS
game_points = 0
lives = 0
level = 0
display_text = 'Welcome to Number Game!\nPress ENTER to begin!'
input_text = ''
game_state = 'Not Running'
current_question = []
questions_asked = []
questions_ans = 0



def is_prime(num):
    return num in primes

def is_composite(num):
    if num <= 1:
        return False
    else:
        return not is_prime(num)

def is_emirp(num):
    digits = get_digits_str(num)
    if is_prime(num) and digits != digits[::-1]:
        return is_prime(int(digits[::-1]))
    return False

def is_semiprime(num):
    ''' Returns true if the number is the product of two prime numbers '''
    # Is only semi-prime if composite
    if not is_composite(num):
        return False
    # Find first prime factor
    for prime in primes:
        if num % prime == 0:
            # return whether or not the number/first prime factor is prime
            return is_prime(num/prime)

def is_nude(num):
    '''
    Returns true if the number can be evenly divisible by all of its digits
    no number with 0 can be included
    '''
    digits = get_digits(num)
    if 0 in digits:
        return False
    for digit in digits:
        if num % digit != 0:
            return False
    return True

def is_emirpimes(num):
    ''' Returns true if the given number is a semiprime and is a 
    different semiprime backwards'''
    digits = get_digits_str(num)
    if digits[-1:] == [0]:
        return False    
    if is_semiprime(num) and digits != digits[::-1]:
        return is_semiprime(int(digits[::-1]))
    return False

def is_twin_prime(num):
    ''' Returns true if num is part of a twin prime number '''
    return (is_prime(num)) and (is_prime(num-2) or is_prime(num+2))

def is_interprime(num):
    ''' Returns true if the number is eqidistant to the prime above and below it '''
    if not is_composite(num):
        return False
    i = 1
    while not is_prime(num + i):
        if (num + i + 1) % 2 == 0:
            i += 2
        else:
            i += 1
    j = 1
    while not is_prime(num - j):
        if (num - j - 1) % 2 == 0:
            j += 2
        else:
            j += 1
    return j == i

def is_emirpretni(num):
    ''' Returns true if num is an interprime and becomes a different interptime backwards'''
    digits = get_digits_str(num)
    if not num % 10:
        return False
    if is_interprime(num) and digits != digits[::-1]:
        return is_interprime(int(digits[::-1]))    

def is_even(num):
    return (num % 2) == 0

def is_odd(num):
    return (num % 2) == 1

def get_digit_sum(num):
    return sum(get_digits(num))

def is_digit_sum(num, summation):
    return get_digit_sum(num) == summation

def is_divisible_by(num, divisor):
    if divisor > 0:
        return num % divisor == 0
    return False

def is_score_divisible(num):
    return is_divisible_by(num, game_points)

def score_is_divisible(num):
    ''' Returns true if the score is divisible by the number '''
    return is_divisible_by(game_points, num)

def is_lives_divisible(num):
    return is_divisible_by(num, lives)

def is_level_divisible(num):
    return is_divisible_by(num, level)

def is_anagram(num1, num2):
    return num1 != num2 and sorted(str(num1)) == sorted(str(num2))

def get_digits(num):
    digits = []
    string = str(num)
    for digit in string:
        digits.append(int(digit))
    return digits

def get_digits_str(num):
    digits = str(num)
    return digits

# A Possible Rule
def get_digit_product(num):
    digits = get_digits(num)
    prod = 1
    for digit in digits:
        prod *= digit
    return prod

def is_digit_sum_eq_prdct(num):
    return (get_digit_sum == get_digit_product)

def is_digit_product(num, product):
    return get_digit_product(num) == product

def is_alternating(num):
    digits = get_digits(num)
    parity = 2
    for digit in digits:
        if (digit % 2) == parity:
            return False
        else:
            parity = (digit % 2)
    return True

def is_nt_alternating(num):
    if num < 10:
        return False
    else:
        return is_alternating(num)

def is_undulating(num):
    '''in form ABAB, A can = B'''
    if num < 10:
        return True
    digits = get_digits(num)
    digit1 = digits[0]
    digit2 = digits[1]
    wanted = digit1
    for digit in digits[2:]:
        if digit != wanted:
            return False
        else:
            if wanted == digit1:
                wanted = digit2
            else:
                wanted = digit1
    return True

def is_nt_undulating(num):
    ''' Checks for non-trivial undulating number, in form ABAB, A != B '''
    if num < 101:
        return False
    digits = get_digits(num)
    digit1 = digits[0]
    digit2 = digits[1]
    if digit1 == digit2:
        return False
    return is_undulating(num)

def is_palindrome(num):
    digits = get_digits_str(num)
    if (digits == digits[::-1]):
        return True
    return False

def is_nt_palindrome(num):
    if num < 10:
        return False
    return is_palindrome(num)

def get_binary(num):
    return int(bin(num)[2:])

def is_binary_palindrome(num):
    binary = get_binary(num)
    return is_palindrome(binary)

def get_hex(num):
    return hex(num)[2:]

def is_hex_palindrome(num):
    hex_value = get_hex(num)
    return is_palindrome(hex_value)

def get_ternary(num):
    ternary = base_repr(num, 3)
    return ternary

def is_ternary_palindrome(num):
    ternary = int(get_ternary(num))
    return is_palindrome(ternary)

def get_octal(num):
    octal = int(oct(num)[2:])
    return octal

def is_octal_palindrome(num):
    octal = get_octal(num)
    return is_palindrome(octal)

def is_odious(num):
    ''' Odious - has an odd number of 1s in it's binary expansion '''
    binary = get_binary(num)
    binary = str(binary)
    num1 = binary.count('1')
    if (num1 % 2) == 1:
        return True
    return False

def is_oddish(num):
    ''' sum of all digits is even '''
    return sum(map(int, str(num))) % 2

def is_evenish(num):
    return not(is_oddish(num))

def is_evil(num):
    ''' Evil - has an even number of 1s in it's binary expansion '''
    return not(is_odious(num))

def is_decreasing(num):
    ''' Each digit is less than or equal to the digit before '''
    digits = get_digits(num)
    x = 10
    for digit in digits:
        if digit <= x:
            x = digit
        else:
            return False
    return True

def is_strictly_decreasing(num):
    ''' Each digit is strictly less than the digit before '''
    digits = get_digits(num)
    x = 10
    for digit in digits:
        if digit < x:
            x = digit
        else:
            return False
    return True

def is_increasing(num):
    digits = get_digits(num)
    x = -1
    for digit in digits:
        if digit >= x:
            x = digit
        else:
            return False
    return True

def is_strictly_increasing(num):
    digits = get_digits(num)
    x = -1
    for digit in digits:
        if digit > x:
            x = digit
        else:
            return False
    return True

def is_niven(num):
    ''' (Harshad) Niven numbers - evenly divisible by the sum of it's digits '''
    if num == 0:
        return False
    ds = get_digit_sum(num)
    if num % ds == 0:
        return True
    else:
        return False

def is_narcissistic(num):
    ''' Equal to the sum of all digits raised to the power of the number of digits ''' 
    ds = get_digits(num)
    m = len(ds)
    total = 0
    for d in ds:
        total += pow(d, m)
    if total == num:
        return True
    else:
        return False

def is_moran(num):
    ''' A niven (Harshad) number who's division by sum of digits is prime '''
    if num == 0:
        return False
    if not is_niven(num):
        return False
    ds = get_digit_sum(num)
    if (num/ds) in primes:
        return True

def is_cyclops(num):
    ''' the digit 0 only appears once in the middle of the number'''
    if num == 0:
        return True
    digits = get_digits(num)
    if (len(digits) % 2 == 0) or (digits.count(0) != 1):
        return False
    else:
        pos = digits.index(0)
        if pos == (len(digits)/2 - 0.5): 
            return True
    return False

def is_single_digit_product(num, digits):
    '''
    A function to test if a number can possibly be a product of x
    or less single digit numbers
    Takes in positive numbers only
    '''
    # if the number is prime and larger than 10 it cannot be factored by single digits
    if num > 10 and is_prime(num):
        return False
    # if number is larger than 9^x it is too big
    elif num > pow(9, digits):
        return False
    elif num < 11:
        return True
    # find single digit factors
    factors = []
    for i in range(2, 10):
        if num % i == 0:
            factors.append(i)
    return is_factorable(num, factors, 1, digits)
        
def is_factorable(num, factors, depth, max_depth):
    ''' a function to test if a number can be evenly factored using a 
        at most max_depth's factors from factor list
    '''
    # if max depth is reached return False
    if depth > max_depth:
        return False
    for factor in factors:
        # if num is factorable go down one depth
        if num % factor == 0:
            new_num = num/factor
            if new_num == 1:
                return True
            if is_factorable(new_num, factors, depth + 1, max_depth):
                return True
    return False
            
def num_to_english(num):
    return num2words(num)

ban_letters = ['a', 'e', 'i', 'o', 't', 'u']
def is_ban(num, letter):
    ''' inputs are ['a', 'e', 'i', 'o', 't', 'u'] '''
    num_str = num_to_english(num)
    num_str = num_str.replace(" and", "")    
    ''' Returns true if a number is an oban'''
    return not(letter in num_str)


def digit_product_is(num, rule):
    dp = get_digit_product(num)
    return rule(dp)

def digit_sum_is(num, rule):
    ds = get_digit_sum(num)
    return rule(ds)

# Functions for running rules with input lists
def test_rule(rule, in_lst=list(range(max_num))):
    lst = []
    for i in in_lst:
        if rule(i):
            lst.append(i)
    return lst

def test_rule_two_input(rule, input2, in_lst=list(range(max_num))):
    lst = []
    for i in in_lst:
        if rule(i, input2):
            lst.append(i)
    return lst

def sort_rules(rules_lst, modulars, all_rules=[]):
    ''' Modifies input lists '''
    if all_rules == []:
        for rule_level in rules:
            all_rules.extend(rule_level)
    rule_ids = []
    for rule in rules_lst:
        rule_ids.append(all_rules.index(rule))
    while rule_ids != sorted(rule_ids):
        for i in range(0, len(rule_ids) - 1):
            if rule_ids[i] > rule_ids[i + 1]:
                switch_id = rule_ids[i]
                switch_func = rules_lst[i]
                switch_mod = modulars[i]
                rule_ids[i] = rule_ids[i + 1]
                rule_ids[i + 1] = switch_id
                rules_lst[i] = rules_lst[i + 1]
                rules_lst[i + 1] = switch_func
                modulars[i] = modulars[i + 1]
                modulars[i + 1] = switch_mod
    return None
                
rules = [[]]
# LEVEL 1
rules.append([is_digit_sum, is_digit_sum, is_score_divisible, is_lives_divisible, is_level_divisible, score_is_divisible, is_even, is_odd, is_increasing, is_decreasing, is_evenish, is_oddish, is_cyclops, is_ban, is_digit_sum])
# LEVEL 2
rules.append([digit_sum_is, is_prime, is_composite, is_alternating, is_undulating, is_palindrome, is_twin_prime, is_digit_product, is_digit_sum_eq_prdct, is_ban, is_nude])
# LEVEL 3
rules.append([digit_product_is, digit_product_is, digit_sum_is, is_nt_alternating, is_nt_undulating, is_semiprime, is_interprime, is_semiprime, is_interprime, is_digit_sum, is_digit_product, is_nt_palindrome, is_strictly_decreasing, is_strictly_increasing])
# LEVEL 4
rules.append([digit_product_is, digit_sum_is, is_niven, is_narcissistic, is_emirp, is_emirpimes, is_digit_sum, is_emirpretni, is_digit_product])
# LEVEL 5
rules.append([digit_product_is, digit_sum_is, is_moran, is_ban, is_digit_product, is_digit_sum])
# LEVEL 6
rules.append([digit_product_is, digit_sum_is, is_digit_product])
#LEVEL 7
rules.append([])
#LEVEL 8
rules.append([])
#LEVEL 9
rules.append([])
#LEVEL 10
rules.append([])

def build_rules(level, min_num, max_num, questions_asked=[]):
    # Get Rules List
    level_rules = []
    for i in range(1, level + 1):
        level_rules.extend(rules[i])
    while True:
        curr_rules = sample(level_rules, num_rules)
        #make sum and product exlusions
        product_exclusion = []
        ban_exclusion = []
        sum_exclusion = [is_even, is_odd]
        if check_rule_exclusions(curr_rules, level, min_num, max_num) and check_rule_not_same(curr_rules, questions_asked, level):     
            lst = list(range(min_num, max_num+1))
            modulars = []
            for i in range(0, len(curr_rules)):
                rule = curr_rules[i]
                if rule is is_digit_sum:
                    test_lst = []
                    tries = 0
                    while test_lst == [] and tries < 100:                    
                        rand_num = randint(1, len((str(max_num-1))*9))
                        test_lst = test_rule_two_input(rule, rand_num, lst)
                        tries += 1
                    if rand_num == game_points:
                        rand_num = 'your score'
                    elif rand_num == lives:
                        rand_num = 'your remaining lives'
                    elif rand_num == level:
                        rand_num = 'your current level'
                    lst = test_lst
                    modulars.append(rand_num)
                elif rule is is_digit_product:
                    test_lst = []
                    tries = 0
                    shuffle(single_digit_productable)
                    while test_lst == [] and tries < len(single_digit_productable):
                        if single_digit_productable[tries] not in product_exclusion:
                            test_lst = test_rule_two_input(rule, single_digit_productable[tries], lst)
                        tries = tries + 1
                    lst = test_lst
                    if single_digit_productable[tries-1] == game_points:
                        modulars.append('your score')
                    elif single_digit_productable[tries-1] == lives:
                        modulars.append('your remaining lives')
                    elif single_digit_productable[tries-1] == level:
                        modulars.append('your current level')    
                    else:
                        modulars.append(single_digit_productable[tries -1])
                    product_exclusion.append(single_digit_productable[tries -1])
                elif rule is is_ban:
                    test_lst = []
                    shuffle(ban_letters)
                    for letter in ban_letters:
                        # Don't use an aban number if the max number is less than 1000 (it is redundant)
                        if letter not in ban_exclusion and (letter != 'a' or max_num > 1000):
                            test_lst = test_rule_two_input(rule, letter, lst)
                            if test_lst != []:
                                break
                    lst = test_lst
                    modulars.append(letter)
                    ban_exclusion.append(letter)
                elif rule is digit_product_is or rule is digit_sum_is:
                    test_lst = []
                    shuffle(level_rules)
                    tried_rules = [is_digit_product, is_digit_sum, is_ban, digit_product_is, digit_sum_is, is_digit_sum_eq_prdct]
                    tries = 0
                    while test_lst == [] and tries < len(level_rules):
                        new_rule = level_rules[tries]
                        if new_rule not in tried_rules and ((rule is digit_product_is and level_rules[tries] not in product_exclusion) or (rule is digit_sum_is and level_rules[tries] not in sum_exclusion)):
                            test_lst = test_rule_two_input(rule, new_rule, lst)
                            tried_rules.append(new_rule)
                        appendage = new_rule
                        tries += 1
                    lst = test_lst
                    modulars.append(new_rule)
                    if rule is digit_product_is:
                        product_exclusion.append(new_rule)
                    else:
                        sum_exclusion.append(new_rule)
                else:
                    new_lst = test_rule(rule, lst)
                    appendage = ''    
                    if new_lst == []:
                        shuffle(level_rules)
                        # ADD SUPPORT FOR THESE LATER!
                        tried_rules = [is_digit_sum, is_ban, digit_product_is, digit_sum_is]
                        new_rule = is_digit_product
                        tries = -1                    
                    while new_lst == [] and tries < len(level_rules):
                        if new_rule is is_digit_product and level > 1 and tries == -1 and new_rule not in curr_rules:
                            test_lst = []
                            prod_tries = 0
                            shuffle(single_digit_productable)
                            while test_lst == [] and prod_tries < len(single_digit_productable):
                                if single_digit_productable[tries] not in product_exclusion:
                                    test_lst = test_rule_two_input(new_rule, single_digit_productable[prod_tries], lst)
                                prod_tries += 1
                            new_lst = test_lst
                            if single_digit_productable[prod_tries-1] == game_points:
                                appendage = ('your score')
                            elif single_digit_productable[prod_tries-1] == lives:
                                appendage = ('your remaining lives')
                            elif single_digit_productable[prod_tries-1] == level:
                                appendage = ('your current level')
                            else:
                                appendage = single_digit_productable[prod_tries -1]
                            product_exclusion.append(single_digit_productable[prod_tries -1])
                            tried_rules.append(new_rule)
                            curr_rules[i] = new_rule
                        elif new_lst == [] and new_rule not in tried_rules:
                            new_rule = level_rules[tries]
                            curr_rules[i] = new_rule
                            if (new_rule not in curr_rules) and (new_rule not in tried_rules) and (check_rule_exclusions(curr_rules, level, min_num, max_num)) and check_rule_not_same(curr_rules, questions_asked, level):
                                new_lst = test_rule(new_rule, lst)
                                tried_rules.append(new_rule)
                                if lst != []:
                                    print('Generated' + str(new_rule))                                
                        tries += 1
                    lst = new_lst
                    modulars.append(appendage)
                if lst == []:
                    print('failed to generate')
                    global cyclops_trigger
                    if cyclops_trigger:
                        cyclops_trigger = False
                    break
            if (lst != [] and len(lst) <= solutions_per_level[level]):
                # Sort the list of rules
                sort_rules(curr_rules, modulars, level_rules)                        
                if not check_question_asked(curr_rules, modulars, min_num, max_num, questions_asked):
                    if cyclops_trigger:
                        global cyclops_count
                        cyclops_count += 1
                    return (curr_rules, lst, modulars, (min_num, max_num))

def check_rule_not_same(curr_rules, questions_asked, level):
    ''' Returns False if one of the non-modular rules was used in previous questions - increase spread with level '''
    if len(questions_asked) >= level:
        for rule in curr_rules:
            if rule not in [is_ban, is_digit_product, is_digit_sum, digit_product_is, digit_sum_is]:
                for i in range(0, level):
                    if rule in questions_asked[-i][0]:
                        return False
    return True

def check_question_asked(rules, modulars, min_num, max_num, questions_asked):
    ''' Check to see if a question has been asked before 
    returns true if asked before
    '''
    for question in questions_asked:
        if rules == question[0] and modulars == question[1] and question[2][0] == min_num and question[2][1] == max_num and 'your score' not in modulars and 'your current level' not in modulars and 'your remaining lives' not in modulars:
            return True
    return False

def check_rule_exclusions(rules, level, min_num, max_num):
    if rules.count(is_digit_sum) > 1:
        return False
    elif is_emirp in rules and is_prime in rules:
        return False
    elif is_prime in rules and is_twin_prime in rules:
        return False
    elif is_semiprime in rules and is_emirpimes in rules:
        return False
    elif (is_prime in rules or is_emirp in rules or is_twin_prime) and (is_semiprime in rules or is_emirpimes in rules or is_interprime in rules or is_emirpretni in rules):
        return False
    elif is_interprime in rules and is_emirpretni in rules:
        return False
    elif is_odd and is_even in rules:
        return False
    elif is_digit_sum in rules and (is_evenish in rules or is_oddish in rules):
        return False
    elif is_evenish and is_oddish in rules:
        return False
    elif is_niven in rules and is_moran in rules:
        return False
    elif is_decreasing in rules and is_strictly_decreasing in rules:
        return False
    elif is_increasing in rules and is_strictly_increasing in rules:
        return False
    elif is_alternating in rules and is_nt_alternating in rules:
        return False
    elif is_undulating in rules and is_nt_undulating in rules:
        return False
    elif is_palindrome in rules and is_nt_palindrome in rules:
        return False
    elif is_composite in rules and is_digit_product in rules:
        return False
    if is_cyclops in rules:
        if cyclops_count == 0 and min_num < 100:
            global cyclops_trigger
            cyclops_trigger = True
        else:
            return False
    if (is_score_divisible in rules or is_lives_divisible in rules or is_level_divisible in rules or score_is_divisible in rules):
        if score_is_divisible in rules and game_points == 0:
            return False
        if game_points in [0, 1] and is_score_divisible in rules:
            return False
        elif lives in [0, 1] and is_lives_divisible in rules:
            return False
        elif level in [0, 1] and is_level_divisible in rules:
            return False
        elif level == 2 and is_level_divisible in rules and is_even in rules:
            return False
        elif lives == 2 and is_lives_divisible in rules and is_even in rules:
            return False
        elif game_points == 2 and is_score_divisible in rules and is_even in rules:
            return False
        elif is_score_divisible in rules and is_lives_divisible in rules and lives == game_points:
            return False
        elif is_score_divisible in rules and is_level_divisible in rules and game_points == level:
            return False
        elif is_lives_divisible in rules and is_level_divisible in rules and lives == level:
            return False
    elif is_digit_product in rules and digit_product_is in rules:
        return False
    elif is_digit_sum in rules and digit_sum_is in rules:
        return False    
    else:
        return True

def print_rules(given_rules, min_num, max_num, needed_sols):
    global display_text
    display_text = ''
    strs = []
    modulars = copy.deepcopy(given_rules[2])
    #print(given_rules)
    for rule in given_rules[0]:
        curr_mod = modulars.pop(0)
        if rule is is_prime:
            strs.append('X is a prime number')
        elif rule is is_composite:
            strs.append('X is a composite number')
        elif rule is is_even:
            if game_points == 2:
                str1 = "X is evenly divisible by your score"
                str2 = "Your score is a factor of X"
            elif level == 2:
                str2 = "X is evenly divisible by your score"
                str1 = "Your current level is a factor of X"
            elif lives == 2:
                str1 = "X is evenly divisible by your score"
                str2 = "Your reamining number of lives is a factor of X"
            else:
                str1 = 'X is an even number'
                str2 = 'X is not an odd number'
            if game_points % 2 == 0:
                str3 = 'X has the same parity as your current score'
            else:
                str3 = "X's parity is different than your current score's"
            strs.append((choices([str1, str2, str3], weights=(9, 3, 1))[0]))
        elif rule is is_odd:
            if game_points == 2:
                str1 = "Your score is not a facor of X"
                str2 = "X is not evenly divisible by your current score"
            elif level == 2:
                str1 = "Your current level is not a factor of X"
                str2 = "X is not evenly divisible by your current level"
            elif lives == 2:
                str2 = "X is an odd number"
                str1 = "Your remaining number of lives is not a factor of X"
            else:
                str1 = 'X is an odd number'
                str2 = 'X is not an even number'
            if game_points % 2 == 1:
                str3 = 'X has the same parity as your current score'
            else:
                str3 = "X's parity is different than your current score's"            
            strs.append((choices([str1, str2, str3], weights=(9, 3, 1))[0]))
        elif rule is is_digit_sum:
            rand_num = curr_mod
            strs.append("The sum of X's digits is " + str(rand_num))
        elif rule is is_digit_product:
            rand_num = curr_mod
            strs.append("The product of X's digits is " + str(rand_num))
        elif rule is is_ban:
            letter = curr_mod
            if letter in "tu":
                strs.append("X is a " + letter + "ban number in English")
            else:
                strs.append("X is an " + letter + "ban number in English")
        elif rule is is_alternating:
            strs.append('X is an alternating number')
        elif rule is is_nt_alternating:
            strs.append('X is a non-trivial alternating number')
        elif rule is is_undulating:
            strs.append('X is an undulating number')
        elif rule is is_nt_undulating:
            strs.append('X is a non-trivial undulating number')
        elif rule is is_palindrome:
            strs.append('X is a palindrome')
        elif rule is is_nt_palindrome:
            strs.append('X is a non-trivial palindrome')
        elif rule is is_decreasing:
            strs.append('X is a decreasing Number')
        elif rule is is_strictly_decreasing:
            strs.append('X is a strictly decreasing number')
        elif rule is is_increasing:
            strs.append('X is an increasing number')
        elif rule is is_strictly_increasing:
            strs.append('X is a strictly increasing number')
        elif rule is is_niven:
            strs.append('X is a niven (Harshad) number')
        elif rule is is_narcissistic:
            strs.append('X is a narcissistic (Armstrong) number')
        elif rule is is_moran:
            strs.append('X is a Moran number')
        elif rule is is_cyclops:
            strs.append('X is a cyclops number')
        elif rule is is_emirp:
            strs.append('X is an emirp')
        elif rule is is_oddish:
            str1 = 'X is an oddish number'
            str2 = 'X is not an evenish number'
            strs.append((choices([str1, str2], weights=(3, 1))[0]))
        elif rule is is_evenish:
            str1 = 'X is an evenish number'
            str2 = 'X is not an oddish number'
            strs.append((choices([str1, str2], weights=(3, 1))[0]))
        elif rule is is_semiprime:
            strs.append('X is a semiprime number')
        elif rule is is_emirpimes:
            strs.append('X is an emirpimes number')
        elif rule is is_nude:
            strs.append('X is a nude number')
        elif rule is is_interprime:
            strs.append('X is an interprime number')
        elif rule is is_emirpretni:
            strs.append('X is an emirpretni number')
        elif rule is is_twin_prime:
            strs.append('X is a twin prime number')
        elif rule is is_digit_sum_eq_prdct:
            str1 = "X's digit sum & digit product are equal"
            str2 = "X's digit product & digit sum are equal"
            strs.append(choice([str1, str2]))
        elif rule is is_score_divisible:
            strs.append("X is evenly divisible by your current score")
        elif rule is score_is_divisible:
            strs.append("Your current score is evenly divisible by X")
        elif rule is is_lives_divisible:
            strs.append("X is evenly divisible by your remaining lives")
        elif rule is is_level_divisible:
            strs.append("X is evenly divisible by your current level")
        elif rule is digit_product_is:
            strs.append(print_modular_rule(rule, curr_mod))
        elif rule is digit_sum_is:
            strs.append(print_modular_rule(rule, curr_mod))
        else:
            strs.append(str(rule))
    num_sols = str(len(given_rules[1]))
    #display_text += 'Your Current Maximum Number is: ' + str(max_num) + '\n'
    #display_text += 'Your Current Mimumum Number is: ' + str(min_num) + '\n'
    if num_sols == '1':
        display_text += 'This question has 1 solution\n'
    else:
        display_text += 'This question has ' + num_sols + ' solutions\n'
    #if needed_sols == 1 and num_sols == 1:
        #display_text += "Find it to complete this question"
    #elif needed_sols == 1:
        #display_text += "Find 1 solution to complete this question"
    #else:
    if needed_sols > 1:
        display_text += "Find " + str(needed_sols) + " solutions to complete this question\n"
    # Shuffle the order of the rules
    shuffle(strs)
    for string in strs:
        display_text += string + '\n'

def print_modular_rule(rule, modular_rule):
    ''' Used for generating message for Digit product and digit sum modular rules '''
    result = "X's "
    if rule is digit_product_is:
        result += "digit product is "
    else:
        result += "digit sum is "
    if modular_rule is is_prime:
        result += "a prime number"
    elif modular_rule is is_composite:
        result += "a composite number"
    elif modular_rule is is_alternating:
        result += "an alternating number"
    elif modular_rule is is_nt_alternating:
        result += "a non-trivial alternating number"
    elif modular_rule is is_undulating:
        result += "an undulating number"
    elif modular_rule is is_nt_undulating:
        result += "a non-trivial undulating number"
    elif modular_rule is is_palindrome:
        result += "a palindromic number"
    elif modular_rule is is_nt_palindrome:
        result += "a non-trivial palindrome"
    elif modular_rule is is_decreasing:
        result += "a decreasing number"
    elif modular_rule is is_strictly_decreasing:
        result += "a stricty decreasing number"
    elif modular_rule is is_increasing:
        result += "an increasing number"
    elif modular_rule is is_strictly_increasing:
        result += "a stricty increasing number"
    elif modular_rule is is_niven:
        result += "a niven number"
    elif modular_rule is is_narcissistic:
        result += "a narcissistic number"
    elif modular_rule is is_cyclops:
        result += "a cyclops number"
    elif modular_rule is is_emirp:
        result += "an emirp"
    elif modular_rule is is_oddish:
        str1 = "an oddish number"
        str2 = "not an evenish number"
        result += choices([str1, str2], weights=(3, 1))[0]
    elif modular_rule is is_odd:
        result += "an odd number"
    elif modular_rule is is_even:
        result += "an even number"
    elif modular_rule is is_evenish:
        str1 = "an evenish number"
        str2 = "not an oddish number"
        result += choices([str1, str2], weights=(3, 1))[0]
    elif modular_rule is is_semiprime:
        result += "a semiprime number"
    elif modular_rule is is_emirpimes:
        result += "an emirpimes number"
    elif modular_rule is is_nude:
        result += "a nude number"
    elif modular_rule is is_interprime:
        result += "an interprime number"
    elif modular_rule is is_emirpretni:
        result += "an emirpretni number"
    elif modular_rule is is_twin_prime:
        result += "a twin prime number"
    elif modular_rule is is_digit_sum_eq_prdct:
        result = result[:-2] + "'s digit product is equal to it's digit sum"
    elif modular_rule is is_score_divisible:
        result += "divisible by your current score"
    elif modular_rule is is_lives_divisible:
        result += "is divisible by your remaining lives"
    elif modular_rule is is_level_divisible:
        result += "is divisible by your current level"
    elif modular_rule is score_is_divisible:
        result += "is a factor of your score"
    else:
        result += str(modular_rule)
    return result
        
def rand_correct_message():
    ''' Returns a random success message '''
    messages = ['WOW CONGRATS ON A CORRECT ANSWER', 'THAT IS... CORRECT... NERD', 'DANG, YOU GOT THAT RIGHT!']
    messages.extend(['COOL, YOU GOT THIS ONE RIGHT', 'UwU u got anovver onye wight', 'NICE JOB, THAT IS CORRECT'])
    messages.extend(['ARE YOU A MATH WHIZ?\nTHAT IS A RIGHT ANSWER!', 'SO SMORT, THAT WORKS!'])
    return choice(messages)


def load_question(level, lives=3, game_points=0, questions_asked=[]):
    max_num = max_nums[randint(0, level)]
    min_num = True
    while min_num is True or min_num >= max_num:
        min_num = min_nums[randint(0, level)]
    rules = build_rules(level, min_num, max_num, questions_asked)
    global needed_sols
    needed_sols = min(min_sol_per_level[level], len(rules[1]))
    print_rules(rules, min_num, max_num, needed_sols)
    if debug:
        print(rules[1])
    global start_time
    start_time = time()
    global prev_answers
    prev_answers = []
    global buffer_points
    buffer_points = 0
    global question_number
    question_number += 1
    questions_asked.append([rules[0], rules[2], rules[3]])
    global input_text
    input_text = 'Enter A Value'
    return (rules, questions_asked)

def check_answer(answer):
    global current_question
    global start_time
    global level
    global game_points
    global display_text
    global game_state
    global lives
    global input_text
    global questions_ans
    global game_time
    global prev_answers
    global buffer_points
    global needed_sols
    time_taken = time() - start_time
    try:
        int(answer)
        x = True
    except:
        x = False
    if x:
        if needed_sols > 1 and int(answer) in current_question[1] and int(answer) not in prev_answers:
            points = calculate_point_value(int(answer), current_question, level, time_taken)
            display_text += str(answer) + ' is one of the correct solutions!\n'
            buffer_points += points
            needed_sols -= 1
        elif int(answer) in current_question[1]:
            game_time += time_taken
            display_text = ''
            display_text += rand_correct_message() + '\n'
            display_text += 'Time taken: ' + str(int(time_taken)) + 's\n'
            points = calculate_point_value(int(answer), current_question, level, time_taken)
            if points + buffer_points == 1:
                display_text += 'You have earned 1 point!\n'
            else:
                display_text += 'You have earned ' + str(points + buffer_points) + ' points!\n'
            game_points += points + buffer_points
            questions_ans += 1
            display_text += 'Your new point total is: ' + str(game_points) + '\n'
            check_levelup()
            input_text = 'Press ENTER'
            game_state = 'Waiting to generate new question'
        else:
            display_text += answer + ' is WRONG! You have lost a life.\n'
            lives -= 1
            if lives <= 0:
                display_text = ''
                display_text += 'Game Over!\n'
                display_text += 'You earned ' +  str(game_points) + ' points.\n'
                display_text += 'In ' + str(questions_ans) + ' question'
                if questions_ans != 1:
                    display_text += 's'
                display_text += '\n'
                display_text += 'You played for ' + str(int(game_time + time_taken)) + 's\n'
                display_text += 'Press Enter to play again\n'
                input_text = 'PRESS ENTER'
                game_state = 'Not Running'
    #except:
        #input_text = 'Try Again'

    return (game_points, lives, questions_asked)    


def calculate_point_value(answer, given_rules, level, time_taken):
    # Points = ceil(Answer * rules_value / possible solutions)
    # Calculate rules value
    rules_values = []
    for rule in given_rules[0]:
        for i in range(1, level + 1):
            if rule in rules[i]:
                rules_values.append(i)
                break
    rules_values.sort(reverse=True)
    rules_value = 1
    for i in list(range(1, len(rules_values)+1))[::-1]:
        rules_value *= max(1, rules_values.pop(0) * i/len(given_rules[0]))
    # calculate time modifier
    if time_taken <= 5:
        time_modifier = 3
    else:
        time_modifier = max(0.5, min(pow(0.97, time_taken-5) + 1, pow(0.99, time_taken-77)))
    # get number of possible solutions
    possible_solutions = len(given_rules[1])
    # get solutions modifier
    if possible_solutions == 1:
        sol_modifier = 3
    elif possible_solutions == 2:
        sol_modifier = 2
    else:
        sol_modifier = 1 + 1/(possible_solutions**(1/2))
    # get answer value
    #ans_value = min(max(1, math.sqrt(answer)), max(1, answer/20))
    ans_modifier = max(1, min(answer**(1/4), answer/216 + 1))
    points = ceil(ans_modifier * rules_value * time_modifier * sol_modifier)
    return points


def check_levelup():
    global game_points
    global levelup_table
    global level
    global lives
    global display_text
    if (level < 10 and game_points >= levelup_table[level]):
        level += 1
        display_text += 'LEVEL UP\n'
        display_text += '+1 LIFE!\n'
        display_text += 'Press Enter to go to next level\n'
        lives += 1    


def start_game(start_level=1):
    global game_state
    global game_points
    global lives
    global level
    global display_text
    global game_time
    game_time = 0
    game_state = 'Awaiting Answer'
    game_points = 0
    global question_number
    question_number = 0
    level = start_level
    lives = starting_lives
    global cyclops_count
    cyclops_count = 0
    global questions_ans
    questions_ans = 0
    global questions_asked
    questions_asked = []
    question_results = load_question(level, lives, game_points, questions_asked)
    global current_question
    current_question = question_results[0]
    questions_asked = question_results[1]


def next_question():
    global game_state
    global game_points
    global lives
    global level
    global display_text
    global questions_ans
    global questions_asked
    question_results = load_question(level, lives, game_points, questions_asked)
    global current_question
    current_question = question_results[0]
    questions_asked = question_results[1]
    game_state = 'Awaiting Answer'

    
def main():
    global display_text
    global input_text
    print(display_text)
    global game_state
    global lives
    global questions_asked
    global current_question
    while True:
        #print(questions_asked)
        #print(current_question)
        try:    
            if game_state == "Not Running":
                in_input = input()
                if in_input == "0118999":
                    start_game(6)
                else:
                    start_game(1)
                print(display_text)
                curr_lives = lives
            elif game_state == "Awaiting Answer":
                check_answer(input())
                if game_state == "Awaiting Answer" and curr_lives > lives:
                    print(display_text + '\n' + input_text)
                elif game_state == "Awaiting Answer":
                    print(display_text)                
                else:
                    print(display_text)
                curr_lives = lives
            elif game_state == 'Waiting to generate new question':
                #input()
                next_question()
                print(display_text)
                curr_lives = lives
        except EOFError:
            break        