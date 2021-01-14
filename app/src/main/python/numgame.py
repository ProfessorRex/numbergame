from numpy import base_repr
from random import randint, choices, choice, shuffle, sample
from math import ceil
from time import time
import copy
from num2words import num2words
from six.moves import input
primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,461,463,467,479,487,491,499,503,509,521,523,541,547,557,563,569,571,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661,673,677,683,691,701,709,719,727,733,739,743,751,757,761,769,773,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,883,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997,1009,1013,1019,1021,1031,1033,1039,1049,1051,1061,1063,1069,1087,1091,1093,1097,1103,1109,1117,1123,1129,1151,1153,1163,1171,1181,1187,1193,1201,1213,1217,1223,1229,1231,1237,1249,1259,1277,1279,1283,1289,1291,1297,1301,1303,1307,1319,1321,1327,1361,1367,1373,1381,1399,1409,1423,1427,1429,1433,1439,1447,1451,1453,1459,1471,1481,1483,1487,1489,1493,1499,1511,1523,1531,1543,1549,1553,1559,1567,1571,1579,1583,1597,1601,1607,1609,1613,1619,1621,1627,1637,1657,1663,1667,1669,1693,1697,1699,1709,1721,1723,1733,1741,1747,1753,1759,1777,1783,1787,1789,1801,1811,1823,1831,1847,1861,1867,1871,1873,1877,1879,1889,1901,1907,1913,1931,1933,1949,1951,1973,1979,1987,1993,1997,1999,2003,2011,2017,2027,2029,2039,2053,2063,2069,2081,2083,2087,2089,2099,2111,2113,2129,2131,2137,2141,2143,2153,2161,2179,2203,2207,2213,2221,2237,2239,2243,2251,2267,2269,2273,2281,2287,2293,2297,2309,2311,2333,2339,2341,2347,2351,2357,2371,2377,2381,2383,2389,2393,2399,2411,2417,2423,2437,2441,2447,2459,2467,2473,2477,2503,2521,2531,2539,2543,2549,2551,2557,2579,2591,2593,2609,2617,2621,2633,2647,2657,2659,2663,2671,2677,2683,2687,2689,2693,2699,2707,2711,2713,2719,2729,2731,2741,2749,2753,2767,2777,2789,2791,2797,2801,2803,2819,2833,2837,2843,2851,2857,2861,2879,2887,2897,2903,2909,2917,2927,2939,2953,2957,2963,2969,2971,2999,3001,3011,3019,3023,3037,3041,3049,3061,3067,3079,3083,3089,3109,3119,3121,3137,3163,3167,3169,3181,3187,3191,3203,3209,3217,3221,3229,3251,3253,3257,3259,3271,3299,3301,3307,3313,3319,3323,3329,3331,3343,3347,3359,3361,3371,3373,3389,3391,3407,3413,3433,3449,3457,3461,3463,3467,3469,3491,3499,3511,3517,3527,3529,3533,3539,3541,3547,3557,3559,3571,3581,3583,3593,3607,3613,3617,3623,3631,3637,3643,3659,3671,3673,3677,3691,3697,3701,3709,3719,3727,3733,3739,3761,3767,3769,3779,3793,3797,3803,3821,3823,3833,3847,3851,3853,3863,3877,3881,3889,3907,3911,3917,3919,3923,3929,3931,3943,3947,3967,3989,4001,4003,4007,4013,4019,4021,4027,4049,4051,4057,4073,4079,4091,4093,4099,4111,4127,4129,4133,4139,4153,4157,4159,4177,4201,4211,4217,4219,4229,4231,4241,4243,4253,4259,4261,4271,4273,4283,4289,4297,4327,4337,4339,4349,4357,4363,4373,4391,4397,4409,4421,4423,4441,4447,4451,4457,4463,4481,4483,4493,4507,4513,4517,4519,4523,4547,4549,4561,4567,4583,4591,4597,4603,4621,4637,4639,4643,4649,4651,4657,4663,4673,4679,4691,4703,4721,4723,4729,4733,4751,4759,4783,4787,4789,4793,4799,4801,4813,4817,4831,4861,4871,4877,4889,4903,4909,4919,4931,4933,4937,4943,4951,4957,4967,4969,4973,4987,4993,4999,5003,5009,5011,5021,5023,5039,5051,5059,5077,5081,5087,5099,5101,5107,5113,5119,5147,5153,5167,5171,5179,5189,5197,5209,5227,5231,5233,5237,5261,5273,5279,5281,5297,5303,5309,5323,5333,5347,5351,5381,5387,5393,5399,5407,5413,5417,5419,5431,5437,5441,5443,5449,5471,5477,5479,5483,5501,5503,5507,5519,5521,5527,5531,5557,5563,5569,5573,5581,5591,5623,5639,5641,5647,5651,5653,5657,5659,5669,5683,5689,5693,5701,5711,5717,5737,5741,5743,5749,5779,5783,5791,5801,5807,5813,5821,5827,5839,5843,5849,5851,5857,5861,5867,5869,5879,5881,5897,5903,5923,5927,5939,5953,5981,5987,6007,6011,6029,6037,6043,6047,6053,6067,6073,6079,6089,6091,6101,6113,6121,6131,6133,6143,6151,6163,6173,6197,6199,6203,6211,6217,6221,6229,6247,6257,6263,6269,6271,6277,6287,6299,6301,6311,6317,6323,6329,6337,6343,6353,6359,6361,6367,6373,6379,6389,6397,6421,6427,6449,6451,6469,6473,6481,6491,6521,6529,6547,6551,6553,6563,6569,6571,6577,6581,6599,6607,6619,6637,6653,6659,6661,6673,6679,6689,6691,6701,6703,6709,6719,6733,6737,6761,6763,6779,6781,6791,6793,6803,6823,6827,6829,6833,6841,6857,6863,6869,6871,6883,6899,6907,6911,6917,6947,6949,6959,6961,6967,6971,6977,6983,6991,6997,7001,7013,7019,7027,7039,7043,7057,7069,7079,7103,7109,7121,7127,7129,7151,7159,7177,7187,7193,7207,7211,7213,7219,7229,7237,7243,7247,7253,7283,7297,7307,7309,7321,7331,7333,7349,7351,7369,7393,7411,7417,7433,7451,7457,7459,7477,7481,7487,7489,7499,7507,7517,7523,7529,7537,7541,7547,7549,7559,7561,7573,7577,7583,7589,7591,7603,7607,7621,7639,7643,7649,7669,7673,7681,7687,7691,7699,7703,7717,7723,7727,7741,7753,7757,7759,7789,7793,7817,7823,7829,7841,7853,7867,7873,7877,7879,7883,7901,7907,7919,7927,7933,7937,7949,7951,7963,7993,8009,8011,8017,8039,8053,8059,8069,8081,8087,8089,8093,8101,8111,8221,8231,8233,8237,8243,8263,8269,8273,8287,8291,8293,8297,8311,8317,8329,8353,8363,8369,8377,8387,8389,8419,8423,8429,8431,8443,8447,8461,8467,8501,8513,8521,8527,8537,8539,8543,8563,8573,8581,8597,8599,8609,8623,8627,8629,8641,8647,8663,8669,8677,8681,8689,8693,8699,8707,8713,8719,8731,8737,8741,8747,8753,8761,8779,8783,8803,8807,8819,8821,8831,8837,8839,8849,8861,8863,8867,8887,8893,8923,8929,8933,8941,8951,8963,8969,8971,8999,9001,9007,9011,9013,9029,9041,9043,9049,9059,9067,9091,9103,9109,9127,9133,9137,9151,9157,9161,9173,9181,9187,9199,9203,9209,9221,9227,9239,9241,9257,9277,9281,9283,9293,9311,9319,9323,9337,9341,9343,9349,9371,9377,9391,9397,9403,9413,9419,9421,9431,9433,9437,9439,9461,9463,9467,9473,9479,9491,9497,9511,9521,9533,9539,9547,9551,9587,9601,9613,9619,9623,9629,9631,9643,9649,9661,9677,9679,9689,9697,9719,9721,9733,9739,9743,9749,9767,9769,9781,9787,9791,9803,9811,9817,9829,9833,9839,9851,9857,9859,9871,9883,9887,9901,9907,9923,9929,9931,9941,9949,9967,9973,10007]
single_digit_productable = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 24, 25, 27, 28, 30, 32, 35, 36, 40, 42, 45, 48, 49, 50, 54, 56, 60, 63, 64, 70, 72, 75, 80, 81, 84, 90, 96, 98, 100, 105, 108, 112, 120, 125, 126, 128, 135, 140, 144, 147, 150, 160, 162, 168, 175, 180, 189, 192, 196, 200, 210, 216, 224, 225, 240, 243, 245, 250, 252, 256, 270, 280, 288, 294, 300, 315, 320, 324, 336, 343, 350, 360, 375, 378, 384, 392, 400, 405, 420, 432, 441, 448, 450, 480, 486, 490, 500, 504, 512, 525, 540, 560, 567, 576, 588, 600, 625, 630, 640, 648, 672, 675, 686, 700, 720, 729, 735, 750, 756, 768, 784, 800, 810, 840, 864, 875, 882, 896, 900, 945, 960, 972, 980, 1000, 1008, 1024, 1029, 1050, 1080, 1120, 1125, 1134, 1152, 1176, 1200, 1215, 1225, 1260, 1280, 1296, 1323, 1344, 1350, 1372, 1400, 1440, 1458, 1470, 1512, 1536, 1568, 1575, 1600, 1620, 1680, 1701, 1715, 1728, 1764, 1792, 1800, 1890, 1920, 1944, 1960, 2016, 2025, 2048, 2058, 2160, 2187, 2205, 2240, 2268, 2304, 2352, 2401, 2430, 2520, 2560, 2592, 2646, 2688, 2744, 2835, 2880, 2916, 3024, 3072, 3087, 3136, 3240, 3402, 3456, 3528, 3584, 3645, 3888, 3969, 4032, 4096, 4374, 4536, 4608, 5103, 5184, 5832, 6561]

