from queue import Queue
import heapq
import math
import time
start_time = time.time()
f = open("input.txt","r")
# print(f.read())
dimensions = []
i = 0
#this is the SearchType BFS hai ya DFS hai A* hai
searchType = ""
# W -->  H -->
wH = ""
# Initial Landing Site
landingSite = ""
#This is the threshold value
threshHold = 0
#no of target sites is the no of sites given for us to check(Target Sites)
noofTargetSites = 0
#these are the target sites in a list
targetSites = []
#just to take the input
rowCounter = 1
#this is my array
array2D = []
#lets keep a duplicate target site list and set
dupTargetsite = []
# ye set se you will remove the targets for UCS and BFS to get the ans
dupTargetsiteset = set()

# W = Columns (Width) and H = Rows (Height)
W = 0
H = 0
# I will make a target site to add the r-stripped target sites
finaltargetS = set()
# target  list to print
listToPrintTarget = []
#answer list for UCS
ansList = []

for line in f.readlines():
    if(i==0):
        searchType = line.rstrip()
    elif(i==1):
        wH = line
        dimensions = wH.split()
        test = 0
        for dim in dimensions:
            if (test == 0):
                W = int(dim)
            else:
                H = int(dim)
            test += 1
    elif(i==2):
        landingSite = line
    elif(i==3):
        threshHold = int(line)
    elif(i==4):
        noofTargetSites = int(line)
        # print(i," yaha hai i ")
    elif(i>=5 and noofTargetSites >=1):
        targetSites.append(line.rstrip())
        # print("yaha ake target sites h ",noofTargetSites," i h ",i)
        # print("vahi line h ",line)
        i+=1
        noofTargetSites = noofTargetSites - 1
        continue
    else:
        if(rowCounter<=H):
            array2D.append(line)
            rowCounter+=1
            continue
    i+=1



# getting my final targets in a SET removing the /n at the end using rstrip
for loc in targetSites:
    temp = loc.rstrip()
    # finaltargetS.add(temp)
    coorwork = temp.split(" ")
    # print(coorwork,"coorwork aya hai kakas")
    dupTargetsiteset.add(coorwork[0]+","+coorwork[1])
    finaltargetS.add(coorwork[0]+","+coorwork[1])
    listToPrintTarget.append(coorwork[0]+","+coorwork[1])

# print("ye hai list ", dupTargetsite," ye hai set ",listToPrintTarget)

#mapList || PREPARING MY MARSMAP GRID
marsGrid = []

for part in array2D:
    part.rstrip()
    p = part.split()
    # print(p)
    res = list(map(int, p))
    marsGrid.append(res)



#A and Y Coordinates of landing point
# LandingX means the row number of the cell where  it  landed
landingX = 0
# LandingY means the column number of the cell where it landed
landingY = 0
# x of landing point and y of landing point
t = landingSite.split()
chi = 0
for all in t:
    if (chi==1):
        landingX = int(all)
    else:
        landingY = int(all)
    chi+=1

print("landing x is",landingX,"landing y is",landingY)



class state_BFS:
    def __init__(self,parentLoc,currentLoc,rowno,columnno,parentState):
        self.parentLoc = parentLoc
        self.currentLoc = currentLoc
        self.rowno = rowno
        self.columnno = columnno
        self.parentState = parentState

# how to initialize a queue
# q = Queue()

#Elevation Checker Function
def height_Difference(gsi,gsj,psi,psj):
    elevationGs = marsGrid[gsi][gsj]
    elevationPs = marsGrid[psi][psj]
    elevationDiff = abs(elevationGs-elevationPs)
    return elevationDiff


#Path print function
def print_Path(path_start):
    ans = path_start.currentLoc
    while(ans != "noParent"):
        toprint = path_start.currentLoc
        ans = path_start.parentLoc
        print("YE HAI PATH" , toprint)
        path_start = path_start.parentState

# Dekh bhai pehle jo de rkha hai vo asliyat me y coordinate hai!

# BFS Function
def BFS(goal_state):
    visited = set()
    state_String = str(landingY)+','+str(landingX)
    print("State String hai",state_String)
    start_State = state_BFS("noParent",state_String,landingX,landingY,None)

    q = Queue()
    visited.add(state_String)
    q.put(start_State)
    print(visited.__len__(),"Len of visited")
    while(not q.empty()):
        state_outofQueue = q.get()
        currX = state_outofQueue.rowno
        currY = state_outofQueue.columnno
        string_ofNodeDeq = state_outofQueue.currentLoc
        if(goal_state == string_ofNodeDeq):
            print(string_ofNodeDeq+" ending of it BFS")
            print("Curr x ",currX,"y",currY)
            print(marsGrid[currX][currY])
            print_Path(state_outofQueue)
            ansList.append(state_outofQueue)
            break

        if((currX-1)>=0):

            if((currY-1)>=0):
                x_Cor = currX-1
                y_Cor = currY-1
                next_Statestring = str(y_Cor) + ',' + str(x_Cor)
                if(next_Statestring not in visited and height_Difference(currX,currY,currX-1,currY-1)<=threshHold):
                    node_tobeadded = state_BFS(state_outofQueue.currentLoc,next_Statestring,x_Cor,y_Cor,state_outofQueue)
                    q.put(node_tobeadded)
                    visited.add(next_Statestring)

            if ((currY + 1) < W):
                x_Cor = currX - 1
                y_Cor = currY + 1
                next_Statestring = str(y_Cor) + ',' + str(x_Cor)
                if(next_Statestring not in visited and height_Difference(currX,currY,currX-1,currY+1)<=threshHold):
                    node_tobeadded = state_BFS(state_outofQueue.currentLoc, next_Statestring, x_Cor, y_Cor,state_outofQueue)
                    q.put(node_tobeadded)
                    visited.add(next_Statestring)

            # next_Statestring = str(currX) + ' ' + str(currY)
            x_Cor = currX - 1
            y_Cor = currY
            next_Statestring = str(y_Cor) + ',' + str(x_Cor)
            if (next_Statestring not in visited and height_Difference(currX,currY,currX-1,currY)<=threshHold):
                node_tobeadded = state_BFS(state_outofQueue.currentLoc, next_Statestring, x_Cor, y_Cor,state_outofQueue)
                q.put(node_tobeadded)
                visited.add(next_Statestring)

        if(currX+1 < H):
            if ((currY - 1) >= 0):
                x_Cor = currX + 1
                y_Cor = currY - 1
                next_Statestring = str(y_Cor) + ',' + str(x_Cor)
                if (next_Statestring not in visited and height_Difference(currX,currY,currX + 1,currY - 1) <= threshHold):
                    node_tobeadded = state_BFS(state_outofQueue.currentLoc, next_Statestring, x_Cor, y_Cor,state_outofQueue)
                    q.put(node_tobeadded)
                    visited.add(next_Statestring)

            if ((currY + 1) < W):
                x_Cor = currX + 1
                y_Cor = currY + 1
                next_Statestring = str(y_Cor) + ',' + str(x_Cor)
                if (next_Statestring not in visited and height_Difference(currX,currY,currX + 1,currY + 1) <= threshHold):
                    node_tobeadded = state_BFS(state_outofQueue.currentLoc, next_Statestring, x_Cor, y_Cor,state_outofQueue)
                    q.put(node_tobeadded)
                    visited.add(next_Statestring)

                # next_Statestring = str(currX) + ' ' + str(currY)
            x_Cor = currX + 1
            y_Cor = currY
            next_Statestring = str(y_Cor) + ',' + str(x_Cor)
            if (next_Statestring not in visited and height_Difference(currX, currY, currX + 1,currY) <= threshHold):
                node_tobeadded = state_BFS(state_outofQueue.currentLoc, next_Statestring, x_Cor, y_Cor,state_outofQueue)
                q.put(node_tobeadded)
                visited.add(next_Statestring)


        if (currY-1 >= 0):
            x_Cor = currX
            y_Cor = currY - 1
            next_Statestring = str(y_Cor) + ',' + str(x_Cor)
            if (next_Statestring not in visited and height_Difference(currX, currY, currX,currY - 1) <= threshHold):
                node_tobeadded = state_BFS(state_outofQueue.currentLoc, next_Statestring, x_Cor, y_Cor,state_outofQueue)
                q.put(node_tobeadded)
                visited.add(next_Statestring)

        if (currY + 1 < W):
            x_Cor = currX
            y_Cor = currY + 1
            next_Statestring = str(y_Cor) + ',' + str(x_Cor)
            if (next_Statestring not in visited and height_Difference(currX, currY, currX - 1,currY + 1) <= threshHold):
                node_tobeadded = state_BFS(state_outofQueue.currentLoc, next_Statestring, x_Cor, y_Cor,state_outofQueue)
                q.put(node_tobeadded)
                visited.add(next_Statestring)



# this function calls bfs!
def call_BFS_forTS():
    print(targetSites)
    for items in targetSites:
        site = items.rstrip()
        two_points = site.split()
        s = ""
        valz = 0
        for z in two_points:
            if valz == 0:
                s+=z
                s+=","
            else:
                s+=z
            valz+=1
        print(s, "BFS BEING CALLED FOR THIS")
        BFS(s)

####### Print UCS Path ##
def print_UCS_path(pc_Dict,gS):
    # print("YHA AKE PC H ",pc_Dict)
    # print("KAAM KARO")
    # print(pc_Dict)
    child = gS
    parent = pc_Dict[child]
    # print("YE UCS ka bacha h",child)
    while(parent != "startingPoint"):
        # print(child)
        child = parent
        parent = pc_Dict[child]


