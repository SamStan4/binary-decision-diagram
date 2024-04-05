#!/bin/python3

from pyeda.inter import * # grabs us all of the functions and symbols from the pyeda library
from pyeda.boolalg.bdd import *
import os # for clearing the terminal and pausing the terminal

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

x_variables = [bddvar('x{}'.format(i)) for i in range(1, 6)]     # this will create the boolean variables that we are going to want 
y_variables = [bddvar('y{}'.format(i)) for i in range(1, 6)]     # and format it in the form { x1, x2, ... , x6 } and { y1, y2, ... , y6 }
z_variables = [bddvar('z{}'.format(i)) for i in range(1, 6)]     # for .compose() and .smoothing

def clear_terminal() -> None:

    if os.name == "nt": # windows
        os.system('cls')
    else: # mac / linux
        os.system('clear')

def pause() -> None:
    if os.name == 'nt': # windows
        os.system('pause')
    else: # mac/linux
        input("Press " + colors.B_MAGENTA + "Enter" + colors.RESET + " to continue...")

def print_title() -> None:
        clear_terminal()
        print(colors.F_MAGENTA)
        print("  ___     ___.        .___  .___  ___     \n / _ \_/\ \_ |__    __| _/__| _/ / _ \_/\ \n \/ \___/  | __ \  / __ |/ __ |  \/ \___/ \n           | \_\ \/ /_/ / /_/ |           \n           |___  /\____ \____ |           \n               \/      \/    \/           \n")
        print(colors.RESET)

def main_menu() -> int:

    x = True
    list_decisions = [ 1, 2, 3, 4, 5, 6, 7, 8, 9]

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
        print("enter '7' to run test cases on quantifier BDD")
        print("enter '8' to run all test cases                   " + colors.RESET + colors.B_MAGENTA + "<-- TA choose this option"  + colors.RESET + colors.F_GREEN)
        print("enter '9' to exit the program")

        print(colors.RESET)


        try: # try block to that this input doesnt crash the program
            decision = int(input("\nEnter here: "))

            if decision in list_decisions:
                x = False
        except:
            x = True

    return decision

def main() -> None:
    decision = 0

    RR_BDD = make_RR_BDD()
    EVEN_BDD = make_EVEN_BDD()
    PRIME_BDD = make_PRIME_BDD()
    RR2_BDD = make_RR2_BDD(RR_BDD)

    while (decision != 9):
        decision = main_menu()

        if (decision == 1):
            print_RR_BDD(RR_BDD)
        elif (decision == 2):
            print_EVEN_BDD(EVEN_BDD)
        elif (decision == 3):
            print_prime_BDD(PRIME_BDD)
        elif (decision == 4):
            run_RR_EVEN_PRIME_BDD_tests(RR_BDD, EVEN_BDD, PRIME_BDD)
        elif (decision == 5):
            RR2_BDD_test_mask(RR2_BDD)
        elif (decision == 6):
            print("running test cases on RRstar BDD")
        elif (decision == 7):
            print("running test cases on quantifier BDD")
        elif (decision == 8):
            run_all_test_cases(RR_BDD, EVEN_BDD, PRIME_BDD, RR2_BDD)
        elif (decision == 9):
            break
        
        pause()

def evaluate_dicts(D1 : dict, D2 : dict) -> bool:
    for i in D1:
        if i not in D2:
            return False
        elif D1[i] != D2[i]:
            return False
    return True

def print_RR_BDD(RR_BDD : BinaryDecisionDiagram) -> None:
    clear_terminal()
    print(colors.F_MAGENTA)
    print("  ___                     ___.        .___  .___  ___     \n / _ \_/\ ______________  \_ |__    __| _/__| _/ / _ \_/\ \n \/ \___/ \_  __ \_  __ \  | __ \  / __ |/ __ |  \/ \___/ \n           |  | \/|  | \/  | \_\ \/ /_/ / /_/ |           \n           |__|   |__|     |___  /\____ \____ |           \n                               \/      \/    \/           \n")
    print(colors.F_GREEN + str(bdd2expr(RR_BDD)) + "\n" + colors.RESET)

def print_EVEN_BDD(EVEN_BDD : BinaryDecisionDiagram) -> None:
    clear_terminal()
    print(colors.F_MAGENTA)
    print("  ___                                 ___.        .___  .___  ___     \n / _ \_/\   _______  __ ____   ____   \_ |__    __| _/__| _/ / _ \_/\ \n \/ \___/ _/ __ \  \/ // __ \ /    \   | __ \  / __ |/ __ |  \/ \___/ \n          \  ___/\   /\  ___/|   |  \  | \_\ \/ /_/ / /_/ |           \n           \___  >\_/  \___  >___|  /  |___  /\____ \____ |           \n               \/          \/     \/       \/      \/    \/           \n")
    print(colors.F_GREEN + str(bdd2expr(EVEN_BDD)) + "\n" + colors.RESET)