max_nums = [100, 100, 1000, 1000, 10_000, 10_000, 10_000]
max_num = 100
min_nums = [0, 0, 10, 10, 100, 1000, 1000]
num_rules = 3
starting_lives = 3
start_time = 0

#GLOBALS
game_points = 0
lives = 0
level = 1
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
rules.append([is_even, is_odd, is_digit_sum, is_cyclops, is_increasing, is_digit_sum, is_nude, is_decreasing, is_evenish, is_digit_sum, is_oddish, is_ban])
# LEVEL 2
rules.append([is_prime, is_composite, is_alternating, is_undulating, is_palindrome, is_twin_prime, is_digit_product, is_ban])
# LEVEL 3
rules.append([is_nt_alternating, is_nt_undulating, is_semiprime, is_interprime, is_semiprime, is_interprime, is_digit_sum, is_digit_product, is_nt_palindrome, is_strictly_decreasing, is_strictly_increasing])
# LEVEL 4
rules.append([is_niven, is_narcissistic, is_emirp, is_emirpimes, is_digit_sum, is_emirpretni, is_digit_product])
# LEVEL 5
rules.append([is_moran, is_ban, is_digit_product, is_digit_sum])
# LEVEL 6
rules.append([is_digit_product])

def build_rules(level, min_num, max_num, questions_asked=[]):
    # Get Rules List
    level_rules = []
    for i in range(1, level + 1):
        level_rules.extend(rules[i])
    not_generated = True
    while not_generated:
        curr_rules = sample(level_rules, num_rules)
        #make sum and product exlusions
        product_exlusion = []
        ban_exclusion = []
        if check_rule_exclusions(curr_rules, level):     
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
                    lst = test_lst
                    modulars.append(rand_num)
                elif rule is is_digit_product:
                    test_lst = []
                    tries = 0
                    shuffle(single_digit_productable)
                    while test_lst == [] and tries < len(single_digit_productable):
                        if single_digit_productable[tries] not in product_exlusion:
                            test_lst = test_rule_two_input(rule, single_digit_productable[tries], lst)
                        tries = tries + 1
                    lst = test_lst
                    modulars.append(single_digit_productable[tries - 1])
                    product_exlusion.append(single_digit_productable[tries -1])
                elif rule is is_ban:
                    test_lst = []
                    shuffle(ban_letters)
                    for letter in ban_letters:
                        if letter not in ban_exclusion:
                            test_lst = test_rule_two_input(rule, letter, lst)
                            if test_lst != []:
                                break
                    lst = test_lst
                    modulars.append(letter)
                    ban_exclusion.append(letter)
                else:
                    new_lst = test_rule(rule, lst)
                    tries = 25
                    appendage = ''
                    while new_lst == [] and tries < 25:
                        new_rule = is_digit_product
                        curr_rules[i] = new_rule
                        if new_rule is is_digit_product and level > 1:
                            test_lst = []
                            tries = 0
                            shuffle(single_digit_productable)
                            while test_lst == [] and tries < len(single_digit_productable):
                                if single_digit_productable[tries] not in product_exlusion:
                                    test_lst = test_rule_two_input(new_rule, single_digit_productable[tries], lst)
                                tries = tries + 1
                            new_lst = test_lst
                            appendage = single_digit_productable[tries -1]
                            product_exlusion.append(single_digit_productable[tries -1])
                        new_rule = choice(level_rules)
                        curr_rules[i] = new_rule
                        if (new_rule not in curr_rules) and (new_rule not in [is_ban, is_digit_sum, is_digit_product]) and (check_rule_exclusions(curr_rules, level)):
                            new_lst = test_rule(new_rule, lst)                        
                        tries += 1
                    lst = new_lst
                    modulars.append(appendage)
                if lst == []:
                    break
            if (lst != []):
                # Sort the list of rules
                sort_rules(curr_rules, modulars, level_rules)                        
                if not check_question_asked(curr_rules, modulars, min_num, max_num, questions_asked):
                    return (curr_rules, lst, modulars, (min_num, max_num))

