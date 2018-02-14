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
                self.left = BST(key, data, parent = self)
            else:
                self.left[key] = data
        elif key > self.key:
            if self.right is None:
                self.right = BST(key, data, parent = self)
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
    
    #places a subtree in the minimum available position under another tree
    #used by my old, bad deletion algorithm
    def mergeleft(self, other):
        if other is None:
            return
        crnt = self
        while crnt.left is not None:
            crnt = crnt.left
        crnt.left = other
        other.parent = crnt
    
    #places a subtree in the maximum available position under another subtree
    #used by my old, bad deletion algorithm
    def mergeright(self, other):
        if other is None:
            return
        crnt = self
        while crnt.right is not None:
            crnt = crnt.right
        crnt.right = other
        other.parent = crnt
    
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
