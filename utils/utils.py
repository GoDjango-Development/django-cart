from .wrapper import Wrapper

class ReferencedCounter:
    counter = 0
    def __init__(self, counter) -> None:
        self.counter = counter

class MappedDict(dict):
    path = []
    debug = False
    def __init__(self, content: dict = {}):
        super().__init__(content)
        # self.debug = True # Uncomment this to enable debug programmatically

    def dig_into(self, looking_for: str, offset = 0):
        if self.debug:
            print("===============================================================>")
            print("Started")
            print(self, ": ", offset)
        def __dig_into(target: dict, looking_for: str, offset: ReferencedCounter):
            if self.debug:
                print(target, " : ", offset.counter)
            #res = None
            for key in target.keys():
                if self.debug:
                    print("Searching key: %s"%key)
                    print("Value target: %s"%target[key])
                    print("How evaluate first block?: %s"%(str(key) == looking_for))
                    print("First block data: \nstr(key)->%s & looking_for->%s\n"%(str(key), looking_for))
                    print("How evaluate second block?: %s"%(
                        type(target[key]) is dict or 
                        type(target[key]) is Wrapper or
                        type(target[key]) is MappedDict
                        ))
                    print("Second block data: \ntype(target[key])->%s(dict, Wrapper?)"%(type(target[key])))
                    
                if str(key) == looking_for:
                    if offset.counter == 0:
                        if self.debug:
                            print("JACKPOT!!!", target[key])
                        return target
                    offset.counter -= 1
                elif (
                    type(target[key]) is dict or 
                    type(target[key]) is Wrapper or 
                    type(target[key]) is MappedDict
                    ):
                    if self.debug:
                        print("Searching recursively: %s "%target[key])
                    res =__dig_into(target[key], looking_for, offset)
                    if res:
                        return res
            return None
        res = __dig_into(self, looking_for, ReferencedCounter(offset)) or {}
        if self.debug:
            print(res)
            print("Ended")
            print("===============================================================>")
        return res

    def resolve(self, ):
        def __resolve(target: dict, i = 0):
            i += 1
            if i > len(self.path):
                return target
            return __resolve(target[self.path[i - 1]], i)
        return __resolve(self)
    
    def get_path(self, ):
        return self.path.copy()

    def explore_path(self, index, value):
        if type(index) is str:
            for way_i in range(len(self.path)):
                if str(self.path[way_i]) == index:
                    res = self.get_path()
                    res[way_i] = value
                    return res
            return []
        res = self.get_path()
        if len(res) < index:
            res[index] = value
            return res
        return []
    
    def travel(self, index, value):
        content = self
        for step in self.explore_path(index, value):
            content = content.get(step, {})
        return content

    def find_step_pos(self, index):
        if type(index) is str:
            for way_i in range(len(self.path)):
                if str(self.path[way_i]) == index:
                    return way_i
        return None

    def get_total_of(self, index: str):
        res = 0
        i = 0
        while True:
            n = self.dig_into(index, i).get(index, None)
            i += 1
            if n is None:
                break
            try:
                n = int(n)
            except:
                continue
            res += n
        return res
    
    def get_total_prod_of(self, index1: str, index2: str):
        res = 0
        i = 0
        while True:
            s1 = self.dig_into(index1, i).get(index1, None)
            s2 = self.dig_into(index2, i).get(index2, None)
            i += 1
            if s1 is None or s2 is None:
                break
            res += s1 * s2
        return res
    
    def get_all_operated(self, *indexs: str, oper_func, ret_func=None):
        res = 0
        i = 0
        while True:
            ss = []
            for index in indexs:
                ss.append(self.dig_into(index, i).get(index, None))
            i += 1
            if ss.count(None) == len(ss):
                break
            ss.insert(0, res)
            res = oper_func(ss)
        if ret_func is not None:
            res = ret_func(res, i)
        return res

    def get(self, key: str, default=None):
        key = str(key)
        if self.__contains__(key):
            return self[key]
        return default

    def get_last_value(self, ):
        if len(self.values()) == 0:
            return None
        return list(self.values())[-1]
    
    def get_last_key(self, ):
        if len(self.keys()) == 0:
            return None
        return list(self.keys())[-1]

    def iter_get(self, *keys):
        res = None
        for key in keys:
            res = self.get(key, None)
            if res is None:
                break
        return res
    
    def iter_set(self, *key_pair):
        for k, v in key_pair:
            self[k] = v

    def rset(self, *args, value, to=None):
        # Shortcut to cascade_set
        return self.cascade_set(*args, value=value, to=to)

    def rget(self, *args, value, to=None):
        # Shortcut to explore_path
        # TODO
        raise NotImplementedError("TODO")

    def make_sure(self, key, value=None):
        if not self.keys().__contains__(key):
            self[key] = value or MappedDict({})
        return self

    def cascade_set(self, *keys, value, to=None):
        keys = list(keys)
        temp = {
            keys.pop(): value
        }
        for key in keys[::-1]:
            temp = {
                key: temp
            }
        self.merge(temp, data1=to)
        return self
    
    def merge(self, data2: dict, data1: dict=None):
        data1 = data1 if data1 is not None else self
        def _merge(arg1: dict, arg2: dict):
            for key in arg2.keys():
                if not arg1.__contains__(key):
                    arg1[key] = arg2[key]
                elif (type(arg2[key]) is dict or MappedDict) and (type(arg1[key]) is dict or MappedDict):
                    _merge(arg2[key], arg1[key])
                elif (type(arg2[key]) is not type(data1[key])):
                    raise ValueError("Cannot merge this two dicts")
                else:
                    print("Here?")
            return arg1
        return _merge(data1, data2)