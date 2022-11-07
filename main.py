from random import randint
from itertools import permutations
from typing import List
from math import sqrt
import time

operand = ['+', '-', '*', '/']
startTime = time.time()
result = 0


def get_all_possible_val(p_numlist: List) -> List:
    all_possiblepos_val = dict()
    for nums in p_numlist:
        a, b, c, d = nums
        L1 = pos_val((a, str(a)), (b, str(b)))
        L2 = pos_val((c, str(c)), (d, str(d)))
        for x1, str_x1 in L1:
            for x2, str_x2 in L2:
                possible = pos_val((x1, str_x1), (x2, str_x2))
                val, equ = findClosestValue(possible, result)
                if val not in all_possiblepos_val:
                    all_possiblepos_val[val] = equ
                elif len(equ) < len(all_possiblepos_val[val]):
                    all_possiblepos_val[val] = equ
                if val == result and len(equ) <= 15 and "√" not in equ:
                    print("found way after: " +
                          str(len(all_possiblepos_val)) + " ways")
                    return [(val, equ)]

    print("all possible way: " + str(len(all_possiblepos_val)) + " ways")
    return list(all_possiblepos_val.items())


def pos_val(num1: tuple(), num2: tuple()) -> tuple():
    pos_value = []

    num1, str1 = num1
    num2, str2 = num2
    pos_value += pos_val_basic((num1, str1), (num2, str2))
    pos_value += pos_val_basic((-num1, f'-{str1}'), (num2, str2))

    temp1 = sqrt(abs(num1))
    temp2 = sqrt(abs(num2))

    pos_value += pos_val_basic((temp1,
                                f'root|{str1}|'), ((temp2, f'root|{str2}|')))
    pos_value += pos_val_basic((-temp1,
                                f'-root|{str1}|'), ((temp2, f'root|{str2}|')))

    pos_value += pos_val_basic((temp1,
                                f'root|{str1}|'), ((num2, str2)))
    pos_value += pos_val_basic((-temp1,
                                f'-root|{str1}|'), ((num2, str2)))

    pos_value += pos_val_basic((num1, str1),
                               ((temp2, f'root|{str2}|')))
    pos_value += pos_val_basic((-num1,
                                f'-{str1}'), (temp2, f'root|{str2}|'))

    dic = dict()
    perfect_equ = list(filter(lambda x: x[0] == result, pos_value))
    if len(perfect_equ) == 0:
        for val, string in pos_value:
            if abs(val - result) < 20:
                if val not in dic:
                    dic[val] = string
                elif len(string) < len(dic[val]):
                    dic[val] = string

        pos_value = list(dic.items())
        return pos_value
    else:
        ansEqu = perfect_equ[0][1]
        for _, equ in perfect_equ:
            if len(equ) < len(ansEqu):
                ansEqu = equ
            if len(ansEqu) <= 20:
                return [(result, ansEqu)]
        return [(result, ansEqu)]


def pos_val_basic(num1: tuple(), num2: tuple()) -> tuple():
    pos_value = []
    num1, str1 = num1
    num2, str2 = num2
    for oper in operand:
        if oper == '/' and num2 == 0:
            continue
        # value = eval(f'{num1}{oper}{num2}')
        if oper == '+':
            value = num1 + num2
        if oper == '-':
            value = num1 - num2
        if oper == '*':
            value = num1 * num2
        if oper == '/':
            value = num1 / num2

        pos_value.append((value, f'({str1}{oper}{str2})'))
    return pos_value


def findClosestValue(all_possible_val: List, target: int) -> tuple:
    maxx = 1e9
    ansVal = 0
    ansEqu = ''
    for val, equ in all_possible_val:
        if abs(val - target) < maxx:
            maxx = abs(val - target)
            ansVal = val
            ansEqu = equ
    ansEqu = ansEqu.replace('-+', '-').replace('--', '+')\
        .replace('+-', '-').replace('|(', '|').replace(')|', '|').replace('root', '√')
    return (ansVal, ansEqu)


def removeParenthesis(equ: str) -> str:
    val, equ = equ
    parenthesis = []
    remove = True
    for i in range(len(equ)):
        if len(parenthesis) != 0:
            if parenthesis[0] != 0:
                remove = False
                break
        if equ[i] == '(':
            parenthesis.append(i)
        elif equ[i] == ')':
            parenthesis.pop(-1)
    if remove:
        equ = equ[1:-1]
    return (val, equ)


def main():
    global result
    numlist = [randint(0, 9) for _ in range(4)]
    while(numlist.count(0) >= 2):
        numlist = [randint(0, 9) for _ in range(4)]
    result = randint(0, 2400)//100

    p_numlist = list(permutations(numlist))
    prototype = f'{numlist[0]} {numlist[1]} {numlist[2]} {numlist[3]} = {result}'
    print(prototype)

    all_possible = get_all_possible_val(p_numlist)
    best_way = findClosestValue(all_possible, result)
    best_way = removeParenthesis(best_way)
    val, equ = best_way

    print(f'best way: {equ} = {val}')
    print(f'cost time: {time.time()-startTime}')


if __name__ == "__main__":
    main()
