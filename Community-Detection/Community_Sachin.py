import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import time
import warnings


## Data Loaders

def import_facebook_data(path):
    f = open(path,'r')
    edgeList = []
    line  = f.readline()
    while line :
        a, b = line.split()
        edgeList.append((int(a),int(b)))
        edgeList.append((int(b),int(a)))
        line  = f.readline()   
    return edgeList

def import_bitcoin_data(path):
    btc = open(path,'r')
    edgeList = []
    line = btc.readline()
    nodes = 5881
    while line :
        a, b, c, _ = line.split(',')
        for i in range(int(c)+11):
            edgeList.append((int(a)-1,int(b)-1))
        #edgeList.append((int(b),int(a)))
        line  = btc.readline()
    return edgeList


## All the helper Functions

def getAdjMat(edgeList):
    st = set([])
    for i, j in edgeList:
        st.add(i)
        st.add(j)
    nodNum = max(st)+1
    #print(nodNum)
    adjMat  = np.zeros((nodNum, nodNum))
    for i,j in edgeList:
        adjMat[i,j] += 0.5
        adjMat[j,i] += 0.5
    return adjMat

def getSubAdjMatfromIdx(adjMat, ids):
    return adjMat[np.ix_(ids, ids)]

def getLaplacianMatrix(adjMat):
    lapMat = -adjMat
    for i in range(adjMat.shape[0]):
        lapMat[i,i] = np.abs(np.sum(lapMat[i]))
    return lapMat.astype(int)

def graphPartition(communities, nodNum):
    partition = np.zeros((nodNum,2))
    for li in communities:
        for node in li:
            partition[node,0] = node
            partition[node,1] = min(li)     
            
    return partition.astype(int)

def getFreidel(lapLacMat):
    eigVals, eigVecs = np.linalg.eig(lapLacMat)
    sortedIndex = np.argsort(eigVals)
    fdlVec = eigVecs[:,sortedIndex[1]]
    ids = np.argsort(fdlVec)
    return fdlVec, ids
    
def getNwAdjMatfromIds(adjMat, ids):
    nwAdjMat = np.zeros(adjMat.shape)
    for i, k in enumerate(ids):
        for j, l in enumerate(ids):
            nwAdjMat[i,j] = adjMat[k,l]
    return nwAdjMat

## FriedelVector is Sorted
## Use max gap and averag Gap, i.e. if 3*avg < max then split
def isSplittable(freidelVec): ## We pass sublist fo fvector, reppresenting community to know further splittable,
    
    n = freidelVec.shape[0] 
    if n < 100:
        return False
    
    maxG = sumG = 0
    
    for i in range(freidelVec.shape[0]-1):
        gap = freidelVec[i+1] - freidelVec[i]
        sumG += gap
        if gap >maxG:
            maxG = gap
            
    if maxG > 100*(sumG/(n-1)):
        return True
    
    return False

def d_Merg(i, mapp, part, deg, adj):
  Com = mapp[i]
  Com_nodes = part[Com]
  si_tot = sum(deg[node] for node in Com_nodes)
  k_i_out = 2*np.sum(adj[i,Com_nodes])
  k_i = deg[i]
  Q_dmrg = 2*k_i*si_tot - 2*k_i**2 - k_i_out
  return Q_dmrg

def merge(i,C, part, deg, adj):
  Com_nodes = part[C]
  si_tot = sum(deg[node] for node in Com_nodes)
  k_i_in = 2*np.sum(adj[i,Com_nodes])
  k_i = deg[i]
  Q_mrg = k_i_in - 2*si_tot*k_i
  return Q_mrg

def showAdjMatrix(matrix):     
    ## Plot Adjecancy Matrix
    plt.figure(figsize=(7,7))
    plt.imshow( matrix , cmap = 'inferno' )
    plt.show()

