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

# Encode codon frequencies for a 64bit-width register or memory address
# Please read ENCODING.md for more info

HSAPIENS = b"""
*,TAA,0.30
*,TAG,0.24
*,TGA,0.47
A,GCA,0.23
A,GCC,0.40
A,GCG,0.11
A,GCT,0.27
C,TGC,0.54
C,TGT,0.46
D,GAC,0.54
D,GAT,0.46
E,GAA,0.42
E,GAG,0.58
F,TTC,0.54
F,TTT,0.46
G,GGA,0.25
G,GGC,0.34
G,GGG,0.25
G,GGT,0.16
H,CAC,0.58
H,CAT,0.42
I,ATA,0.17
I,ATC,0.47
I,ATT,0.36
K,AAA,0.43
K,AAG,0.57
L,CTA,0.07
L,CTC,0.20
L,CTG,0.40
L,CTT,0.13
L,TTA,0.08
L,TTG,0.13
M,ATG,1.00
N,AAC,0.53
N,AAT,0.47
P,CCA,0.28
P,CCC,0.32
P,CCG,0.11
P,CCT,0.29
Q,CAA,0.27
Q,CAG,0.73
R,AGA,0.21
R,AGG,0.21
R,CGA,0.11
R,CGC,0.18
R,CGG,0.20
R,CGT,0.08
S,AGC,0.24
S,AGT,0.15
S,TCA,0.15
S,TCC,0.22
S,TCG,0.05
S,TCT,0.19
T,ACA,0.28
T,ACC,0.36
T,ACG,0.11
T,ACT,0.25
V,GTA,0.12
V,GTC,0.24
V,GTG,0.46
V,GTT,0.18
W,TGG,1.00
Y,TAC,0.56
Y,TAT,0.44
"""

BSUBTILIS = b"""
*,UAA,0.61
*,UAG,0.15
*,UGA,0.24
A,GCA,0.28
A,GCC,0.22
A,GCG,0.26
A,GCU,0.24
C,UGC,0.54
C,UGU,0.46
D,GAC,0.36
D,GAU,0.64
E,GAA,0.68
E,GAG,0.32
F,UUC,0.32
F,UUU,0.68
G,GGA,0.31
G,GGC,0.34
G,GGG,0.16
G,GGU,0.19
H,CAC,0.32
H,CAU,0.68
I,AUA,0.13
I,AUC,0.37
I,AUU,0.49
K,AAA,0.70
K,AAG,0.30
L,CUA,0.05
L,CUC,0.11
L,CUG,0.24
L,CUU,0.23
L,UUA,0.21
L,UUG,0.16
M,AUG,1.00
N,AAC,0.44
N,AAU,0.56
P,CCA,0.19
P,CCC,0.09
P,CCG,0.44
P,CCU,0.28
Q,CAA,0.52
Q,CAG,0.48
R,AGA,0.25
R,AGG,0.10
R,CGA,0.10
R,CGC,0.20
R,CGG,0.17
R,CGU,0.18
S,AGC,0.23
S,AGU,0.11
S,UCA,0.23
S,UCC,0.13
S,UCG,0.10
S,UCU,0.20
T,ACA,0.40
T,ACC,0.17
T,ACG,0.27
T,ACU,0.16
V,GUA,0.20
V,GUC,0.26
V,GUG,0.26
V,GUU,0.28
W,UGG,1.00
Y,UAC,0.35
Y,UAU,0.65
"""

CELEGANS = b"""
*,UAA,0.43
*,UAG,0.18
*,UGA,0.39
A,GCA,0.31
A,GCC,0.20
A,GCG,0.13
A,GCU,0.36
C,UGC,0.45
C,UGU,0.55
D,GAC,0.32
D,GAU,0.68
E,GAA,0.62
E,GAG,0.38
F,UUC,0.51
F,UUU,0.49
G,GGA,0.59
G,GGC,0.12
G,GGG,0.08
G,GGU,0.20
H,CAC,0.39
H,CAU,0.61
I,AUA,0.16
I,AUC,0.31
I,AUU,0.53
K,AAA,0.59
K,AAG,0.41
L,CUA,0.09
L,CUC,0.17
L,CUG,0.14
L,CUU,0.25
L,UUA,0.11
L,UUG,0.23
M,AUG,1.00
N,AAC,0.38
N,AAU,0.62
P,CCA,0.53
P,CCC,0.09
P,CCG,0.20
P,CCU,0.18
Q,CAA,0.66
Q,CAG,0.34
R,AGA,0.29
R,AGG,0.08
R,CGA,0.23
R,CGC,0.10
R,CGG,0.09
R,CGU,0.21
S,AGC,0.10
S,AGU,0.15
S,UCA,0.26
S,UCC,0.13
S,UCG,0.15
S,UCU,0.21
T,ACA,0.34
T,ACC,0.18
T,ACG,0.15
T,ACU,0.32
V,GUA,0.16
V,GUC,0.22
V,GUG,0.23
V,GUU,0.39
W,UGG,1.00
Y,UAC,0.44
Y,UAU,0.56
"""

