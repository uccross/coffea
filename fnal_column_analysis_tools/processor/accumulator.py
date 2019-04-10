from abc import ABCMeta, abstractmethod
import collections


class AccumulatorABC(metaclass=ABCMeta):
    '''
    ABC for an accumulator.  Derived must implement:
        identity: returns a new object of same type as self,
            such that self + self.identity() == self
        add(other): adds an object of same type as self to self

    Concrete implementations are provided for __add__, __iadd__
    '''
    @abstractmethod
    def identity(self):
        pass

    @abstractmethod
    def add(self, other):
        pass

    def __add__(self, other):
        ret = self.identity()
        ret.add(self)
        ret.add(other)
        return ret

    def __iadd__(self, other):
        self.add(other)
        return self


class accumulator(AccumulatorABC):
    '''
    Holds a value, of type and identity as provided to initializer
    '''
    def __init__(self, identity):
        self.value = identity
        self._identity = identity

    def identity(self):
        return accumulator(self._identity)

    def add(self, other):
        if isinstance(other, accumulator):
            self.value += other.value
        else:
            self.value += other


class set_accumulator(set, AccumulatorABC):
    '''
    A set with accumulator semantics
    '''
    def identity(self):
        return set_accumulator()

    def add(self, other):
        if isinstance(other, collections.abc.Set):
            set.update(self, other)
        else:
            set.add(self, other)


class dict_accumulator(dict, AccumulatorABC):
    '''
    Like a dict but also has accumulator semantics
    It is assumed that the contents of the dict have accumulator semantics
    '''
    def identity(self):
        ret = dict_accumulator()
        for key, value in self.items():
            ret[key] = value.identity()
        return ret

    def add(self, other):
        if isinstance(other, dict_accumulator):
            for key, value in other.items():
                if key not in self:
                    self[key] = value.identity()
                self[key] += value
        else:
            raise ValueError


class defaultdict_accumulator(collections.defaultdict, AccumulatorABC):
    '''
    Like a defaultdict but also has accumulator semantics
    It is assumed that the contents of the dict have accumulator semantics
    '''
    def identity(self):
        return defaultdict_accumulator(self.default_factory)

    def add(self, other):
        for key, value in other.items():
            self[key] += value
