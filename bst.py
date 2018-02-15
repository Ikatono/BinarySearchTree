#only needed for old deletion algorithm
#from random import getrandbits

#A basic binary search tree
#duplicate keys are not allowed; it will overwrite instead
#all methods except successor assume they are being called by the top of the tree
class BST:
    
    #for now I'm assuming all keys are immutable and comparable
    #typeorder = (str, bool, (int, float))
    
    def __init__(self, key=None, data=None, parent=None):
        self.key = key
        self.data = data
        self.parent = parent
        self.left = None
        self.right = None
    
    def __getitem__(self, key):
        if self.key is None:
            raise KeyError('key %s does not exist' % key)
        crnt = self
        while key != crnt.key:
            if key < crnt.key:
                if crnt.left is None:
                    raise KeyError('key %s does not exist' % key)
                crnt = crnt.left
            else:
                if crnt.right is None:
                    raise KeyError('key %s does not exist' % key)
                crnt = crnt.right
        return crnt.data
    
    #TODO replace recursion with loop
    def __setitem__(self, key, data):
        if self.key is None:
            self.key = key
            self.data = data
        if key < self.key:
            if self.left is None:
                self.left = BST(key, data, parent=self)
            else:
                self.left[key] = data
        elif key > self.key:
            if self.right is None:
                self.right = BST(key, data, parent=self)
            else:
                self.right[key] = data
        elif key == self.key:
            self.data = data
        else:
            raise KeyError('key %s cannot be compared to other keys' % key)
    
    #deletes given node or node corresponding to given key
    #follows the algorithm given in CLRS
    def __delitem__(self, entry):
        if not isinstance(entry, BST):
            entry = self.getnode(entry)
        if entry.left is None:
            #no children
            if entry.right is None:
                if entry.parent.left is entry:
                    entry.parent.left = None
                else:
                    entry.parent.right = None
            #right child only
            else:
                entry.key = entry.right.key
                entry.data = entry.right.data
                entry.left = entry.right.left
                entry.right = entry.right.right
        else:
            #left child only
            if entry.right is None:
                entry.key = entry.left.key
                entry.data = entry.left.data
                entry.right = entry.left.right
                entry.left = entry.left.left
            else:
                suc = entry.successor()
                entry.key = suc.key
                entry.data = suc.data
                self.newdel(suc)
    
    #returns node or key following the provided node or key
    #if given a node returns a node else returns a key
    #if entry is not defined, it is replaced with self
    #either way, returns None if given the maximum
    def successor(self, entry=None):
        if entry is None:
            entry = self
        isnode = isinstance(entry, BST)
        node = entry if isnode else self.getnode(entry)
        if node.right is not None:
            return node.right.minimum(isnode)
        p = node.parent
        while p is not None and p.right is None:
            p = p.parent
        if p.right is not None:
            return p.minimum(isnode)
        return None
    
    
    def getnode(self, key):
        crnt = self
        while key != crnt.key:
            if key < crnt.key:
                crnt = crnt.left
            elif key > crnt.key:
                crnt = crnt.right
            if crnt is None:
                raise KeyError('key %s does not exist' % key)
        return crnt
    
    #a deletion algorithm I came up with before consulting CLRS
    #when deleting a node with two children this sometimes makes the tree taller
    # def __delitem__(self, key):
        # if self.key is None:
            # raise KeyError('key %s does not exist' % key)
        # crnt = self
        # while key != crnt.key:
            # if key < crnt.key:
                # if crnt.left is None:
                    # raise KeyError('key %s does not exist' % key)
                # crnt = crnt.left
            # else:
                # if crnt.right is None:
                    # raise KeyError('key %s does not exist' % key)
                # crnt = crnt.right
        # if crnt.left is None:
            # if crnt.right is None:
                # if crnt.parent is None:
                    # crnt.key = None
                    # crnt.data = None
                # else:
                    # if crnt.parent.left is crnt:
                        # crnt.parent.left = None
                    # else:
                        # crnt.parent.right = None
            # else:
                # crnt.key = crnt.right.key
                # crnt.data = crnt.right.data
                # crnt.left = crnt.right.left
                # crnt.right = crnt.right.right
        # elif crnt.right is None:
            # crnt.key = crnt.left.key
            # crnt.data = crnt.left.data
            # crnt.right = crnt.left.right
            # crnt.left = crnt.left.left
        # else:
            # #randomly determines which child to replace itself with
            # #choosing one child consistently could lead to a lopsided list
            # if not getrandbits(1):
                # #pull left
                # crnt.key = crnt.left.key
                # crnt.data = crnt.left.key
                # crnt.right.mergeleft(crnt.left.right)
                # crnt.left = crnt.left.left
            # else:
                # #pull right
                # crnt.key = crnt.right.key
                # crnt.data = crnt.right.data
                # crnt.left.mergeright(crnt.right.left)
                # crnt.right = crnt.right.right
    
    #TODO replace recursion with loop
    def inorder(self):
        outp = ''
        if self.left is not None:
            outp = self.left.inorder() + ', '
        outp += str(self.key) + ': ' + str(self.data)
        if self.right is not None:
            outp += ', ' + self.right.inorder()
        return outp
    
    #returns a generator that iterates through keys in order
    #TODO remove recursion
    def keys(self):
        if self.left is not None:
            for i in self.left.keys():
                yield i
        yield self.key
        if self.right is not None:
            for i in self.right.keys():
                yield i
        
    #returns a generator that iterates through nodes in order of keys
    #TODO remove recursion
    def nodes(self):
        if self.left is not None:
            for i in self.left.nodes():
                yield i
        yield self
        if self.right is not None:
            for i in self.right.nodes():
                yield i
    
    # #places a subtree in the minimum available position under another tree
    # #used by my old, bad deletion algorithm
    # def mergeleft(self, other):
        # if other is None:
            # return
        # crnt = self
        # while crnt.left is not None:
            # crnt = crnt.left
        # crnt.left = other
        # other.parent = crnt
    
    # #places a subtree in the maximum available position under another subtree
    # #used by my old, bad deletion algorithm
    # def mergeright(self, other):
        # if other is None:
            # return
        # crnt = self
        # while crnt.right is not None:
            # crnt = crnt.right
        # crnt.right = other
        # other.parent = crnt
    
    #returns minimum key or node
    def minimum(self, retnode=False):
        crnt = self
        while crnt.left is not None:
            crnt = crnt.left
        return crnt if retnode else crnt.key
    
    #returns maximum key or node
    def maximum(self, retnode=False):
        crnt = self
        while crnt.right is not None:
            crnt = crnt.right
        return crnt if retnode else crnt.key