DMELANOGASTER = b"""
*,UAA,0.41
*,UAG,0.33
*,UGA,0.25
A,GCA,0.17
A,GCC,0.45
A,GCG,0.19
A,GCU,0.19
C,UGC,0.71
C,UGU,0.29
D,GAC,0.47
D,GAU,0.53
E,GAA,0.33
E,GAG,0.67
F,UUC,0.62
F,UUU,0.38
G,GGA,0.29
G,GGC,0.43
G,GGG,0.07
G,GGU,0.21
H,CAC,0.60
H,CAU,0.40
I,AUA,0.19
I,AUC,0.47
I,AUU,0.34
K,AAA,0.30
K,AAG,0.70
L,CUA,0.09
L,CUC,0.15
L,CUG,0.43
L,CUU,0.10
L,UUA,0.05
L,UUG,0.18
M,AUG,1.00
N,AAC,0.56
N,AAU,0.44
P,CCA,0.25
P,CCC,0.33
P,CCG,0.29
P,CCU,0.13
Q,CAA,0.30
Q,CAG,0.70
R,AGA,0.09
R,AGG,0.11
R,CGA,0.15
R,CGC,0.33
R,CGG,0.15
R,CGU,0.16
S,AGC,0.25
S,AGU,0.14
S,UCA,0.09
S,UCC,0.24
S,UCG,0.20
S,UCU,0.08
T,ACA,0.20
T,ACC,0.38
T,ACG,0.26
T,ACU,0.17
V,GUA,0.11
V,GUC,0.24
V,GUG,0.47
V,GUU,0.19
W,UGG,1.00
Y,UAC,0.63
Y,UAU,0.37
"""

ECOLI = b"""
*,UAA,0.64
*,UAG,0.07
*,UGA,0.29
A,GCA,0.21
A,GCC,0.27
A,GCG,0.36
A,GCU,0.16
C,UGC,0.56
C,UGU,0.44
D,GAC,0.37
D,GAU,0.63
E,GAA,0.69
E,GAG,0.31
F,UUC,0.43
F,UUU,0.57
G,GGA,0.11
G,GGC,0.41
G,GGG,0.15
G,GGU,0.34
H,CAC,0.43
H,CAU,0.57
I,AUA,0.07
I,AUC,0.42
I,AUU,0.51
K,AAA,0.76
K,AAG,0.24
L,CUA,0.04
L,CUC,0.10
L,CUG,0.50
L,CUU,0.10
L,UUA,0.13
L,UUG,0.13
M,AUG,1.00
N,AAC,0.55
N,AAU,0.45
P,CCA,0.19
P,CCC,0.12
P,CCG,0.53
P,CCU,0.16
Q,CAA,0.35
Q,CAG,0.65
R,AGA,0.04
R,AGG,0.02
R,CGA,0.06
R,CGC,0.40
R,CGG,0.10
R,CGU,0.38
S,AGC,0.28
S,AGU,0.15
S,UCA,0.12
S,UCC,0.15
S,UCG,0.15
S,UCU,0.15
T,ACA,0.13
T,ACC,0.44
T,ACG,0.27
T,ACU,0.16
V,GUA,0.15
V,GUC,0.22
V,GUG,0.37
V,GUU,0.26
W,UGG,1.00
Y,UAC,0.43
Y,UAU,0.57
"""

