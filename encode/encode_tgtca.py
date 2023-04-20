#!/bin/python3

#############################################################################
# Copyright (c) 2023 Chubak Bidpaa                                          #
# Permission is hereby granted, free of charge, to any person obtaining     #
# a copy of this software and associated documentation files (the           #
# "Software"), to deal in the Software without restriction, including       #
# without limitation the rights to use, copy, modify, merge, publish,       #
# distribute, sublicense, and/or sell copies of the Software, and to        #
# permit persons to whom the Software is furnished to do so, subject to     #
# the following conditions:                                                 #
# The above copyright notice and this permission notice shall be            #
# included in all copies or substantial portions of the Software.           #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,           #
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF        #
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND                     #
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE    #
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION    #
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION     #
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.           #
#############################################################################

# Encode codon tables for a 64bit-width register or memory address
# Please read ENCODING.md for more info


from encode_data import GENETIC_TABLE, FREQ_TABLES
from zinteger import ZUint8 as U8
from zinteger import ZUint64 as U64
from itertools import product
from functools import reduce

NUC_GLYPHS = "ACGT"
PEP_GLYPHS = "ARNDCQEGHILKMFPSTWYV"

TYPE_CONTAINER = 0
TYPE_ENCODEOBJ = 1
TYPE_PACKEROBJ = 2
TYPE_MISCULANS = 2


NO_CALL_OBJECT = 0
DO_CALL_OBJECT = 1

class EncoderNS:
    pass

def execdescriptor(fn: callable, objident="EncoderNS"):
    results = fn()
    if fn.__defaults__ is None:
        raise ValueError("Type of emitted object not specified in function defaults")
    
    object_type, object_call = fn.__defaults__[0]
    if object_type in [TYPE_ENCODEOBJ, TYPE_PACKEROBJ, TYPE_MISCULANS]:
        descriptors = {
            k: type(k, (),
                    {"__get__": lambda _self, _cls, _inst: v if object_call == NO_CALL_OBJECT else v()
                            })() for k, v in results.items()}
    elif object_type == TYPE_CONTAINER:
        descriptors = { k: type(k, (), {"vals": v, "valtype": type(v[0]),
                     "__getitem__": lambda self, key: self.vals[key],
                     "__setitem__": lambda self, key, value: self.vals.__setitem__(key, self.valtype(value)),
                        })() for k, v in results.items()}
    else:
        raise TypeError("Unknown object type specified")

    globals()[objident] = type(
        objident, (), { 
        **descriptors, 
        **globals()[objident].__dict__
        }
    )

    return fn

def execfunction(fn: callable):
    fn()
    return fn

@execdescriptor
def fndescr_symbols(_=(TYPE_MISCULANS, NO_CALL_OBJECT)):
    return {
        "nucs": type("Nucleotides", (), {
            "glyphs": NUC_GLYPHS,
            "pbytes": bytearray(NUC_GLYPHS, encoding='ascii'),
            "cbytes": [U8(glyph) for glyph in bytearray(NUC_GLYPHS, encoding='ascii')],
            "glyphs_pmuted": list(map("".join, product(NUC_GLYPHS, repeat=3))),
            "pbytes_pmuted": list(product(bytearray(NUC_GLYPHS, encoding='ascii'), repeat=3)),
            "cbytes_pmuted": list(product([U8(glyph) for glyph in bytearray(NUC_GLYPHS, encoding='ascii')], repeat=3)),
        }),
        "peps": type("Peptides", (), {
            "glyphs": PEP_GLYPHS,
            "pbytes": bytearray(PEP_GLYPHS, encoding='ascii'),
            "cbytes": [U8(glyph) for glyph in bytearray(PEP_GLYPHS, encoding='ascii')]
        }),
    }

@execdescriptor
def fndescr_nuccontainers(_=(TYPE_CONTAINER, NO_CALL_OBJECT)):
    return {
        "nucs_cbytes_encoded": [U8(0)] * 4,
        "peps_cbytes_encoded": [U8(0)] * 20,
        "nucs_pmuted_upacked": [U8(0)] * 64,
        "nucs_pmuted_opacked": [U64(0)] * 8,
        "nucs_pmuted_encoded": [[U8(0)] * 3] * 64,
    }