def print_prime_BDD(PRIME_BDD : BinaryDecisionDiagram) -> None:
    clear_terminal()
    print(colors.F_MAGENTA)
    print("  ___                  .__                 ___.        .___  .___  ___     \n / _ \_/\ _____________|__| _____   ____   \_ |__    __| _/__| _/ / _ \_/\ \n \/ \___/ \____ \_  __ \  |/     \_/ __ \   | __ \  / __ |/ __ |  \/ \___/ \n          |  |_> >  | \/  |  Y Y  \  ___/   | \_\ \/ /_/ / /_/ |           \n          |   __/|__|  |__|__|_|  /\___  >  |___  /\____ \____ |           \n          |__|                  \/     \/       \/      \/    \/           \n")
    print(colors.F_GREEN + str(bdd2expr(PRIME_BDD)) + "\n" + colors.RESET)

def edge_rule(x_node : int, y_node : int) -> bool:
    if ((((x_node + 3) % 32) == (y_node % 32)) or (((x_node + 8) % 32) == (y_node % 32))):
        return True
    else:
        return False

def convert_into_five_bit_array(num : int) -> list:
    result = [0, 0, 0, 0, 0]
    for i in range(4, -1, -1):
        if num >= 2 ** i:
            result[i] = 1 # LSB on the left, MSB on the right
            num -= 2 ** i
    if (num > 0):
        print(colors.B_RED + "overflow inside binary conversion function!" + colors.RESET)
    return result

def get_X_dictionary(num : int) -> dict:
    bools = convert_into_five_bit_array(num)
    result = {}
    for i in range(0, 5, 1):
        result[x_variables[i]] = bools[i]
    return result

def get_XY_dictionary(xnum : int, ynum : int) -> dict:
    xbools = convert_into_five_bit_array(xnum)
    ybools = convert_into_five_bit_array(ynum)
    result = {}
    for i in range(0, 5, 1):
        result[x_variables[i]] = xbools[i]
    for i in range(0, 5, 1):
        result[y_variables[i]] = ybools[i]
    return result

def get_Y_dictionary(num : int) -> dict:
    bools = convert_into_five_bit_array(num)
    result = {}
    for i in range(0, 5, 1):
        result[y_variables[i]] = bools[i]
    return result

def make_RR_edge(x_node : int, y_node : int) -> BinaryDecisionDiagram:
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

def make_RR_BDD() -> BinaryDecisionDiagram:
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
    return RR_formula

def evaluate_RR_BDD(RR_BDD : BinaryDecisionDiagram, num1 : int, num2 : int) -> bool:
    xy_edge = make_RR_edge(num1, num2)
    xy_bools = xy_edge.satisfy_one() # there is only one set of boolean values that satisfy a boolean edge
    RR_bools = RR_BDD.satisfy_all()
    for i in RR_bools:
        if (evaluate_dicts(i, xy_bools)):
            return True
    return False

def make_EVEN_edge(num : int) -> BinaryDecisionDiagram:
    y_table = get_Y_dictionary(num)
    fomula = None
    if (y_table[y_variables[0]] == 1):
        formula = y_variables[0]
    else:
        formula = ~y_variables[0]
    for i in range(1, len(y_variables), 1):
        if (y_table[y_variables[i]] == 1):
            formula &= y_variables[i]
        else:
            formula &= ~y_variables[i]
    return formula

def make_EVEN_BDD() -> BinaryDecisionDiagram:
    node_list = [0, 2, 4, 6, 8,
                 10, 12, 14, 16, 18,
                 20, 22, 24, 26, 28,
                 30]
    EVEN_formula = None
    for i in node_list:
        if (EVEN_formula == None):
            EVEN_formula = make_EVEN_edge(i)
        else:
            EVEN_formula |= make_EVEN_edge(i)
    return EVEN_formula

def evaluate_EVEN_BDD(EVEN_BDD : BinaryDecisionDiagram, num : int) -> bool:
    y_edge = make_EVEN_edge(num)
    y_bools = y_edge.satisfy_one() # there should only be one boolean set that satisfies this
    EVEN_bools = EVEN_BDD.satisfy_all()
    for i in EVEN_bools:
        if (evaluate_dicts(i, y_bools)):
            return True
    return False

def make_PRIME_edge(num : int) -> BinaryDecisionDiagram:
    x_table = get_X_dictionary(num)
    formua = None
    if (x_table[x_variables[0]] == 1):
        formula = x_variables[0]
    else:
        formula = ~x_variables[0]
    for i in range(1, len(x_variables), 1):
        if (x_table[x_variables[i]] == 1):
            formula &= x_variables[i]
        else:
            formula &= ~x_variables[i]
    return formula

