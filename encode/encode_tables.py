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


GENETIC_TABLE = {
    "1": {
        b"F": [b"TTT", b"TTC"],
        b"L": [b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG"],
        b"S": [b"TCT", b"TCC", b"TCA", b"TCG", b"AGT", b"AGC"],
        b"Y": [b"TAT", b"TAC"],
        b"*": [b"TAA", b"TAG", b"TGA"],
        b"C": [b"TGT", b"TGC"],
        b"W": [b"TGG"],
        b"P": [b"CCT", b"CCC", b"CCA", b"CCG"],
        b"H": [b"CAT", b"CAC"],
        b"Q": [b"CAA", b"CAG"],
        b"R": [b"CGT", b"CGC", b"CGA", b"CGG", b"AGA", b"AGG"],
        b"I": [b"ATT", b"ATC", b"ATA"],
        b"M": [b"ATG"],
        b"T": [b"ACT", b"ACC", b"ACA", b"ACG"],
        b"N": [b"AAT", b"AAC"],
        b"K": [b"AAA", b"AAG"],
        b"V": [b"GTT", b"GTC", b"GTA", b"GTG"],
        b"A": [b"GCT", b"GCC", b"GCA", b"GCG"],
        b"D": [b"GAT", b"GAC"],
        b"E": [b"GAA", b"GAG"],
        b"G": [b"GGT", b"GGC", b"GGA", b"GGG"],
        b"X": [],
        b"B": [b"AAT", b"AAC", b"GAT", b"GAC"],
        b"J": [
            b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG", b"ATT", b"ATC",
            b"ATA"
        ],
        b"Z": [b"CAA", b"CAG", b"GAA", b"GAG"]
    },
    "2": {
        b"F": [b"TTT", b"TTC"],
        b"L": [b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG"],
        b"S": [b"TCT", b"TCC", b"TCA", b"TCG", b"AGT", b"AGC"],
        b"Y": [b"TAT", b"TAC"],
        b"*": [b"TAA", b"TAG", b"AGA", b"AGG"],
        b"C": [b"TGT", b"TGC"],
        b"W": [b"TGA", b"TGG"],
        b"P": [b"CCT", b"CCC", b"CCA", b"CCG"],
        b"H": [b"CAT", b"CAC"],
        b"Q": [b"CAA", b"CAG"],
        b"R": [b"CGT", b"CGC", b"CGA", b"CGG"],
        b"I": [b"ATT", b"ATC"],
        b"M": [b"ATA", b"ATG"],
        b"T": [b"ACT", b"ACC", b"ACA", b"ACG"],
        b"N": [b"AAT", b"AAC"],
        b"K": [b"AAA", b"AAG"],
        b"V": [b"GTT", b"GTC", b"GTA", b"GTG"],
        b"A": [b"GCT", b"GCC", b"GCA", b"GCG"],
        b"D": [b"GAT", b"GAC"],
        b"E": [b"GAA", b"GAG"],
        b"G": [b"GGT", b"GGC", b"GGA", b"GGG"],
        b"B": [b"AAT", b"AAC", b"GAT", b"GAC"],
        b"J": [b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG", b"ATT", b"ATC"],
        b"Z": [b"CAA", b"CAG", b"GAA", b"GAG"]
    },
    "3": {
        b"F": [b"TTT", b"TTC"],
        b"L": [b"TTA", b"TTG"],
        b"S": [b"TCT", b"TCC", b"TCA", b"TCG", b"AGT", b"AGC"],
        b"Y": [b"TAT", b"TAC"],
        b"*": [b"TAA", b"TAG"],
        b"C": [b"TGT", b"TGC"],
        b"W": [b"TGA", b"TGG"],
        b"T": [b"CTT", b"CTC", b"CTA", b"CTG", b"ACT", b"ACC", b"ACA", b"ACG"],
        b"P": [b"CCT", b"CCC", b"CCA", b"CCG"],
        b"H": [b"CAT", b"CAC"],
        b"Q": [b"CAA", b"CAG"],
        b"R": [b"CGT", b"CGC", b"CGA", b"CGG", b"AGA", b"AGG"],
        b"I": [b"ATT", b"ATC"],
        b"M": [b"ATA", b"ATG"],
        b"N": [b"AAT", b"AAC"],
        b"K": [b"AAA", b"AAG"],
        b"V": [b"GTT", b"GTC", b"GTA", b"GTG"],
        b"A": [b"GCT", b"GCC", b"GCA", b"GCG"],
        b"D": [b"GAT", b"GAC"],
        b"E": [b"GAA", b"GAG"],
        b"G": [b"GGT", b"GGC", b"GGA", b"GGG"],
        b"X": [],
        b"B": [b"AAT", b"AAC", b"GAT", b"GAC"],
        b"J": [b"TTA", b"TTG", b"ATT", b"ATC"],
        b"Z": [b"CAA", b"CAG", b"GAA", b"GAG"]
    },
    "4": {
        b"F": [b"TTT", b"TTC"],
        b"L": [b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG"],
        b"S": [b"TCT", b"TCC", b"TCA", b"TCG", b"AGT", b"AGC"],
        b"Y": [b"TAT", b"TAC"],
        b"*": [b"TAA", b"TAG"],
        b"C": [b"TGT", b"TGC"],
        b"W": [b"TGA", b"TGG"],
        b"P": [b"CCT", b"CCC", b"CCA", b"CCG"],
        b"H": [b"CAT", b"CAC"],
        b"Q": [b"CAA", b"CAG"],
        b"R": [b"CGT", b"CGC", b"CGA", b"CGG", b"AGA", b"AGG"],
        b"I": [b"ATT", b"ATC", b"ATA"],
        b"M": [b"ATG"],
        b"T": [b"ACT", b"ACC", b"ACA", b"ACG"],
        b"N": [b"AAT", b"AAC"],
        b"K": [b"AAA", b"AAG"],
        b"V": [b"GTT", b"GTC", b"GTA", b"GTG"],
        b"A": [b"GCT", b"GCC", b"GCA", b"GCG"],
        b"D": [b"GAT", b"GAC"],
        b"E": [b"GAA", b"GAG"],
        b"G": [b"GGT", b"GGC", b"GGA", b"GGG"],
        b"X": [],
        b"B": [b"AAT", b"AAC", b"GAT", b"GAC"],
        b"J": [
            b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG", b"ATT", b"ATC",
            b"ATA"
        ],
        b"Z": [b"CAA", b"CAG", b"GAA", b"GAG"]
    },
    "5": {
        b"F": [b"TTT", b"TTC"],
        b"L": [b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG"],
        b"S": [b"TCT", b"TCC", b"TCA", b"TCG", b"AGT", b"AGC", b"AGA", b"AGG"],
        b"Y": [b"TAT", b"TAC"],
        b"*": [b"TAA", b"TAG"],
        b"C": [b"TGT", b"TGC"],
        b"W": [b"TGA", b"TGG"],
        b"P": [b"CCT", b"CCC", b"CCA", b"CCG"],
        b"H": [b"CAT", b"CAC"],
        b"Q": [b"CAA", b"CAG"],
        b"R": [b"CGT", b"CGC", b"CGA", b"CGG"],
        b"I": [b"ATT", b"ATC"],
        b"M": [b"ATA", b"ATG"],
        b"T": [b"ACT", b"ACC", b"ACA", b"ACG"],
        b"N": [b"AAT", b"AAC"],
        b"K": [b"AAA", b"AAG"],
        b"V": [b"GTT", b"GTC", b"GTA", b"GTG"],
        b"A": [b"GCT", b"GCC", b"GCA", b"GCG"],
        b"D": [b"GAT", b"GAC"],
        b"E": [b"GAA", b"GAG"],
        b"G": [b"GGT", b"GGC", b"GGA", b"GGG"],
        b"X": [],
        b"B": [b"AAT", b"AAC", b"GAT", b"GAC"],
        b"J": [b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG", b"ATT", b"ATC"],
        b"Z": [b"CAA", b"CAG", b"GAA", b"GAG"]
    },
    "6": {
        b"F": [b"TTT", b"TTC"],
        b"L": [b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG"],
        b"S": [b"TCT", b"TCC", b"TCA", b"TCG", b"AGT", b"AGC"],
        b"Y": [b"TAT", b"TAC"],
        b"Q": [b"TAA", b"TAG", b"CAA", b"CAG"],
        b"C": [b"TGT", b"TGC"],
        b"*": [b"TGA"],
        b"W": [b"TGG"],
        b"P": [b"CCT", b"CCC", b"CCA", b"CCG"],
        b"H": [b"CAT", b"CAC"],
        b"R": [b"CGT", b"CGC", b"CGA", b"CGG", b"AGA", b"AGG"],
        b"I": [b"ATT", b"ATC", b"ATA"],
        b"M": [b"ATG"],
        b"T": [b"ACT", b"ACC", b"ACA", b"ACG"],
        b"N": [b"AAT", b"AAC"],
        b"K": [b"AAA", b"AAG"],
        b"V": [b"GTT", b"GTC", b"GTA", b"GTG"],
        b"A": [b"GCT", b"GCC", b"GCA", b"GCG"],
        b"D": [b"GAT", b"GAC"],
        b"E": [b"GAA", b"GAG"],
        b"G": [b"GGT", b"GGC", b"GGA", b"GGG"],
        b"X": [],
        b"B": [b"AAT", b"AAC", b"GAT", b"GAC"],
        b"J": [
            b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG", b"ATT", b"ATC",
            b"ATA"
        ],
        b"Z": [b"TAA", b"TAG", b"CAA", b"CAG", b"GAA", b"GAG"]
    },
    "9": {
        b"F": [b"TTT", b"TTC"],
        b"L": [b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG"],
        b"S": [b"TCT", b"TCC", b"TCA", b"TCG", b"AGT", b"AGC", b"AGA", b"AGG"],
        b"Y": [b"TAT", b"TAC"],
        b"*": [b"TAA", b"TAG"],
        b"C": [b"TGT", b"TGC"],
        b"W": [b"TGA", b"TGG"],
        b"P": [b"CCT", b"CCC", b"CCA", b"CCG"],
        b"H": [b"CAT", b"CAC"],
        b"Q": [b"CAA", b"CAG"],
        b"R": [b"CGT", b"CGC", b"CGA", b"CGG"],
        b"I": [b"ATT", b"ATC", b"ATA"],
        b"M": [b"ATG"],
        b"T": [b"ACT", b"ACC", b"ACA", b"ACG"],
        b"N": [b"AAT", b"AAC", b"AAA"],
        b"K": [b"AAG"],
        b"V": [b"GTT", b"GTC", b"GTA", b"GTG"],
        b"A": [b"GCT", b"GCC", b"GCA", b"GCG"],
        b"D": [b"GAT", b"GAC"],
        b"E": [b"GAA", b"GAG"],
        b"G": [b"GGT", b"GGC", b"GGA", b"GGG"],
        b"X": [],
        b"B": [b"AAT", b"AAC", b"AAA", b"GAT", b"GAC"],
        b"J": [
            b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG", b"ATT", b"ATC",
            b"ATA"
        ],
        b"Z": [b"CAA", b"CAG", b"GAA", b"GAG"]
    },
    "10": {
        b"F": [b"TTT", b"TTC"],
        b"L": [b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG"],
        b"S": [b"TCT", b"TCC", b"TCA", b"TCG", b"AGT", b"AGC"],
        b"Y": [b"TAT", b"TAC"],
        b"*": [b"TAA", b"TAG"],
        b"C": [b"TGT", b"TGC", b"TGA"],
        b"W": [b"TGG"],
        b"P": [b"CCT", b"CCC", b"CCA", b"CCG"],
        b"H": [b"CAT", b"CAC"],
        b"Q": [b"CAA", b"CAG"],
        b"R": [b"CGT", b"CGC", b"CGA", b"CGG", b"AGA", b"AGG"],
        b"I": [b"ATT", b"ATC", b"ATA"],
        b"M": [b"ATG"],
        b"T": [b"ACT", b"ACC", b"ACA", b"ACG"],
        b"N": [b"AAT", b"AAC"],
        b"K": [b"AAA", b"AAG"],
        b"V": [b"GTT", b"GTC", b"GTA", b"GTG"],
        b"A": [b"GCT", b"GCC", b"GCA", b"GCG"],
        b"D": [b"GAT", b"GAC"],
        b"E": [b"GAA", b"GAG"],
        b"G": [b"GGT", b"GGC", b"GGA", b"GGG"],
        b"X": [],
        b"B": [b"AAT", b"AAC", b"GAT", b"GAC"],
        b"J": [
            b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG", b"ATT", b"ATC",
            b"ATA"
        ],
        b"Z": [b"CAA", b"CAG", b"GAA", b"GAG"]
    },
    "11": {
        b"F": [b"TTT", b"TTC"],
        b"L": [b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG"],
        b"S": [b"TCT", b"TCC", b"TCA", b"TCG", b"AGT", b"AGC"],
        b"Y": [b"TAT", b"TAC"],
        b"*": [b"TAA", b"TAG", b"TGA"],
        b"C": [b"TGT", b"TGC"],
        b"W": [b"TGG"],
        b"P": [b"CCT", b"CCC", b"CCA", b"CCG"],
        b"H": [b"CAT", b"CAC"],
        b"Q": [b"CAA", b"CAG"],
        b"R": [b"CGT", b"CGC", b"CGA", b"CGG", b"AGA", b"AGG"],
        b"I": [b"ATT", b"ATC", b"ATA"],
        b"M": [b"ATG"],
        b"T": [b"ACT", b"ACC", b"ACA", b"ACG"],
        b"N": [b"AAT", b"AAC"],
        b"K": [b"AAA", b"AAG"],
        b"V": [b"GTT", b"GTC", b"GTA", b"GTG"],
        b"A": [b"GCT", b"GCC", b"GCA", b"GCG"],
        b"D": [b"GAT", b"GAC"],
        b"E": [b"GAA", b"GAG"],
        b"G": [b"GGT", b"GGC", b"GGA", b"GGG"],
        b"X": [],
        b"B": [b"AAT", b"AAC", b"GAT", b"GAC"],
        b"J": [
            b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG", b"ATT", b"ATC",
            b"ATA"
        ],
        b"Z": [b"CAA", b"CAG", b"GAA", b"GAG"]
    },
    "12": {
        b"F": [b"TTT", b"TTC"],
        b"L": [b"TTA", b"TTG", b"CTT", b"CTC", b"CTA"],
        b"S": [b"TCT", b"TCC", b"TCA", b"TCG", b"CTG", b"AGT", b"AGC"],
        b"Y": [b"TAT", b"TAC"],
        b"*": [b"TAA", b"TAG", b"TGA"],
        b"C": [b"TGT", b"TGC"],
        b"W": [b"TGG"],
        b"P": [b"CCT", b"CCC", b"CCA", b"CCG"],
        b"H": [b"CAT", b"CAC"],
        b"Q": [b"CAA", b"CAG"],
        b"R": [b"CGT", b"CGC", b"CGA", b"CGG", b"AGA", b"AGG"],
        b"I": [b"ATT", b"ATC", b"ATA"],
        b"M": [b"ATG"],
        b"T": [b"ACT", b"ACC", b"ACA", b"ACG"],
        b"N": [b"AAT", b"AAC"],
        b"K": [b"AAA", b"AAG"],
        b"V": [b"GTT", b"GTC", b"GTA", b"GTG"],
        b"A": [b"GCT", b"GCC", b"GCA", b"GCG"],
        b"D": [b"GAT", b"GAC"],
        b"E": [b"GAA", b"GAG"],
        b"G": [b"GGT", b"GGC", b"GGA", b"GGG"],
        b"X": [],
        b"B": [b"AAT", b"AAC", b"GAT", b"GAC"],
        b"J": [b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"ATT", b"ATC", b"ATA"],
        b"Z": [b"CAA", b"CAG", b"GAA", b"GAG"]
    },
    "13": {
        b"F": [b"TTT", b"TTC"],
        b"L": [b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG"],
        b"S": [b"TCT", b"TCC", b"TCA", b"TCG", b"AGT", b"AGC"],
        b"Y": [b"TAT", b"TAC"],
        b"*": [b"TAA", b"TAG"],
        b"C": [b"TGT", b"TGC"],
        b"W": [b"TGA", b"TGG"],
        b"P": [b"CCT", b"CCC", b"CCA", b"CCG"],
        b"H": [b"CAT", b"CAC"],
        b"Q": [b"CAA", b"CAG"],
        b"R": [b"CGT", b"CGC", b"CGA", b"CGG"],
        b"I": [b"ATT", b"ATC"],
        b"M": [b"ATA", b"ATG"],
        b"T": [b"ACT", b"ACC", b"ACA", b"ACG"],
        b"N": [b"AAT", b"AAC"],
        b"K": [b"AAA", b"AAG"],
        b"G": [b"AGA", b"AGG", b"GGT", b"GGC", b"GGA", b"GGG"],
        b"V": [b"GTT", b"GTC", b"GTA", b"GTG"],
        b"A": [b"GCT", b"GCC", b"GCA", b"GCG"],
        b"D": [b"GAT", b"GAC"],
        b"E": [b"GAA", b"GAG"],
        b"X": [],
        b"B": [b"AAT", b"AAC", b"GAT", b"GAC"],
        b"J": [b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG", b"ATT", b"ATC"],
        b"Z": [b"CAA", b"CAG", b"GAA", b"GAG"]
    },
    "14": {
        b"F": [b"TTT", b"TTC"],
        b"L": [b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG"],
        b"S": [b"TCT", b"TCC", b"TCA", b"TCG", b"AGT", b"AGC", b"AGA", b"AGG"],
        b"Y": [b"TAT", b"TAC", b"TAA"],
        b"*": [b"TAG"],
        b"C": [b"TGT", b"TGC"],
        b"W": [b"TGA", b"TGG"],
        b"P": [b"CCT", b"CCC", b"CCA", b"CCG"],
        b"H": [b"CAT", b"CAC"],
        b"Q": [b"CAA", b"CAG"],
        b"R": [b"CGT", b"CGC", b"CGA", b"CGG"],
        b"I": [b"ATT", b"ATC", b"ATA"],
        b"M": [b"ATG"],
        b"T": [b"ACT", b"ACC", b"ACA", b"ACG"],
        b"N": [b"AAT", b"AAC", b"AAA"],
        b"K": [b"AAG"],
        b"V": [b"GTT", b"GTC", b"GTA", b"GTG"],
        b"A": [b"GCT", b"GCC", b"GCA", b"GCG"],
        b"D": [b"GAT", b"GAC"],
        b"E": [b"GAA", b"GAG"],
        b"G": [b"GGT", b"GGC", b"GGA", b"GGG"],
        b"X": [],
        b"B": [b"AAT", b"AAC", b"AAA", b"GAT", b"GAC"],
        b"J": [
            b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG", b"ATT", b"ATC",
            b"ATA"
        ],
        b"Z": [b"CAA", b"CAG", b"GAA", b"GAG"]
    },
    "15": {
        b"F": [b"TTT", b"TTC"],
        b"L": [b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG"],
        b"S": [b"TCT", b"TCC", b"TCA", b"TCG", b"AGT", b"AGC"],
        b"Y": [b"TAT", b"TAC"],
        b"*": [b"TAA", b"TGA"],
        b"Q": [b"TAG", b"CAA", b"CAG"],
        b"C": [b"TGT", b"TGC"],
        b"W": [b"TGG"],
        b"P": [b"CCT", b"CCC", b"CCA", b"CCG"],
        b"H": [b"CAT", b"CAC"],
        b"R": [b"CGT", b"CGC", b"CGA", b"CGG", b"AGA", b"AGG"],
        b"I": [b"ATT", b"ATC", b"ATA"],
        b"M": [b"ATG"],
        b"T": [b"ACT", b"ACC", b"ACA", b"ACG"],
        b"N": [b"AAT", b"AAC"],
        b"K": [b"AAA", b"AAG"],
        b"V": [b"GTT", b"GTC", b"GTA", b"GTG"],
        b"A": [b"GCT", b"GCC", b"GCA", b"GCG"],
        b"D": [b"GAT", b"GAC"],
        b"E": [b"GAA", b"GAG"],
        b"G": [b"GGT", b"GGC", b"GGA", b"GGG"],
        b"X": [],
        b"B": [b"AAT", b"AAC", b"GAT", b"GAC"],
        b"J": [
            b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG", b"ATT", b"ATC",
            b"ATA"
        ],
        b"Z": [b"TAG", b"CAA", b"CAG", b"GAA", b"GAG"]
    },
    "16": {
        b"F": [b"TTT", b"TTC"],
        b"L": [b"TTA", b"TTG", b"TAG", b"CTT", b"CTC", b"CTA", b"CTG"],
        b"S": [b"TCT", b"TCC", b"TCA", b"TCG", b"AGT", b"AGC"],
        b"Y": [b"TAT", b"TAC"],
        b"*": [b"TAA", b"TGA"],
        b"C": [b"TGT", b"TGC"],
        b"W": [b"TGG"],
        b"P": [b"CCT", b"CCC", b"CCA", b"CCG"],
        b"H": [b"CAT", b"CAC"],
        b"Q": [b"CAA", b"CAG"],
        b"R": [b"CGT", b"CGC", b"CGA", b"CGG", b"AGA", b"AGG"],
        b"I": [b"ATT", b"ATC", b"ATA"],
        b"M": [b"ATG"],
        b"T": [b"ACT", b"ACC", b"ACA", b"ACG"],
        b"N": [b"AAT", b"AAC"],
        b"K": [b"AAA", b"AAG"],
        b"V": [b"GTT", b"GTC", b"GTA", b"GTG"],
        b"A": [b"GCT", b"GCC", b"GCA", b"GCG"],
        b"D": [b"GAT", b"GAC"],
        b"E": [b"GAA", b"GAG"],
        b"G": [b"GGT", b"GGC", b"GGA", b"GGG"],
        b"X": [],
        b"B": [b"AAT", b"AAC", b"GAT", b"GAC"],
        b"J": [
            b"TTA", b"TTG", b"TAG", b"CTT", b"CTC", b"CTA", b"CTG", b"ATT",
            b"ATC", b"ATA"
        ],
        b"Z": [b"CAA", b"CAG", b"GAA", b"GAG"]
    },
    "21": {
        b"F": [b"TTT", b"TTC"],
        b"L": [b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG"],
        b"S": [b"TCT", b"TCC", b"TCA", b"TCG", b"AGT", b"AGC", b"AGA", b"AGG"],
        b"Y": [b"TAT", b"TAC"],
        b"*": [b"TAA", b"TAG"],
        b"C": [b"TGT", b"TGC"],
        b"W": [b"TGA", b"TGG"],
        b"P": [b"CCT", b"CCC", b"CCA", b"CCG"],
        b"H": [b"CAT", b"CAC"],
        b"Q": [b"CAA", b"CAG"],
        b"R": [b"CGT", b"CGC", b"CGA", b"CGG"],
        b"I": [b"ATT", b"ATC"],
        b"M": [b"ATA", b"ATG"],
        b"T": [b"ACT", b"ACC", b"ACA", b"ACG"],
        b"N": [b"AAT", b"AAC", b"AAA"],
        b"K": [b"AAG"],
        b"V": [b"GTT", b"GTC", b"GTA", b"GTG"],
        b"A": [b"GCT", b"GCC", b"GCA", b"GCG"],
        b"D": [b"GAT", b"GAC"],
        b"E": [b"GAA", b"GAG"],
        b"G": [b"GGT", b"GGC", b"GGA", b"GGG"],
        b"X": [],
        b"B": [b"AAT", b"AAC", b"AAA", b"GAT", b"GAC"],
        b"J": [b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG", b"ATT", b"ATC"],
        b"Z": [b"CAA", b"CAG", b"GAA", b"GAG"]
    },
    "22": {
        b"F": [b"TTT", b"TTC"],
        b"L": [b"TTA", b"TTG", b"TAG", b"CTT", b"CTC", b"CTA", b"CTG"],
        b"S": [b"TCT", b"TCC", b"TCG", b"AGT", b"AGC"],
        b"*": [b"TCA", b"TAA", b"TGA"],
        b"Y": [b"TAT", b"TAC"],
        b"C": [b"TGT", b"TGC"],
        b"W": [b"TGG"],
        b"P": [b"CCT", b"CCC", b"CCA", b"CCG"],
        b"H": [b"CAT", b"CAC"],
        b"Q": [b"CAA", b"CAG"],
        b"R": [b"CGT", b"CGC", b"CGA", b"CGG", b"AGA", b"AGG"],
        b"I": [b"ATT", b"ATC", b"ATA"],
        b"M": [b"ATG"],
        b"T": [b"ACT", b"ACC", b"ACA", b"ACG"],
        b"N": [b"AAT", b"AAC"],
        b"K": [b"AAA", b"AAG"],
        b"V": [b"GTT", b"GTC", b"GTA", b"GTG"],
        b"A": [b"GCT", b"GCC", b"GCA", b"GCG"],
        b"D": [b"GAT", b"GAC"],
        b"E": [b"GAA", b"GAG"],
        b"G": [b"GGT", b"GGC", b"GGA", b"GGG"],
        b"X": [],
        b"B": [b"AAT", b"AAC", b"GAT", b"GAC"],
        b"J": [
            b"TTA", b"TTG", b"TAG", b"CTT", b"CTC", b"CTA", b"CTG", b"ATT",
            b"ATC", b"ATA"
        ],
        b"Z": [b"CAA", b"CAG", b"GAA", b"GAG"]
    },
    "23": {
        b"F": [b"TTT", b"TTC"],
        b"*": [b"TTA", b"TAA", b"TAG", b"TGA"],
        b"L": [b"TTG", b"CTT", b"CTC", b"CTA", b"CTG"],
        b"S": [b"TCT", b"TCC", b"TCA", b"TCG", b"AGT", b"AGC"],
        b"Y": [b"TAT", b"TAC"],
        b"C": [b"TGT", b"TGC"],
        b"W": [b"TGG"],
        b"P": [b"CCT", b"CCC", b"CCA", b"CCG"],
        b"H": [b"CAT", b"CAC"],
        b"Q": [b"CAA", b"CAG"],
        b"R": [b"CGT", b"CGC", b"CGA", b"CGG", b"AGA", b"AGG"],
        b"I": [b"ATT", b"ATC", b"ATA"],
        b"M": [b"ATG"],
        b"T": [b"ACT", b"ACC", b"ACA", b"ACG"],
        b"N": [b"AAT", b"AAC"],
        b"K": [b"AAA", b"AAG"],
        b"V": [b"GTT", b"GTC", b"GTA", b"GTG"],
        b"A": [b"GCT", b"GCC", b"GCA", b"GCG"],
        b"D": [b"GAT", b"GAC"],
        b"E": [b"GAA", b"GAG"],
        b"G": [b"GGT", b"GGC", b"GGA", b"GGG"],
        b"X": [],
        b"B": [b"AAT", b"AAC", b"GAT", b"GAC"],
        b"J": [b"TTG", b"CTT", b"CTC", b"CTA", b"CTG", b"ATT", b"ATC", b"ATA"],
        b"Z": [b"CAA", b"CAG", b"GAA", b"GAG"]
    },
    "24": {
        b"F": [b"TTT", b"TTC"],
        b"L": [b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG"],
        b"S": [b"TCT", b"TCC", b"TCA", b"TCG", b"AGT", b"AGC", b"AGA"],
        b"Y": [b"TAT", b"TAC"],
        b"*": [b"TAA", b"TAG"],
        b"C": [b"TGT", b"TGC"],
        b"W": [b"TGA", b"TGG"],
        b"P": [b"CCT", b"CCC", b"CCA", b"CCG"],
        b"H": [b"CAT", b"CAC"],
        b"Q": [b"CAA", b"CAG"],
        b"R": [b"CGT", b"CGC", b"CGA", b"CGG"],
        b"I": [b"ATT", b"ATC", b"ATA"],
        b"M": [b"ATG"],
        b"T": [b"ACT", b"ACC", b"ACA", b"ACG"],
        b"N": [b"AAT", b"AAC"],
        b"K": [b"AAA", b"AAG", b"AGG"],
        b"V": [b"GTT", b"GTC", b"GTA", b"GTG"],
        b"A": [b"GCT", b"GCC", b"GCA", b"GCG"],
        b"D": [b"GAT", b"GAC"],
        b"E": [b"GAA", b"GAG"],
        b"G": [b"GGT", b"GGC", b"GGA", b"GGG"],
        b"X": [],
        b"B": [b"AAT", b"AAC", b"GAT", b"GAC"],
        b"J": [
            b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG", b"ATT", b"ATC",
            b"ATA"
        ],
        b"Z": [b"CAA", b"CAG", b"GAA", b"GAG"]
    },
    "25": {
        b"F": [b"TTT", b"TTC"],
        b"L": [b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG"],
        b"S": [b"TCT", b"TCC", b"TCA", b"TCG", b"AGT", b"AGC"],
        b"Y": [b"TAT", b"TAC"],
        b"*": [b"TAA", b"TAG"],
        b"C": [b"TGT", b"TGC"],
        b"G": [b"TGA", b"GGT", b"GGC", b"GGA", b"GGG"],
        b"W": [b"TGG"],
        b"P": [b"CCT", b"CCC", b"CCA", b"CCG"],
        b"H": [b"CAT", b"CAC"],
        b"Q": [b"CAA", b"CAG"],
        b"R": [b"CGT", b"CGC", b"CGA", b"CGG", b"AGA", b"AGG"],
        b"I": [b"ATT", b"ATC", b"ATA"],
        b"M": [b"ATG"],
        b"T": [b"ACT", b"ACC", b"ACA", b"ACG"],
        b"N": [b"AAT", b"AAC"],
        b"K": [b"AAA", b"AAG"],
        b"V": [b"GTT", b"GTC", b"GTA", b"GTG"],
        b"A": [b"GCT", b"GCC", b"GCA", b"GCG"],
        b"D": [b"GAT", b"GAC"],
        b"E": [b"GAA", b"GAG"],
        b"X": [],
        b"B": [b"AAT", b"AAC", b"GAT", b"GAC"],
        b"J": [
            b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG", b"ATT", b"ATC",
            b"ATA"
        ],
        b"Z": [b"CAA", b"CAG", b"GAA", b"GAG"]
    },
    "26": {
        b"F": [b"TTT", b"TTC"],
        b"L": [b"TTA", b"TTG", b"CTT", b"CTC", b"CTA"],
        b"S": [b"TCT", b"TCC", b"TCA", b"TCG", b"AGT", b"AGC"],
        b"Y": [b"TAT", b"TAC"],
        b"*": [b"TAA", b"TAG", b"TGA"],
        b"C": [b"TGT", b"TGC"],
        b"W": [b"TGG"],
        b"A": [b"CTG", b"GCT", b"GCC", b"GCA", b"GCG"],
        b"P": [b"CCT", b"CCC", b"CCA", b"CCG"],
        b"H": [b"CAT", b"CAC"],
        b"Q": [b"CAA", b"CAG"],
        b"R": [b"CGT", b"CGC", b"CGA", b"CGG", b"AGA", b"AGG"],
        b"I": [b"ATT", b"ATC", b"ATA"],
        b"M": [b"ATG"],
        b"T": [b"ACT", b"ACC", b"ACA", b"ACG"],
        b"N": [b"AAT", b"AAC"],
        b"K": [b"AAA", b"AAG"],
        b"V": [b"GTT", b"GTC", b"GTA", b"GTG"],
        b"D": [b"GAT", b"GAC"],
        b"E": [b"GAA", b"GAG"],
        b"G": [b"GGT", b"GGC", b"GGA", b"GGG"],
        b"X": [],
        b"B": [b"AAT", b"AAC", b"GAT", b"GAC"],
        b"J": [b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"ATT", b"ATC", b"ATA"],
        b"Z": [b"CAA", b"CAG", b"GAA", b"GAG"]
    },
    "27": {
        b"F": [b"TTT", b"TTC"],
        b"L": [b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG"],
        b"S": [b"TCT", b"TCC", b"TCA", b"TCG", b"AGT", b"AGC"],
        b"Y": [b"TAT", b"TAC"],
        b"Q": [b"TAA", b"TAG", b"CAA", b"CAG"],
        b"C": [b"TGT", b"TGC"],
        b"W": [b"TGA", b"TGG"],
        b"P": [b"CCT", b"CCC", b"CCA", b"CCG"],
        b"H": [b"CAT", b"CAC"],
        b"R": [b"CGT", b"CGC", b"CGA", b"CGG", b"AGA", b"AGG"],
        b"I": [b"ATT", b"ATC", b"ATA"],
        b"M": [b"ATG"],
        b"T": [b"ACT", b"ACC", b"ACA", b"ACG"],
        b"N": [b"AAT", b"AAC"],
        b"K": [b"AAA", b"AAG"],
        b"V": [b"GTT", b"GTC", b"GTA", b"GTG"],
        b"A": [b"GCT", b"GCC", b"GCA", b"GCG"],
        b"D": [b"GAT", b"GAC"],
        b"E": [b"GAA", b"GAG"],
        b"G": [b"GGT", b"GGC", b"GGA", b"GGG"],
        b"X": [],
        b"B": [b"AAT", b"AAC", b"GAT", b"GAC"],
        b"J": [
            b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG", b"ATT", b"ATC",
            b"ATA"
        ],
        b"Z": [b"TAA", b"TAG", b"CAA", b"CAG", b"GAA", b"GAG"]
    },
    "28": {
        b"F": [b"TTT", b"TTC"],
        b"L": [b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG"],
        b"S": [b"TCT", b"TCC", b"TCA", b"TCG", b"AGT", b"AGC"],
        b"Y": [b"TAT", b"TAC"],
        b"Q": [b"TAA", b"TAG", b"CAA", b"CAG"],
        b"C": [b"TGT", b"TGC"],
        b"W": [b"TGA", b"TGG"],
        b"P": [b"CCT", b"CCC", b"CCA", b"CCG"],
        b"H": [b"CAT", b"CAC"],
        b"R": [b"CGT", b"CGC", b"CGA", b"CGG", b"AGA", b"AGG"],
        b"I": [b"ATT", b"ATC", b"ATA"],
        b"M": [b"ATG"],
        b"T": [b"ACT", b"ACC", b"ACA", b"ACG"],
        b"N": [b"AAT", b"AAC"],
        b"K": [b"AAA", b"AAG"],
        b"V": [b"GTT", b"GTC", b"GTA", b"GTG"],
        b"A": [b"GCT", b"GCC", b"GCA", b"GCG"],
        b"D": [b"GAT", b"GAC"],
        b"E": [b"GAA", b"GAG"],
        b"G": [b"GGT", b"GGC", b"GGA", b"GGG"],
        b"X": [],
        b"B": [b"AAT", b"AAC", b"GAT", b"GAC"],
        b"J": [
            b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG", b"ATT", b"ATC",
            b"ATA"
        ],
        b"Z": [b"TAA", b"TAG", b"CAA", b"CAG", b"GAA", b"GAG"]
    },
    "29": {
        b"F": [b"TTT", b"TTC"],
        b"L": [b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG"],
        b"S": [b"TCT", b"TCC", b"TCA", b"TCG", b"AGT", b"AGC"],
        b"Y": [b"TAT", b"TAC", b"TAA", b"TAG"],
        b"C": [b"TGT", b"TGC"],
        b"*": [b"TGA"],
        b"W": [b"TGG"],
        b"P": [b"CCT", b"CCC", b"CCA", b"CCG"],
        b"H": [b"CAT", b"CAC"],
        b"Q": [b"CAA", b"CAG"],
        b"R": [b"CGT", b"CGC", b"CGA", b"CGG", b"AGA", b"AGG"],
        b"I": [b"ATT", b"ATC", b"ATA"],
        b"M": [b"ATG"],
        b"T": [b"ACT", b"ACC", b"ACA", b"ACG"],
        b"N": [b"AAT", b"AAC"],
        b"K": [b"AAA", b"AAG"],
        b"V": [b"GTT", b"GTC", b"GTA", b"GTG"],
        b"A": [b"GCT", b"GCC", b"GCA", b"GCG"],
        b"D": [b"GAT", b"GAC"],
        b"E": [b"GAA", b"GAG"],
        b"G": [b"GGT", b"GGC", b"GGA", b"GGG"],
        b"X": [],
        b"B": [b"AAT", b"AAC", b"GAT", b"GAC"],
        b"J": [
            b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG", b"ATT", b"ATC",
            b"ATA"
        ],
        b"Z": [b"CAA", b"CAG", b"GAA", b"GAG"]
    },
    "30": {
        b"F": [b"TTT", b"TTC"],
        b"L": [b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG"],
        b"S": [b"TCT", b"TCC", b"TCA", b"TCG", b"AGT", b"AGC"],
        b"Y": [b"TAT", b"TAC"],
        b"E": [b"TAA", b"TAG", b"GAA", b"GAG"],
        b"C": [b"TGT", b"TGC"],
        b"*": [b"TGA"],
        b"W": [b"TGG"],
        b"P": [b"CCT", b"CCC", b"CCA", b"CCG"],
        b"H": [b"CAT", b"CAC"],
        b"Q": [b"CAA", b"CAG"],
        b"R": [b"CGT", b"CGC", b"CGA", b"CGG", b"AGA", b"AGG"],
        b"I": [b"ATT", b"ATC", b"ATA"],
        b"M": [b"ATG"],
        b"T": [b"ACT", b"ACC", b"ACA", b"ACG"],
        b"N": [b"AAT", b"AAC"],
        b"K": [b"AAA", b"AAG"],
        b"V": [b"GTT", b"GTC", b"GTA", b"GTG"],
        b"A": [b"GCT", b"GCC", b"GCA", b"GCG"],
        b"D": [b"GAT", b"GAC"],
        b"G": [b"GGT", b"GGC", b"GGA", b"GGG"],
        b"X": [],
        b"B": [b"AAT", b"AAC", b"GAT", b"GAC"],
        b"J": [
            b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG", b"ATT", b"ATC",
            b"ATA"
        ],
        b"Z": [b"TAA", b"TAG", b"GAA", b"GAG", b"CAA", b"CAG"]
    },
    "31": {
        b"F": [b"TTT", b"TTC"],
        b"L": [b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG"],
        b"S": [b"TCT", b"TCC", b"TCA", b"TCG", b"AGT", b"AGC"],
        b"Y": [b"TAT", b"TAC"],
        b"E": [b"TAA", b"TAG", b"GAA", b"GAG"],
        b"C": [b"TGT", b"TGC"],
        b"W": [b"TGA", b"TGG"],
        b"P": [b"CCT", b"CCC", b"CCA", b"CCG"],
        b"H": [b"CAT", b"CAC"],
        b"Q": [b"CAA", b"CAG"],
        b"R": [b"CGT", b"CGC", b"CGA", b"CGG", b"AGA", b"AGG"],
        b"I": [b"ATT", b"ATC", b"ATA"],
        b"M": [b"ATG"],
        b"T": [b"ACT", b"ACC", b"ACA", b"ACG"],
        b"N": [b"AAT", b"AAC"],
        b"K": [b"AAA", b"AAG"],
        b"V": [b"GTT", b"GTC", b"GTA", b"GTG"],
        b"A": [b"GCT", b"GCC", b"GCA", b"GCG"],
        b"D": [b"GAT", b"GAC"],
        b"G": [b"GGT", b"GGC", b"GGA", b"GGG"],
        b"X": [],
        b"B": [b"AAT", b"AAC", b"GAT", b"GAC"],
        b"J": [
            b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG", b"ATT", b"ATC",
            b"ATA"
        ],
        b"Z": [b"TAA", b"TAG", b"GAA", b"GAG", b"CAA", b"CAG"]
    },
    "32": {
        b"F": [b"TTT", b"TTC"],
        b"L": [b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG"],
        b"S": [b"TCT", b"TCC", b"TCA", b"TCG", b"AGT", b"AGC"],
        b"Y": [b"TAT", b"TAC"],
        b"*": [b"TAA", b"TGA"],
        b"W": [b"TAG", b"TGG"],
        b"C": [b"TGT", b"TGC"],
        b"P": [b"CCT", b"CCC", b"CCA", b"CCG"],
        b"H": [b"CAT", b"CAC"],
        b"Q": [b"CAA", b"CAG"],
        b"R": [b"CGT", b"CGC", b"CGA", b"CGG", b"AGA", b"AGG"],
        b"I": [b"ATT", b"ATC", b"ATA"],
        b"M": [b"ATG"],
        b"T": [b"ACT", b"ACC", b"ACA", b"ACG"],
        b"N": [b"AAT", b"AAC"],
        b"K": [b"AAA", b"AAG"],
        b"V": [b"GTT", b"GTC", b"GTA", b"GTG"],
        b"A": [b"GCT", b"GCC", b"GCA", b"GCG"],
        b"D": [b"GAT", b"GAC"],
        b"E": [b"GAA", b"GAG"],
        b"G": [b"GGT", b"GGC", b"GGA", b"GGG"],
        b"X": [],
        b"B": [b"AAT", b"AAC", b"GAT", b"GAC"],
        b"J": [
            b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG", b"ATT", b"ATC",
            b"ATA"
        ],
        b"Z": [b"CAA", b"CAG", b"GAA", b"GAG"]
    },
    "33": {
        b"F": [b"TTT", b"TTC"],
        b"L": [b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG"],
        b"S": [b"TCT", b"TCC", b"TCA", b"TCG", b"AGT", b"AGC", b"AGA"],
        b"Y": [b"TAT", b"TAC", b"TAA"],
        b"*": [b"TAG"],
        b"C": [b"TGT", b"TGC"],
        b"W": [b"TGA", b"TGG"],
        b"P": [b"CCT", b"CCC", b"CCA", b"CCG"],
        b"H": [b"CAT", b"CAC"],
        b"Q": [b"CAA", b"CAG"],
        b"R": [b"CGT", b"CGC", b"CGA", b"CGG"],
        b"I": [b"ATT", b"ATC", b"ATA"],
        b"M": [b"ATG"],
        b"T": [b"ACT", b"ACC", b"ACA", b"ACG"],
        b"N": [b"AAT", b"AAC"],
        b"K": [b"AAA", b"AAG", b"AGG"],
        b"V": [b"GTT", b"GTC", b"GTA", b"GTG"],
        b"A": [b"GCT", b"GCC", b"GCA", b"GCG"],
        b"D": [b"GAT", b"GAC"],
        b"E": [b"GAA", b"GAG"],
        b"G": [b"GGT", b"GGC", b"GGA", b"GGG"],
        b"X": [],
        b"B": [b"AAT", b"AAC", b"GAT", b"GAC"],
        b"J": [
            b"TTA", b"TTG", b"CTT", b"CTC", b"CTA", b"CTG", b"ATT", b"ATC",
            b"ATA"
        ],
        b"Z": [b"CAA", b"CAG", b"GAA", b"GAG"]
    }
}


__METHOD_DOC_COMM = {
    "NucleotideEncodingMethod": "3 & (<nucleotide> >> 1)",
    "NucleotideEncodingMapping": {
        "A": 0,
        "C": 1,
        "T": 2,
        "G": 3,
    },
    "NucleotidePackedMaxNbits": 7,
    "NucleotidePackedMaxValue": 63,
    "CorrespondingFile": "Github/chubek/TransGatacca/encoding/encode_tables.py",
}

__METHOD_DOC_NUC = {
    **__METHOD_DOC_COMM,
    "TripletPackingMethod": "(<nucletide_1> << 4) | (<nucletide_2> << 2) | <nucletide_3>",
    "IndexingMethod": "ARRAY[<packed_nucleotide>] = <peptide>",
    "PackedTripletExample": "MSB=01 B1=11 LSB=00 -> CGA"
}
__METHOD_DOC_PEP = {
    **__METHOD_DOC_COMM,
    "CodonPackingMethod": "foreach Nth <packed_triplet>: packed |= <packed_triplet> << (<pack_offset> inc by 6)",
    "PackOffsetInitial": 4,
    "PackOffsetMax": 54,
    "PackMaxNbits": 54,
    "MaxNumberOfCodons": 9,
    "MinNumberOfCodons": 1,
    "MaxNumberOfCodonsNBits": 4,
    "CodonsNumEncodingMethod": "<packed_codons> | <number_of_codons>",
    "IndexingMethod": "ARRAY[<ASCII_VAL(peptide) - 65>] = <packed_codons>",
    "PackedCodonsExample": "MSB=001110 B1=111100 LSB=0010 -> (AGT, GGA, len=2)",
}


def execfn(fn: type):
    nucs, peps = fn()
    globals()["__ENCODED__"] = (nucs, peps)
    return fn


@execfn
def encode_gtable(gtable=GENETIC_TABLE) -> tuple[dict[str, list[int]], dict[str, list[int]]]:
    final_encoded_peps = {}
    final_encoded_nucs = {}

    def enc_nuc(nuc): return 3 & (nuc >> 1)
    iss = []

    for genetic_code, table in gtable.items():
        final_encoded_nucs[genetic_code] = [0] * 64
        final_encoded_peps[genetic_code] = [0] * 26
        for peptide, nucleotide_triplets in table.items():
            peptide_idx = ord(peptide) - 65
            shl_amount = 4
            for i, trip in enumerate(nucleotide_triplets):
                indx = (enc_nuc(trip[0]) << 4) & 0xff
                indx |= (enc_nuc(trip[1]) << 2) & 0xff
                indx |= enc_nuc(trip[2])
                final_encoded_nucs[genetic_code][indx] = ord(peptide)
                final_encoded_peps[genetic_code][peptide_idx] |= (
                    indx << shl_amount)
                shl_amount += 6

            final_encoded_peps[genetic_code][peptide_idx] |= len(
                nucleotide_triplets)

    return final_encoded_nucs, final_encoded_peps


if __name__ == "__main__":
    encd_nucs, encd_peps = globals()["__ENCODED__"]

    import sys
    import json
    if len(sys.argv) < 4:
        print("Arg number must be 3")
        exit(1)
    cmd, file_nuc, file_pep = sys.argv[1:4]
    fnuc = open(file_nuc, "w")
    fpep = open(file_pep, "w")
    if cmd.startswith("c"):
        print("{", file=fnuc)
        print("{", file=fpep)
        for i in range(37):

            if str(i) in encd_nucs:
                gtable_enc = encd_nucs[str(i)]
                print(
                    "{", ", ".join(list(map(str, gtable_enc))), "},", file=fnuc)
                gtable_enc = encd_peps[str(i)]
                print(
                    "{", ", ".join(list(map(str, gtable_enc))), "},", file=fpep)
            else:
                print("ARR_ZERO_64,", file=fnuc)
                print("ARR_ZERO_26,", file=fpep)
        print("}", file=fnuc)
        print("}", file=fpep)
    elif cmd.startswith("j"):
        encd_nucs["Method"] = __METHOD_DOC_NUC
        encd_peps["Method"] = __METHOD_DOC_PEP
        fnuc.write(json.dumps(encd_nucs, indent=4))
        fpep.write(json.dumps(encd_peps, indent=4))
    else:
        print("Unknown command: " + cmd)
        fnuc.close()
        fpep.close()
        exit(1)

    fnuc.close()
    fpep.close()
