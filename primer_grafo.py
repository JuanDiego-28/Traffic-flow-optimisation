#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 16:29:39 2023

@author: jdiego

"""

import networkx as nw
import matplotlib.pyplot as plt

# Define the graph 

grafos = nw.DiGraph()

# Define the 30 nodes 

nodos = []
for i in range (0,31): 
    nodos.append(str(i))

# Add nodes: 
grafos.add_nodes_from(nodos)


#print(grafos.order())

# Add edges

edges = [('0','1'),('1','2'),('2','3'),('3','4'),('4','5'),('4','6'),
         ('6','7'),('7','8'),('5','9'),('9','10'),('10','13'),('8','11'),
         ('11','12'),('12','16'),('16','17'),('17','18'),('16','19'),('19','15'),
         ('15','20'),('20','21'),('21','22'),('18','22'),('13','14'),('14','15'),
         ('15','23'),('23','24'),('24','25'),('25','26'),('26','27'),('26','27'),
         ('27','28'),('29','28'),('23','30')]
    
grafos.add_edges_from(edges)

# To print the size of graph
#print(grafos.size())

#nw.draw(grafos,with_labels=True)
    
nw.draw(grafos, node_size=15, 
        node_color="skyblue", pos=nw.spectral_layout(grafos))
plt.title("spectral")
plt.show()