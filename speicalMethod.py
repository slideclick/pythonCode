class CustomList(object):

    def __init__(self, container=None):
        # the class is just a wrapper around another list to 
        # illustrate special methods
        if container is None:
            self.container = []
        else:
            self.container = container

    def __len__(self):
        # called when a user calls len(CustomList instance)
        return len(self.container)

    def __getitem__(self, index):
        # called when a user uses square brackets for indexing 
        return self.container[index]

    def __setitem__(self, index, value):
        # called when a user performs an index assignment
        if index <= len(self.container):
            self.container[index] = value
        else:
            raise IndexError()

    def __contains__(self, value):
        # called when the user uses the 'in' keyword
        return value in self.container

    def append(self, value):
        self.container.append(value)

    def __repr__(self):
        return str(self.container)

    def __add__(self, otherList):
        # provides support for the use of the + operator 
        return CustomList(self.container + otherList.container)
        
        
myList = CustomList() 
myList.append(1)    
myList.append(2)
myList.append(3)
myList.append(4)
len(myList)
     