#red black tree
#self-organizes to limit height to 2log(n+1)
class RBT(BST):
    
    def __init__(self, key=None, data=None, parent=None, red=False):
        self.key = key
        self.data = data
        self.parent = parent
        self.red = red
        self.left = None
        self.right = None
    
    def __setitem__(self, key, data):
        if self.key is None:
            self.key = key
            self.data = data
            return
        crnt = self
        while key != crnt.key:
            if key < crnt.key:
                if crnt.left is None:
                    #insert, fix, and return
                    crnt.left = RBT(key, data, parent=crnt, red=True)
                    self.insertfixup(crnt.left)
                    return
                else:
                    crnt = crnt.left
            else:
                if crnt.right is None:
                    #insert, fix, and return
                    crnt.right = RBT(key, data, parent=crnt, red=True)
                    self.insertfixup(crnt.right)
                    return
                else:
                    crnt = crnt.right
        crnt.data = data
    
    def insertfixup(self, crnt):
        while RBT.isred(crnt.parent):
            # if crnt.parent is None or crnt.parent.parent is None:
                # break
            #if crnt.parent is a left child
            if crnt.parent is crnt.parent.parent.left:
                y = crnt.parent.parent.right
                if RBT.isred(y):
                    crnt.parent.red = False
                    y.red = False
                    crnt.parent.parent.red = True
                    crnt = crnt.parent.parent
                else:
                    if crnt.parent.right is crnt:
                        crnt = crnt.parent
                        self.rotleft(crnt)
                        crnt = crnt.left
                    crnt.parent.red = False
                    crnt.parent.parent.red = True
                    self.rotright(crnt.parent.parent)
            #if crnt.parent is a right child
            else:
                y = crnt.parent.parent.left
                if RBT.isred(y):
                    crnt.parent.red = False
                    y.red = False
                    crnt.parent.parent.red = True
                    crnt = crnt.parent.parent
                else:
                    if crnt.parent.left is crnt:
                        crnt = crnt.parent
                        self.rotright(crnt)
                        crnt = crnt.right
                    crnt.parent.red = False
                    crnt.parent.parent.red = True
                    self.rotleft(crnt.parent.parent)
        self.red = False
    
    #deletes given node or node corresponding to given key
    #follows the algorithm given in CLRS
    #TODO rename x, y and z
    def __delitem__(self, key):
        z = self.getnode(key)
        if z.left is None or z.right is None:
            y = z
        else:
            y = self.successor(z)
        if y.left is not None:
            x = y.left
        else:
            x = y.right()
        x.parent = y.parent
        if y.parent is None:
            x = self
        else:
            if y is y.parent.left:
                y.parent.left = x
            else:
                y.parent.right = x
        if y is not z:
            z.key = y.key
        if not y.red:
            self.deletefixup(x)
    
    #performs rotations and recolors after a deletion to maintain RB structure
    def deletefixup(self, crnt):
        pass
    
    #new left rotate algorithm that doesn't distinguish between root and other nodes
    def rotleft(self, entry=None):
        if entry is None:
            entry = self
        if not isinstance(entry, RBT):
            entry = self.getnode(entry)
        if entry.right is None:
            raise RuntimeError('Cannot perform left rotation on node without right child')
        l = RBT(entry.key, entry.data, entry, entry.red)
        l.left = entry.left
        if l.left is not None:
            l.left.parent = l
        l.right = entry.right.left
        if l.right is not None:
            l.right.parent = l
        entry.key = entry.right.key
        entry.data = entry.right.data
        entry.red = entry.right.red
        entry.left = l
        entry.right = entry.right.right
        if entry.right is not None:
            entry.right.parent = entry
    
    #new left rotate algorithm that doesn't distinguish between root and other nodes
    def rotright(self, entry=None):
        if entry is None:
            entry = self
        if not isinstance(entry, RBT):
            entry = self.getnode(entry)
        if entry.left is None:
            raise RuntimeError('Cannot perform right rotation on node without left child')
        r = RBT(entry.key, entry.data, entry, entry.red)
        r.right = entry.right
        if r.right is not None:
            r.right.parent = r
        r.left = entry.left.right
        if r.left is not None:
            r.left.parent = r
        entry.key = entry.left.key
        entry.data = entry.left.data
        entry.red = entry.left.red
        entry.right = r
        entry.left = entry.left.left
        if entry.left is not None:
            entry.left.parent = entry
    
    #tests that this is a valid red black tree
    #returns the black height if the tree is valid, 0 if not
    #doesn't verify that the root is black, so it can be run on subtrees
    def diagnostic(self):
        if self.red:
            if RBT.isred(self.left) or RBT.isred(self.right):
                return 0
        if self.left is None:
            lh = 1
        else:
            lh = self.left.diagnostic()
            if self.key < self.left.key:
                return 0
        if self.right is None:
            rh = 1
        else:
            rh = self.right.diagnostic()
            if self.key > self.right.key:
                return 0
        if not (rh and lh):
            return 0
        if rh != lh:
            return 0
        return rh + (not self.red)
    
    #returns a lift of nodes who don't know who their parents are
    #ignores nodes whose parents are root
    def orphans(self, entry=None):
        if entry is None:
            entry = self
        elif not isinstance(entry, RBT):
            entry = self.getnode(entry)
        o = []
        if entry.left is not None:
            o += entry.left.orphans()
        if entry.right is not None:
            o += entry.right.orphans()
        if self.parent is not None and self not in (self.parent.left, self.parent.right):
            o += [entry]
        return o
    
    #returns a rough string representation of the tree
    #set entry to print only a subtree
    def printme(self, entry=None):
        if entry is None:
            entry = self
        elif not isinstance(entry, RBT):
            entry = self.getnode(entry)
        s = str(entry.key)
        if entry.left is not None or entry.right is not None:
            s += '('
            if entry.left is not None:
                s += entry.left.printme()
            s += ','
            if entry.right is not None:
                s += entry.right.printme()
            s += ')'
        return s
    
    #adds ' after key in red nodes
    def printcolor(self, entry=None):
        if entry is None:
            entry = self
        elif not isinstance(entry, RBT):
            entry = self.getnode(entry)
        s = str(entry.key) + "'"
        if entry.left is not None or entry.right is not None:
            s += '('
            if entry.left is not None:
                s += entry.left.printcolor()
            s += ','
            if entry.right is not None:
                s += entry.right.printcolor()
            s += ')'
        return s
    
    #allows you to test the color of a node without first verifying that it isn't None
    def isred(entry):
        if entry is None or not entry.red:
            return False
        return True

#quickly makes a large tree for testing purposes
def maketest():
    a = BST()
    a[10] = '10'
    a[5] = '5'
    a[2] = '2'
    a[1] = '1'
    a[0] = '0'
    a[3] = '3'
    a[7] = '7'
    a[6] = '6'
    a[8] = '8' 
    a[9] = '9'
    a[15] = '15'
    a[13] = '13'
    a[17] = '17'
    a[19] = '19'
    a[18] = '18'
    return a

#quickly makes a large red-black tree for testing purposes
def makerbt(n=20):
    import random
    a = RBT()
    lst = list(range(n))
    random.shuffle(lst)
    for i in lst:
        print(i)
        a[i] = str(i)
        print(' '.join([str(i) for i in a.keys()]))
        print(a.diagnostic())
        yield a
    #return a

#tests a large number of insertions in a red black tree
def insertiontest(n=100):
    a = RBT()
    lst = list(range(n))
    import random
    random.shuffle(lst)
    cnt = 0
    for i in lst:
        print(cnt)
        a[i] = str(i)
        cnt += 1
    return (a.diagnostic(), a)