# def plotGrapVisualize(partition, idOrd, adjMat):
#     ### Need to change ######################################3
#     G = nx.Graph(adjMat)
#     pos = nx.spring_layout(G, iterations=20)
#     values = []
#     diffCom = len(list(set(partition[:,1])))
#     #print(diffCom)
#     val = np.linspace(0.1, 1, diffCom)
#     for i in range(len(idOrd)):
#         # print(row.shape,int(row[1]))
#         # print(val[0])
#         commun = partition[i,1]
#         values.append(val[commun])   
    
#     colormap = ListedColormap(plt.cm.tab20.colors[:diffCom])
#     nx.draw(G, pos, node_color=np.array(values),cmap=colormap, node_size= 50)

 
def createSortedAdjMat(partition, edg_list):    
    initMat = getAdjMat(edg_list)
    
    partDic = {}
    for row in partition:
        if row[1] not in partDic:
            partDic[row[1]] = [row[0]]
        else:
            partDic[row[1]].append(row[0])
            
    numEachComm = []
    for comm in partDic.keys():
        numEachComm.append(len(partDic[comm]))
    
    argSrt = np.argsort(np.array(numEachComm))
    keyList = list(partDic.keys())
    orderedKeys = [keyList[i] for i in argSrt]
    finIds = []
    for k in orderedKeys:
        li = partDic[k]
        for node in li:
            finIds.append(node)
    return getNwAdjMatfromIds(initMat, finIds)


## Methods for Spectral Decomposition

def spectralDecomp_OneIter(edgeList): #  return
    adjMat = getAdjMat(edgeList)
    lplc = getLaplacianMatrix(adjMat)
    fdl, ord = getFreidel(lplc)
    part = [[],[]]
    for i, val in enumerate(fdl):
        if val < 0:
            part[0].append(i)
        else:
            part[1].append(i)
            
    ## Plot Sorted Fiedler vector
    print("Plotting Sorted Fiedler Vector: \n")
    plotFiedler(np.sort(fdl))
    
    ## Plot Corresponding Adjacency Matrix
    print("\n\nPlotting Corresponding Adjacency Matrix: \n")
    nMat = getNwAdjMatfromIds(adjMat, ord)
    showAdjMatrix(nMat)
    
    prt = graphPartition(part,adjMat.shape[0])
    
    print("\n\n Creating Network graph with Spectral Decomposition for first Iteration") 
    G = nx.Graph(nMat)
    pos = nx.spring_layout(G, iterations=20)
    values = []
    diffCom = len(part)
    #print(diffCom)
    
    val = np.linspace(0.1, 1, diffCom)
    commIds = list(set(prt[:,1]))
    ids = list(range(len(commIds)))
    for i in ord: # ord
        # print(row.shape,int(row[1]))
        # print(val[0])
        commun = prt[i,1]
        values.append(val[commIds.index(commun)])   
    colormap = ListedColormap(plt.cm.tab20.colors[:diffCom])
    nx.draw(G, pos, node_color=np.array(values),cmap=colormap, node_size= 50)
    return fdl, adjMat, prt

def plotFiedler(fdl): 

    plt.scatter(list(range(fdl.shape[0])),fdl, linewidths=0.1)

