#!/bin/python3

from pyeda.inter import * # grabs us all of the functions and symbols from the pyeda library
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
#   function name       : make_32_node_BDD()
#   functional purpose  : this function will create a 32 (0 - 32) node BDD representation of a graph with edge rule: 
#                         there is an edge from node i to node j iff (i + 3)%32 = j%32 or (i + 8)%32 = j%32.
#   inputs              : int
#   outputs             : a boolean decision diagram
#   preconditions       : none
#   postconditions      : none
#   programmer          : Sam Stanley


def make_edge(node_one, node_two):
    return "hi"

def make_32_node_BDD():

    #binary_32 = convert_int_to_binary_6_bit_array(64)

    for i in range(0, 32, 1):
        for j in range(0, 32, 1):
            if ((((i + 3) % 32) == (j % 32)) or (((i + 8) % 32) == (j % 32))):
                print("there is an edge from node " + str(i) + " --> node " + str(j))

    return "hi"

#*********************************************************************************************************************************************#
#   function name       : clear_terminal()
#   functional purpose  : clears terminal like system("clear"); does in c/c++
#   inputs              : none
#   outputs             : none
#   preconditions       : none
#   postconditions      : none
#   programmer          : Sam Stanley

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

#*********************************************************************************************************************************************#
#   function name       : main_menu()
#   functional purpose  : a menu for the user to select what they want to do from
#   inputs              : none
#   outputs             : int
#   preconditions       : none
#   postconditions      : none
#   programmer          : Sam Stanley

def main_menu():

    x = True
    list_decisions = { 1 }

    while (x):

        clear_terminal()

        print("---Main Menu---\n")

        print("enter '1' to build the BDD and run the program\n")

        try: # try block to that this input doesnt crash the program
            decision = int(input("Enter here: "))

            if decision in list_decisions:
                x = False
        except:
            x = True

    return decision

#*********************************************************************************************************************************************#
#   function name       : main()
#   functional purpose  : main routine, like in c/c++
#   inputs              : none
#   outputs             : none
#   preconditions       : none
#   postconditions      : none
#   programmer          : Sam Stanley

def main():
    decision = main_menu()

    if (decision == 1):
        test_BDD = make_32_node_BDD()

    print(test_BDD)




#*********************************************************************************************************************************************#

main()