GGALIUS = b"""
*,UAA,0.32
*,UAG,0.20
*,UGA,0.47
A,GCA,0.26
A,GCC,0.32
A,GCG,0.13
A,GCU,0.29
C,UGC,0.60
C,UGU,0.40
D,GAC,0.50
D,GAU,0.50
E,GAA,0.43
E,GAG,0.57
F,UUC,0.55
F,UUU,0.45
G,GGA,0.27
G,GGC,0.31
G,GGG,0.25
G,GGU,0.18
H,CAC,0.60
H,CAU,0.40
I,AUA,0.18
I,AUC,0.46
I,AUU,0.35
K,AAA,0.44
K,AAG,0.56
L,CUA,0.06
L,CUC,0.18
L,CUG,0.41
L,CUU,0.13
L,UUA,0.08
L,UUG,0.13
M,AUG,1.00
N,AAC,0.57
N,AAU,0.43
P,CCA,0.28
P,CCC,0.30
P,CCG,0.14
P,CCU,0.27
Q,CAA,0.27
Q,CAG,0.73
R,AGA,0.22
R,AGG,0.21
R,CGA,0.10
R,CGC,0.19
R,CGG,0.18
R,CGU,0.10
S,AGC,0.26
S,AGU,0.14
S,UCA,0.15
S,UCC,0.20
S,UCG,0.07
S,UCU,0.18
T,ACA,0.30
T,ACC,0.31
T,ACG,0.14
T,ACU,0.25
V,GUA,0.12
V,GUC,0.22
V,GUG,0.45
V,GUU,0.21
W,UGG,1.00
Y,UAC,0.60
Y,UAU,0.40
"""

MMUSCULUS = b"""
*,UAA,0.28
*,UAG,0.23
*,UGA,0.49
A,GCA,0.23
A,GCC,0.38
A,GCG,0.09
A,GCU,0.29
C,UGC,0.52
C,UGU,0.48
D,GAC,0.55
D,GAU,0.45
E,GAA,0.41
E,GAG,0.59
F,UUC,0.56
F,UUU,0.44
G,GGA,0.26
G,GGC,0.33
G,GGG,0.23
G,GGU,0.18
H,CAC,0.59
H,CAU,0.41
I,AUA,0.16
I,AUC,0.50
I,AUU,0.34
K,AAA,0.39
K,AAG,0.61
L,CUA,0.08
L,CUC,0.20
L,CUG,0.39
L,CUU,0.13
L,UUA,0.07
L,UUG,0.13
M,AUG,1.00
N,AAC,0.57
N,AAU,0.43
P,CCA,0.29
P,CCC,0.30
P,CCG,0.10
P,CCU,0.31
Q,CAA,0.26
Q,CAG,0.74
R,AGA,0.22
R,AGG,0.22
R,CGA,0.12
R,CGC,0.17
R,CGG,0.19
R,CGU,0.08
S,AGC,0.24
S,AGU,0.15
S,UCA,0.14
S,UCC,0.22
S,UCG,0.05
S,UCU,0.20
T,ACA,0.29
T,ACC,0.35
T,ACG,0.10
T,ACU,0.25
V,GUA,0.12
V,GUC,0.25
V,GUG,0.46
V,GUU,0.17
W,UGG,1.00
Y,UAC,0.57
Y,UAU,0.43
"""

MMUSCULUSDOMSETICUS = b"""
*,UAA,0.27
*,UAG,0.45
*,UGA,0.27
A,GCA,0.30
A,GCC,0.36
A,GCG,0.11
A,GCU,0.23
C,UGC,0.55
C,UGU,0.45
D,GAC,0.61
D,GAU,0.39
E,GAA,0.49
E,GAG,0.51
F,UUC,0.61
F,UUU,0.39
G,GGA,0.29
G,GGC,0.32
G,GGG,0.22
G,GGU,0.17
H,CAC,0.65
H,CAU,0.35
I,AUA,0.29
I,AUC,0.43
I,AUU,0.27
K,AAA,0.58
K,AAG,0.42
L,CUA,0.14
L,CUC,0.21
L,CUG,0.35
L,CUU,0.13
L,UUA,0.07
L,UUG,0.10
M,AUG,1.00
N,AAC,0.59
N,AAU,0.41
P,CCA,0.34
P,CCC,0.30
P,CCG,0.10
P,CCU,0.26
Q,CAA,0.24
Q,CAG,0.76
R,AGA,0.34
R,AGG,0.25
R,CGA,0.10
R,CGC,0.13
R,CGG,0.13
R,CGU,0.06
S,AGC,0.23
S,AGU,0.13
S,UCA,0.21
S,UCC,0.21
S,UCG,0.06
S,UCU,0.16
T,ACA,0.40
T,ACC,0.28
T,ACG,0.08
T,ACU,0.24
V,GUA,0.19
V,GUC,0.24
V,GUG,0.43
V,GUU,0.14
W,UGG,1.00
Y,UAC,0.59
Y,UAU,0.41
"""