def make_PRIME_BDD() -> BinaryDecisionDiagram:
    node_list = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    PRIME_formula = None
    for i in node_list:
        if (PRIME_formula == None):
            PRIME_formula = make_PRIME_edge(i)
        else:
            PRIME_formula |= make_PRIME_edge(i)
    return PRIME_formula

def evaluate_PRIME_BDD(PRIME_BDD : BinaryDecisionDiagram, num : int) -> bool:
    x_edge = make_PRIME_edge(num)
    x_bools = x_edge.satisfy_one() # there should only be one boolean set that satisfies this
    PRIME_bools = PRIME_BDD.satisfy_all()
    for i in PRIME_bools:
        if (evaluate_dicts(i, x_bools)):
            return True
    return False

def run_RR_BDD_test_cases(RR_BDD : BinaryDecisionDiagram) -> None:
    test_27_03 = evaluate_RR_BDD(RR_BDD, 27, 3)
    test_16_20 = evaluate_RR_BDD(RR_BDD, 16, 20)
    if (test_27_03):
        print("RR(27, 03) -------> " + colors.B_GREEN + "is true " + colors.RESET + "   (expected)")
    else:
        print("RR(27, 03) -------> " + colors.B_RED + "is false" + colors.RESET + "   (not expected)")
    if (test_16_20):
        print("RR(16, 20) -------> " + colors.B_GREEN + "is true " + colors.RESET + "   (not expected)")
    else:
        print("RR(16, 20) -------> " + colors.B_RED + "is false" + colors.RESET + "   (expected)")

def run_EVEN_BDD_test_cases(EVEN_BDD : BinaryDecisionDiagram) -> None:
    test_14 = evaluate_EVEN_BDD(EVEN_BDD, 14)
    test_13 = evaluate_EVEN_BDD(EVEN_BDD, 13)
    if (test_14):
        print("EVEN(14) ---------> " + colors.B_GREEN + "is true " + colors.RESET + "   (expected)")
    else:
        print("EVEN(14) ---------> " + colors.B_RED + "is false" + colors.RESET + "   (not expected)")
    if (test_13):
        print("EVEN(13) ---------> " + colors.B_GREEN + "is true " + colors.RESET + "   (not expected)")
    else:
        print("EVEN(13) ---------> " + colors.B_RED + "is false" + colors.RESET + "   (expected)")

def run_PRIME_BDD_test_cases(PRIME_BDD : BinaryDecisionDiagram) -> None:
    test_7 = evaluate_PRIME_BDD(PRIME_BDD, 7)
    test_2 = evaluate_PRIME_BDD(PRIME_BDD, 2)
    if (test_7):
        print("PRIME(7) ---------> " + colors.B_GREEN + "is true " + colors.RESET + "   (expected)")
    else:
        print("PRIME(7) ---------> " + colors.B_RED + "is false" + colors.RESET + "   (not expected)")
    if (test_2):
        print("PRIME(2) ---------> " + colors.B_GREEN + "is true " + colors.RESET + "   (not expected)")
    else:
        print("PRIME(2) ---------> " + colors.B_RED + "is false" + colors.RESET + "   (expected)")

def run_RR2_BDD_test_cases(RR2_BDD : BinaryDecisionDiagram) -> None:
    test_27_6 = evaluate_RR2_BDD(RR2_BDD, 27, 6)
    test_27_9 = evaluate_RR2_BDD(RR2_BDD, 27, 9)
    if (test_27_6):
        print("RR2(27, 06) ------> " + colors.B_GREEN + "is true " + colors.RESET + "   (expected)")
    else:
        print("RR2(27, 06) ------> " + colors.B_RED + "is false" + colors.RESET + "   (not expected)")
    if (test_27_9):
        print("RR2(27, 09) ------> " + colors.B_GREEN + "is true " + colors.RESET + "   (not expected)")
    else:
        print("RR2(27, 09) ------> " + colors.B_RED + "is false" + colors.RESET + "   (expected)")
        
