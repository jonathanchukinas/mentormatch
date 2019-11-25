class MyClass:

    def __init__(self):
        self.letters = self._letters()

    def _letters(self):
        print("first call to get_next_letter")
        for letter in 'abc':
            print(f"getting letter {repr(letter)}")
            yield letter
        return

myobj = MyClass()
print("Just created myobj")
for _ in range(6):
    try:
        print("about to get a letter")
        letter = next(myobj.letters)
        print(letter)
    except StopIteration:
        print("No more letters")