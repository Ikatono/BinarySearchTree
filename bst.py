from random import getrandbits

#A basic binary search tree
#duplicate keys are not allowed; it will overwrite instead
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
        current = self
        while key != current.key:
            if key < current.key:
                if current.left is None:
                    raise KeyError('key %s does not exist' % key)
                current = current.left
            else:
                if current.right is None:
                    raise KeyError('key %s does not exist' % key)
                current = current.right
        return current.data
    
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
    
    def __delitem__(self, key):
        if self.key is None:
            raise KeyError('key %s does not exist' % key)
        current = self
        while key != current.key:
            if key < current.key:
                if current.left is None:
                    raise KeyError('key %s does not exist' % key)
                current = current.left
            else:
                if current.right is None:
                    raise KeyError('key %s does not exist' % key)
                current = current.right
        if current.left is None:
            if current.right is None:
                if current.parent is None:
                    current.key = None
                    current.data = None
                else:
                    if current.parent.left is current:
                        current.parent.left = None
                    else:
                        current.parent.right = None
            else:
                current.key = current.right.key
                current.data = current.right.data
                current.left = current.right.left
                current.right = current.right.right
        elif current.right is None:
            current.key = current.left.key
            current.data = current.left.data
            current.right = current.left.right
            current.left = current.left.left
        else:
            #randomly determines which child to replace itself with
            #choosing one child consistently could lead to a lopsided list
            if not getrandbits(1):
                #pull left
                current.key = current.left.key
                current.data = current.left.key
                current.right.mergeleft(current.left.right)
                current.left = current.left.left
            else:
                #pull right
                current.key = current.right.key
                current.data = current.right.data
                current.left.mergeright(current.right.left)
                current.right = current.right.right
    
    #TODO replace recursion with loop
    def inorder(self):
        outp = ''
        if self.left is not None:
            outp = self.left.inorder() + ', '
        outp += str(self.key) + ': ' + str(self.data)
        if self.right is not None:
            outp += ', ' + self.right.inorder()
        return outp
    
    def mergeleft(self, other):
        if other is None:
            return
        current = self
        while current.left is not None:
            current = current.left
        current.left = other
        other.parent = current
    
    def mergeright(self, other):
        if other is None:
            return
        current = self
        while current.right is not None:
            current = current.right
        current.right = other
        other.parent = current

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
