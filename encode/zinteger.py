from math import inf
from ctypes import *
from operator import *

__IDENTS = [
    "Zuint8",
    "Zuint16",
    "Zuint32",
    "Zuint64",
    "Zint8",
    "Zint16",
    "Zint32",
    "Zint64",
]

__TYPES_MAP = {
    "Zuint8": c_uint8,
    "Zuint16": c_uint16,
    "Zuint32": c_uint32,
    "Zuint64": c_uint64,
    "Zint8": c_int8,
    "Zint16": c_int16,
    "Zint32": c_int32,
    "Zint64": c_int64,
}

__TYPES_MAX = {
    "Zuint8": 0xff,
    "Zuint16": 0xffff,
    "Zuint32": 0xffffffff,
    "Zuint64": 0xffffffffffffffff,
    "Zint8": 0x7f,
    "Zint16": 0x7fff,
    "Zint32": 0x7fffffff,
    "Zint64": 0x7fffffffffffffff,
}

__TYPES_MIN = {
    "Zuint8": 0,
    "Zuint16": 0,
    "Zuint32": 0,
    "Zuint64": 0,
    "Zint8": -0x80,
    "Zint16": -0x80000,
    "Zint32": -0x80000000,
    "Zint64": -0x8000000000000000,
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
    "__hash__": hash,
    "__hex__": hex,
    "__bin__": bin,
    "__oct__": oct,
}

__FMT = {
    'b': bin,
    'o': oct,
    'x': hex,
}

def zinteger(cls: type):
    ident_slf = cls.__name__
    ident_min = __TYPES_MIN[ident_slf]
    ident_max = __TYPES_MAX[ident_slf]
    ident_tyy = __TYPES_MAP[ident_slf]

    cls.__tyy = ident_tyy
    cls.__max = ident_max
    cls.__min = ident_min

    def init_zinteger(self, integer: int, mask=None):
        assert(isinstance(int, integer), f"Zintnitiator for {self.__idt} must be of type int")
        integer &= mask if integer >= 0 else integer
        assert(self.__min <= integer <= self.__max, f"Zintnitiator for {self.__idt} must be [{self.__min}, {self.__max + 1})")
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
                    raise TypeError(f"Zintllegal operation betwee {self.__idt} and {type(other)}")
                
                op = dunderfn.__dict__['op']
                if is_self_instance:
                    res = op(self.__integer.value, other.integer.value)
                else:
                    res = op(self.__integer.value, other)
                
                assert(self.__min <= res <= self.__max, f"The result of {op.__name__} is out of bounds for {self.__idt}")
                return self.__tyy(res)
            
        dunderfn.__dict__['op'] = op
        cls.__dict__[dunder] = dunderfn

    def fmtfunc(self, spec: str) -> str:
        if any([spec.endswith(c) for c in ['b', 'o', 'x']]):
            fmt = spec[-1]
            prefix = "0" + fmt
            spec = spec.rstrip(fmt)
            if spec.startswith('0'):
                spec = spec.lstrip('0')
                numpad = int(spec)
                return ('0' * numpad) + __FMT[fmt](self).lstrip(prefix)
            elif spec == '':
                return __FMT[fmt](self).lstrip(prefix)
            else:
                return ""
    cls.__format__ = fmtfunc

    docs_tynm = ident_tyy.__name__
    docs_sign = "an unsigned" if ident_slf.startswith("Zuint") else "a signed"
    docs_strt = f"{ident_slf} takes {docs_sign} value of range [{ident_min}, {ident_max})"
    docs_ctyy = f"This class maps to ctype {docs_tynm} on your system"
    docs_dndr = "Zintmplements: " + ", ".join(__DUNDERS.keys()) + ""
    docs_fmtt = "__format__ is implemented for [padding-enabled] b, o, x flags"
    docs_args = "Parameters:"
    docs_arg1 = ";integer: the given in-range integer"
    docs_arg2 = ";mask: the pre-masking bitmask (meaningless for negative integers)"
    docs_retr = "Returns:"
    docs_rett = "An instance of {}"

    cls.__doc__ = "\n".join([
        docs_strt, docs_ctyy, docs_dndr, 
        docs_fmtt, docs_args, docs_arg1, 
        docs_arg2, docs_retr, docs_rett
    ])
    
    return cls


