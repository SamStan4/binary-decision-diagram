#!/bin/python3

from pyeda.inter import * # grabs us all of the functions and symbols from the pyeda library
from pyeda.boolalg.bdd import *
import os # for clearing the terminal

# this is for changing the color of the terminal, these are the same escape sequences
# that I use when I am changing color in c/c++

class colors:
    F_BLACK = '\033[30m'
    F_RED = '\033[31m'
    F_GREEN = '\033[32m'
    F_YELLOW = '\033[33m'
    F_BLUE = '\033[34m'
    F_MAGENTA = '\033[35m'
    F_CYAN = '\033[36m'
    F_WHITE = '\033[37m'
    
    B_BLACK = '\033[40m'
    B_RED = '\033[41m'
    B_GREEN = '\033[42m'
    B_YELLOW = '\033[43m'
    B_BLUE = '\033[44m'
    B_MAGENTA = '\033[45m'
    B_CYAN = '\033[46m'
    B_WHITE = '\033[47m'
    
    RESET = '\033[0m'

x_variables = [exprvar('x{}'.format(i)) for i in range(1, 6)]     # this will create the boolean variables that we are going to want 
y_variables = [exprvar('y{}'.format(i)) for i in range(1, 6)]     # and format it in the form { x1, x2, ... , x6 } and { y1, y2, ... , y6 }


def clear_terminal():

    if os.name == "nt": # windows
        os.system('cls')
    else: # mac / linux
        os.system('clear')

def pause():
    if os.name == 'nt': # windows
        os.system('pause')
    else: # mac/linux
        input('Press Enter to continue...')

def print_title():
        clear_terminal()
        print(colors.F_MAGENTA)
        print("  ___     ___.        .___  .___  ___     \n / _ \_/\ \_ |__    __| _/__| _/ / _ \_/\ \n \/ \___/  | __ \  / __ |/ __ |  \/ \___/ \n           | \_\ \/ /_/ / /_/ |           \n           |___  /\____ \____ |           \n               \/      \/    \/           \n")
        print(colors.RESET)

def main_menu():

    x = True
    list_decisions = [ 1, 2, 3, 4, 5, 6, 7, 8]

    while (x):

        print_title()
        print(colors.F_GREEN)
        #print(colors.B_CYAN + "---Main Menu---\n" + colors.RESET)

        print("enter '1' to print the RR BDD")
        print("enter '2' to print the EVEN BDD")
        print("enter '3' to print the PRIME BDD")
        print("enter '4' to run test cases on RR, EVEN, and PRIME BDDs")
        print("enter '5' to run test cases on RR2")
        print("enter '6' to run test cases on RR star")
        print("enter '7' to run all test cases         " + colors.RESET + colors.B_MAGENTA + "<-- TA choose this option"  + colors.RESET + colors.F_GREEN)
        print("enter '8' to exit the program")

        print(colors.RESET)


        try: # try block to that this input doesnt crash the program
            decision = int(input("\nEnter here: "))

            if decision in list_decisions:
                x = False
        except:
            x = True

    return decision

def main():
    decision = 0

    RR_BDD = make_RR_BDD()

    while (decision != 8):
        decision = main_menu()

        if (decision == 1):
            print("option one")
        elif (decision == 2):
            print("option two")
        elif (decision == 3):
            print("option three")
        elif (decision == 4):
            print("option four")
        elif (decision == 5):
            print("running test cases on RR2 BDD")
        elif (decision == 6):
            print("running test cases on RRstar BDD")
        elif (decision == 7):
            print("running all test cases")
        elif (decision == 8):
            break
        
        pause()

#*********************************************************************************************************************************************#
#   function name       : make_32_node_BDD()
#   functional purpose  : this function answers the question: (i + 3)%32 = j%32 or (i + 8)%32 = j%32.
#   inputs              : int, int
#   outputs             : boolean
#   preconditions       : none
#   postconditions      : none
#   programmer          : Sam Stanley

def edge_rule(x_node, y_node):
    if ((((x_node + 3) % 32) == (y_node % 32)) or (((x_node + 8) % 32) == (y_node % 32))):
        return True
    else:
        return False

def convert_into_five_bit_array(num):
    result = [0, 0, 0, 0, 0]
    for i in range(4, -1, -1):
        if num >= 2 ** i:
            result[i] = 1 # LSB on the left, MSB on the right
            num -= 2 ** i
    if (num > 0):
        print(colors.B_RED + "overflow inside binary conversion function!" + colors.RESET)
    return result

def get_X_dictionary(num):
    bools = convert_into_five_bit_array(num)
    result = {}
    for i in range(0, 5, 1):
        result[x_variables[i]] = bools[i]
    return result

def get_XY_dictionary(xnum, ynum):
    xbools = convert_into_five_bit_array(xnum)
    ybools = convert_into_five_bit_array(ynum)
    result = {}
    for i in range(0, 5, 1):
        result[x_variables[i]] = xbools[i]
    for i in range(0, 5, 1):
        result[y_variables[i]] = ybools[i]
    return result

def get_Y_dictionary(num):
    bools = convert_into_five_bit_array(num)
    result = {}
    for i in range(0, 5, 1):
        result[y_variables[i]] = bools[i]
    return result

def make_RR_edge(x_node, y_node):
    x_table = get_X_dictionary(x_node)
    Y_table = get_Y_dictionary(y_node)
    formula = None
    if (x_table[x_variables[0]] == 1):
        formula = x_variables[0]
    else:
        formula = ~x_variables[0]
    for i in range(1, len(x_variables), 1):
        if (x_table[x_variables[i]] == 1):
            formula &= x_variables[i]
        else:
            formula &= ~x_variables[i]
    for i in range(0, len(y_variables), 1):
        if (Y_table[y_variables[i]] == 1):
            formula &= y_variables[i]
        else:
            formula &= ~y_variables[i]
    return formula

def make_RR_BDD():
    node_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 
                 30, 31]
    RR_formula = None
    for i in node_list:
        for j in node_list:
            if edge_rule(i, j):
                if RR_formula == None:
                    RR_formula = make_RR_edge(i, j)
                else:
                    RR_formula |= make_RR_edge(i, j)
    return expr2bdd(RR_formula)

def evaluate_RR_BDD(RR_BDD, num1, num2):
    xy_edge = make_RR_edge(num1, num2)
    xy_edge = expr2bdd(xy_edge)
    xy_bools = xy_edge.satisfy_one() # there is only one set of boolean values that satisfy a boolean edge
    RR_bools = RR_BDD.satisfy_all()
    for i in RR_bools:
        if (i == xy_bools):
            return True
    return False

main()