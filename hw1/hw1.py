import collections
import sys
import queue

iddfsnodes = 0


#b =1 = right
class node():
    def __init__(self, lc, lw, rc, rw, b, parent, action, depth):
        self.lc = lc
        self.rc = rc
        self.lw = lw
        self.rw = rw
        self.b = b
        self.depth = depth
        self.state = tuple([self.lc] + [self.lw] + [self.rc] + [self.rw] + [self.b])
        self.parent = parent
        self.action = action
        self.key = int(rc) + int(rw) + int(b)
        self.cost = int(depth) + (int(rc) + int(rw) - int(b))
    def __lt__(self, other):
        return self.cost < other.cost



def getnode(filename):
    f = open(filename,'r')
    line1 = f.readline()
    line1 = line1.split(',')
    line2 = f.readline()
    line2 = line2.split(',')
    new_node = node(line1[0],line1[1],line2[0],line2[1],line2[2].rstrip("\n"), None, None, str(0))
    return new_node

def validation(currnode,chiken, wolf):
    rc = int(currnode.rc)
   
    rw = int(currnode.rw)
    
    lc = int(currnode.lc)
    
    lw = int(currnode.lw)
  
    b = int(currnode.b)

    dep = int(currnode.depth)

    if b == 1:
        if chiken <= rc and wolf <= rw: 
            if ((rc-chiken > 0) and (rc - chiken) >= (rw - wolf)):
                if ((lc+chiken > 0) and (lc + chiken) >= (lw + wolf)):
                   
                    return node(str(lc + chiken), str(lw + wolf), str(rc - chiken), str(rw - wolf), str(0), currnode, tuple([chiken] + [wolf] + [b]), str(dep+1))
                elif (lc+chiken == 0):
             
                    return node(str(lc + chiken), str(lw + wolf), str(rc - chiken), str(rw - wolf), str(0), currnode, tuple([chiken] + [wolf] + [b]), str(dep+1))


            elif (rc-chiken == 0):
                if ((lc+chiken > 0) and (lc + chiken) >= (lw + wolf)):
                   
                    return node(str(lc + chiken), str(lw + wolf), str(rc - chiken), str(rw - wolf), str(0), currnode, tuple([chiken] + [wolf] + [b]), str(dep+1))
                elif (lc+chiken == 0):
                
                    return node(str(lc + chiken), str(lw + wolf), str(rc - chiken), str(rw - wolf), str(0), currnode, tuple([chiken] + [wolf] + [b]), str(dep+1))


    if b == 0:
        if chiken <= lc and wolf <= lw:
            if ((lc-chiken > 0) and (lc - chiken) >= (lw - wolf)):
                if ((rc+chiken > 0) and (rc + chiken) >= (rw + wolf)):
                   
                    return node(str(lc - chiken), str(lw - wolf), str(rc + chiken), str(rw + wolf), str(1), currnode, tuple([chiken] + [wolf] + [b]), str(dep+1))
                elif (rc+chiken == 0):
                  
                    return node(str(lc - chiken), str(lw - wolf), str(rc + chiken), str(rw + wolf), str(1), currnode, tuple([chiken] + [wolf] + [b]), str(dep+1))
            
            elif (lc-chiken == 0):
                if ((rc+chiken > 0) and (rc + chiken) >= (rw + wolf)):
                   
                    return node(str(lc - chiken), str(lw - wolf), str(rc + chiken), str(rw + wolf), str(1), currnode, tuple([chiken] + [wolf] + [b]), str(dep+1))
                elif (rc+chiken == 0):
                 
                    return node(str(lc - chiken), str(lw - wolf), str(rc + chiken), str(rw + wolf), str(1), currnode, tuple([chiken] + [wolf] + [b]), str(dep+1))


def expand(currnode):
    re_states = collections.deque()

    if validation(currnode, 1, 0):
        re_states.append(validation(currnode, 1, 0)) 

  
    if validation(currnode, 2, 0):
        re_states.append(validation(currnode, 2, 0))
    
   
 
    if validation(currnode, 0, 1):

        re_states.append(validation(currnode, 0, 1))
   
    if validation(currnode, 1, 1):
       
        re_states.append(validation(currnode, 1, 1))
    

    if validation(currnode, 0, 2):

        re_states.append(validation(currnode, 0, 2))
  

    return re_states

    
def getresult(curr):
    result = collections.deque()
    while curr.parent:
        result.append(curr.action)
        curr = curr.parent
    return result
        
def outresult(result, outfile):
    f = open(outfile, "w")
    count = 0
    while result:
        out = result.pop()
        count += 1
        if out[2] == 1:
            print(count)
            line = "Move {} chiken and {} wolf from right to left\n".format(out[0], out[1])
            f.write(line)
            print(line)
        else:
            print(count)
            line = "Move {} chiken and {} wolf from left to right\n".format(out[0], out[1])
            f.write(line)
            print(line)