def check_question_asked(rules, modulars, min_num, max_num, questions_asked):
    ''' Check to see if a question has been asked before 
    returns true if asked before
    '''
    for question in questions_asked:
        if rules == question[0] and modulars == question[1] and question[2][0] == min_num and question[2][1] == max_num:
            return True
    return False

def check_rule_exclusions(rules, level):
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
    elif level <= 2 and is_cyclops in rules:
        return False
    else:
        return True

def print_rules(given_rules, min_num, max_num):
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
            str1 = ('X is an Even Number')
            str2 = ('X is not an odd number')
            strs.append((choices([str1, str2], weights=(3, 1))[0]))
        elif rule is is_odd:
            str1 = ('X is an Odd Number')
            str2 = ('X is not an even number')
            strs.append((choices([str1, str2], weights=(3, 1))[0]))
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
            str1 = ('X is an oddish number')
            str2 = ('X is not an evenish number')
            strs.append((choices([str1, str2], weights=(3, 1))[0]))
        elif rule is is_evenish:
            str1 = ('X is an evenish number')
            str2 = ('X is not an oddish number')
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
        else:
            strs.append(rule)
    num_sols = str(len(given_rules[1]))
    display_text += 'Your Current Maximum Number is: ' + str(max_num) + '\n'
    display_text += 'Your Current Mimumum Number is: ' + str(min_num) + '\n'
    if num_sols == '1':
        display_text += 'This question has 1 solution\n'
    else:
        display_text += 'This question has ' + num_sols + ' solutions\n'
    # Shuffle the order of the rules
    shuffle(strs)
    for string in strs:
        display_text += string + '\n'

