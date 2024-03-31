#!/bin/python3

from pyeda.inter import * # grabs us all of the functions and symbols from the pyeda library
import os # for clearing the terminal

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




#*********************************************************************************************************************************************#

main()

