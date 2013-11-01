import fileinput

D = {}
for k in fileinput.input(['part-m-00001', 'part-m-00002', 'part-m-00003']):
#for k in open('part-m-00001.txt'): #use dictionary to store all vertices and values
    raw = k.rstrip() #remove trailing whitespace, if any
    line_array = k.split("\t") #split on the tab
    vertex = line_array[0]
    value = float(line_array[1])
    #print "Vertex:", vertex, value

    if value in D:
        tmp = D[value]
        tmp.append(vertex) #append in case two vertices are tied
        D[value] = tmp
    else:
        D[value]  = [vertex] #initialize key with one if seen for first time.

s = sorted(D, reverse=True) #sort so largest is first
for sk in s[0:19]: #iterate over top values
    print'Vertex:', D[sk], "\tValue:", sk #print the results
