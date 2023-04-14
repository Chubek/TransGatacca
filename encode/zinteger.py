from math import inf
from ctypes import *
from operator import *

__IDENTS = [
    "U8",
    "U16",
    "U32",
    "U64",
    "I8",
    "I16",
    "I32",
    "I64",
]

__TYPES_MAP = {
    "U8": c_uint8,
    "U16": c_uint16,
    "U32": c_uint32,
    "U64": c_uint64,
    "I8": c_int8,
    "I16": c_int16,
    "I32": c_int32,
    "I64": c_int64,
}

__TYPES_MAX = {
    "U8": 0xff,
    "U16": 0xffff,
    "U32": 0xffffffff,
    "U64": 0xffffffffffffffff,
    "I8": 0x7f,
    "I16": 0x7fff,
    "I32": 0x7fffffff,
    "I64": 0x7fffffffffffffff,
    "F32": inf,
    "F64": inf,
}

__TYPES_MIN = {
    "U8": 0,
    "U16": 0,
    "U32": 0,
    "U64": 0,
    "I8": -0x80,
    "I16": -0x80000,
    "I32": -0x80000000,
    "I64": -0x8000000000000000,
    "F32": -inf,
    "F64": -inf,
}

__DUNDERS = {
    "__add__": add,
    "__sub__": sub,
    "__mul__": mul,
    "__trudiv__": truediv,
    "__floordiv__": floordiv,
    "__mod__": mod,
    "__pow__": pow,
    "__and__": and_,
    "__or__": or_,
    "__xor__": xor,
    "__not__": not_,
    "__lshift__": lshift,
    "__rshift__": rshift,
    "__neg__": neg,
    "__pos__": pos,
    "__lt__": lt,
    "__le__": le,
    "__eq__": eq,
    "__ne__": ne,
    "__ge__": ge,
    "__gt__": gt,
    "__iadd__": iadd,
    "__isub__": isub,
    "__imul__": imul,
    "__itrudiv__": itruediv,
    "__ifloordiv__": ifloordiv,
    "__imod__": imod,
    "__ipow__": ipow,
    "__iand__": iand,
    "__ior__": ior,
    "__ixor__": ixor,
    "__ilshift__": ilshift,
    "__irshift__": irshift,
}


def generate_zinteger(cls: type):
    ident_slf = cls.__name__
    ident_min = __TYPES_MIN[ident_slf]
    ident_max = __TYPES_MAX[ident_slf]
    ident_tyy = __TYPES_MAP[ident_slf]

    cls.__tyy = ident_tyy
    cls.__max = ident_max
    cls.__min = ident_min

    def init_zinteger(self, integer: int, mask=None):
        assert(isinstance(int, integer), f"Initiator for {self.__idt} must be of type int")
        integer &= mask if integer >= 0 else integer
        assert(self.__min <= integer <= self.__max, f"Initiator for {self.__idt} must be [{self.__min}, {self.__max + 1})")
        self.__integer = integer
    init_zinteger.__defaults__[0] = cls.__max
    
    cls.__init__ = init_zinteger

    for dunder, op in __DUNDERS.items():
        if dunder.startswith("__i"):
            def dunderfn(self):
                op = dunderfn.__dict__['op']
                return op(self)
        else:
            def dunderfn(self, other):
                is_self_instance = isinstance(self.__tyy, other)
                is_comp_instance = isinstance(int, other)
                if not (is_self_instance or is_comp_instance):
                    raise TypeError(f"Illegal operation betwee {self.__idt} and {type(other)}")
                
                op = dunderfn.__dict__['op']
                if is_self_instance:
                    res = op(self.__integer.value, other.integer.value)
                else:
                    res = op(self.__integer.value, other)
                
                assert(self.__min <= res <= self.__max, f"The result of {op.__name__} is out of bounds for {self.__idt}")
                return self.__tyy(res)
            
        dunderfn.__dict__['op'] = op

        cls.__dict__[dunder] = dunderfn

    docs_tynm = ident_tyy.__name__
    docs_sign = "an unsigned" if ident_slf.startswith("U") else "a signed"
    docs_strt = f"{ident_slf} takes {docs_sign} value of range [{ident_min}, {ident_max})"
    docs_ctyy = f"This class maps to ctype {docs_tynm}"
    docs_dndr = "Implements: " + ", ".join(__DUNDERS.keys()) + ""
    docs_args = "Parameters:"
    docs_arg1 = ";integer: the given in-range integer"
    docs_arg2 = ";mask: the pre-masking bitmask (meaningless for negative integers)"
    docs_retr = "Returns:"
    docs_rett = "An instance of {}"

    cls.__doc__ = "\n".join([
        docs_strt, docs_ctyy, docs_dndr, 
        docs_args, docs_arg1, docs_arg2, 
        docs_retr, docs_rett])
    
    return cls