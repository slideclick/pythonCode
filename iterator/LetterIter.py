class LetterIter:
    """An iterator over letters of the alphabet in ASCII order."""
    def __init__(self, start='a', end='e'):
        self.next_letter = start
        self.end = end
    def __iter__(self):        
        return self
    def __next__(self):
        if self.next_letter == self.end:
            raise StopIteration
        letter = self.next_letter
        self.next_letter = chr(ord(letter)+1)
        return letter
letter_iter = LetterIter()
for i in  letter_iter:
        print(i)
print()   
     
def reverse(data):
    for index in range(len(data)-1, -1, -1):
        yield data[index]
for char in reverse('golf'):
    print(char) 

print(sum(reverse([12,3])))    
print(max(reverse([12,3])))  