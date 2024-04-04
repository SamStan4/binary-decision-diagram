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

x_variables = [exprvar('x{}'.format(i)) for i in range(1, 7)]     # this will create the boolean variables that we are going to want 
y_variables = [exprvar('y{}'.format(i)) for i in range(1, 7)]     # and format it in the form { x1, x2, ... , x6 } and { y1, y2, ... , y6 }

#*********************************************************************************************************************************************#
#   function name       : convert_int_to_binary_6_bit_array()
#   functional purpose  : this function will convert an integer into a 6 bit boolean array
#   inputs              : int
#   outputs             : boolean array
#   preconditions       : none
#   postconditions      : none
#   programmer          : Sam Stanley

def convert_int_to_binary_6_bit_array(target):
    
    boolean_list = [ False, False, False, False, False, False ] # 6 bits, initialize it to zero

    for i in range(5, -1, -1):
        
        if ((2 ** i) <= target):
            boolean_list[len(boolean_list) - i - 1] = True
            target -= 2 ** i
        else:
            boolean_list[len(boolean_list) - i - 1] = False

    
    if (target > 0):
        print(colors.B_RED + "overflow inside binary conversion function!" + colors.RESET)

    return boolean_list

#*********************************************************************************************************************************************#
#   function name       : make_edge_bool_formula()
#   functional purpose  : this function will create a boolean formula that represnets that there is an edge between two nodes in a graph
#   inputs              : two integer variables
#   outputs             : boolean formula
#   preconditions       : none
#   postconditions      : none
#   programmer          : Sam Stanley

def make_edge_bool_formula(x_node, y_node):
    #x1, x1, x3 = map()

    forumla_function = None

    x_node_list = convert_int_to_binary_6_bit_array(x_node)     # convert both of these into boolean arrays length 6
    y_node_list = convert_int_to_binary_6_bit_array(y_node)

    if (x_node_list[0]):           # initialize to be the first x variable
        forumla_function = x_variables[0]
    else:
        forumla_function = ~x_variables[0]

    for i in range (1, 6, 1):      # add the x variables
        if (x_node_list[i]):
            forumla_function &= x_variables[i]
        else:
            forumla_function &= ~x_variables[i]

    for i in range (0, 6, 1):     # add the y variables
        if (y_node_list[i]):
            forumla_function &= y_variables[i]
        else:
            forumla_function &= ~y_variables[i]

    return expr2bdd(forumla_function)

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

#*********************************************************************************************************************************************#
#   function name       : make_32_node_BDD()
#   functional purpose  : this function will create a 32 (0 - 32) node BDD representation of a graph with edge rule: 
#                         there is an edge from node i to node j iff (i + 3)%32 = j%32 or (i + 8)%32 = j%32.
#   inputs              : list
#   outputs             : a boolean decision diagram
#   preconditions       : none
#   postconditions      : none
#   programmer          : Sam Stanley

def make_BDD(num_set):

    temp_boolean_formula = None
    local_boolean_formula = None

    for i in range(0, len(num_set), 1):
        for j in range(0, len(num_set), 1):
            if (edge_rule(num_set[i], num_set[j])):
                temp_boolean_formula = make_edge_bool_formula(num_set[i], num_set[j])
                if (local_boolean_formula == None):
                    local_boolean_formula = temp_boolean_formula
                else:
                    local_boolean_formula |= temp_boolean_formula

    return expr2bdd(local_boolean_formula)

#*********************************************************************************************************************************************#
#   function name       : make_PRIME_BDD()
#   functional purpose  : returns a bdd for the edge rule using only the prime nodes
#   inputs              : none
#   outputs             : BDD
#   preconditions       : none
#   postconditions      : none
#   programmer          : Sam Stanley

def make_PRIME_BDD():
    node_list = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    return make_BDD(node_list)

#*********************************************************************************************************************************************#
#   function name       : make_EVEN_BDD()
#   functional purpose  : returns a bdd for the edge rule using only the even nodes
#   inputs              : none
#   outputs             : BDD
#   preconditions       : none
#   postconditions      : none
#   programmer          : Sam Stanley