def spectralDecomposition(edgeList):
    
    start = time.time_ns()
    
    adjMat = getAdjMat(edgeList)
    lplc = getLaplacianMatrix(adjMat)
    fdl, ids = getFreidel(lplc)
    partId = -1
    for i in ids:
        if fdl[i] > 0:
            partId = i
            break
    lis = []
    srtFdl = np.sort(fdl) 
    lis.append((srtFdl[:partId], ids[:partId]))
    lis.append((srtFdl[partId:], ids[partId:]))
    
    i = 0
    while i<len(lis):
        comm = lis[i]
        if isSplittable(comm[0]):
            ## Repetively do the same work as before
            newAdj = getSubAdjMatfromIdx(adjMat, comm[1])
            
            lplc = getLaplacianMatrix(newAdj)
            fdl, ids = getFreidel(lplc)
            partId = -1
            for j in ids:
                if fdl[j] > 0:
                    partId = j
                    break
            if partId >= fdl.shape[0]-20 or partId<20:
                i += 1
                continue
            newIds = np.array([comm[1][k] for k in ids])   
            srtFdl = np.sort(fdl) 
            lis[i] = (srtFdl[:partId], newIds[:partId])
            lis.insert(i+1,(srtFdl[partId:], newIds[partId:]))
            
        else:   
            i += 1
    
    comm = [i[1] for i in lis]
    
    print("Total Number of Communities: ",len(lis))
    prt = graphPartition(comm, adjMat.shape[0])
    
    end = time.time_ns()
    print("Time Taken by Spectral Decomposition is ", (end-start)/(10**9)," seconds")
    
    finalIdsOrder = [nd for li in comm for nd in li]
    
    print("\nPlotting Adjacency matrix corresponding to sorted Fiedler vectors for subgraphs: ")
    nAdj = getNwAdjMatfromIds(adjMat, finalIdsOrder)
    showAdjMatrix(nAdj)
    
    print("\n\n Creating Network graph below with ",len(lis)," communities with Spectral Decomposition") 
    # plotGrapVisualize(prt, finalIdsOrder, adjMat):
    G = nx.Graph(nAdj)
    pos = nx.spring_layout(G, iterations=20)
    values = []
    diffCom = len(lis)
    #print(diffCom)
    
    val = np.linspace(0.1, 1, diffCom)
    commIds = list(set(prt[:,1]))
    ids = list(range(len(commIds)))
    for i in finalIdsOrder:
        # print(row.shape,int(row[1]))
        # print(val[0])
        commun = prt[i,1]
        values.append(val[commIds.index(commun)])   
    colormap = ListedColormap(plt.cm.tab20.colors[:diffCom])
    nx.draw(G, pos, node_color=np.array(values),cmap=colormap, node_size= 50)
    
    return prt

## Method for Louvain Algorithm

def louvain_one_iter(edge_list):
  
  start = time.time_ns()
  
  adjMat = getAdjMat(edge_list)
  degree = list(np.sum(adjMat, axis=1))
  adjMat = adjMat/sum(degree)
  degree = degree/sum(degree)
  nodes = list(range(adjMat.shape[0]))
  
  # Creating Neighbors list
  neighbors = {}
  for i in nodes:
    for j in nodes:
      if adjMat[i][j] != 0:
        if i not in neighbors:
          neighbors[i] = [j]
        else:
          neighbors[i].append(j)
    if sum(adjMat[i]) == 0:
      neighbors[i] = []
  
  # for i in neighbors:
  #   print("key ", i, "Neigh",neighbors[i])
  
  # Creating Partitions, community ----> Nodes
  partitions = {}
  for i in range(len(nodes)):
    partitions[i] = [nodes[i]]

  # member partition, basically particular node is part of which partition , node ---> Community
  mapp = {}
  for i in range(len(nodes)):
    mapp[i] = nodes[i]

  while(True):
    flag = 0
    for node in nodes:
      best_comm = mapp[node]
      connected_communities = []
      for neighbor in neighbors[node]:
        if mapp[neighbor] != best_comm:
          connected_communities.append(mapp[neighbor])
      
      delta_Q_max = 0
      delta_Q_curr = d_Merg(node, mapp, partitions, degree, adjMat)
      
      for comm in connected_communities:
        delta_Q_comm = merge(node,comm, partitions, degree, adjMat)
        delta_Q = delta_Q_curr + delta_Q_comm
        if delta_Q > delta_Q_max:
          delta_Q_max = delta_Q
          max_comm = comm

      if delta_Q_max > 0:
        partitions[best_comm].remove(node)
        mapp[node] = max_comm
        partitions[max_comm].append(node)
        flag += 1
    if flag == 0:
      # print("###---STOPPED---###")
      break

    # print("###---CHANGED---###")
    tempDict = {key:val for key,val in partitions.items() if len(val)>0}
    # print(len(tempDict))
  
  end = time.time_ns()
  print("Time Taken by Louvain Algorithm is ", (end-start)/(10**9)," seconds")
  
  print("Total Number of Communities: ",len(tempDict.keys()))
  
  partit = np.zeros((len(nodes),2))
  for li in list(tempDict.values()):
    commId = min(li)
    for nd in li:
      partit[nd, 0] = nd
      partit[nd, 1] = commId
      
  print("\n\n Creating Community Network graph generted through Louvain Algorithm: \n")
  partDic = {}
  for row in partit:
    if row[1] not in partDic:
      partDic[row[1]] = [row[0]]
    else:
      partDic[row[1]].append(row[0])
            
  numEachComm = []
  for comm in partDic.keys():
    numEachComm.append(len(partDic[comm]))
  
  G = nx.Graph(createSortedAdjMat(partit.astype(int), edge_list))
  
  pos = nx.spring_layout(G, iterations=20)
  values = []
  diffCom = len(numEachComm)
  #print(diffCom)
    
  val = np.linspace(0.1, 1, diffCom)
  clr = 0
  for num in numEachComm:
    for count in range(num):
      values.append(val[clr])   
    clr += 1
  colormap = ListedColormap(plt.cm.tab20.colors[:diffCom])
  nx.draw(G, pos, node_color=np.array(values),cmap=colormap, node_size= 50)
    
  return partit.astype(int)


