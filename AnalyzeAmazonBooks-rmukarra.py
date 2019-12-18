# -*- coding: utf-8 -*-
"""
Copyright 2019, Arizona Board of Regents, Arizona State University, Luque E
"""
#Ryyan Mukarram  
print ()

import networkx
from operator import itemgetter
import matplotlib.pyplot

# read the data from the amazon-books.txt;
# populate amazonProducts nested dicitonary;
# key = ASIN; value = MetaData associated with ASIN
fhr = open('./amazon-books-version-3.txt', 'r', encoding='utf-8', errors='ignore')
amazonBooks = {}
fhr.readline()
for line in fhr:
    cell = line.split('\t')
    MetaData = {}
    MetaData['Id'] = cell[0].strip() 
    ASIN = cell[1].strip()
    MetaData['Title'] = cell[2].strip()
    MetaData['Categories'] = cell[5].strip()
    MetaData['Group'] = cell[4].strip()
    MetaData['Copurchased'] = cell[5].strip()
    MetaData['SalesRank'] = int(cell[6].strip())
    MetaData['TotalReviews'] = int(cell[7].strip())
    MetaData['AvgRating'] = float(cell[8].strip())
    MetaData['DegreeCentrality'] = int(cell[9].strip())
    MetaData['ClusteringCoeff'] = float(cell[10].strip())
    amazonBooks[ASIN] = MetaData
fhr.close()

# read the data from amazon-books-copurchase.adjlist;
# assign it to copurchaseGraph weighted Graph;
# node = ASIN, edge= copurchase, edge weight = category similarity
fhr=open("amazon-books-copurchase-version-3.edgelist", 'rb')
copurchaseGraph=networkx.read_weighted_edgelist(fhr)
fhr.close()

# now let's assume a person is considering buying the following book;
# what else can we recommend to them based on copurchase behavior 
# we've seen from other users?
print ("Looking for Recommendations for Customer Purchasing this Book:")
print ("--------------------------------------------------------------")
asin = '0812580036' 

# let's first get some metadata associated with this book
print ("ASIN = ", asin)
print ("Title = ", amazonBooks[asin]['Title'])
print ("SalesRank = ", amazonBooks[asin]['SalesRank'])
print ("TotalReviews = ", amazonBooks[asin]['TotalReviews'])
print ("AvgRating = ", amazonBooks[asin]['AvgRating'])
print ("DegreeCentrality = ", amazonBooks[asin]['DegreeCentrality'])
print ("ClusteringCoeff = ", amazonBooks[asin]['ClusteringCoeff'])
    
# now let's look at the ego network associated with this asin
# which is esentially comprised of all the books that have been
# copurchased with this book in the past
egoA = networkx.ego_graph(copurchaseGraph, asin, radius=1)
print ("Ego Network:", "Nodes=", egoA.number_of_nodes(), "Edges=", egoA.number_of_edges())
print ()

print ("Top 5 Recommendations based on Copurchase Data and Average Ratings")
print ("------------------------------------------------------------------")

# how can we pick the Top  recomemndations for this person?
# let's first use the island method to remove edges with
# edge weight below a threshold
threshold = 0.5
egotrimA = networkx.Graph()
for n1, n2, e in egoA.edges(data=True):
    if e['weight'] >= threshold:
        egotrimA.add_edge(n1,n2, weight=e['weight'])
print ("Trimmed Ego Network:", 
       "Threshold=", threshold,
       "Nodes=", egotrimA.number_of_nodes(), 
        "Edges=", egotrimA.number_of_edges())
egoA = egotrimA
print ()

# now let's consider the average rating of all the nodes
# connected to the ego node by a single hop, and sort them
# by descending order of avverage rating

#The Degree Centrality will be switched out with Avg Rating 
myegoNeighbors = [(asin, n, amazonBooks[n]['DegreeCentrality']) for n in egoA.neighbors(asin)]
myegoNeighbors = sorted(myegoNeighbors, key=itemgetter(2), reverse=True)

# print Top 3 recommendations based on average rating
for asin, n, rating in myegoNeighbors[:5]:
    print ("ASIN             = ", n) 
    print ("Title            = ", amazonBooks[n]['Title'])
    print ("SalesRank        = ", amazonBooks[n]['SalesRank'])
    print ("TotalReviews     = ", amazonBooks[n]['TotalReviews'])
    print ("AvgRating        = ", amazonBooks[n]['AvgRating'])
    print ("DegreeCentrality = ", amazonBooks[n]['DegreeCentrality'])
    print ("ClusteringCoeff  = ", amazonBooks[n]['ClusteringCoeff'])
    print ()