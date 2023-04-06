The followng are the methods used to encode codons table and frequency table into integers.

1- **To encode triplets**, we pack all 3 2-bit integers into a 6-bit intger (order of bits is not important, but the deocder must use the same order) and thus we will have a maximum of 64 different integers. We can create an array of 64, with each 6-bit index representing a peptide corresponding to that nucleotide triplet. We now have an array where `arr[i] = byte value of peptide`.

2- **To encode peptides**, we take all the possible triplets that we encoded before, which non-empty numbers can range from 1 to 10, and pack all those 6-bit integers that we got into an n \* 6 bit integer, with n being the number of possible degenerate triplets for that peptide. We then shift the length of the possible triplets by 60. Finally, for example, for peptide `F` in table `33` we get:

| Bit Num | 63  | 62  | 61  | 60  | ... | 11  | 10  | 9   | 8   | 7   | 6   | 5   | 4   | 3   | 2   | 1   | 0   |
| ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Bit     | 0   | 0   | 1   | 0   | ... | 1   | 0   | 1   | 0   | 1   | 0   | 1   | 0   | 1   | 0   | 0   | 1   |

We will then lay them an array of size 26, after we subtract `64` from peptide (`'A' - 1`). We now have an array where `arr[n] = packed values`.

3 - **To encode codon frequency**: By subtracting `64` from peptide, we are left with a 5-bit integer. We apply the following to the encoded triplet:

```
(nuc1 | (nuc3 << 1)) ^ nuc2
```

We now have a 3-bit integer which we can append to the end of `pep - 64` by shifting the said value 3 to the left and OR'ing it with the 3-bit integer. We now can use this value to index the frequency. But how do we represent the frequency? Basically, we take the first two digits after the decimal point and `atoi` them (or just `int(s.split(".")[-1][:2])`). The maximum our index can be is 255 so we store everythng n an array of size 256, where `arr[i] = freq`.


Files inside `encode` directory are an implementation of this encoding in Python.