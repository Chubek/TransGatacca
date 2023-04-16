import sys
from ctypes import *
from math import inf
from operator import *
from copy import copy, deepcopy


SELF_INSTANCE = 0
TYPE_INSTANCE = 1
INTG_INSTANCE = 2
OTHR_INSTANCE = -1


__TYPES_MAP = {
    "ZUint8": c_uint8,
    "ZUint16": c_uint16,
    "ZUint32": c_uint32,
    "ZUint64": c_uint64,
    "ZInt8": c_int8,
    "ZInt16": c_int16,
    "ZInt32": c_int32,
    "ZInt64": c_int64,
}

__TYPES_MAX = {
    "ZUint8": 0xff,
    "ZUint16": 0xffff,
    "ZUint32": 0xffffffff,
    "ZUint64": 0xffffffffffffffff,
    "ZInt8": 0x7f,
    "ZInt16": 0x7fff,
    "ZInt32": 0x7fffffff,
    "ZInt64": 0x7fffffffffffffff,
}

__TYPES_MIN = {
    "ZUint8": 0,
    "ZUint16": 0,
    "ZUint32": 0,
    "ZUint64": 0,
    "ZInt8": -0x80,
    "ZInt16": -0x80000,
    "ZInt32": -0x80000000,
    "ZInt64": -0x8000000000000000,
}

__DUNDERS_UNARY = {
    "__hash__": hash,
    "__hex__": hex,
    "__bin__": bin,
    "__oct__": oct,
    "__not__": not_,
    "__neg__": neg,
    "__pos__": pos,
}

__DUNDERS_BINARY = {
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
    "__lshift__": lshift,
    "__rshift__": rshift,
    "__lt__": lt,
    "__le__": le,
    "__eq__": eq,
    "__ne__": ne,
    "__ge__": ge,
    "__gt__": gt,
}