def make_EVEN_BDD():
    node_list = [0, 2, 4, 6, 8,
                 10, 12, 14, 16, 18,
                 20, 22, 24, 26, 28,
                 30]
    return make_BDD(node_list)

#*********************************************************************************************************************************************#
#   function name       : make_RR_BDD()
#   functional purpose  : returns a bdd for the edge rule using all nodes { 0, 1, ... , 31}
#   inputs              : none
#   outputs             : BDD
#   preconditions       : none
#   postconditions      : none
#   programmer          : Sam Stanley

def make_RR_BDD():
    node_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 
                 30, 31]
    return make_BDD(node_list)


#*********************************************************************************************************************************************#
#   function name       : clear_terminal()
#   functional purpose  : clears terminal like system("clear"); does in c/c++
#   inputs              : none
#   outputs             : none
#   preconditions       : none
#   postconditions      : none
#   programmer          : Sam Stanley

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

#*********************************************************************************************************************************************#
#   function name       : main_menu()
#   functional purpose  : a menu for the user to select what they want to do from
#   inputs              : none
#   outputs             : int
#   preconditions       : none
#   postconditions      : none
#   programmer          : Sam Stanley

def print_title():
        clear_terminal()
        print(colors.F_MAGENTA)
        print("  ___     ___.        .___  .___  ___     \n / _ \_/\ \_ |__    __| _/__| _/ / _ \_/\ \n \/ \___/  | __ \  / __ |/ __ |  \/ \___/ \n           | \_\ \/ /_/ / /_/ |           \n           |___  /\____ \____ |           \n               \/      \/    \/           \n")
        print(colors.RESET)


def main_menu():

    x = True
    list_decisions = [ 1, 2, 3, 4, 5, 6, 7 ]

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
        print("enter '7' to exit the program")

        print(colors.RESET)


        try: # try block to that this input doesnt crash the program
            decision = int(input("\nEnter here: "))

            if decision in list_decisions:
                x = False
        except:
            x = True

    return decision

#*********************************************************************************************************************************************#
#   function name       : print_BDD()
#   functional purpose  : this function will accept a BDD and print it to the terminal
#   inputs              : bdd
#   outputs             : none
#   preconditions       : input is a BDD
#   postconditions      : none
#   programmer          : Sam Stanley

def print_BDD(target_bdd):
    print_title()
    print(colors.F_CYAN)
    print(bdd2expr(target_bdd))
    print(colors.RESET)

def RR_tests(RR_BDD):
    true_RR_list = list(RR_BDD.satisfy_all())

    RR_27_3_test_case = {x_variables[0]: 0, x_variables[1]: 0, x_variables[2]: 0, x_variables[3]: 0, x_variables[4]: 0, x_variables[5]: 0,
                         y_variables[0]: 0, y_variables[1]: 0, y_variables[2]: 0, y_variables[3]: 0, y_variables[4]: 1, y_variables[5]: 1}

    print("Satisfying Combinations:")
    print(true_RR_list)
    print("Test Case:")
    print(RR_27_3_test_case)

    if RR_27_3_test_case in true_RR_list:
        print("yes")
    else:
        print("no")                
#*********************************************************************************************************************************************#
#   function name       : main()
#   functional purpose  : main routine, like in c/c++
#   inputs              : none
#   outputs             : none
#   preconditions       : none
#   postconditions      : none
#   programmer          : Sam Stanley

def main():
    RR_BDD = make_RR_BDD()
    EVEN_BDD = make_EVEN_BDD()
    PRIME_BDD = make_PRIME_BDD()

    decision = 0

    while (decision != 7):
        decision = main_menu()

        if (decision == 1):
            print_BDD(RR_BDD)
        elif (decision == 2):
            print_BDD(EVEN_BDD)
        elif (decision == 3):
            print_BDD(PRIME_BDD)
        elif (decision == 4):
            RR_tests(RR_BDD)
        elif (decision == 5):
            print("running test cases on RR2 BDD")
        elif (decision == 6):
            print("running test cases on RRstar BDD")
        elif (decision == 7):
            break
        
        pause()

        #RR_BDD.compose(RR_BDD)

    clear_terminal()

    

    
#*********************************************************************************************************************************************#

main()

