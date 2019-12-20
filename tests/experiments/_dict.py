class MyClass:
    def __init__(self):
        self.x = 5

    @property
    def y(self):
        return 6

    # def _asdict(self):
    #     return {
    #         attr: getattr(self, attr)
    #         for attr in 'x y'.split()
    #     }

    def keys(self):
        return list("xyz")

    def __getitem__(self, key):
        return getattr(self, key, None)

myobj = MyClass()
mydict = dict(myobj)
print(mydict)
