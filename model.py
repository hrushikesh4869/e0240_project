from circular_profile import *
from sympy import *

p_miss = symbols('p_miss')


class Model:
    def __init__(self, profile: CircularProfile, policy):
        self.p = profile
        self.policy = policy
        self.n_dict = {}

    def find_avg_n(self):
        for d in range(1, self.p.d):
            numer = 0
            denom = 0
            n_ = 0
            for i in range(201):
                if self.p.profile.get((d, i)) != None:
                    print(d, i, self.p.profile[(d, i)])
                    numer += self.p.profile[(d, i)] * i
                    denom += self.p.profile[(d, i)]

            if denom != 0:
                self.n_dict[d] = numer/denom

    # def find_roots(self):

    def s(self, d, n, p, _d, _n):

        if n == 0:
            return 0

        if n > 0 and _d - d == p and p < self.p.cache.associativity:
            return self.p_dist() * p_miss * (1 - self.rpf(p)) * (1 - self.p_shift(p)) * self.s(d-1, n-1, p, _d, _n) \
                + self.p_dist() * p_miss * (1 - self.rpf(p)) * self.p_shift(p) * self.s(d-1, n-1, p+1, _d, _n) \
                + (1 - self.p_dist()) * self.s(d, n-1, p, _d, _n) \
                + self.p_dist() * (1 - p_miss) * self.s(d-1, n-1, p+1, _d, _n) \
                + self.p_dist() * p_miss * self.rpf(p)

        if n > 0 and _d - d > p and p == self.p.cache.associativity:
            return self.p_dist() * (1 - self.rpf(p)) * self.s(d-1, n-1, p, _d, _n) \
                + (1 - self.p_dist()) * (1 - p_miss) * self.s(d, n-1, p, _d, _n) \
                + (1 - self.p_dist()) * p_miss * (1 - self.rpf(p)) * self.s(d, n-1, p, _d, _n)\
                + self.p_dist() * self.rpf(p) \
                + (1 - self.p_dist()) * p_miss * self.rpf(p)

        if n > 0 and _d - d == p and p == self.p.cache.associativity:
            return self.p_dist() * (1 - self.rpf(p)) * self.s(d-1, n-1, p, _d, _n) \
                + (1 - self.p_dist()) * self.s(d, n-1, p, _d, _n) \
                + self.p_dist() * self.rpf(p)

        else:
            return self.p_dist() * p_miss * (1 - self.rpf(p)) * (1 - self.p_shift(p)) * self.s(d-1, n-1, p, _d, _n) \
                + self.p_dist() * p_miss * (1 - self.rpf(p)) * self.p_shift(p) * self.s(d-1, n-1, p+1, _d, _n) \
                + self.p_dist() * (1-p_miss) * self.s(d-1, n-1, p+1, _d, _n) \
                + (1 - self.p_dist()) * p_miss * (1 - self.rpf(p)) * (1 - self.p_shift(p)) * self.s(d, n-1, p, _d, _n) \
                + (1 - self.p_dist()) * p_miss * (1 - self.rpf(p)) * self.p_shift(p) * self.s(d, n-1, p+1, _d, _n) \
                + (1 - self.p_dist()) * (1 - p_miss) * self.s(d, n-1, p, _d, _n) \
                + p_miss * self.rpf(p)

    def obtain_p_miss(self):
        numer = 0
        denom = 0
        for d in range(1, self.p.d):
            n_ = 0
            for i in range(201):
                if self.p.profile.get((d, i)) != None:
                    print(d, i, self.p.profile[(d, i)])
                    numer += self.p.profile[(d, i)] * self.s(
                        d-1, floor(self.n_dict[d])-1, 1, d, floor(self.n_dict[d]))
                    denom += self.p.profile[(d, i)]

        equation = numer/denom - p_miss
        # print(equation)
        print(solve(equation, p_miss))

    def rpf(self, i):
        if self.policy == "LRU":
            if i == self.p.cache.associativity:
                return 1
            else:
                return 0

        elif self.policy == "Random":
            return 1/self.p.cache.associativity

    def p_shift(self, p):
        p = 1
        numer = 0
        denom = 1 - self.rpf(p)

        for i in range(p+1, self.p.cache.associativity+1):
            numer += self.rpf(p)

        return numer/denom

    def p_dist(self):
        return self.p.d/self.p.n


if __name__ == "__main__":
    c = Cache()
    p = CircularProfile(c, 24, 200)

    with open("smalltrace.din") as file:
        data = file.read()
        accesses = data.split("\n")
        accesses = accesses[:-1]
        for i in accesses:
            p.parse_access(i)

        p.find_profile()

    print(p.profile)
    m = Model(p, "Random")
    m.find_avg_n()
    m.obtain_p_miss()