def bfs(st, go):
    expandedNode = 0
    front = collections.deque([st])
    frontstate = collections.defaultdict(list)
    frontstate[st.key].append(st.state)
    explored = collections.deque()
    exploredstate = collections.defaultdict(list)
    while front:
        curr = front.popleft()  
        frontstate[curr.key].remove(curr.state)
        if curr.state == go.state:

            result = getresult(curr)
            print("depth = {}\n".format(curr.depth))
            print("# of expanded nodes = {}\n".format(expandedNode))
            return result
        
        explored.append(curr)
        exploredstate[curr.key].append(curr.state)

        expandedNode += 1
        suc = expand(curr)
        
        for node in suc:
            
            if node.state not in exploredstate[node.key]:
                if node.state not in frontstate[node.key]:
                    front.append(node)
                    frontstate[node.key].append(node.state)
                      
                         
    print("no solution")   
    return "nosol"
            
                
def dfs(st, go):
    expandedNode = 0
    front = collections.deque([st])
    frontstate = collections.defaultdict(list)
    frontstate[st.key].append(st.state)
    
    explored = collections.deque()
    exploredstate = collections.defaultdict(list)
    while front:
        curr = front.pop()
        frontstate[curr.key].remove(curr.state)
        if curr.state == go.state:
            result = getresult(curr)
            print("depth = {}\n".format(curr.depth))
            print("# of expanded nodes = {}\n".format(expandedNode))
            return result
        
        explored.append(curr)
        exploredstate[curr.key].append(curr.state)
        

        expandedNode += 1
        suc = expand(curr)

        for node in suc:
            
            if node.state not in exploredstate[node.key]:
                if node.state not in frontstate[node.key]:
                    front.append(node)
                    frontstate[node.key].append(node.state)
                    
                    
    print("no solution")
    return "nosol"    

def ndfs(n, st, go):
    front = collections.deque([st])
    frontstate = collections.defaultdict(list)
    frontstate[st.key].append(st.state)
    explored = collections.deque()
    exploredstate = collections.defaultdict(list)

    while front:
        curr = front.pop()
        frontstate[curr.key].remove(curr.state)
        global iddfsnodes 
        if curr.state == go.state:
            result = getresult(curr)
            print("depth = {}\n".format(curr.depth))
            print("# of expanded nodes = {}\n".format(iddfsnodes))
            return result

        explored.append(curr)
        exploredstate[curr.key].append(curr.state)
        iddfsnodes += 1
        
        if n > int(curr.depth):
            suc = expand(curr)
            for node in suc:
                if node.state not in exploredstate[node.key]:
                    if node.state not in frontstate[node.key]:
                        front.append(node)
                        frontstate[node.key].append(node.state)
                   
    
    return "nosol"



def iddfs(st, go):
    print("wait ... processing ... if it is test3, it would take about 10 sec")
    for n in range(sys.maxsize):
        result = ndfs(n, st, go)
        if result == "nosol":
            continue
        else:
            return result
    print("no solution")
    return "nosol"


def astar(st, go):
    expandedNode = 0
    front = queue.PriorityQueue()
    front.put((st.cost, st))
    explored = collections.deque()
    exploredstate = collections.defaultdict(list)

    while front:
        curr = front.get()
        curr = curr[1]

        if curr.state == go.state:
            result = getresult(curr)
            print("depth = {}\n".format(curr.depth))
            #print("cost = {}\n".format(curr.cost))
            print("# of expanded nodes = {}\n".format(expandedNode))
            return result

        explored.append(curr)
        exploredstate[curr.key].append(curr.state)
        expandedNode += 1
        suc = expand(curr)

        for node in suc:
            if node.state not in exploredstate[node.key]:
                front.put((node.cost, node))
        
    print("no soultion")
    return "nosol"


def main():
    start = sys.argv[1]
    goal = sys.argv[2]
    mode = sys.argv[3]
    out = sys.argv[4]

    st_node = getnode(start)
    go_node = getnode(goal)


    if mode == "bfs":
        result = bfs(st_node, go_node)
        if result != "nosol":
            outresult(result, out)

    elif mode == "dfs":
        result = dfs(st_node, go_node)
        if result != "nosol":
            outresult(result,out)

    elif mode == "iddfs":
        result = iddfs(st_node, go_node)
        if result != "nosol":
            outresult(result,out)

    elif mode == "astar":
        result = astar(st_node, go_node)
        if result != "nosol":
            outresult(result, out)

if __name__ == "__main__":
    main()