###################################################################### UCS ##############################
def UCS(goal_State):

    # open list me vo states hongi jo queue me hongi
    openList = set()

    # closed list me vo states hongi jo visited ho chuki hongi
    closedList = set()

    # parent child ki dictionary - key hoga child and value hogi parent
    pc_Dict = {}

    # State 0,3 means it has landed on 3,0
    landingSite_State = str(landingY)+","+str(landingX)

    # parent Child Dictionary Update ki!
    pc_Dict[landingSite_State] = "startingPoint"

    q = []

    # make a priority queue
    #priority queue me state node daal with all the info you need
    # structure of tuple jo priority queue me jaa rha h is (dist_till_now,state_of_Curr)
    heapq.heappush(q,(0,landingSite_State))

    # jaise hi queue me dala open me daal do us state ko
    openList.add(landingSite_State)

    while (q.__len__() is not 0):
        state_Queuetop = heapq.heappop(q)

        # Distance string
        first_Tentry = state_Queuetop[0]
        # print(first_Tentry,"Dist till now hai ye")

        # get the state of the node in queue that has been popped
        state_StringQT = state_Queuetop[1]
        # print(state_StringQT)

        # jab bhi queue se nikalo to closedList me daal do matlab visited vali list me me
        # CLOSED LIST MATLAB JO VISITED HAI
        closedList.add(state_StringQT)

        # print(closedList,"tera baap aya hai closed me tu kya krega ab")
        if(state_StringQT == goal_State):
            # print(pc_Dict,"JATE HUE YE HAI")
            # print_UCS_path(pc_Dict,goal_State)
            print(goal_State)
            break

        coord = state_StringQT.split(',')

        # Row Number
        currX = int(coord[1])
        # Column number
        currY = int(coord[0])

        # distance till now
        dist_Tn = int(first_Tentry)

        if(currX-1>=0):

            # ye diagonal movement hai
            if(currY-1>=0):

                locX = currX - 1
                locY = currY - 1
                # next child ke coordinated kre hai ye

                #next child's state
                next_Childstate = str(locY)+","+str(locX)

                # new distance for this node (g)
                g = dist_Tn + 14
                # distance to be added in this case is 14 (PATH-COST CHILD)

                # if no node in open or closed has child's state
                if(next_Childstate not in closedList and next_Childstate not in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                    # 1) Push In The Priority Queue
                    heapq.heappush(q, (g, next_Childstate))

                    # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                    openList.add(next_Childstate)

                    # 3) parent child dict update
                    pc_Dict[next_Childstate] = state_StringQT

                elif(next_Childstate in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                    req_tup = ()

                    for infos in q:

                        check = infos[1]
                        # ye state hai har tuple ki in PQ

                        if(next_Childstate == check):
                            pathcost_Node = infos[0]

                            if (pathcost_Node > g):
                                q.remove(infos)
                                q.append((g,next_Childstate))
                                pc_Dict[next_Childstate] = state_StringQT
                                heapq.heapify(q)
                                break
                                # the following break is to break the for loop for infos
                                # break

            # ye hai diagonal up right
            if (currY + 1 < W):

                locX = currX - 1
                locY = currY + 1
                # next child ke coordinated kre hai ye

                # next child's state
                next_Childstate = str(locY) + ',' + str(locX)

                # new distance for this node (g)
                g = dist_Tn + 14
                # distance to be added in this case is 14 (PATH-COST CHILD)

                # and height_Difference(currX, currY, currX + 1, currY - 1) <= threshHold --> YE CONDITION DALNI H

                # if no node in open or closed has child's state
                if (next_Childstate not in closedList and next_Childstate not in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                    # 1) Push In The Priority Queue
                    heapq.heappush(q, (g, next_Childstate))

                    # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                    openList.add(next_Childstate)

                    # 3) parent child dict update
                    pc_Dict[next_Childstate] = state_StringQT

                elif (next_Childstate in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                    req_tup = ()

                    for infos in q:

                        check = infos[1]
                        # ye state hai har tuple ki in PQ

                        if (next_Childstate == check):
                            pathcost_Node = infos[0]

                            if (pathcost_Node > g):
                                q.remove(infos)
                                q.append((g, next_Childstate))
                                pc_Dict[next_Childstate] = state_StringQT
                                heapq.heapify(q)
                                # the following break is to break the for loop for infos
                                break

            ################## Check for indentation #######################
            # final case ki vo sath me hi h (i-1,j)
            locX = currX - 1
            locY = currY
            # next child ke coordinated kre hai ye

            # next child's state
            next_Childstate = str(locY) + "," + str(locX)

            # new distance for this node (g)
            g = dist_Tn + 10
            # distance to be added in this case is 14 (PATH-COST CHILD)

            # and height_Difference(currX, currY, currX + 1, currY - 1) <= threshHold --> YE CONDITION DALNI H

            # if no node in open or closed has child's state
            if (next_Childstate not in closedList and next_Childstate not in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                # 1) Push In The Priority Queue
                heapq.heappush(q, (g, next_Childstate))

                # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                openList.add(next_Childstate)

                # 3) parent child dict update
                pc_Dict[next_Childstate] = state_StringQT

            elif (next_Childstate in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                req_tup = ()

                for infos in q:

                    check = infos[1]
                    # ye state hai har tuple ki in PQ

                    if (next_Childstate == check):
                        pathcost_Node = infos[0]

                        if (pathcost_Node > g):
                            q.remove(infos)
                            q.append((g, next_Childstate))
                            pc_Dict[next_Childstate] = state_StringQT
                            heapq.heapify(q)
                            # the following break is to break the for loop for infos
                            break

        ############## Second time currx vala check aya hai #################
        if (currX + 1 < H):

            # ye diagonal movement hai
            if (currY - 1 >= 0):

                locX = currX + 1
                locY = currY - 1
                # next child ke coordinated kre hai ye

                # next child's state
                next_Childstate = str(locY) + "," + str(locX)

                # new distance for this node (g)
                g = dist_Tn + 14
                # distance to be added in this case is 14 (PATH-COST CHILD)

                # if no node in open or closed has child's state
                if (next_Childstate not in closedList and next_Childstate not in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                    # 1) Push In The Priority Queue
                    heapq.heappush(q, (g, next_Childstate))

                    # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                    openList.add(next_Childstate)

                    # 3) parent child dict update
                    pc_Dict[next_Childstate] = state_StringQT

                elif (next_Childstate in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                    req_tup = ()

                    for infos in q:

                        check = infos[1]
                        # ye state hai har tuple ki in PQ

                        if (next_Childstate == check):
                            pathcost_Node = infos[0]

                            if (pathcost_Node > g):
                                q.remove(infos)
                                q.append((g, next_Childstate))
                                pc_Dict[next_Childstate] = state_StringQT
                                heapq.heapify(q)
                                # the following break is to break the for loop for infos
                                break

            # ye hai diagonal up right
            if (currY + 1 < W):

                locX = currX + 1
                locY = currY + 1
                # next child ke coordinated kre hai ye

                # next child's state
                next_Childstate = str(locY) + "," + str(locX)

                # new distance for this node (g)
                g = dist_Tn + 14
                # distance to be added in this case is 14 (PATH-COST CHILD)

                # and height_Difference(currX, currY, currX + 1, currY - 1) <= threshHold --> YE CONDITION DALNI H

                # if no node in open or closed has child's state
                if (next_Childstate not in closedList and next_Childstate not in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                    # 1) Push In The Priority Queue
                    heapq.heappush(q, (g, next_Childstate))

                    # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                    openList.add(next_Childstate)

                    # 3) parent child dict update
                    pc_Dict[next_Childstate] = state_StringQT

                elif (next_Childstate in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                    req_tup = ()

                    for infos in q:

                        check = infos[1]
                        # ye state hai har tuple ki in PQ

                        if (next_Childstate == check):
                            pathcost_Node = infos[0]

                            if (pathcost_Node > g):
                                q.remove(infos)
                                q.append((g, next_Childstate))
                                pc_Dict[next_Childstate] = state_StringQT
                                heapq.heapify(q)
                                # the following break is to break the for loop for infos
                                break

            ################## Check for indentation #######################
            # final case ki vo sath me hi h (i-1,j)
            locX = currX + 1
            locY = currY
            # next child ke coordinated kre hai ye

            # next child's state
            next_Childstate = str(locY) + "," + str(locX)

            # new distance for this node (g)
            g = dist_Tn + 10
            # distance to be added in this case is 14 (PATH-COST CHILD)

            # and height_Difference(currX, currY, currX + 1, currY - 1) <= threshHold --> YE CONDITION DALNI H

            # if no node in open or closed has child's state
            if (next_Childstate not in closedList and next_Childstate not in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                # 1) Push In The Priority Queue
                heapq.heappush(q, (g, next_Childstate))

                # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                openList.add(next_Childstate)

                # 3) parent child dict update
                pc_Dict[next_Childstate] = state_StringQT

            elif (next_Childstate in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                req_tup = ()

                for infos in q:

                    check = infos[1]
                    # ye state hai har tuple ki in PQ

                    if (next_Childstate == check):
                        pathcost_Node = infos[0]

                        if (pathcost_Node > g):
                            q.remove(infos)
                            q.append((g, next_Childstate))
                            pc_Dict[next_Childstate] = state_StringQT
                            heapq.heapify(q)
                            # the following break is to break the for loop for infos
                            break

        # Now ye hai side valo ke lie check ##################

        if (currY - 1 >= 0):

            locX = currX
            locY = currY - 1
            # next child ke coordinated kre hai ye

            # next child's state
            next_Childstate = str(locY) + "," + str(locX)

            # new distance for this node (g)
            g = dist_Tn + 10
            # distance to be added in this case is 14 (PATH-COST CHILD)

            # if no node in open or closed has child's state
            if (next_Childstate not in closedList and next_Childstate not in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                # 1) Push In The Priority Queue
                heapq.heappush(q, (g, next_Childstate))

                # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                openList.add(next_Childstate)

                # 3) parent child dict update
                pc_Dict[next_Childstate] = state_StringQT

            elif (next_Childstate in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                req_tup = ()

                for infos in q:

                    check = infos[1]
                    # ye state hai har tuple ki in PQ

                    if (next_Childstate == check):
                        pathcost_Node = infos[0]

                        if (pathcost_Node > g):
                            q.remove(infos)
                            q.append((g, next_Childstate))
                            pc_Dict[next_Childstate] = state_StringQT
                            heapq.heapify(q)
                            # the following break is to break the for loop for infos
                            break


        if (currY + 1 < W):

            locX = currX
            locY = currY + 1
            # next child ke coordinated kre hai ye

            # next child's state
            next_Childstate = str(locY) + "," + str(locX)

            # new distance for this node (g)
            g = dist_Tn + 10
            # distance to be added in this case is 14 (PATH-COST CHILD)

            # if no node in open or closed has child's state
            if (next_Childstate not in closedList and next_Childstate not in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                # 1) Push In The Priority Queue
                heapq.heappush(q, (g, next_Childstate))

                # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                openList.add(next_Childstate)

                # 3) parent child dict update
                pc_Dict[next_Childstate] = state_StringQT

            elif (next_Childstate in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                req_tup = ()

                for infos in q:

                    check = infos[1]
                    # ye state hai har tuple ki in PQ

                    if (next_Childstate == check):
                        pathcost_Node = infos[0]

                        if (pathcost_Node > g):
                            q.remove(infos)
                            q.append((g, next_Childstate))
                            pc_Dict[next_Childstate] = state_StringQT
                            heapq.heapify(q)
                            # the following break is to break the for loop for infos
                            break



##################### UCS NE MAA CHOD DI H ############################

def UCS21(goal_State):

    # open list me vo states hongi jo queue me hongi
    openList = set()

    # closed list me vo states hongi jo visited ho chuki hongi
    closedList = set()

    # parent child ki dictionary - key hoga child and value hogi parent
    pc_Dict = {}

    # State 0,3 means it has landed on 3,0
    landingSite_State = str(landingY)+","+str(landingX)

    # parent Child Dictionary Update ki!
    pc_Dict[landingSite_State] = "startingPoint"

    q = []

    # make a priority queue
    #priority queue me state node daal with all the info you need
    # structure of tuple jo priority queue me jaa rha h is (dist_till_now,state_of_Curr)
    heapq.heappush(q,(0,landingSite_State))

    # jaise hi queue me dala open me daal do us state ko
    openList.add(landingSite_State)

    while (q.__len__() is not 0):
        state_Queuetop = heapq.heappop(q)

        # Distance string
        first_Tentry = state_Queuetop[0]
        # print(first_Tentry,"Dist till now hai ye")

        # get the state of the node in queue that has been popped
        state_StringQT = state_Queuetop[1]
        # print(state_StringQT)
        if(state_StringQT in closedList):
            continue

        # jab bhi queue se nikalo to closedList me daal do matlab visited vali list me me
        # CLOSED LIST MATLAB JO VISITED HAI
        closedList.add(state_StringQT)

        # print(closedList,"tera baap aya hai closed me tu kya krega ab")
        if(state_StringQT == goal_State):
            # print(pc_Dict,"JATE HUE YE HAI")
            # print_UCS_path(pc_Dict,goal_State)
            print(goal_State)
            break

        coord = state_StringQT.split(',')

        # Row Number
        currX = int(coord[1])
        # Column number
        currY = int(coord[0])

        # distance till now
        dist_Tn = int(first_Tentry)

        if(currX-1>=0):

            # ye diagonal movement hai
            if(currY-1>=0):

                locX = currX - 1
                locY = currY - 1
                # next child ke coordinated kre hai ye

                #next child's state
                next_Childstate = str(locY)+","+str(locX)

                # new distance for this node (g)
                g = dist_Tn + 14
                # distance to be added in this case is 14 (PATH-COST CHILD)

                # if no node in open or closed has child's state
                if(next_Childstate not in closedList and next_Childstate not in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                    # 1) Push In The Priority Queue
                    heapq.heappush(q, (g, next_Childstate))

                    # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                    openList.add(next_Childstate)

                    # 3) parent child dict update
                    pc_Dict[next_Childstate] = state_StringQT

                elif(next_Childstate in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                    req_tup = ()

                    for infos in q:

                        check = infos[1]
                        # ye state hai har tuple ki in PQ

                        if(next_Childstate == check):
                            pathcost_Node = infos[0]

                            if (pathcost_Node > g):
                                q.remove(infos)
                                q.append((g,next_Childstate))
                                pc_Dict[next_Childstate] = state_StringQT
                                heapq.heapify(q)
                                break
                                # the following break is to break the for loop for infos
                                # break

            # ye hai diagonal up right
            if (currY + 1 < W):

                locX = currX - 1
                locY = currY + 1
                # next child ke coordinated kre hai ye

                # next child's state
                next_Childstate = str(locY) + ',' + str(locX)

                # new distance for this node (g)
                g = dist_Tn + 14
                # distance to be added in this case is 14 (PATH-COST CHILD)

                # and height_Difference(currX, currY, currX + 1, currY - 1) <= threshHold --> YE CONDITION DALNI H

                # if no node in open or closed has child's state
                if (next_Childstate not in closedList and next_Childstate not in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                    # 1) Push In The Priority Queue
                    heapq.heappush(q, (g, next_Childstate))

                    # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                    openList.add(next_Childstate)

                    # 3) parent child dict update
                    pc_Dict[next_Childstate] = state_StringQT

                elif (next_Childstate in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                    req_tup = ()

                    for infos in q:

                        check = infos[1]
                        # ye state hai har tuple ki in PQ

                        if (next_Childstate == check):
                            pathcost_Node = infos[0]

                            if (pathcost_Node > g):
                                q.remove(infos)
                                q.append((g, next_Childstate))
                                pc_Dict[next_Childstate] = state_StringQT
                                heapq.heapify(q)
                                # the following break is to break the for loop for infos
                                break

            ################## Check for indentation #######################
            # final case ki vo sath me hi h (i-1,j)
            locX = currX - 1
            locY = currY
            # next child ke coordinated kre hai ye

            # next child's state
            next_Childstate = str(locY) + "," + str(locX)

            # new distance for this node (g)
            g = dist_Tn + 10
            # distance to be added in this case is 14 (PATH-COST CHILD)

            # and height_Difference(currX, currY, currX + 1, currY - 1) <= threshHold --> YE CONDITION DALNI H

            # if no node in open or closed has child's state
            if (next_Childstate not in closedList and next_Childstate not in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                # 1) Push In The Priority Queue
                heapq.heappush(q, (g, next_Childstate))

                # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                openList.add(next_Childstate)

                # 3) parent child dict update
                pc_Dict[next_Childstate] = state_StringQT

            elif (next_Childstate in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                req_tup = ()

                for infos in q:

                    check = infos[1]
                    # ye state hai har tuple ki in PQ

                    if (next_Childstate == check):
                        pathcost_Node = infos[0]

                        if (pathcost_Node > g):
                            q.remove(infos)
                            q.append((g, next_Childstate))
                            pc_Dict[next_Childstate] = state_StringQT
                            heapq.heapify(q)
                            # the following break is to break the for loop for infos
                            break

        ############## Second time currx vala check aya hai #################
        if (currX + 1 < H):

            # ye diagonal movement hai
            if (currY - 1 >= 0):

                locX = currX + 1
                locY = currY - 1
                # next child ke coordinated kre hai ye

                # next child's state
                next_Childstate = str(locY) + "," + str(locX)

                # new distance for this node (g)
                g = dist_Tn + 14
                # distance to be added in this case is 14 (PATH-COST CHILD)

                # if no node in open or closed has child's state
                if (next_Childstate not in closedList and next_Childstate not in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                    # 1) Push In The Priority Queue
                    heapq.heappush(q, (g, next_Childstate))

                    # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                    openList.add(next_Childstate)

                    # 3) parent child dict update
                    pc_Dict[next_Childstate] = state_StringQT

                elif (next_Childstate in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                    req_tup = ()

                    for infos in q:

                        check = infos[1]
                        # ye state hai har tuple ki in PQ

                        if (next_Childstate == check):
                            pathcost_Node = infos[0]

                            if (pathcost_Node > g):
                                q.remove(infos)
                                q.append((g, next_Childstate))
                                pc_Dict[next_Childstate] = state_StringQT
                                heapq.heapify(q)
                                # the following break is to break the for loop for infos
                                break

            # ye hai diagonal up right
            if (currY + 1 < W):

                locX = currX + 1
                locY = currY + 1
                # next child ke coordinated kre hai ye

                # next child's state
                next_Childstate = str(locY) + "," + str(locX)

                # new distance for this node (g)
                g = dist_Tn + 14
                # distance to be added in this case is 14 (PATH-COST CHILD)

                # and height_Difference(currX, currY, currX + 1, currY - 1) <= threshHold --> YE CONDITION DALNI H

                # if no node in open or closed has child's state
                if (next_Childstate not in closedList and next_Childstate not in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                    # 1) Push In The Priority Queue
                    heapq.heappush(q, (g, next_Childstate))

                    # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                    openList.add(next_Childstate)

                    # 3) parent child dict update
                    pc_Dict[next_Childstate] = state_StringQT

                elif (next_Childstate in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                    req_tup = ()

                    for infos in q:

                        check = infos[1]
                        # ye state hai har tuple ki in PQ

                        if (next_Childstate == check):
                            pathcost_Node = infos[0]

                            if (pathcost_Node > g):
                                q.remove(infos)
                                q.append((g, next_Childstate))
                                pc_Dict[next_Childstate] = state_StringQT
                                heapq.heapify(q)
                                # the following break is to break the for loop for infos
                                break

            ################## Check for indentation #######################
            # final case ki vo sath me hi h (i-1,j)
            locX = currX + 1
            locY = currY
            # next child ke coordinated kre hai ye

            # next child's state
            next_Childstate = str(locY) + "," + str(locX)

            # new distance for this node (g)
            g = dist_Tn + 10
            # distance to be added in this case is 14 (PATH-COST CHILD)

            # and height_Difference(currX, currY, currX + 1, currY - 1) <= threshHold --> YE CONDITION DALNI H

            # if no node in open or closed has child's state
            if (next_Childstate not in closedList and next_Childstate not in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                # 1) Push In The Priority Queue
                heapq.heappush(q, (g, next_Childstate))

                # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                openList.add(next_Childstate)

                # 3) parent child dict update
                pc_Dict[next_Childstate] = state_StringQT

            elif (next_Childstate in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                req_tup = ()

                for infos in q:

                    check = infos[1]
                    # ye state hai har tuple ki in PQ

                    if (next_Childstate == check):
                        pathcost_Node = infos[0]

                        if (pathcost_Node > g):
                            q.remove(infos)
                            q.append((g, next_Childstate))
                            pc_Dict[next_Childstate] = state_StringQT
                            heapq.heapify(q)
                            # the following break is to break the for loop for infos
                            break

        # Now ye hai side valo ke lie check ##################

        if (currY - 1 >= 0):

            locX = currX
            locY = currY - 1
            # next child ke coordinated kre hai ye

            # next child's state
            next_Childstate = str(locY) + "," + str(locX)

            # new distance for this node (g)
            g = dist_Tn + 10
            # distance to be added in this case is 14 (PATH-COST CHILD)

            # if no node in open or closed has child's state
            if (next_Childstate not in closedList and next_Childstate not in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                # 1) Push In The Priority Queue
                heapq.heappush(q, (g, next_Childstate))

                # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                openList.add(next_Childstate)

                # 3) parent child dict update
                pc_Dict[next_Childstate] = state_StringQT

            elif (next_Childstate in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                req_tup = ()

                for infos in q:

                    check = infos[1]
                    # ye state hai har tuple ki in PQ

                    if (next_Childstate == check):
                        pathcost_Node = infos[0]

                        if (pathcost_Node > g):
                            q.remove(infos)
                            q.append((g, next_Childstate))
                            pc_Dict[next_Childstate] = state_StringQT
                            heapq.heapify(q)
                            # the following break is to break the for loop for infos
                            break


        if (currY + 1 < W):

            locX = currX
            locY = currY + 1
            # next child ke coordinated kre hai ye

            # next child's state
            next_Childstate = str(locY) + "," + str(locX)

            # new distance for this node (g)
            g = dist_Tn + 10
            # distance to be added in this case is 14 (PATH-COST CHILD)

            # if no node in open or closed has child's state
            if (next_Childstate not in closedList and next_Childstate not in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                # 1) Push In The Priority Queue
                heapq.heappush(q, (g, next_Childstate))

                # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                openList.add(next_Childstate)

                # 3) parent child dict update
                pc_Dict[next_Childstate] = state_StringQT

            elif (next_Childstate in openList and height_Difference(currX,currY,locX,locY)<=threshHold):

                req_tup = ()

                for infos in q:

                    check = infos[1]
                    # ye state hai har tuple ki in PQ

                    if (next_Childstate == check):
                        pathcost_Node = infos[0]

                        if (pathcost_Node > g):
                            q.remove(infos)
                            q.append((g, next_Childstate))
                            pc_Dict[next_Childstate] = state_StringQT
                            heapq.heapify(q)
                            # the following break is to break the for loop for infos
                            break




# UCS start yaha h
# call_BFS_forTS()

# UCS("98,997")

BFSkapathBro = []

def print_Path_BFS(pc_Dict):
    global BFSkapathBro
    finalans = []
    for sitesT in listToPrintTarget:
        lelo = sitesT
        tli = []
        # print(sitesT,"Yaha Ake sites t")
        if (sitesT not in pc_Dict.keys()):
            tli.append("FAIL")
            finalans.append(tli)
            continue
        # tli = []
        tli.append(sitesT)
        while sitesT!= "Noparent":
            # print("ko")
            sitesT = pc_Dict[sitesT]
            if(sitesT!="Noparent"):
                tli.append(sitesT)
        # print(len(tli),"no")
        tli.reverse()
        finalans.append(tli)
    # print(finalans,"ans hai yue")
    BFSkapathBro = finalans


def BFS2():
    # A set for keeping the visited nodes. Jaise hi QUEUE me dala visited hogaya
    visited = set()
    # State String is Column number , Row number
    state_String = str(landingY) + ',' + str(landingX)

    # child parent dictionar bana
    pc_Dict = {}
    pc_Dict[state_String] = "Noparent"

    # make a queue and add 1 (Landing state) node to it
    q = Queue()
    visited.add(state_String)
    q.put(state_String)

    while (not q.empty()):
        state_QT = q.get()
        # get the top state in the queue
        coord = state_QT.split(',')
        currX = int(coord[1])
        currY = int(coord[0])

        #yaha neeche  change kia h ki goal state hata ke ab target sites me check kr rha hu
        # print(state_QT,"yaha ake state QT and state qt is ",dupTargetsiteset)
        if(state_QT in dupTargetsiteset):
            # print("make function again")
            # print(pc_Dict,"sksid")
            dupTargetsiteset.remove(state_QT)
            # print(state_QT)
            if(len(dupTargetsiteset)==0):
                print(len(dupTargetsiteset),"ye hai")
                # print_Path_BFS(pc_Dict)
                break

        if (currX-1>=0):

            if (currY-1>=0):

                childX = currX - 1;
                childY = currY - 1;

                next_Statestring = str(childY) + ',' + str(childX)

                if (next_Statestring not in visited and height_Difference(currX,currY,childX,childY)<=threshHold):
                    pc_Dict[next_Statestring] = state_QT

                    q.put(next_Statestring)
                    visited.add(next_Statestring)

            if (currY+1 < W):

                childX = currX - 1;
                childY = currY + 1;

                next_Statestring = str(childY) + ',' + str(childX)

                if (next_Statestring not in visited and height_Difference(currX,currY,childX,childY)<=threshHold):
                    pc_Dict[next_Statestring] = state_QT
                    q.put(next_Statestring)
                    visited.add(next_Statestring)

            # Last Case ye hai

            childX = currX - 1
            childY = currY

            next_Statestring = str(childY) + ',' + str(childX)

            if (next_Statestring not in visited and height_Difference(currX, currY, childX, childY) <= threshHold):
                pc_Dict[next_Statestring] = state_QT
                q.put(next_Statestring)
                visited.add(next_Statestring)

        if (currX + 1 < H):

            if (currY - 1 >= 0):

                childX = currX + 1;
                childY = currY - 1;

                next_Statestring = str(childY) + ',' + str(childX)

                if (next_Statestring not in visited and height_Difference(currX, currY, childX, childY) <= threshHold):
                    pc_Dict[next_Statestring] = state_QT
                    q.put(next_Statestring)
                    visited.add(next_Statestring)

            if (currY + 1 < W):

                childX = currX + 1;
                childY = currY + 1;

                next_Statestring = str(childY) + ',' + str(childX)

                if (next_Statestring not in visited and height_Difference(currX, currY, childX, childY) <= threshHold):
                    pc_Dict[next_Statestring] = state_QT
                    q.put(next_Statestring)
                    visited.add(next_Statestring)

            # Last Case ye hai

            childX = currX + 1
            childY = currY

            next_Statestring = str(childY) + ',' + str(childX)

            if (next_Statestring not in visited and height_Difference(currX, currY, childX, childY) <= threshHold):
                pc_Dict[next_Statestring] = state_QT
                q.put(next_Statestring)
                visited.add(next_Statestring)


        if(currY-1>=0):
            childX = currX
            childY = currY - 1

            next_Statestring = str(childY) + ',' + str(childX)

            if (next_Statestring not in visited and height_Difference(currX, currY, childX, childY) <= threshHold):
                pc_Dict[next_Statestring] = state_QT
                q.put(next_Statestring)
                visited.add(next_Statestring)

        if (currY + 1 < W):
            childX = currX
            childY = currY + 1

            next_Statestring = str(childY) + ',' + str(childX)

            if (next_Statestring not in visited and height_Difference(currX, currY, childX, childY) <= threshHold):
                pc_Dict[next_Statestring] = state_QT
                q.put(next_Statestring)
                visited.add(next_Statestring)

    print_Path_BFS(pc_Dict)


def heuristic(current_row, current_column, tx,ty):
    # min_dist = min(tx-current_row, ty-current_column)

    dx = abs(tx - current_row)
    dy = abs(ty - current_column)
    min_dist = min(dx, dy)
    # return 14 * min_dist
    # return 5 * (dx + dy) + (7 - 2 * 5) * min_dist
    # return dx + dy
    # return 0
    return 10 * (dx + dy) + (14 - 2 * 10) * min_dist


    # dx = abs(tx-current_row)
    # dy = abs(ty-current_column)
    # curr = marsGrid[current_row][current_column]
    # nextt = marsGrid[tx][ty]
    # vl = abs(curr-nextt)

    # arpan ans
    # min_dist = min(tx - current_row, ty - current_column)
    # dx = abs(tx - current_row)
    # dy = abs(ty - current_column)
    # return dx + dy
    # return 10 * (dx + dy) + (14 - 2 * 10) * min_dist
    # return 0
    # return 5 *min_dist
    # return 2*abs(current_column-ty)+2*abs(current_row-tx)
    # return max((current_row-tx),(current_column-ty))+vl
    # return 10*(dx + dy) + (14 - 2 * 10) * min_dist
    # return 7*(dx + dy) + (11 - 2 * 7) * min_dist
    # return 5*(dx + dy) + (7-2*5)*min_dist



# Heuristic function --> currX row of current
# def heuristic(currX,currY,goalX,goalY):
#     # print("hola")
#     # currX --> row of the current state jiss se hume location of target ki val nikalni h
#     # currY --> column no of current state jiss se hume location of target ki val nikalni h
#     # goalX --> row number of the goal state
#     # goalY --> column number of the goal state
#     heu_val = abs(goalX-currY)+abs(goalY-currY)
#     return heu_val

# print for astar 2 hai ye ab yaha ------>
def print_astar2(pc_dict,startg):
    anlist = list()
    start = startg
    baaplist = list()
    anlist.append(start)
    while (start != "noParent"):

        start = pc_dict[start]
        anlist.append(start)

    print(baaplist)


allpathsforAstar = []

def addtoallpaths(pc_dictn,goalS):
    # print(goalS," YE hai goal state")
    temppath = []

    if(goalS not in pc_dictn.keys()):
        temppath.append("FAIL")
        allpathsforAstar.append(temppath)
        return
    start = goalS
    start = pc_dictn[start]

    temppath.append(goalS)
    while(start!="noParent"):
        temppath.append(start)
        start = pc_dictn[start]

    temppath.reverse()
    allpathsforAstar.append(temppath)
    # print(allpathsforAstar)


# astar 2 ka code hai ye --------------------------------------------------> This is the final A STAR

def atsar2(goal_state):
    # state and f(n) dictionary
    state_f = dict()
    # This is to store the value of g and state
    state_g = dict()
    # This dictionary will be to store the f and state for that f


    # get the state string
    ss_Landing = str(landingY) + ',' + str(landingX)
    # print(ss_Landing,"landing site ye h")

    # get the first site for the state and it will have a g of  0
    state_g[ss_Landing] = 0

    # parent dict and open and closed lists
    # open list me vo states hongi jo queue me hongi
    openList = set()

    # closed list me vo states hongi jo visited ho chuki hongi
    closedList = set()

    # parent child ki dictionary - key hoga child and value hogi parent
    pc_Dict = {}

    # goal state  ke x an d y nikal ke rkhlete hai and remeber y pehle hai and then x hai input format me :(

    ts = goal_state.split(",")
    ts_X = int(ts[1])
    ts_Y = int(ts[0])
    # print(ts)

    # parent Child Dictionary Update ki!
    pc_Dict[ss_Landing] = "noParent"

    q = []

    # make a priority queue
    # priority queue me state node daal with all the info you need
    # structure of tuple jo priority queue me jaa rha h is (dist_till_now,state_of_Curr)

    initial_val = heuristic(landingX, landingY, ts_X, ts_Y)
    heapq.heappush(q, (initial_val, ss_Landing))

    # initial value ko state_f me daalde brooo
    state_f[ss_Landing] = initial_val

    # YE DUSRI BAAR KIA H DEKH LIO KOI DIKKAT NA KRE!!!!
    state_g[ss_Landing] = 0

    # jaise hi queue me dala open me daal do us state ko
    openList.add(ss_Landing)

    #checker
    checker = True

    # start the algo
    while (q.__len__() is not 0):
        # print("Start hai! Train hard to be the best!!! rather BEAST!!")
        # dequeue kar top node (with the smallest val)
        state_QT = heapq.heappop(q)

        # state string of the parent
        state_StringP = state_QT[1]

        # Agar pehle se closed me hai matlab (the path right now is the optimal) then dont visit or consider that node
        if(state_StringP in closedList):
            continue

        # Queue se nikalte hi closed list me daal do
        closedList.add(state_StringP)

        # get X and y (X --> row number and Y --> column number) of the parent state
        transient_vals = state_StringP.split(",")
        currX = int(transient_vals[1])  # Row Number of parent
        currY = int(transient_vals[0])  # Column Number of Parent
        # print(currX,"val of X",currY,"val of Y")

        # get the g value of parent (abhi parent tak ki g value ai h) --> isme we'll add the next action cost and the heuristic to get fn
        g_Valparent = state_g[state_StringP]
        # print(g_Valparent,"parent ki g val h")

        # Agar Goal state mil gai!
        if (state_StringP == goal_state):
            # print(state_g[goal_state],goal_state)
            addtoallpaths(pc_Dict,goal_state)
            checker = False
            break

        # ab sari child states explore kr upar ka row pehle then neeche ka row then right and left to the current cell
        if(currX-1>=0):

            if(currY-1>=0):

                # coordinates of the child
                childX = currX - 1
                childY = currY - 1

                # Elevation of Parent
                parent_Z = marsGrid[currX][currY]
                # Elevation of Child
                child_Z = marsGrid[childX][childY]

                # height Difference between them
                diff_Ht = abs(parent_Z - child_Z)

                # make the child state String
                child_Statestring = str(childY) + "," + str(childX)

                # f(n) for the child = g(n) + h(n) || This one is diagonal Movement
                f_n = g_Valparent + 14 + diff_Ht + heuristic(childX, childY, ts_X, ts_Y)

                if (child_Statestring not in openList and child_Statestring not in closedList and diff_Ht <= threshHold):
                    # print("Queue me add hai bruhhhhhhhhhh")
                    # I will add g for this state to the dictionary here
                    # get the actual cost to reach to this node
                    g_currState = g_Valparent + 14 + diff_Ht
                    # update the dicionary for the current Child Node
                    state_g[child_Statestring] = g_currState

                    # 1) Push In The Priority Queue
                    heapq.heappush(q, (f_n, child_Statestring))

                    # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                    openList.add(child_Statestring)

                    # 3) parent child dict update
                    pc_Dict[child_Statestring] = state_StringP

                    # 4) Store the value for f(n) in a dictionary for the given state
                    state_f[child_Statestring] = f_n

                elif (child_Statestring in openList and height_Difference(currX, currY, childX, childY) <= threshHold):
                    open_Gval = state_g[child_Statestring]
                    # g nikal le jo dalni h
                    g_currState = g_Valparent + 14 + diff_Ht

                    # ajao gn
                    # fn_pop = state_f[child_Statestring]
                    # if(f_n<fn_pop):
                    #     print("LODA LELE APNA MUHH ME")

                    if(g_currState<open_Gval):

                        # if the g value of the state in openlist is more than the new g val then push the new parameters
                        heapq.heappush(q,(f_n,child_Statestring))

                        # update the parent string as acha path mil gaya h than earlier
                        pc_Dict[child_Statestring] = state_StringP
                        # state and g val dictionay ko bhi update krde as better dist mil gaya h
                        state_g[child_Statestring] = g_currState
                        # update the f state dictionary
                        state_f[child_Statestring] = f_n
                        #safe side ke lie ye bhi krde
                        openList.add(child_Statestring)

            if (currY + 1 < W):

                # coordinates of the child
                childX = currX - 1
                childY = currY + 1

                # Elevation of Parent
                parent_Z = marsGrid[currX][currY]
                # Elevation of Child
                child_Z = marsGrid[childX][childY]

                # height Difference between them
                diff_Ht = abs(parent_Z - child_Z)

                # make the child state String
                child_Statestring = str(childY) + "," + str(childX)

                # f(n) for the child = g(n) + h(n) || This one is diagonal Movement
                f_n = g_Valparent + 14 + diff_Ht + heuristic(childX, childY, ts_X, ts_Y)

                if (child_Statestring not in openList and child_Statestring not in closedList and diff_Ht <= threshHold):
                    # print("Queue me add hai bruhhhhhhhhhh")
                    # I will add g for this state to the dictionary here
                    # get the actual cost to reach to this node
                    g_currState = g_Valparent + 14 + diff_Ht
                    # update the dicionary for the current Child Node
                    state_g[child_Statestring] = g_currState

                    # 1) Push In The Priority Queue
                    heapq.heappush(q, (f_n, child_Statestring))

                    # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                    openList.add(child_Statestring)

                    # 3) parent child dict update
                    pc_Dict[child_Statestring] = state_StringP

                    # 4) Store the value for f(n) in a dictionary for the given state
                    state_f[child_Statestring] = f_n

                elif (child_Statestring in openList and height_Difference(currX, currY, childX, childY) <= threshHold):
                    open_Gval = state_g[child_Statestring]
                    # g nikal le jo dalni h
                    g_currState = g_Valparent + 14 + diff_Ht
                    if (g_currState < open_Gval):
                        # if the g value of the state in openlist is more than the new g val then push the new parameters
                        heapq.heappush(q, (f_n, child_Statestring))

                        # update the parent string as acha path mil gaya h than earlier
                        pc_Dict[child_Statestring] = state_StringP
                        # state and g val dictionay ko bhi update krde as better dist mil gaya h
                        state_g[child_Statestring] = g_currState
                        # update the f state dictionary
                        state_f[child_Statestring] = f_n
                        # safe side ke lie ye bhi krde
                        openList.add(child_Statestring)


            childX = currX - 1
            childY = currY

            # Elevation of Parent
            parent_Z = marsGrid[currX][currY]
            # Elevation of Child
            child_Z = marsGrid[childX][childY]

            # height Difference between them
            diff_Ht = abs(parent_Z - child_Z)

            # make the child state String
            child_Statestring = str(childY) + "," + str(childX)

            # f(n) for the child = g(n) + h(n) || This one is diagonal Movement
            f_n = g_Valparent + 10 + diff_Ht + heuristic(childX, childY, ts_X, ts_Y)

            if (child_Statestring not in openList and child_Statestring not in closedList and diff_Ht <= threshHold):
                # print("Queue me add hai bruhhhhhhhhhh")
                # I will add g for this state to the dictionary here
                # get the actual cost to reach to this node
                g_currState = g_Valparent + 10 + diff_Ht
                # update the dicionary for the current Child Node
                state_g[child_Statestring] = g_currState

                # 1) Push In The Priority Queue
                heapq.heappush(q, (f_n, child_Statestring))

                # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                openList.add(child_Statestring)

                # 3) parent child dict update
                pc_Dict[child_Statestring] = state_StringP

                # 4) Store the value for f(n) in a dictionary for the given state
                state_f[child_Statestring] = f_n

            elif (child_Statestring in openList and height_Difference(currX, currY, childX, childY) <= threshHold):
                open_Gval = state_g[child_Statestring]
                # g nikal le jo dalni h
                g_currState = g_Valparent + 10 + diff_Ht
                if (g_currState < open_Gval):
                    # if the g value of the state in openlist is more than the new g val then push the new parameters
                    heapq.heappush(q, (f_n, child_Statestring))

                    # update the parent string as acha path mil gaya h than earlier
                    pc_Dict[child_Statestring] = state_StringP
                    # state and g val dictionay ko bhi update krde as better dist mil gaya h
                    state_g[child_Statestring] = g_currState
                    # update the f state dictionary
                    state_f[child_Statestring] = f_n
                    # safe side ke lie ye bhi krde
                    openList.add(child_Statestring)

        if (currX + 1 < H):

            if (currY - 1 >= 0):

                # coordinates of the child
                childX = currX + 1
                childY = currY - 1

                # Elevation of Parent
                parent_Z = marsGrid[currX][currY]
                # Elevation of Child
                child_Z = marsGrid[childX][childY]

                # height Difference between them
                diff_Ht = abs(parent_Z - child_Z)

                # make the child state String
                child_Statestring = str(childY) + "," + str(childX)

                # f(n) for the child = g(n) + h(n) || This one is diagonal Movement
                f_n = g_Valparent + 14 + diff_Ht + heuristic(childX, childY, ts_X, ts_Y)

                if (child_Statestring not in openList and child_Statestring not in closedList and diff_Ht <= threshHold):
                    # print("Queue me add hai bruhhhhhhhhhh")
                    # I will add g for this state to the dictionary here
                    # get the actual cost to reach to this node
                    g_currState = g_Valparent + 14 + diff_Ht
                    # update the dicionary for the current Child Node
                    state_g[child_Statestring] = g_currState

                    # 1) Push In The Priority Queue
                    heapq.heappush(q, (f_n, child_Statestring))

                    # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                    openList.add(child_Statestring)

                    # 3) parent child dict update
                    pc_Dict[child_Statestring] = state_StringP

                    # 4) Store the value for f(n) in a dictionary for the given state
                    state_f[child_Statestring] = f_n

                elif (child_Statestring in openList and height_Difference(currX, currY, childX, childY) <= threshHold):
                    open_Gval = state_g[child_Statestring]
                    # g nikal le jo dalni h
                    g_currState = g_Valparent + 14 + diff_Ht
                    if (g_currState < open_Gval):
                        # if the g value of the state in openlist is more than the new g val then push the new parameters
                        heapq.heappush(q, (f_n, child_Statestring))

                        # update the parent string as acha path mil gaya h than earlier
                        pc_Dict[child_Statestring] = state_StringP
                        # state and g val dictionay ko bhi update krde as better dist mil gaya h
                        state_g[child_Statestring] = g_currState
                        # update the f state dictionary
                        state_f[child_Statestring] = f_n
                        # safe side ke lie ye bhi krde
                        openList.add(child_Statestring)

            if (currY + 1 < W):

                # coordinates of the child
                childX = currX + 1
                childY = currY + 1

                # Elevation of Parent
                parent_Z = marsGrid[currX][currY]
                # Elevation of Child
                child_Z = marsGrid[childX][childY]

                # height Difference between them
                diff_Ht = abs(parent_Z - child_Z)

                # make the child state String
                child_Statestring = str(childY) + "," + str(childX)

                # f(n) for the child = g(n) + h(n) || This one is diagonal Movement
                f_n = g_Valparent + 14 + diff_Ht + heuristic(childX, childY, ts_X, ts_Y)

                if (child_Statestring not in openList and child_Statestring not in closedList and diff_Ht <= threshHold):
                    # print("Queue me add hai bruhhhhhhhhhh")
                    # I will add g for this state to the dictionary here
                    # get the actual cost to reach to this node
                    g_currState = g_Valparent + 14 + diff_Ht
                    # update the dicionary for the current Child Node
                    state_g[child_Statestring] = g_currState

                    # 1) Push In The Priority Queue
                    heapq.heappush(q, (f_n, child_Statestring))

                    # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                    openList.add(child_Statestring)

                    # 3) parent child dict update
                    pc_Dict[child_Statestring] = state_StringP

                    # 4) Store the value for f(n) in a dictionary for the given state
                    state_f[child_Statestring] = f_n

                elif (child_Statestring in openList and height_Difference(currX, currY, childX, childY) <= threshHold):
                    open_Gval = state_g[child_Statestring]
                    # g nikal le jo dalni h
                    g_currState = g_Valparent + 14 + diff_Ht
                    if (g_currState < open_Gval):
                        # if the g value of the state in openlist is more than the new g val then push the new parameters
                        heapq.heappush(q, (f_n, child_Statestring))

                        # update the parent string as acha path mil gaya h than earlier
                        pc_Dict[child_Statestring] = state_StringP
                        # state and g val dictionay ko bhi update krde as better dist mil gaya h
                        state_g[child_Statestring] = g_currState
                        # update the f state dictionary
                        state_f[child_Statestring] = f_n
                        # safe side ke lie ye bhi krde
                        openList.add(child_Statestring)

            childX = currX + 1
            childY = currY

            # Elevation of Parent
            parent_Z = marsGrid[currX][currY]
            # Elevation of Child
            child_Z = marsGrid[childX][childY]

            # height Difference between them
            diff_Ht = abs(parent_Z - child_Z)

            # make the child state String
            child_Statestring = str(childY) + "," + str(childX)

            # f(n) for the child = g(n) + h(n) || This one is diagonal Movement
            f_n = g_Valparent + 10 + diff_Ht + heuristic(childX, childY, ts_X, ts_Y)

            if (child_Statestring not in openList and child_Statestring not in closedList and diff_Ht <= threshHold):
                # print("Queue me add hai bruhhhhhhhhhh")
                # I will add g for this state to the dictionary here
                # get the actual cost to reach to this node
                g_currState = g_Valparent + 10 + diff_Ht
                # update the dicionary for the current Child Node
                state_g[child_Statestring] = g_currState

                # 1) Push In The Priority Queue
                heapq.heappush(q, (f_n, child_Statestring))

                # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                openList.add(child_Statestring)

                # 3) parent child dict update
                pc_Dict[child_Statestring] = state_StringP

                # 4) Store the value for f(n) in a dictionary for the given state
                state_f[child_Statestring] = f_n

            elif (child_Statestring in openList and height_Difference(currX, currY, childX, childY) <= threshHold):
                open_Gval = state_g[child_Statestring]
                # g nikal le jo dalni h
                g_currState = g_Valparent + 10 + diff_Ht
                if (g_currState < open_Gval):
                    # if the g value of the state in openlist is more than the new g val then push the new parameters
                    heapq.heappush(q, (f_n, child_Statestring))

                    # update the parent string as acha path mil gaya h than earlier
                    pc_Dict[child_Statestring] = state_StringP
                    # state and g val dictionay ko bhi update krde as better dist mil gaya h
                    state_g[child_Statestring] = g_currState
                    # update the f state dictionary
                    state_f[child_Statestring] = f_n
                    # safe side ke lie ye bhi krde
                    openList.add(child_Statestring)

        # LAST @ CASE#S YAHA HAI BAUANUA ----------------------------------->

        if (currY + 1 < W):

            # coordinates of the child
            childX = currX
            childY = currY + 1

            # Elevation of Parent
            parent_Z = marsGrid[currX][currY]
            # Elevation of Child
            child_Z = marsGrid[childX][childY]

            # height Difference between them
            diff_Ht = abs(parent_Z - child_Z)

            # make the child state String
            child_Statestring = str(childY) + "," + str(childX)

            # f(n) for the child = g(n) + h(n) || This one is diagonal Movement
            f_n = g_Valparent + 10 + diff_Ht + heuristic(childX, childY, ts_X, ts_Y)

            if (child_Statestring not in openList and child_Statestring not in closedList and diff_Ht <= threshHold):
                # print("Queue me add hai bruhhhhhhhhhh")
                # I will add g for this state to the dictionary here
                # get the actual cost to reach to this node
                g_currState = g_Valparent + 10 + diff_Ht
                # update the dicionary for the current Child Node
                state_g[child_Statestring] = g_currState

                # 1) Push In The Priority Queue
                heapq.heappush(q, (f_n, child_Statestring))

                # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                openList.add(child_Statestring)

                # 3) parent child dict update
                pc_Dict[child_Statestring] = state_StringP

                # 4) Store the value for f(n) in a dictionary for the given state
                state_f[child_Statestring] = f_n

            elif (child_Statestring in openList and height_Difference(currX, currY, childX, childY) <= threshHold):
                open_Gval = state_g[child_Statestring]
                # g nikal le jo dalni h
                g_currState = g_Valparent + 10 + diff_Ht
                if (g_currState < open_Gval):
                    # if the g value of the state in openlist is more than the new g val then push the new parameters
                    heapq.heappush(q, (f_n, child_Statestring))

                    # update the parent string as acha path mil gaya h than earlier
                    pc_Dict[child_Statestring] = state_StringP
                    # state and g val dictionay ko bhi update krde as better dist mil gaya h
                    state_g[child_Statestring] = g_currState
                    # update the f state dictionary
                    state_f[child_Statestring] = f_n
                    # safe side ke lie ye bhi krde
                    openList.add(child_Statestring)

        if (currY - 1 >=0):

            # coordinates of the child
            childX = currX
            childY = currY - 1

            # Elevation of Parent
            parent_Z = marsGrid[currX][currY]
            # Elevation of Child
            child_Z = marsGrid[childX][childY]

            # height Difference between them
            diff_Ht = abs(parent_Z - child_Z)

            # make the child state String
            child_Statestring = str(childY) + "," + str(childX)

            # f(n) for the child = g(n) + h(n) || This one is diagonal Movement
            f_n = g_Valparent + 10 + diff_Ht + heuristic(childX, childY, ts_X, ts_Y)

            if (child_Statestring not in openList and child_Statestring not in closedList and diff_Ht <= threshHold):
                # print("Queue me add hai bruhhhhhhhhhh")
                # I will add g for this state to the dictionary here
                # get the actual cost to reach to this node
                g_currState = g_Valparent + 10 + diff_Ht
                # update the dicionary for the current Child Node
                state_g[child_Statestring] = g_currState

                # 1) Push In The Priority Queue
                heapq.heappush(q, (f_n, child_Statestring))

                # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                openList.add(child_Statestring)

                # 3) parent child dict update
                pc_Dict[child_Statestring] = state_StringP

                # 4) Store the value for f(n) in a dictionary for the given state
                state_f[child_Statestring] = f_n

            elif (child_Statestring in openList and height_Difference(currX, currY, childX, childY) <= threshHold):
                open_Gval = state_g[child_Statestring]
                # g nikal le jo dalni h
                g_currState = g_Valparent + 10 + diff_Ht
                if (g_currState < open_Gval):
                    # if the g value of the state in openlist is more than the new g val then push the new parameters
                    heapq.heappush(q, (f_n, child_Statestring))

                    # update the parent string as acha path mil gaya h than earlier
                    pc_Dict[child_Statestring] = state_StringP
                    # state and g val dictionay ko bhi update krde as better dist mil gaya h
                    state_g[child_Statestring] = g_currState
                    # update the f state dictionary
                    state_f[child_Statestring] = f_n
                    # safe side ke lie ye bhi krde
                    openList.add(child_Statestring)

    if(checker):
        addtoallpaths(pc_Dict,goal_state)
    # print("yaha ana nhi chahie ")







def  a_Star(goal_state):
    # This is to store the value of g and state
    state_g = dict()

    # get the state string
    ss_Landing = str(landingY) + ',' + str(landingX)
    # print(ss_Landing,"landing site ye h")

    # get the first site for the state and it will have a g of  0
    state_g[ss_Landing] = 0

    # parent dict and open and closed lists
    # open list me vo states hongi jo queue me hongi
    openList = set()

    # closed list me vo states hongi jo visited ho chuki hongi
    closedList = set()

    # parent child ki dictionary - key hoga child and value hogi parent
    pc_Dict = {}

    # goal state  ke x an d y nikal ke rkhlete hai and remeber y pehle hai and then x hai input format me :(

    ts = goal_state.split(",")
    ts_X = int(ts[1])
    ts_Y = int(ts[0])
    # print(ts)

    # parent Child Dictionary Update ki!
    pc_Dict[ss_Landing] = "noParent"

    q = []

    # make a priority queue
    # priority queue me state node daal with all the info you need
    # structure of tuple jo priority queue me jaa rha h is (dist_till_now,state_of_Curr)

    initial_val = heuristic(landingX,landingY,ts_X,ts_Y)
    heapq.heappush(q, (initial_val, ss_Landing))
    state_g[ss_Landing] = 0

    # jaise hi queue me dala open me daal do us state ko
    openList.add(ss_Landing)


    # start the algo

    while (q.__len__() is not 0):
        # print("I have to work hard")

        # pop the least f(n) value element
        state_QT = heapq.heappop(q)

        # state string of the parent
        state_StringP = state_QT[1]
        # print(state_StringP)

        # Queue se nikalte hi closed list me daal do
        closedList.add(state_StringP)
        # print(closedList)

        # get X and y (X --> row number and Y --> column number) of the parent state
        transient_vals = state_StringP.split(",")
        currX = int(transient_vals[1])  # Row Number of parent
        currY = int(transient_vals[0])  # Column Number of Parent
        # print(currX,"val of X",currY,"val of Y")

        # get the g value of parent
        g_Valparent = state_g[state_StringP]
        # print(g_Valparent,"parent ki g val h")

        # Agar Goal state mil gai!
        if (state_StringP == goal_state):
            print(goal_state)
            print(pc_Dict)
            break

        # 1st check
        if(currX-1 >= 0):

            if(currY - 1 >= 0):
                # coordinates of the child
                childX = currX - 1
                childY = currY - 1

                # Elevation of Parent
                parent_Z = marsGrid[currX][currY]
                # Elevation of Child
                child_Z = marsGrid[childX][childY]

                # height Difference between them
                diff_Ht = abs(parent_Z-child_Z)

                # make the child state String
                child_Statestring = str(childY)+","+str(childX)

                # f(n) for the child = g(n) + h(n) || This one is diagonal Movement
                f_n = g_Valparent + 14 + diff_Ht + heuristic(childX,childY,ts_X,ts_Y)

                if(child_Statestring not in openList and child_Statestring not in closedList and diff_Ht <= threshHold):
                    # print("Queue me add hai bruhhhhhhhhhh")
                    # I will add g for this state to the dictionary here
                    # get the actual cost to reach to this node
                    g_currState = g_Valparent + 14 + diff_Ht
                    # update the dicionary for the current Child Node
                    state_g[child_Statestring] = g_currState

                    # 1) Push In The Priority Queue
                    heapq.heappush(q, (f_n, child_Statestring))

                    # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                    openList.add(child_Statestring)

                    # 3) parent child dict update
                    pc_Dict[child_Statestring] = state_StringP


                elif (child_Statestring in openList and diff_Ht<=threshHold):

                    for data in q:

                        q_Presentval = data[1]

                        if(q_Presentval == child_Statestring):
                            fn_Encounterednode = data[0]

                            if(fn_Encounterednode>f_n):
                                q.remove(data)
                                q.append((f_n,child_Statestring))
                                pc_Dict[child_Statestring] = state_StringP
                                state_g[child_Statestring] = g_currState
                                heapq.heapify(q)
                                break

            if (currY + 1 < W):
                # coordinates of the child
                childX = currX - 1
                childY = currY + 1

                # Elevation of Parent
                parent_Z = marsGrid[currX][currY]
                # Elevation of Child
                child_Z = marsGrid[childX][childY]

                # height Difference between them
                diff_Ht = abs(parent_Z - child_Z)

                # make the child state String
                child_Statestring = str(childY) + "," + str(childX)

                # f(n) for the child = g(n) + h(n) || This one is diagonal Movement
                f_n = g_Valparent + 14 + diff_Ht + heuristic(childX, childY, ts_X, ts_Y)

                if (child_Statestring not in openList and child_Statestring not in closedList and diff_Ht <= threshHold):
                    # print("Queue me add hai bruhhhhhhhhhh")
                    # I will add g for this state to the dictionary here
                    # get the actual cost to reach to this node
                    g_currState = g_Valparent + 14 + diff_Ht
                    # update the dicionary for the current Child Node
                    state_g[child_Statestring] = g_currState

                    # 1) Push In The Priority Queue
                    heapq.heappush(q, (f_n, child_Statestring))

                    # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                    openList.add(child_Statestring)

                    # 3) parent child dict update
                    pc_Dict[child_Statestring] = state_StringP


                elif (child_Statestring in openList and diff_Ht <= threshHold):

                    for data in q:

                        q_Presentval = data[1]

                        if (q_Presentval == child_Statestring):
                            fn_Encounterednode = data[0]

                            if (fn_Encounterednode > f_n):
                                q.remove(data)
                                q.append((f_n, child_Statestring))
                                pc_Dict[child_Statestring] = state_StringP
                                state_g[child_Statestring] = g_currState
                                heapq.heapify(q)
                                break

            # last vala case h

            childX = currX - 1
            childY = currY

            # Elevation of Parent
            parent_Z = marsGrid[currX][currY]
            # Elevation of Child
            child_Z = marsGrid[childX][childY]

            # height Difference between them
            diff_Ht = abs(parent_Z - child_Z)

            # make the child state String
            child_Statestring = str(childY) + "," + str(childX)

            # f(n) for the child = g(n) + h(n) || This one is diagonal Movement
            f_n = g_Valparent + 10 + diff_Ht + heuristic(childX, childY, ts_X, ts_Y)

            if (child_Statestring not in openList and child_Statestring not in closedList and diff_Ht <= threshHold):
                # print("Queue me add hai bruhhhhhhhhhh")
                # I will add g for this state to the dictionary here
                # get the actual cost to reach to this node
                g_currState = g_Valparent + 10 + diff_Ht
                # update the dicionary for the current Child Node
                state_g[child_Statestring] = g_currState

                # 1) Push In The Priority Queue
                heapq.heappush(q, (f_n, child_Statestring))

                # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                openList.add(child_Statestring)

                # 3) parent child dict update
                pc_Dict[child_Statestring] = state_StringP


            elif (child_Statestring in openList and diff_Ht <= threshHold):

                for data in q:

                    q_Presentval = data[1]

                    if (q_Presentval == child_Statestring):
                        fn_Encounterednode = data[0]

                        if (fn_Encounterednode > f_n):
                            q.remove(data)
                            q.append((f_n, child_Statestring))
                            pc_Dict[child_Statestring] = state_StringP
                            state_g[child_Statestring] = g_currState
                            heapq.heapify(q)
                            break

        # first vala check khatam SECOND CASE NEECHE SHURU HAI TO DHYAN RAKHNA -------------------------->>>>>>>

        if (currX + 1 < H):

            if (currY - 1 >= 0):
                # coordinates of the child
                childX = currX + 1
                childY = currY - 1

                # Elevation of Parent
                parent_Z = marsGrid[currX][currY]
                # Elevation of Child
                child_Z = marsGrid[childX][childY]

                # height Difference between them
                diff_Ht = abs(parent_Z - child_Z)

                # make the child state String
                child_Statestring = str(childY) + "," + str(childX)

                # f(n) for the child = g(n) + h(n) || This one is diagonal Movement
                f_n = g_Valparent + 14 + diff_Ht + heuristic(childX, childY, ts_X, ts_Y)

                if (child_Statestring not in openList and child_Statestring not in closedList and diff_Ht <= threshHold):
                    # print("Queue me add hai bruhhhhhhhhhh")
                    # I will add g for this state to the dictionary here
                    # get the actual cost to reach to this node
                    g_currState = g_Valparent + 14 + diff_Ht
                    # update the dicionary for the current Child Node
                    state_g[child_Statestring] = g_currState

                    # 1) Push In The Priority Queue
                    heapq.heappush(q, (f_n, child_Statestring))

                    # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                    openList.add(child_Statestring)

                    # 3) parent child dict update
                    pc_Dict[child_Statestring] = state_StringP


                elif (child_Statestring in openList and diff_Ht <= threshHold):

                    for data in q:

                        q_Presentval = data[1]

                        if (q_Presentval == child_Statestring):
                            fn_Encounterednode = data[0]

                            if (fn_Encounterednode > f_n):
                                q.remove(data)
                                q.append((f_n, child_Statestring))
                                pc_Dict[child_Statestring] = state_StringP
                                state_g[child_Statestring] = g_currState
                                heapq.heapify(q)
                                break

            if (currY + 1 < W):
                # coordinates of the child
                childX = currX + 1
                childY = currY + 1

                # Elevation of Parent
                parent_Z = marsGrid[currX][currY]
                # Elevation of Child
                child_Z = marsGrid[childX][childY]

                # height Difference between them
                diff_Ht = abs(parent_Z - child_Z)

                # make the child state String
                child_Statestring = str(childY) + "," + str(childX)

                # f(n) for the child = g(n) + h(n) || This one is diagonal Movement
                f_n = g_Valparent + 14 + diff_Ht + heuristic(childX, childY, ts_X, ts_Y)

                if (child_Statestring not in openList and child_Statestring not in closedList and diff_Ht <= threshHold):
                    # print("Queue me add hai bruhhhhhhhhhh")
                    # I will add g for this state to the dictionary here
                    # get the actual cost to reach to this node
                    g_currState = g_Valparent + 14 + diff_Ht
                    # update the dicionary for the current Child Node
                    state_g[child_Statestring] = g_currState

                    # 1) Push In The Priority Queue
                    heapq.heappush(q, (f_n, child_Statestring))

                    # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                    openList.add(child_Statestring)

                    # 3) parent child dict update
                    pc_Dict[child_Statestring] = state_StringP


                elif (child_Statestring in openList and diff_Ht <= threshHold):

                    for data in q:

                        q_Presentval = data[1]

                        if (q_Presentval == child_Statestring):
                            fn_Encounterednode = data[0]

                            if (fn_Encounterednode > f_n):
                                q.remove(data)
                                q.append((f_n, child_Statestring))
                                pc_Dict[child_Statestring] = state_StringP
                                state_g[child_Statestring] = g_currState
                                heapq.heapify(q)
                                break

            # last vala case h

            childX = currX + 1
            childY = currY

            # Elevation of Parent
            parent_Z = marsGrid[currX][currY]
            # Elevation of Child
            child_Z = marsGrid[childX][childY]

            # height Difference between them
            diff_Ht = abs(parent_Z - child_Z)

            # make the child state String
            child_Statestring = str(childY) + "," + str(childX)

            # f(n) for the child = g(n) + h(n) || This one is diagonal Movement
            f_n = g_Valparent + 10 + diff_Ht + heuristic(childX, childY, ts_X, ts_Y)

            if (child_Statestring not in openList and child_Statestring not in closedList and diff_Ht <= threshHold):
                # print("Queue me add hai bruhhhhhhhhhh")
                # I will add g for this state to the dictionary here
                # get the actual cost to reach to this node
                g_currState = g_Valparent + 10 + diff_Ht
                # update the dicionary for the current Child Node
                state_g[child_Statestring] = g_currState

                # 1) Push In The Priority Queue
                heapq.heappush(q, (f_n, child_Statestring))

                # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                openList.add(child_Statestring)

                # 3) parent child dict update
                pc_Dict[child_Statestring] = state_StringP


            elif (child_Statestring in openList and diff_Ht <= threshHold):

                for data in q:

                    q_Presentval = data[1]

                    if (q_Presentval == child_Statestring):
                        fn_Encounterednode = data[0]

                        if (fn_Encounterednode > f_n):
                            q.remove(data)
                            q.append((f_n, child_Statestring))
                            pc_Dict[child_Statestring] = state_StringP
                            state_g[child_Statestring] = g_currState
                            heapq.heapify(q)
                            break


        # last 2 CASES yaha hai

        # Part no 1

        if(currY-1>=0):

            childX = currX
            childY = currY-1

            # Elevation of Parent
            parent_Z = marsGrid[currX][currY]
            # Elevation of Child
            child_Z = marsGrid[childX][childY]

            # height Difference between them
            diff_Ht = abs(parent_Z - child_Z)

            # make the child state String
            child_Statestring = str(childY) + "," + str(childX)

            # f(n) for the child = g(n) + h(n) || This one is diagonal Movement
            f_n = g_Valparent + 10 + diff_Ht + heuristic(childX, childY, ts_X, ts_Y)

            if (child_Statestring not in openList and child_Statestring not in closedList and diff_Ht <= threshHold):
                # print("Queue me add hai bruhhhhhhhhhh")
                # I will add g for this state to the dictionary here
                # get the actual cost to reach to this node
                g_currState = g_Valparent + 10 + diff_Ht
                # update the dicionary for the current Child Node
                state_g[child_Statestring] = g_currState

                # 1) Push In The Priority Queue
                heapq.heappush(q, (f_n, child_Statestring))

                # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                openList.add(child_Statestring)

                # 3) parent child dict update
                pc_Dict[child_Statestring] = state_StringP


            elif (child_Statestring in openList and diff_Ht <= threshHold):

                for data in q:

                    q_Presentval = data[1]

                    if (q_Presentval == child_Statestring):
                        fn_Encounterednode = data[0]

                        if (fn_Encounterednode > f_n):
                            q.remove(data)
                            q.append((f_n, child_Statestring))
                            pc_Dict[child_Statestring] = state_StringP
                            state_g[child_Statestring] = g_currState
                            heapq.heapify(q)
                            break


        if (currY+1<W):

            childX = currX
            childY = currY + 1

            # Elevation of Parent
            parent_Z = marsGrid[currX][currY]
            # Elevation of Child
            child_Z = marsGrid[childX][childY]

            # height Difference between them
            diff_Ht = abs(parent_Z - child_Z)

            # make the child state String
            child_Statestring = str(childY) + "," + str(childX)

            # f(n) for the child = g(n) + h(n) || This one is diagonal Movement
            f_n = g_Valparent + 10 + diff_Ht + heuristic(childX, childY, ts_X, ts_Y)

            if (child_Statestring not in openList and child_Statestring not in closedList and diff_Ht <= threshHold):
                # print("Queue me add hai bruhhhhhhhhhh")
                # I will add g for this state to the dictionary here
                # get the actual cost to reach to this node
                g_currState = g_Valparent + 10 + diff_Ht
                # update the dicionary for the current Child Node
                state_g[child_Statestring] = g_currState

                # 1) Push In The Priority Queue
                heapq.heappush(q, (f_n, child_Statestring))

                # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                openList.add(child_Statestring)

                # 3) parent child dict update
                pc_Dict[child_Statestring] = state_StringP


            elif (child_Statestring in openList and diff_Ht <= threshHold):

                for data in q:

                    q_Presentval = data[1]

                    if (q_Presentval == child_Statestring):
                        fn_Encounterednode = data[0]

                        if (fn_Encounterednode > f_n):
                            q.remove(data)
                            q.append((f_n, child_Statestring))
                            pc_Dict[child_Statestring] = state_StringP
                            state_g[child_Statestring] = g_currState
                            heapq.heapify(q)
                            break




# [[(3, 0), (3, 1), (3, 2), (2, 3), (1, 3), (0, 3)]]
# 0,3 1,3 2,3 3,2 3,1 3,0

def print_forUCS2(pc_Dict):
    # listToPrintTarget
    # print(listToPrintTarget)
    for targets in listToPrintTarget:
        ansli = []
        if(targets not in pc_Dict.keys()):
            ansli.append("FAIL")
            ansList.append(ansli)
            continue
        start = targets
        ansli.append(start)
        start = pc_Dict[start]
        while(start is not "startingPoint"):
            ansli.append(start)
            start = pc_Dict[start]
            # ansli.append(start)

        ansli.reverse()
        ansList.append(ansli)

    # print("YE HAI ANSWER",ansList)

def printtocheck(gpath):
    print(listToPrintTarget,"ye order match krlio kaka")
    for stat in listToPrintTarget:
        if (stat not in gpath.keys()):
            print(stat,"FAIL")
        else:
            print(gpath[stat],stat)


def UCS2new():
    print("Start")

    # open list me vo states hongi jo queue me hongi
    openList = set()

    # closed list me vo states hongi jo visited ho chuki hongi
    closedList = set()

    # parent child ki dictionary - key hoga child and value hogi parent
    pc_Dict = {}

    # State 0,3 means it has landed on 3,0
    landingSite_State = str(landingY)+","+str(landingX)

    # state g dictionary
    state_g = dict()

    # parent Child Dictionary Update ki!
    pc_Dict[landingSite_State] = "startingPoint"

    q = []

    # make a priority queue
    #priority queue me state node daal with all the info you need
    # structure of tuple jo priority queue me jaa rha h is (dist_till_now,state_of_Curr)
    heapq.heappush(q,(0,landingSite_State))

    # update the g for the state
    state_g[landingSite_State] = 0

    # jaise hi queue me dala open me daal do us state ko
    openList.add(landingSite_State)



    while (q.__len__() is not 0):
        # print("Start")

        # This is the state tuple of (g,state_String)
        state_Qtop = heapq.heappop(q)

        # g_Parent --> abhi tak jo g hai
        g_Parent = state_Qtop[0]

        # state_String of parent
        state_Parentstring = state_Qtop[1]

        # print(state_Parentstring,"Ye hai popped element ki string")

        #agar closed state me hai to uss se better ans ni mil sakta as no -ve cycles
        if(state_Parentstring in closedList):
            continue

        # ab pop hogya hai to closed list me add krdo
        closedList.add(state_Parentstring)


        if(state_Parentstring in dupTargetsiteset):
            dupTargetsiteset.remove(state_Parentstring)
            # print(state_Parentstring)
            # print(state_g[state_Parentstring])
            # print(state_g[state_Parentstring],state_Parentstring)
            # print(len(dupTargetsiteset),dupTargetsiteset)

            if (len(dupTargetsiteset) == 0):
                # print(len(dupTargetsiteset), "Length of duptarget sites when goal achieved")
                # print_Path_BFS(pc_Dict)
                # print("ate hue")
                # print_forUCS2(pc_Dict)

                # print(pc_Dict)
                break

        coord = state_Parentstring.split(',')

        # Row Number
        currX = int(coord[1])
        # Column number
        currY = int(coord[0])

        # distance till now
        dist_Tn = int(g_Parent)

        # upar vali row ka saea kaam kaaj

        if(currX-1>=0):

            if(currY-1>=0):

                locX = currX - 1
                locY = currY - 1
                # next child ke coordinated kre hai ye

                # next child's state
                next_Childstate = str(locY) + "," + str(locX)

                # new distance for this node (g)
                g = dist_Tn + 14
                # distance to be added in this case is 14 (PATH-COST CHILD)

                # if no node in open or closed has child's state
                if (next_Childstate not in closedList and next_Childstate not in openList and height_Difference(currX,currY,locX,locY) <= threshHold):

                    # 1) Push In The Priority Queue
                    heapq.heappush(q, (g, next_Childstate))

                    # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                    openList.add(next_Childstate)

                    # 3) parent child dict update
                    pc_Dict[next_Childstate] = state_Parentstring

                    # 4) update the dictionary of g and state so that I get to know about it
                    state_g[next_Childstate] = g

                elif (next_Childstate in openList and height_Difference(currX, currY, locX, locY) <= threshHold):
                    open_Gval = state_g[next_Childstate]
                    if(g<open_Gval):

                        # if the g value of the state in openlist is more than the new g val then push the new parameters
                        heapq.heappush(q,(g,next_Childstate))
                        # update the parent string as acha path mil gaya h than earlier
                        pc_Dict[next_Childstate] = state_Parentstring
                        # state and g val dictionay ko bhi update krde as better dist mil gaya h
                        state_g[next_Childstate] = g
                        #safe side ke lie ye bhi krde
                        openList.add(next_Childstate)

            if (currY + 1 < W):

                locX = currX - 1
                locY = currY + 1
                # next child ke coordinated kre hai ye

                # next child's state
                next_Childstate = str(locY) + "," + str(locX)

                # new distance for this node (g)
                g = dist_Tn + 14
                # distance to be added in this case is 14 (PATH-COST CHILD)

                # if no node in open or closed has child's state
                if (next_Childstate not in closedList and next_Childstate not in openList and height_Difference(currX,currY,locX,locY) <= threshHold):

                    # 1) Push In The Priority Queue
                    heapq.heappush(q, (g, next_Childstate))

                    # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                    openList.add(next_Childstate)

                    # 3) parent child dict update
                    pc_Dict[next_Childstate] = state_Parentstring

                    # 4) update the dictionary of g and state so that I get to know about it
                    state_g[next_Childstate] = g

                elif (next_Childstate in openList and height_Difference(currX, currY, locX, locY) <= threshHold):
                    open_Gval = state_g[next_Childstate]
                    # abhi currently open me jo g ki value hai for the state (Child state)
                    if (g < open_Gval):
                        # if the g value of the state in openlist is more than the new g val then push the new parameters
                        heapq.heappush(q,(g, next_Childstate))
                        # update the parent string as acha path mil gaya h than earlier
                        pc_Dict[next_Childstate] = state_Parentstring
                        # state and g val dictionay ko bhi update krde as better dist mil gaya h
                        state_g[next_Childstate] = g
                        # safe side ke lie ye bhi krde
                        openList.add(next_Childstate)

            locX = currX - 1
            locY = currY
            # next child ke coordinated kre hai ye

            # next child's state
            next_Childstate = str(locY) + "," + str(locX)

            # new distance for this node (g)
            g = dist_Tn + 10
            # distance to be added in this case is 14 (PATH-COST CHILD)

            # if no node in open or closed has child's state
            if (next_Childstate not in closedList and next_Childstate not in openList and height_Difference(currX,currY,locX,locY) <= threshHold):

                # 1) Push In The Priority Queue
                heapq.heappush(q, (g, next_Childstate))

                # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                openList.add(next_Childstate)

                # 3) parent child dict update
                pc_Dict[next_Childstate] = state_Parentstring

                # 4) update the dictionary of g and state so that I get to know about it
                state_g[next_Childstate] = g

            elif (next_Childstate in openList and height_Difference(currX, currY, locX, locY) <= threshHold):
                open_Gval = state_g[next_Childstate]
                # abhi currently open me jo g ki value hai for the state (Child state)
                if (g < open_Gval):
                    # if the g value of the state in openlist is more than the new g val then push the new parameters
                    heapq.heappush(q,(g, next_Childstate))
                    # update the parent string as acha path mil gaya h than earlier
                    pc_Dict[next_Childstate] = state_Parentstring
                    # state and g val dictionay ko bhi update krde as better dist mil gaya h
                    state_g[next_Childstate] = g
                    # safe side ke lie ye bhi krde
                    openList.add(next_Childstate)

        # neeche vali row ka saara kaam kaaaj karna hai bro -------->

        if (currX + 1 < H):

            if (currY - 1 >= 0):

                locX = currX + 1
                locY = currY - 1
                # next child ke coordinated kre hai ye

                # next child's state
                next_Childstate = str(locY) + "," + str(locX)

                # new distance for this node (g)
                g = dist_Tn + 14
                # distance to be added in this case is 14 (PATH-COST CHILD)

                # if no node in open or closed has child's state
                if (next_Childstate not in closedList and next_Childstate not in openList and height_Difference(currX,currY,locX,locY) <= threshHold):

                    # 1) Push In The Priority Queue
                    heapq.heappush(q, (g, next_Childstate))

                    # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                    openList.add(next_Childstate)

                    # 3) parent child dict update
                    pc_Dict[next_Childstate] = state_Parentstring

                    # 4) update the dictionary of g and state so that I get to know about it
                    state_g[next_Childstate] = g

                elif (next_Childstate in openList and height_Difference(currX, currY, locX, locY) <= threshHold):
                    open_Gval = state_g[next_Childstate]
                    if (g < open_Gval):
                        # if the g value of the state in openlist is more than the new g val then push the new parameters
                        heapq.heappush(q,(g, next_Childstate))
                        # update the parent string as acha path mil gaya h than earlier
                        pc_Dict[next_Childstate] = state_Parentstring
                        # state and g val dictionay ko bhi update krde as better dist mil gaya h
                        state_g[next_Childstate] = g
                        # safe side ke lie ye bhi krde
                        openList.add(next_Childstate)

            if (currY + 1 < W):

                locX = currX + 1
                locY = currY + 1
                # next child ke coordinated kre hai ye

                # next child's state
                next_Childstate = str(locY) + "," + str(locX)

                # new distance for this node (g)
                g = dist_Tn + 14
                # distance to be added in this case is 14 (PATH-COST CHILD)

                # if no node in open or closed has child's state
                if (next_Childstate not in closedList and next_Childstate not in openList and height_Difference(currX,currY,locX,locY) <= threshHold):

                    # 1) Push In The Priority Queue
                    heapq.heappush(q, (g, next_Childstate))

                    # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                    openList.add(next_Childstate)

                    # 3) parent child dict update
                    pc_Dict[next_Childstate] = state_Parentstring

                    # 4) update the dictionary of g and state so that I get to know about it
                    state_g[next_Childstate] = g

                elif (next_Childstate in openList and height_Difference(currX, currY, locX, locY) <= threshHold):
                    open_Gval = state_g[next_Childstate]
                    # abhi currently open me jo g ki value hai for the state (Child state)
                    if (g < open_Gval):
                        # if the g value of the state in openlist is more than the new g val then push the new parameters
                        heapq.heappush(q,(g, next_Childstate))
                        # update the parent string as acha path mil gaya h than earlier
                        pc_Dict[next_Childstate] = state_Parentstring
                        # state and g val dictionay ko bhi update krde as better dist mil gaya h
                        state_g[next_Childstate] = g
                        # safe side ke lie ye bhi krde
                        openList.add(next_Childstate)

            locX = currX + 1
            locY = currY
            # next child ke coordinated kre hai ye

            # next child's state
            next_Childstate = str(locY) + "," + str(locX)

            # new distance for this node (g)
            g = dist_Tn + 10
            # distance to be added in this case is 14 (PATH-COST CHILD)

            # if no node in open or closed has child's state
            if (next_Childstate not in closedList and next_Childstate not in openList and height_Difference(currX,currY,locX,locY) <= threshHold):

                # 1) Push In The Priority Queue
                heapq.heappush(q, (g, next_Childstate))

                # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                openList.add(next_Childstate)

                # 3) parent child dict update
                pc_Dict[next_Childstate] = state_Parentstring

                # 4) update the dictionary of g and state so that I get to know about it
                state_g[next_Childstate] = g

            elif (next_Childstate in openList and height_Difference(currX, currY, locX, locY) <= threshHold):
                open_Gval = state_g[next_Childstate]
                # abhi currently open me jo g ki value hai for the state (Child state)
                if (g < open_Gval):
                    # if the g value of the state in openlist is more than the new g val then push the new parameters
                    heapq.heappush(q,(g, next_Childstate))
                    # update the parent string as acha path mil gaya h than earlier
                    pc_Dict[next_Childstate] = state_Parentstring
                    # state and g val dictionay ko bhi update krde as better dist mil gaya h
                    state_g[next_Childstate] = g
                    # safe side ke lie ye bhi krde
                    openList.add(next_Childstate)

        # Last 2 cases jo bache h!---------->

        if (currY - 1 >=0):

            locX = currX
            locY = currY - 1
            # next child ke coordinated kre hai ye

            # next child's state
            next_Childstate = str(locY) + "," + str(locX)

            # new distance for this node (g)
            g = dist_Tn + 10
            # distance to be added in this case is 14 (PATH-COST CHILD)

            # if no node in open or closed has child's state
            if (next_Childstate not in closedList and next_Childstate not in openList and height_Difference(currX,currY,locX,locY) <= threshHold):

                # 1) Push In The Priority Queue
                heapq.heappush(q, (g, next_Childstate))

                # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                openList.add(next_Childstate)

                # 3) parent child dict update
                pc_Dict[next_Childstate] = state_Parentstring

                # 4) update the dictionary of g and state so that I get to know about it
                state_g[next_Childstate] = g

            elif (next_Childstate in openList and height_Difference(currX, currY, locX, locY) <= threshHold):
                open_Gval = state_g[next_Childstate]
                # abhi currently open me jo g ki value hai for the state (Child state)
                if (g < open_Gval):
                    # if the g value of the state in openlist is more than the new g val then push the new parameters
                    heapq.heappush(q,(g, next_Childstate))
                    # update the parent string as acha path mil gaya h than earlier
                    pc_Dict[next_Childstate] = state_Parentstring
                    # state and g val dictionay ko bhi update krde as better dist mil gaya h
                    state_g[next_Childstate] = g
                    # safe side ke lie ye bhi krde
                    openList.add(next_Childstate)


        if (currY + 1 <W):

            locX = currX
            locY = currY + 1
            # next child ke coordinated kre hai ye

            # next child's state
            next_Childstate = str(locY) + "," + str(locX)

            # new distance for this node (g)
            g = dist_Tn + 10
            # distance to be added in this case is 14 (PATH-COST CHILD)

            # if no node in open or closed has child's state
            if (next_Childstate not in closedList and next_Childstate not in openList and height_Difference(currX,currY,locX,locY) <= threshHold):

                # 1) Push In The Priority Queue
                heapq.heappush(q, (g, next_Childstate))

                # 2) Add It In The Set Of Open (Ki vo Queue Me hai)
                openList.add(next_Childstate)

                # 3) parent child dict update
                pc_Dict[next_Childstate] = state_Parentstring

                # 4) update the dictionary of g and state so that I get to know about it
                state_g[next_Childstate] = g

            elif (next_Childstate in openList and height_Difference(currX, currY, locX, locY) <= threshHold):
                open_Gval = state_g[next_Childstate]
                # abhi currently open me jo g ki value hai for the state (Child state)
                if (g < open_Gval):
                    # if the g value of the state in openlist is more than the new g val then push the new parameters
                    heapq.heappush(q,(g, next_Childstate))
                    # update the parent string as acha path mil gaya h than earlier
                    pc_Dict[next_Childstate] = state_Parentstring
                    # state and g val dictionay ko bhi update krde as better dist mil gaya h
                    state_g[next_Childstate] = g
                    # safe side ke lie ye bhi krde
                    openList.add(next_Childstate)


    # printtocheck(state_g)
    # print("Bhoshandike")
    print_forUCS2(pc_Dict)






# BFS2
# UCS2new

def file_writer(main_print):
    # print("bhosandike")
    iceland = ""
    for path in main_print:
        for point in path:
            iceland+=point
            iceland+=" "
        iceland += "\n"

    # filo = open("testing.txt", "w")
    # print("SOJA")
    with open("output.txt","w") as filo:
        filo.write(iceland)


def callTomainSearch():
    # if(searchType  == "BFS"):
    # print(searchType)
    if(searchType == "A*"):
        # print("A* and len of dup",len(dupTargetsite))
        for sit in listToPrintTarget:
            atsar2(sit)
        # print("bhai chud rha h kya code?", allpathsforAstar)
        file_writer(allpathsforAstar)

    # print("bhai chud rha h kya code?",allpathsforAstar)
    # now I have the path in a list of list for A*

    # filo = open("testing.txt","w")
    # filo.write(allpathsforAstar)

    if (searchType == "UCS"):
        # print("UCS AYA ")
        UCS2new()
        file_writer(ansList)
        # print(ansList, "Ye hai UCS KA")

    if (searchType == "BFS"):
        # print("BFS")
        BFS2()
        file_writer(BFSkapathBro)
        # print(BFSkapathBro, "BFS ka Path hai")

    # print(BFSkapathBro,"BFS ka Path hai")
    #  ye path bfs ka hai
    # print(ansList,"Ye hai UCS KA")

    end_time = time.time()
    print(end_time-start_time,"end time h ")


callTomainSearch()
# BFS2("98,997")