__DUNDERS_INPLACE = {
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


__FMT = {
    'b': bin,
    'o': oct,
    'x': hex,
}

def exec(func):
    globals()[func.__defaults__[0]] = func()
    return func

@exec
def generate_unary_dunders(_="UNARY_DUNDERS"):
    unary_dunderfuncs = {}

    for unary_dunder, unary_op in __DUNDERS_UNARY.items():

        def dunder_factory(unary_dunder, unary_op):
            def dunderfn(self):
                op = dunderfn.__dict__['op']
                return op(self.val)                  
              
            dunderfn.__dict__['op'] = unary_op
            dunderfn.__name__ = unary_dunder
            dunderfn.__qualname__ = unary_dunder
        
            return dunderfn

        unary_dunderfuncs[unary_dunder] = dunder_factory(unary_dunder, unary_op)

    return unary_dunderfuncs

@exec
def generate_binary_dunders(_="BINARY_DUNDERS"):
    binary_dunderfuncs = {}
    
    for binary_dunder, binary_op in __DUNDERS_BINARY.items():

        def dunder_factory(binary_dunder, binary_op):
            def dunderfn(self, other):
                op = dunderfn.__dict__['op']
                instance_check = self.__instancecheck__(other)

                if instance_check == SELF_INSTANCE:
                    res = op(self.val, other.__integer.value)
                elif instance_check == TYPE_INSTANCE:
                    res= op(self.val, other.value)
                elif instance_check == INTG_INSTANCE:
                    res = op(self.val, other)
                else:
                    raise TypeError(
                        f"Ilegal operation {op.__name__} between \
                            {self.clsname} and {other.__class__.__name__}")

                return self.clstype(res)
            
            dunderfn.__dict__['op'] = binary_op
            dunderfn.__name__ = binary_dunder
            dunderfn.__qualname__ = binary_dunder

            return dunderfn

        binary_dunderfuncs[binary_dunder] = dunder_factory(binary_dunder, binary_op)

    return binary_dunderfuncs

@exec
def generate_inplace_dunders(_="INPLACE_DUNDERS"):
    inplace_dunderfuncs = {}

    for inplace_dunder, inplace_op in __DUNDERS_INPLACE.items():
        
        def dunder_factory(inplace_dunder, inplace_op):
            def dunderfn(self, other):
                op = dunderfn.__dict__['op']

                instance_check = self.__instancecheck__(other)
                if instance_check == SELF_INSTANCE:
                    res = op(self.val, other.val)
                elif instance_check == TYPE_INSTANCE:
                    res= op(self.val, other.value)
                elif instance_check == INTG_INSTANCE:
                    res = op(self.val, other)
                else:
                    raise TypeError(
                        f"Ilegal operation {op.__name__} between \
                            {self.clsname} and {other.__class__.__name__}")

                self = self.clstype(res)
        
            dunderfn.__dict__['op'] = inplace_op
            dunderfn.__name__ = inplace_dunder
            dunderfn.__qualname__ = inplace_dunder

            return dunderfn
        
        inplace_dunderfuncs[inplace_dunder] = dunder_factory(inplace_dunder, inplace_op)
    
    return inplace_dunderfuncs

def init_zinteger(self, integer: int, mask=None):
    integer &= mask if integer >= 0 else integer
    self.__integer = self.ctype(integer)

def inst_zinteger(self, other) -> bool:
    cls_other = other.__class__
    cls_self = self.clsname
    cls_type = self.ctype
    cls_int = int(0).__class__

    if cls_self == cls_other:
        return SELF_INSTANCE
    elif cls_type == cls_other:
        return TYPE_INSTANCE
    elif cls_int == cls_other:
        return INTG_INSTANCE
    
    return OTHR_INSTANCE

def repr_zinteger(self) -> str:
    return f"<'Zinteger.{self.clsname}; Mapped={self.ctyname}; Value={self.val}'>"

def strn_zinteger(self) -> str:
    return str(self.val)

def frmt_zinteger(self, spec: str) -> str:
    fmtfn = frmt_zinteger.__dict__['frmt_zintegers']
    if any([spec.endswith(c) for c in ['b', 'o', 'x']]):
        fmt = spec[-1]
        prefix = "0" + fmt
        spec = spec.rstrip(fmt)
        if spec.startswith('0'):
            spec = spec.lstrip('0')
            numpad = int(spec)
            return ('0' * numpad) + fmtfn[fmt](self).lstrip(prefix)
        elif spec == '':
            return fmtfn[fmt](self).lstrip(prefix)
        else:
            return ""
    return ""

def docs_zinteger(ident_tyy, ident_slf, ident_min, ident_max):
    docs_tynm = ident_tyy.__name__
    docs_sign = "an unsigned" if ident_slf.startswith("ZUint") else "a signed"
    docs_bitw = ident_slf.lstrip("Z").lstrip("U").lstrip("I").lstrip("int")
    docs_strt = f"{ident_slf} takes {docs_sign}, {docs_bitw}-bit value of range [{ident_min}, {ident_max})"
    docs_ctyy = f"This class maps to ctype {docs_tynm} on your system. It may differ on other systems."
    docs_dndr = "ZIntmplements: " + ", ".join(__DUNDERS_BINARY.keys()) + ""
    docs_fmtt = "__format__ is implemented for [padding-enabled] b, o, x flags"
    docs_args = "Parameters:"
    docs_arg1 = ";integer: the given in-range integer"
    docs_arg2 = ";mask: the pre-masking bitmask (meaningless for negative integers)"
    docs_retr = "Returns:"
    docs_rett = "An instance of {}"
    docs_sepr = "-------"

    return "\n".join([
        docs_strt, docs_sepr, 
        docs_ctyy, docs_dndr, 
        docs_fmtt, docs_sepr, 
        docs_args, docs_arg1, 
        docs_arg2, docs_sepr, 
        docs_retr, docs_rett 
    ])

def gtvl_zinteger(self, name) -> int:
    if name == "value" or name == "val" or name == "int":
        return self.__integer.value
    elif name == "cint" or name == "cval" or name == "cvalue":
        return self.__integer
    elif name == "ctype" or name == "cty":
        return self.__tyy
    elif name == "ctyname":
        return self.__tyy.__name__
    elif name == "clsname":
        return self.__class__.__name__
    elif name == "clstype":
        return self.__class__
    elif name == "min" or name == "mimimum":
        return self.__min
    elif name == "max" or name == "maxmimum":
        return self.__max
    else:
        raise AttributeError

def zinteger(cls: type):
    dunderfuncs = {
        **globals()['UNARY_DUNDERS'],
        **globals()['BINARY_DUNDERS'],
        **globals()['INPLACE_DUNDERS'],
    }

    ident_slf = cls.__name__
    ident_min = __TYPES_MIN[ident_slf]
    ident_max = __TYPES_MAX[ident_slf]
    ident_tyy = __TYPES_MAP[ident_slf]

    this_init = copy(init_zinteger)
    this_frmt = copy(frmt_zinteger)
    this_inst = copy(inst_zinteger)
    this_repr = copy(repr_zinteger)
    this_strn = copy(strn_zinteger)
    this_gtvl = copy(gtvl_zinteger)

    this_docs = docs_zinteger(ident_tyy, ident_slf, ident_min, ident_max)

    this_init.__defaults__ = (ident_max, *this_init.__defaults__[1:])
    this_frmt.__dict__['frmt_zintegers'] = __FMT

    cls = type(ident_slf, (), {
        "__tyy": ident_tyy,
        "__min": ident_min,
        "__max": ident_max,
        "__idt": ident_slf,
        "__str__": this_strn,
        "__init__": this_init,
        "__repr__": this_repr,
        "__format__": this_frmt,
        "__getattr__": this_gtvl,
        "__instancecheck__": this_inst,
        **dunderfuncs
    })
    cls.__doc__ = this_docs
    cls.__str__.__name__ = "__str__"
    cls.__init__.__name__ = "__init__"
    cls.__repr__.__name__ = "__repr__"
    cls.__format__.__name__ = "__format__"
    cls.__instancecheck__.__name__ = "__instancecheck__"
    cls.__qualname__ = "Zinteger." + ident_slf

    return cls


@zinteger
class ZUint8:
    pass
@zinteger
class ZUint16:
    pass
@zinteger
class ZUint32:
    pass
@zinteger
class ZUint64:
    pass
@zinteger
class ZInt8:
    pass
@zinteger
class ZInt16:
    pass
@zinteger
class ZInt32:
    pass
@zinteger
class ZInt64:
    pass




z = ZUint8(1)

print(z + 1)


#if __name__ == "__main__":
  #  Zinteger.ZUint8.__test__()
   # Zinteger.ZUint16.__test__()
   # Zinteger.ZUint32.__test__()
   # Zinteger.Zuint64.__test__()

   # Zinteger.ZInt8.__test__()
   # Zinteger.ZInt16.__test__()
   # Zinteger.ZInt36.__test__()
  #  Zinteger.ZInt64.__test__()
