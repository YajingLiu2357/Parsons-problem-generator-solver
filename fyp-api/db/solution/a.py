class Node:
    def __init__(self, elm, nxt):
        self.elm = elm
        self.nxt = nxt


class LnLs:
    def __init__(self, s=None):
        self.head = None
        if s:
            for x in s:
                self.push(x)
            self.reverse()

    def __bool__(self):
        return self.head is not None

    def top(self):
        if not self:
            raise IndexError
        return self.head.elm

    def push(self, x):
        self.head = Node(x, self.head)

    def pop(self):
        x = self.top()
        self.head = self.head.nxt
        return x

    def __iter__(self):
        p = self.head
        while p:
            yield p.elm
            p = p.nxt

    def index_of(self, x):
        for i, y in enumerate(self):
            if x == y:
                return i
        return -1


    def reverse(self):
        q, p = None, self.head
        # q points to the previous node
        while p:
            t = p.nxt
            p.nxt = q
            q = p
            p = t
        self.head = q


#beginning
    def last_index_of(self,x):
        i = -1
        for j, y in enumerate(self):
            if x == y :
                i = j
        return i

    def __repr__(self):
        temp = self.pop()
        str1 ='\'' + temp + '\''
        for i in iter(self):
            str1 = str1 +'->' + '\'' + i + '\''
        str1 = str1 + '-/'
        self.push(temp)
        return str1
    def __len__(self):
        count = 0
        for i in iter(self):
            count = count + 1
        return count

    def __getitem__(self, i):
        if i < -len(self) or i >= len(self):
            raise ImportError
        else:
            if i < 0:
                i = len(self) + i
            for j, x in enumerate(self):
                if i == j:
                    return x
    def __setitem__(self, i, x):
        p = self.head
        count = 0
        if i < -len(self) or i >= len(self):
            raise ImportError
        else:
            if i < 0 :
                i = len(self) + i
            while p:
                if i == count:
                    p.elm = x
                p = p.nxt
                count = count + 1
    def __iadd__(self, s):
        p = self.head
        ll1 = LnLs()
        for i in s:
            ll1.push(i)
        ll1.reverse()
        count = 1
        for i in iter(self):
            if count == len(self) :
                p.nxt = ll1.head
                break
            p = p.nxt
            count = count + 1
        return self
    def __add__(self, s):
        lnls = LnLs()
        for i in iter(self):
            temp = i
            lnls.push(temp)
        for i in s:
            temp = i
            lnls.push(temp)
        lnls.reverse()
        return lnls





if __name__ == '__main__':
    ll = LnLs()
    ll.push('apple')
    ll.push('orange')
    ll.push('peach')
    list = [1,2,3]
    lss = LnLs(list)
    print(lss.last_index_of(3))
    #ll[-1] = 'banana'
    t = ll + ['a','b','c']
    print(t)
    print(repr(ll))
    print(len(ll))
    print(ll[-1])
    print('orange', ll.index_of('orange'), ll[ll.index_of('orange')])
    print('apple', ll.last_index_of('apple'))
    print('banana', ll.index_of('banana'))
    ll.pop()
    ll.push('banana')
    print([x + '>' for x in ll])
    ll.reverse()
    print([x + '<' for x in ll])
    ll = LnLs(range(10))
    print(list(ll))
