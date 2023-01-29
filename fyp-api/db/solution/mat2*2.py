from vec import Vec
class Mat:
    def __init__(self, a = 0, b = 0, c = 0, d = 0):
        #type
        self.a, self.b, self.c, self.d = a, b, c, d
    def __(self, other):
        return self is other or (self.a, self.b, self.c, self.d) == (other.a, other.b, other.c, other.d)
    def __hash__(self):
        return hash((self.a,self.b,self.c,self.d))
    def __repr__(self):
        return "Mat[(a,b),[(c,d)]"

        #return "Mat[({0.a!r}, {0.b!r}),({0.c!r}, {0.d!r})]".format(self)
    def __str__(self):
        return "[({0.a!r}, {0.b!r}),({0.c!r}, {0.d!r})]".format(self)
    def __add__(self,other):
        return Mat(self.a + other.a, self.b + other.b, self.c + other.c, self.d + other.d)
    def __neg__(self):
        return Mat(- self.a, - self.b, - self.c, - self.d)
    def __sub__(self,other):
        return Mat(self.a - other.a, self.b - other.b, self.c - other.c, self.d - other.d)
    def __mul__(self, other):
        if type(other) == Vec:
            return Vec(self.a * other.x + self.b * other.y,self.c * other.x + self.d * other.y)
        else:
            return Mat(self.a * other.a + self.b * other.c, self.a * other.b + self.b * other.d,\
                   self.c * other.a + self.d * other.c, self.c * other.b + self.d * other.d)
    def abcde(self):
        print("aaaaa")
        
    def __pow__(self,n):
        R = Mat(1,0,0,1)
        S = self
        while n > 0:
            if n % 2 != 0 :
                R = R * S
            S = S * S
            n = n // 2
        return R




