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
        #self.depth = (self.key is not None) * 1
    
    #TODO unroll
    def __getitem__(self, key):
        if self.key is None:
            raise KeyError('key %s does not exist' % key)
        if key == self.key:
            return self.data
        elif key < self.key:
            if self.left is None:
                raise KeyError('key %s does not exist' % key)
            else:
                return self.left[key]
        elif key > self.key:
            if self.right is None:
                raise KeyError('key %s does not exist' % key)
            else:
                return self.right[key]
        else:
            raise KeyError('key %s cannot be compared to other keys' % key)
    
    #TODO unroll
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
        if key < self.key:
            if self.left is None:
                raise KeyError('key %s does not exist' % key)
            else:
                del self.left[key]
        elif key > self.key:
            if self.right is None:
                raise KeyError('key %s does not exist' % key)
            else:
                del self.right[key]
        elif key == self.key:
            isleft = self.parent.left is self
            #randomly determines which child to replace itself with
            #choosing one child consistently could lead to a lopsided list
            if self.left is None:
                if self.right is None:
                    if isleft:
                        self.parent.left = None
                    else:
                        self.parent.right = None
                    return
                else:
                    pullleft = False
            elif self.right is None:
                pullleft = True
            else:
                pullleft = not getrandbits(1)
            if isleft:
                if pullleft:
                    self.parent.left = self.left
                    self.left.parent = self.parent
                    self.right.mergeleft(self.left.right)
                    self.left.right = self.right
                else:
                    self.parent.left = self.right
                    self.right.parent = self.parent
                    self.left.mergeright(self.right.left)
                    self.right.left = self.left
            else:
                if pullleft:
                    self.parent.right = self.left
                    self.left.parent = self.parent
                    self.right.mergeleft(self.left.right)
                    self.left.right = self.right
                else:
                    self.parent.right = self.right
                    self.right.parent = self.parent
                    self.right.mergeleft(self.right.left)
                    self.right.left = self.left
            
        else:
            raise KeyError('key %s cannot be compared to other keys' % key)
        
    
    def inorder(self):
        outp = ''
        if self.left is not None:
            outp = self.left.inorder() + ', '
        outp += str(self.key) + ': ' + str(self.data)
        if self.right is not None:
            outp += ', ' + self.right.inorder()
        return outp
    
    #TODO unroll
    def mergeleft(self, other):
        if other is None:
            return
        if self.left is None:
            self.left = other
            other.parent = self
        else:
            self.left.mergeleft(other)
    
    #TODO unroll
    def mergeright(self, other):
        if other is None:
            return
        if self.right is None:
            self.right = other
            other.parent = self
        else:
            self.right.mergeright(other)

def maketest():
    a = BST()
    a[10] = ''
    a[5] = ''
    a[2] = ''
    a[1] = ''
    a[0] = ''
    a[3] = ''
    a[7] = ''
    a[6] = ''
    a[8] = '' 
    a[9] = ''
    a[15] = ''
    a[13] = ''
    a[17] = ''
    a[19] = ''
    a[18] = ''
    return a
