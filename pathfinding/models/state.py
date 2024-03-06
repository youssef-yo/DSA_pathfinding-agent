
class State:
    def __init__(self, node, time, parent, g, f_score) -> None:
        self.node = node # node is a tuple (x, y)
        self.time = time
        self.parentNode = parent
        self.g = g
        self.f = f_score

    def getNode(self):
        return self.node
    
    def getParentNode(self):
        return self.parentNode
    
    def getTime(self):  
        return self.time
    
    def __lt__(self, other):
        return self.f < other.f
    
    def __eq__(self, other):
        return self.f == other.f
        
    def __le__(self, other):
        return self.f <= other.f
        
    def __gt__(self, other):
        return self.f > other.f
        
    def __ge__(self, other):
        return self.f >= other.f
        
    def __ne__(self, other):
        return self.f != other.f


    


    

    