def rand_correct_message():
    ''' Returns a random success message '''
    messages = ['WOW CONGRATS ON A CORRECT ANSWER', 'THAT IS... CORRECT... NERD', 'DANG, YOU GOT THAT RIGHT!']
    messages.extend(['COOL, YOU GOT THIS ONE RIGHT', 'UwU u got anovver onye wight', 'NICE JOB, THAT IS CORRECT'])
    messages.extend(['ARE YOU A MATH WHIZ? THAT IS A RIGHT ANSWER!', 'SO SMORT, THAT WORKS!'])
    return choice(messages)


def load_question(level, lives=3, game_points=0, questions_asked=[]):
    max_num = max_nums[randint(0, level)]
    min_num = True
    while min_num is True or min_num >= max_num:
        min_num = min_nums[randint(0, level)]
    rules = build_rules(level, min_num, max_num, questions_asked)
    print_rules(rules, min_num, max_num)
    #print(rules[1])
    global start_time
    start_time = time()
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
    try:
        if int(answer) in current_question[1]:
            display_text = ''
            display_text += rand_correct_message() + '\n'
            display_text += 'Time taken: ' + str(int(time() - start_time)) + 's\n'
            points = calculate_point_value(int(answer), current_question, level, time() - start_time)
            display_text += 'You have earned ' + str(points) + ' points!\n'
            game_points += points
            questions_ans += 1
            display_text += 'Your new point total is: ' + str(game_points) + '\n'
            check_levelup()
            input_text = 'Press ENTER'
            game_state = 'Waiting to generate new question'
        else:
            display_text += answer + ' is WRONG! You have lost a life.\n'
            lives -= 1
            if lives > 0:
                input_text = 'TRY AGAIN'
            else:
                display_text = ''
                display_text += 'Game Over!\n'
                display_text += 'You earned ' +  str(game_points) + ' points.\n'
                display_text += 'In ' + str(questions_ans) + ' questions\n'
                display_text += 'Press Enter to play again\n'
                input_text = 'PRESS ENTER'
                game_state = 'Not Running'
    except:
        input_text = 'Try Again'

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

levelup_table = [0, 50, 200, 600, 1500, 3000]

def check_levelup():
    global game_points
    global levelup_table
    global level
    global lives
    global display_text
    if (level < 6 and game_points >= levelup_table[level]):
        level += 1
        display_text += 'LEVEL UP\n'
        display_text += '+1 LIFE!\n'
        display_text += 'Press Enter to go to next level\n'
        lives += 1    


def start_game(start_level):
    global game_state
    global game_points
    global lives
    global level
    global display_text
    game_state = 'Awaiting Answer'
    game_points = 0
    level = start_level
    lives = 3
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