#!/bin/python3

from pyeda.inter import * # grabs us all of the functions and symbols from the pyeda library
from pyeda.boolalg.bdd import *

x_variables = [bddvar('x{}'.format(i)) for i in range(1, 6)]     # this will create the boolean variables that we are going to want 
y_variables = [bddvar('y{}'.format(i)) for i in range(1, 6)]     # and format it in the form { x1, x2, ... , x6 } and { y1, y2, ... , y6 }
z_variables = [bddvar('z{}'.format(i)) for i in range(1, 6)]     # for .compose() and .smoothing

def compare_dicks(dick1 : dict, dick2 : dict) -> bool:
    # dick1 could be smaller than dick2, and the function could still return true
    for inches in dick1:
        if inches not in dick2:
            return False
        elif (dick1[inches] != dick2[inches]):
            return False
    return True # dick1 is inside dick2

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
    return result

def make_RR_edge(num1 : int, num2 : int) -> BinaryDecisionDiagram:
    x_arr = convert_into_five_bit_array(num1)
    y_arr = convert_into_five_bit_array(num2)
    edge_bdd = 1
    for i in range(0, len(x_variables), 1):
        if (x_arr[i]):
            edge_bdd &= x_variables[i]
        else:
            edge_bdd &= ~x_variables[i]
    for i in range(0, len(y_variables), 1):
        if (y_arr[i]):
            edge_bdd &= y_variables[i]
        else:
            edge_bdd &= ~y_variables[i]


    return edge_bdd

def evaluate_RR_bdd(RR_BDD : BinaryDecisionDiagram, node1 : int, node2 : int) -> bool:
    xy_edge = make_RR_edge(node1, node2)
    xy_bools = xy_edge.satisfy_one() # returns an arbitrary mapping of bddvar : bool(1 or 0) that satisfy the the given BDD
    RR_BDD_bools = RR_BDD.satisfy_all()
    for i in RR_BDD_bools:
        if compare_dicks(i, xy_bools):
            return True
    return False

def make_RR_BDD() -> BinaryDecisionDiagram:
    node_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 
                 30, 31]
    RR_BDD = 0
    for i in node_list:
        for j in node_list:
            if (edge_rule(i, j)):
                RR_BDD |= make_RR_edge(i, j)
    return RR_BDD

def make_RR2_BDD(RR_BDD : BinaryDecisionDiagram) -> BinaryDecisionDiagram:
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
    z_replace_y_BDD = RR_BDD.compose(z_replace_y)
    # print(bdd2expr(z_replace_y_BDD))
    # print("-----------------------------------------------------------")
    z_replace_x_BDD = RR_BDD.compose(z_replace_x)
    # print(bdd2expr(z_replace_x_BDD))
    # print("-----------------------------------------------------------")
    x_z_y_BDD = z_replace_y_BDD & z_replace_x_BDD
    # print(bdd2expr(x_z_y_BDD))
    # print("-----------------------------------------------------------")
    RR2_BDD = x_z_y_BDD.smoothing(z_list)
    # print(bdd2expr(RR2_BDD))
    # print("-----------------------------------------------------------")
    return RR2_BDD















def get_Y_dictionary(num : int) -> dict:
    bools = convert_into_five_bit_array(num)
    result = {}
    for i in range(0, 5, 1):
        result[y_variables[i]] = bools[i]
    return result

def make_EVEN_edge(num : int) -> BinaryDecisionDiagram:
    edge_BDD = 1
    y_dict = convert_into_five_bit_array(num)
    for i in range(0, 5, 1):
        if (y_dict[i]):
            edge_BDD &= y_variables[i]
        else:
            edge_BDD &= ~y_variables[i]
    return edge_BDD



def make_even_BDD() -> BinaryDecisionDiagram:
    node_list = [0, 2, 4, 6, 8,
                 10, 12, 14, 16, 18,
                 20, 22, 24, 26, 28,
                 30]
    EVEN_BDD = 0
    for i in node_list:
        EVEN_BDD |= make_EVEN_edge(i)
    return EVEN_BDD


def make_RR2star_BDD(RR2_BDD : BinaryDecisionDiagram) -> BinaryDecisionDiagram:
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

    bad_apple = RR2_BDD
    while True:
        banana = bad_apple
        print(bdd2expr(banana))
        bad_apple = (banana.compose(z_replace_y) & banana.compose(z_replace_x)).smoothing(z_list) | banana
        if (banana.equivalent(bad_apple)):
            break
    return banana




# print(bdd2expr(make_even_BDD()))

















RR_BDD = make_RR_BDD()

RR2_BDD = make_RR2_BDD(RR_BDD)

RR2star_BDD = make_RR2star_BDD(RR_BDD)
# result = evaluate_RR_bdd(RR2_BDD, 27, 9)


# print(result)
    