def run_RR_EVEN_PRIME_BDD_tests(RR_BDD : BinaryDecisionDiagram, EVEN_BDD : BinaryDecisionDiagram, PRIME_BDD : BinaryDecisionDiagram) -> None:
    clear_terminal()
    print(colors.F_MAGENTA + "  ___       __                   __                                          ___     \n/ _ \_/\ _/  |_  ____   _______/  |_    ____ _____    ______ ____   ______ / _ \_/\ \n\/ \___/ \   __\/ __ \ /  ___/\   __\ _/ ___\\__  \  /  ___// __ \ /  ___/ \/ \___/ \n          |  | \  ___/ \___ \  |  |   \  \___ / __ \_\___ \\  ___/ \___ \           \n          |__|  \___  >____  > |__|    \___  >____  /____  >\___  >____  >          \n                    \/     \/              \/     \/     \/     \/     \/           \n" + colors.RESET)
    run_RR_BDD_test_cases(RR_BDD)
    run_EVEN_BDD_test_cases(EVEN_BDD)
    run_PRIME_BDD_test_cases(PRIME_BDD)
    print()

def RR2_BDD_test_mask(RR2_BDD : BinaryDecisionDiagram) -> None:
    clear_terminal()
    print(colors.F_MAGENTA + "  ___       __                   __                                          ___     \n/ _ \_/\ _/  |_  ____   _______/  |_    ____ _____    ______ ____   ______ / _ \_/\ \n\/ \___/ \   __\/ __ \ /  ___/\   __\ _/ ___\\__  \  /  ___// __ \ /  ___/ \/ \___/ \n          |  | \  ___/ \___ \  |  |   \  \___ / __ \_\___ \\  ___/ \___ \           \n          |__|  \___  >____  > |__|    \___  >____  /____  >\___  >____  >          \n                    \/     \/              \/     \/     \/     \/     \/           \n" + colors.RESET)
    run_RR2_BDD_test_cases(RR2_BDD)
    print()

def run_all_test_cases(RR_BDD : BinaryDecisionDiagram, EVEN_BDD : BinaryDecisionDiagram, PRIME_BDD : BinaryDecisionDiagram, RR2_BDD : BinaryDecisionDiagram) -> None:
    clear_terminal()
    print(colors.F_MAGENTA + "  ___       __                   __                                          ___     \n/ _ \_/\ _/  |_  ____   _______/  |_    ____ _____    ______ ____   ______ / _ \_/\ \n\/ \___/ \   __\/ __ \ /  ___/\   __\ _/ ___\\__  \  /  ___// __ \ /  ___/ \/ \___/ \n          |  | \  ___/ \___ \  |  |   \  \___ / __ \_\___ \\  ___/ \___ \           \n          |__|  \___  >____  > |__|    \___  >____  /____  >\___  >____  >          \n                    \/     \/              \/     \/     \/     \/     \/           \n" + colors.RESET)
    run_RR_BDD_test_cases(RR_BDD)
    run_EVEN_BDD_test_cases(EVEN_BDD)
    run_PRIME_BDD_test_cases(PRIME_BDD)
    run_RR2_BDD_test_cases(RR2_BDD)
    print()

def make_RR2_BDD(RR_BDD : BinaryDecisionDiagram) -> BinaryDecisionDiagram:
    # we know that RR2 => RR compose RR, so lets code it
    z_list = [ z_variables[0], z_variables[1], z_variables[2], z_variables[3], z_variables[4] ]
    z_replace_y  = {
        y_variables[0] : z_variables[0],
        y_variables[1] : z_variables[1],
        y_variables[2] : z_variables[2],
        y_variables[3] : z_variables[3],
        y_variables[4] : z_variables[4] }
    z_replace_x = {
        x_variables[0] : z_variables[0],
        x_variables[1] : z_variables[1],
        x_variables[2] : z_variables[2],
        x_variables[3] : z_variables[3],
        x_variables[4] : z_variables[4] }
    
    RR_replace_Y_Z = RR_BDD.compose(z_replace_y) # there is a lot going on here under the hood
    RR_replace_X_Z = RR_BDD.compose(z_replace_x)
    combo = RR_replace_X_Z & RR_replace_Y_Z
    combo = combo.smoothing(z_list)
    return combo

def make_RR2star_BDD(RR_BDD : BinaryDecisionDiagram) -> BinaryDecisionDiagram:
    return None

def evaluate_RR2_BDD(RR2_BDD : BinaryDecisionDiagram, num1 : int, num2 : int) -> bool:
    xy_edge = make_RR_edge(num1, num2)
    xy_bools = xy_edge.satisfy_one() # there is only one set of boolean values that satisfy a boolean edge
    RR2_bools = RR2_BDD.satisfy_all()
    for i in RR2_bools:
        if (evaluate_dicts(i, xy_bools)):
            return True
    return False

main()

# RR_test = make_RR_BDD()

# RR2_test = make_RR2_BDD(RR_test)

# # print(bdd2expr(RR2_test))

# run_RR2_BDD_test_cases(RR2_test)

# # print(str('\u2200') + "u, (PRIME(u) " + str('\u2192') + " " + str('\u2203') + "v, (EVEN(v) " + str('\u2227') + " RR2star(u, v))")