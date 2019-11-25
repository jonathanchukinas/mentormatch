class BaseClass:

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.happy = None


class SubClass(BaseClass):

    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)
        self.happy = True


a = 1
b = 2
subobj = SubClass(a, b)
print(subobj.happy)


# this isn't working...