@execdescriptor
def fndescr_uniencoders(_=(TYPE_ENCODEOBJ, DO_CALL_OBJECT)):
    return {
        "nuc_enctype": type(
                "NucEnctype", (), 
                {
                "__encode__": lambda  idx, nuc:  EncoderNS.nucs_cbytes_encoded.__setitem__(idx, (nuc >> 1) & 0b11),
                "__init__": lambda self: list(map(lambda i, nuc, self=self: self.__encode__(i, nuc), enumerate(EncoderNS.nucs.cbytes)))
                },
            ),
        "pep_enctype": type(
                "PepEnctype", (), 
                {
                "__encode__": lambda idx, pep: EncoderNS.peps_cbytes_encoded.__setitem__(idx, pep & 0b11111),
                "__init__": lambda self: list(map(lambda i, pep, self=self: self.__encode__(i, pep), enumerate(EncoderNS.peps.cbytes)))
                })
    }

@execdescriptor
def fndescr_tripencoders(_=(TYPE_ENCODEOBJ, DO_CALL_OBJECT)):
    return {
        "unitrip_enctype": type("TripEncoder", (), {
            "__encode__": lambda nuc1, nuc2, nuc3, idx: EncoderNS.__setitem
        })
    }

@execdescriptor
def fndescr_packtype(_=(TYPE_ENCODEOBJ, NO_CALL_OBJECT)):
    return {
        "unitriplet_packtype": type(
            "UniTripletPacktype", (),
            {
            "__trip_encdd": [U8(0)] * 3,
            "__trip_packd": U8(0),
            "__init__": lambda self, enc_trip, : list(map(lambda i, nuc, self=self: self.__trip_encdd[i].__setitem__(i, nuc), enumerate(enc_trip))),
            "__pack__": lambda 
    }),
        "octtriplet_packtype": type(
                        "UniTripletPacktype", (),
            {
                "__uni_packed": [[U8(0)] * 3] * 64,
                "__oct_packed": [U64(0)] * 8,
                "__pack_mainopr__": lambda self, unix, octx, slx: self.__oct_packed[octx].__ior__(self.uni_packed[unix].__lshift__(slx << 1)),
                "__pack_permute__": lambda self, oct, idx: list(map(lambda args, self=self: self.__pack_mainop__(*args), product(range(64), range(8), range(8)))),                    
                "__init__": lambda self, enc_trips: list(map(lambda i, trip, self=self: self.__uni_packed.__setitem__(i, trip), enumerate(enc_trips)))
            }
        ),
    }



@execdescriptor
def fndescr_packers():
    return {
        "packer_cbytetrip": lambda cbyte_trip, ident, i: ident.__setitem__(i, (n3 << 4) | (n2 << 2) | n1),
    }

@execdescriptor
def fndescr_4encodednucs(_=True):
    return {
        "encoded_nucs": [U8(0)] * 4
    }

@execdescriptor
def fndescr_8packedtriplets(_=True):
    return {
        "packed_triplets": type("PackedOctaDoubleWordInteger", (), {
            "__idx": U8(0),
            "__u64p": [U64(0)] * 8,
            "__ilshift__": lambda self, amount: self.__u64p[self.__idx.val].__ilshift(amount),
            "__ior__": lambda self, imm: self.__u64p[self.__idx.val].__ior__(imm),
            "__lshift__": lambda self, imm: self.__u64p[self.__idx.val].__lshift__(imm),
            "__or__": lambda self, imm: self.__u64p[self.__idx.val].__or__(imm),
            "__pos__": lambda self: self.__idx.__iadd__(1),
            "__neg__": lambda self: self.__idx.__isub__(1),
            "__pack__": 
        })(),
    }


@execdescriptor
def fndescr_20encodedpeps(_=True):
    return {
        "encoded_peps": [U8(0)] * 20
    }

@execdescriptor
def fndescr_64triplets(_=True):
    return {
        "cbyte_triplets": type("CbyteTriplet", (), {
            ""
        }),
        "glyph_triplets": ["\0\0\0"] * 64, 
        "pack_triplets": [U8(0)] * 64
    }


@execfunction
def fnfunc_encodenucs():
    for i, nuccbyte in enumerate(EncoderNS.nuc_cbytes):
        EncoderNS.encoded_nucs[i] = (nuccbyte >> 1) & 3
        EncoderNS.nucs_encodd = EncoderNS.encoded_nucs

@execfunction
def fnfunc_encodepeps():
    for i, pepcbyte in enumerate(EncoderNS.pep_cbytes):
        EncoderNS.encoded_peps[i] = pepcbyte & 31

@execfunction
def fnfunc_gentriplets():
    permute_glyphs = product(EncoderNS.nuc_glyphs, repeat=3)
    permute_cbytes = product(EncoderNS.nuc_cbytes, repeat=3)
    permute_encodd = product(EncoderNS.nuc_encodd, repeat=3)

    for i, (permglyph, permcbyte, permencdd) in zip(permute_glyphs, permute_cbytes, permute_encodd):
        EncoderNS.cbyte_triplets = 


    

