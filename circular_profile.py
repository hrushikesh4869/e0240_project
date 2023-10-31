class Cache:
    # Pass associativity and block size in bits so actual associativity = 2^(associativity)
    def __init__(self,associativity = 8,sets = 11, block_size = 6):
        self.associativity = associativity
        self.sets = sets
        self.block_size = block_size
        self.addr_bits = 48
        # self.block_mask 


class CircularProfile:
    def __init__(self,cache:Cache, d, n):
        self.cache = cache
        self.d = min(3*self.cache.associativity,d)
        self.n = min(200,n)
        self.profile = {}
        self.set_accesses = {}


    def parse_access(self,s):
        if(s[0]=='i'):
            return
        s = s.split(" ")
        addr = s[1]
        addr = int(addr,16)
        #print(addr)
        #print(hex(addr))
        # print(s)
        self.analyse_access(addr)
    
    def analyse_access(self,addr):
        tag_mask = 2**(self.cache.addr_bits) - 1
        tag_mask = tag_mask & (2**(self.cache.sets + self.cache.block_size)-1)
        cache_set  = (addr & tag_mask) >> self.cache.block_size
        
        if self.set_accesses.get(cache_set) == None:
            self.set_accesses[cache_set] = []
        
        block_addr = addr >> self.cache.block_size

        self.set_accesses[cache_set].append(hex(block_addr))
    
    def count_sequences(self,accesses):
        length = len(accesses)

        for i in range(0,length):
            curr = accesses[i]
            mp = {}
            mp[accesses[i]] = 1
            j = i+1
            while j<length and accesses[j] != curr:
                mp[accesses[j]] = 1
                j = j+1
            
            d = len(mp)
            n = j-i+1
            if n>201:
                n = 200
            if self.profile.get((d,n)) == None:
                self.profile[(d,n)] = 1
            else:
                self.profile[(d,n)] += 1

    def find_profile(self):
        for i in self.set_accesses.values():
            self.count_sequences(i)


if __name__ == "__main__":
    c = Cache()
    p = CircularProfile(c,24,200)
    
    with open("smalltrace.din") as file:
        data = file.read()
        accesses = data.split("\n")
        accesses = accesses[:-1]
        for i in accesses:
            p.parse_access(i)
        
        p.find_profile()
        print(p.profile)


