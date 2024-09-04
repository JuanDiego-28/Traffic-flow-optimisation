#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 12:23:26 2024

@author: jdiego
"""
import networkx as nx
import numpy as np
import osmnx as ox
import functions


def path_finder(initial_node, final_node , G ):
    
    """
    This functions simulates an agent thar looks for the best path to follow from one node to another
    """

    # get dictionary with geocordinates of each of the nodes
    coordiantes = functions.get_geo_coordinates(G)

    node_i = initial_node 

    # to store the routes:
    route= {}

    path = []

    # bug list
    bug_list = []

    # no exit list 
    no_exit_list = []

    # loop to finde the path: 
    while node_i != final_node:

        # store all nodes the agent pass through: 
        path.append(node_i)
    
        # measure the angle and distnac between the node_i and the destination node
        angle_i = functions.get_angle( coordiantes[ node_i ], coordiantes[ final_node] )
        dist_i = functions.get_distance( coordiantes[ node_i ], coordiantes[ final_node] ) 

        # get the neighbours of the node. The neighbours are directed nodes
        neighbors = list(G.neighbors(node_i))

        # get probality of pick a given neighbour
        factors = {}

        for node in neighbors :
            # measure angle and dist of neighbors towards final node 
            angle_neighbor = functions.get_angle( coordiantes[ node ], coordiantes[ final_node] )
            dist_neighbor = functions.get_distance( coordiantes[ node ], coordiantes[ final_node] )
        
            # calculate the probability of picking a node 
            factors[node] = functions.get_factor(dist_neighbor , angle_neighbor , dist_i , angle_i , 0.6, 0.4 )

        # get probabilities
        proba_dic = functions.get_probability(factors)


        #print("estoy en el nodo  ", node_i, " mis opciones son : ", proba_dic)

        # list of probable nodes_id: 
        list_proba = list(proba_dic.keys())

        # contador de veces que paso por un nodo 
        repeticions = path.count(node_i)

        for node in list_proba:
            counter = path.count(node)
            if node in path:
                proba_dic[node] = proba_dic[node]*0.4
                if counter > 2:
                    proba_dic[node] = proba_dic[node]*(0.4**counter)


        # if i have pass more than two times by a node 
        if repeticions > 2:
        
            # sotre node_i in wich bug is produced 
            bug_node = node_i
            bug_list.append(node_i)
            #print("bugg en el nodo : " , bug_node )

            # count how many times a bug node has been pass through.
            counter = bug_list.count(node_i)

            if counter >= 3:
                vecinos_i = list(G.neighbors(node_i))
                for vecino in vecinos_i:
                    if vecino in  bug_list:
                        route[bug_node][vecino] = 0.0
                        proba_dic[vecino] = route[bug_node][vecino]
                        #print("me quedo en el nodo: " , node_i, "acualice probabiliades: ", proba_dic)
                        #print(route)
                #break
        
        # check for node with no exit i.e no neighbors 
        if len(neighbors) == 0:
            # store in route 
            #print("estoy en el nodo " , node_i , "no hay salida")
            no_exit_node = node_i
            route[no_exit_node] = {}
            no_exit_list.append(no_exit_node)

            # acutalizo la posicion al nodo anterior
            node_i= path[-2]

            # check neihbours
            vecino_j = list(G.neighbors(node_i))

            # acualizo la proabilidad de volver al nodo sin salida a 0
            for vecino in vecino_j:
                if vecino in no_exit_list:
                    route[node_i][no_exit_node] = 0.0
                    proba_dic = route[node_i]
                    #print("volvi al nodo: ", node_i, "se acutliazo las lista de probilidades a : " ,proba_dic)
            #break
                
        # check if the node has no posible routes to the destination
        no_options = all( options == 0 for options in proba_dic.values())       
        if no_options:
            position = path.index(node_i)
            no_options_node = node_i
            no_exit_list.append(node_i)
            #print("ninguno de los caminos posibles es correcto")
            #print("regreso al nodo", path[position - 1 ])
            node_i =  path[position - 1 ]
            route[node_i][no_options_node] = 0.0
            proba_dic = route[node_i]
        
            # checkear que no vuelva a una ruta sin salida: 
            vecino_z = vecino_j = list(G.neighbors(node_i))
            for vecino in vecino_z:
                if vecino in no_exit_list:
                    position_i = path.index(node_i)
                    node_j = path[position_i -1]
                    #print("debo regresar al node " , node_j, " no debo ir a ", node_i)
                    route[node_j][node_i] = 0.0
                    proba_dic = route[node_j]
                    print(proba_dic)
            #break

        # stop simulation if bug 
        if repeticions > 15:
            print(" ERROR: el nodo " , node_i ," se repite mas de 15 veces")
            break

        # add to route:
        route[node_i] = proba_dic
    
        # ge the node id with max probability
        node_id = max(proba_dic , key= proba_dic.get)

        # get the max probability    
        Proba = proba_dic[node_id]
        
        #print("estoy en el nodo: " , node_id)

        # update position
        node_i = node_id

    route[final_node] = {final_node:1.0}

    return route, path