if __name__ == "__main__":

    ## For avoiding Warnings
    warnings.filterwarnings("ignore")
    
    ##----------------------------FB Data --------------------------------
    print("Starting Community Detection for FB Data\n")
    
    ## Spectral Decomposition
    print("1. Using Spectral Decomposition: \n")
    
    nodes_connectivity_list_fb = import_facebook_data("../data/facebook_combined.txt")
    fielder_vec_fb, adj_mat_fb, graph_partition_fb = spectralDecomp_OneIter(nodes_connectivity_list_fb)
    print("One Iteration Done for FB Data using Spectral Algo")
    
    ## Full Execution of Spectral Decomposition
    graph_partition_fb = spectralDecomposition(nodes_connectivity_list_fb)
    clustered_adj_mat_fb = createSortedAdjMat(graph_partition_fb, nodes_connectivity_list_fb)
    print("Sorted Adjcacency Matrix after Spectral Algo: \n")
    showAdjMatrix(clustered_adj_mat_fb)
    
    ## Louvain Algorithm
    print("\n\n2. Using Louvain Algorithm: \n")
    graph_partition_louvain_fb = louvain_one_iter(nodes_connectivity_list_fb)
    
    clustered_adj_mat_fb = createSortedAdjMat(graph_partition_louvain_fb, nodes_connectivity_list_fb)
    print("Sorted Adjcacency Matrix after Lovain Algorithm: \n")
    showAdjMatrix(clustered_adj_mat_fb)
    
    ## --------------------------Bitcoin Data ------------------------------
    print("\n\n\nStarting Community Detection for Bitcoin Data\n")
    ## Spectral Decomposition
    print("1. Using Spectral Decomposition: \n")
    nodes_connectivity_list_btc = import_bitcoin_data("../data/soc-sign-bitcoinotc.csv")
    fielder_vec_btc, adj_mat_btc, graph_partition_btc = spectralDecomp_OneIter(nodes_connectivity_list_btc)
    print("One Iteration for bitcoin data using Spectral decomposition")
    
    ## Full Execution of Spectral Decomposition
    graph_partition_btc = spectralDecomposition(nodes_connectivity_list_btc)
    clustered_adj_mat_btc = createSortedAdjMat(graph_partition_btc, nodes_connectivity_list_btc)
    print("Sorted Adjcacency Matrix after Spectral Algorithm: \n")
    showAdjMatrix(clustered_adj_mat_btc)
    
    ## Louvain Algorithm
    print("\n\n2. Using Louvain Algorithm: \n")
    graph_partition_louvain_btc = louvain_one_iter(nodes_connectivity_list_btc)
    
    clustered_adj_mat_btc = createSortedAdjMat(graph_partition_louvain_btc, nodes_connectivity_list_btc)
    print("Sorted Adjcacency Matrix after Lovain Algorithm: \n")
    showAdjMatrix(clustered_adj_mat_btc)