SCEREVISIAE = b"""
*,UAA,0.47
*,UAG,0.23
*,UGA,0.30
A,GCA,0.29
A,GCC,0.22
A,GCG,0.11
A,GCU,0.38
C,UGC,0.37
C,UGU,0.63
D,GAC,0.35
D,GAU,0.65
E,GAA,0.70
E,GAG,0.30
F,UUC,0.41
F,UUU,0.59
G,GGA,0.22
G,GGC,0.19
G,GGG,0.12
G,GGU,0.47
H,CAC,0.36
H,CAU,0.64
I,AUA,0.27
I,AUC,0.26
I,AUU,0.46
K,AAA,0.58
K,AAG,0.42
L,CUA,0.14
L,CUC,0.06
L,CUG,0.11
L,CUU,0.13
L,UUA,0.28
L,UUG,0.29
M,AUG,1.00
N,AAC,0.41
N,AAU,0.59
P,CCA,0.42
P,CCC,0.15
P,CCG,0.12
P,CCU,0.31
Q,CAA,0.69
Q,CAG,0.31
R,AGA,0.48
R,AGG,0.21
R,CGA,0.07
R,CGC,0.06
R,CGG,0.04
R,CGU,0.14
S,AGC,0.11
S,AGU,0.16
S,UCA,0.21
S,UCC,0.16
S,UCG,0.10
S,UCU,0.26
T,ACA,0.30
T,ACC,0.22
T,ACG,0.14
T,ACU,0.35
V,GUA,0.21
V,GUC,0.21
V,GUG,0.19
V,GUU,0.39
W,UGG,1.00
Y,UAC,0.44
Y,UAU,0.56
"""

TABLES = {
    "b_subtilis": BSUBTILIS,
    "c_elegans": CELEGANS,
    "d_melanogaster": DMELANOGASTER,
    "e_coli": ECOLI,
    "g_gallus": GGALIUS,
    "h_sapiens": HSAPIENS,
    "m_musculus": MMUSCULUS,
    "m_musculus_domesticus": MMUSCULUSDOMSETICUS,
    "s_cerevisiiae": SCEREVISIAE,
}

def execfn(fn: type):
    freqs, codes = fn()
    globals()["__ENCODED__"] = (freqs, codes)
    return fn

@execfn
def encode_freqs(tables=TABLES) -> tuple[str, list[int]]:
    encode_single_nuc = lambda x: 3 & (x >> 1)
    
    tables_list = list(tables.keys())
    encoded_freqs = [[0] * 256] * len(tables_list)
    
    for species, csv in tables.items():
        for l in csv.strip().split(b"\n"):
            peptide, nuc_triplet, freq = l.split(b",")
            peptide = peptide[0] - 65
            nuc_triplet = [encode_single_nuc(b) for b in nuc_triplet]
            indx = (peptide << 3) | (nuc_triplet[0] |
                                    (nuc_triplet[2] << 1) ^ nuc_triplet[1])

            freq = freq.split(b".")[-1][:2]
            freq = 99 if freq == "00" else int(freq.decode())
            encoded_freqs[tables_list.index(species)][indx] = freq
    
    return encoded_freqs, tables_list


if __name__ == "__main__":
    freqs, lut = globals()["__ENCODED__"]

    import sys
    import json
    if len(sys.argv) < 2:
        print("Arg number must be 2")
        exit(1)
    cmd, file_frq = sys.argv[1:3]
    ffrq = open(file_frq, "w")

    if cmd.startswith("c"):

        print("FREQ = [", file=ffrq)
        for freq in freqs:
            print("[ ", ", ".join(map(str, freq)) + " ],", file=ffrq)
        print("]", file=ffrq)

        print("LUT = [ ", ", ".join(map(lambda x: f'"{x}"', lut)) + " ],", file=ffrq)
    elif cmd.startswith("j"):
        combined = {k: freqs[lut.index(k)] for k in lut}
        ffrq.write(json.dumps(combined, indent=4))
    else:
        print('Wrong command')
        ffrq.close()
        exit(1)
