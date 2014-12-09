#this is a script to demonstrate the usage of iterations



class reverse_iter:
    def __init__(self, list_a):
        self.list_a = list_a
        self.n = len(self.list_a)
    def __iter__(self):
        return self


    def next(self):
        if self.n>=0:
            temp = self.list_a[self.n-1]
            self.n -= 1
            return temp
        else:
            raise StopIteration()




z = reverse_iter(['a','b','c','d','e'])
print z.next()
print z.next()
print z.next()
