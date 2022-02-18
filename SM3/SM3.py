from projectq import MainEngine
from projectq.ops import H, CNOT, Measure, Toffoli, X, All, Swap
from projectq.backends import CircuitDrawer, ResourceCounter, CommandPrinter, ClassicalSimulator
from projectq.meta import Loop, Compute, Uncompute, Control
import random


def init_value(eng, A, B, C, D, E, F, G, H):
    for i in range(0, 32):
        box = [0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1]
        if box[i] == 1:
            X | (A[i])

    for i in range(0, 32):
        box = [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1]
        if box[i] == 1:
            X | (B[i])

    for i in range(0, 32):
        box = [0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1]
        if box[i] == 1:
            X | (C[i])

    for i in range(0, 32):
        box = [1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        if box[i] == 1:
            X | (D[i])

    for i in range(0, 32):
        box = [1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0]
        if box[i] == 1:
            X | (E[i])

    for i in range(0, 32):
        box = [0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0]
        if box[i] == 1:
            X | (F[i])

    for i in range(0, 32):
        box = [1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1]
        if box[i] == 1:
            X | (G[i])

    for i in range(0, 32):
        box = [1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0]
        if box[i] == 1:
            X | (H[i])


def init_MSG_Exp(eng, update_W, W0, W1, W2,W3,W4,p):
    with Compute(eng):
        for i in range(32):
            CNOT | (W1[i], W0[i])
        for i in range(32):
            CNOT | (W2[(i+15)%32], W0[i])
        permutation_P1(eng, W0, p)

    for i in range(32):
        CNOT | (W0[i],update_W[i])
    for i in range(32):
        CNOT | (W3[(i+7)%32], update_W[i])
    for i in range(32):
        CNOT | (W4[i], update_W[i])

    Uncompute(eng)


def MSG_Exp_0(eng, W_low, W_high):
    for i in range(32):
        CNOT | (W_high[i], W_low[i])


def T_0(eng, T, j):
    if j > -1 and j < 16:
        box = [0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1] #15 #240
        for i in range(32):
            if box[i] == 1:
                X | T[i]
    if j > 15 and j < 64:
        box = [0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0] #17 #816
        for i in range(32):
            if box[i] == 1:
                X | T[i]

    for k in range(j % 32):  # right shift c_bit (same with (32-c-bit) left)
        for i in range(31):
            Swap | (T[i], T[i + 1])



def SS_1(eng, A, E, T, j, c0):
    for k in range(12):  # right shift c_bit (same with (32-c-bit) left)
        for i in range(31):
            Swap | (A[i], A[i + 1])

    ripple_carry_add(eng, A, E, c0)
    ripple_carry_add(eng, T, E, c0)

    for k in range(7):  # right shift c_bit (same with (32-c-bit) left)
        for i in range(31):
            Swap | (E[i], E[i + 1])



def SS_2(eng, E, A):
    for i in range(32):
        CNOT | (E[i], A[i])


def TT_1(eng, FF, D, SS2, w, j, c0):
    ripple_carry_add(eng, FF, D,c0)
    ripple_carry_add(eng, SS2, D, c0)
    ripple_carry_add(eng, w, D, c0)


def TT_2(eng, GG, H, SS1, W, j, c0):
    ripple_carry_add(eng, GG, H, c0)
    ripple_carry_add(eng, SS1, H, c0)
    ripple_carry_add(eng, W, H, c0)


def ripple_carry_add(eng, a, b, c0):
    MAJ(eng, a[31], b[31], c0)
    for i in range(31):
        MAJ(eng, a[31 - ((i + 0 + 1) % 32)], b[31 - ((i + 0 + 1) % 32)], a[31 - ((0 + i) % 32)])

    for i in range(31):
        UMA(eng, a[i % 32], b[i % 32], a[31 - (31 - 1 - i) % 32])
    UMA(eng, a[31], b[31], c0)



def MAJ(eng, a, b, c):
    CNOT | (a, c)
    CNOT | (a, b)
    Toffoli | (b, c, a)

def MAJ_reverse(eng, a, b, c):
    Toffoli | (b, c, a)
    CNOT | (a, b)
    CNOT | (a, c)

def UMA(eng, a, b, c):
    Toffoli | (c, b, a)
    CNOT | (a, c)
    CNOT | (c, b)


def UMA_reverse(eng, a, b, c):
    CNOT | (c, b)
    CNOT | (a, c)
    Toffoli | (c, b, a)



def permutation_P0(eng, x):
    Swap | (x[0], x[31])
    Swap | (x[1], x[30])
    Swap | (x[2], x[29])
    Swap | (x[3], x[28])
    Swap | (x[4], x[27])
    Swap | (x[5], x[26])
    Swap | (x[6], x[25])
    Swap | (x[7], x[24])
    Swap | (x[8], x[23])
    Swap | (x[9], x[22])
    Swap | (x[10], x[21])
    Swap | (x[11], x[20])
    Swap | (x[12], x[19])
    Swap | (x[13], x[18])
    Swap | (x[14], x[17])
    Swap | (x[15], x[16])

    CNOT | (x[22], x[31])
    CNOT | (x[14], x[31])

    CNOT | (x[21], x[30])
    CNOT | (x[13], x[30])

    CNOT | (x[20], x[29])
    CNOT | (x[12], x[29])

    CNOT | (x[19], x[28])
    CNOT | (x[11], x[28])

    CNOT | (x[18], x[27])
    CNOT | (x[10], x[27])

    CNOT | (x[17], x[26])
    CNOT | (x[9], x[26])

    CNOT | (x[16], x[25])
    CNOT | (x[8], x[25])

    CNOT | (x[15], x[24])
    CNOT | (x[7], x[24])

    CNOT | (x[14], x[23])
    CNOT | (x[6], x[23])

    CNOT | (x[13], x[22])
    CNOT | (x[5], x[22])

    CNOT | (x[12], x[21])
    CNOT | (x[4], x[21])

    CNOT | (x[11], x[20])
    CNOT | (x[3], x[20])

    CNOT | (x[10], x[19])
    CNOT | (x[2], x[19])

    CNOT | (x[9], x[18])
    CNOT | (x[1], x[18])

    CNOT | (x[8], x[17])
    CNOT | (x[0], x[17])
    

    CNOT | (x[7], x[16])
    CNOT | (x[31], x[16])
    CNOT | (x[22], x[16])
    CNOT | (x[14], x[16])
    CNOT | (x[13], x[16])
    CNOT | (x[5], x[16])

    CNOT | (x[6], x[15])
    CNOT | (x[30], x[15])
    CNOT | (x[21], x[15])
    CNOT | (x[13], x[15])
    CNOT | (x[12], x[15])
    CNOT | (x[4], x[15])

    CNOT | (x[5], x[14])
    CNOT | (x[29], x[14])
    CNOT | (x[20], x[14])
    CNOT | (x[12], x[14])
    CNOT | (x[11], x[14])
    CNOT | (x[3], x[14])

    CNOT | (x[4], x[13])
    CNOT | (x[28], x[13])
    CNOT | (x[19], x[13])
    CNOT | (x[11], x[13])
    CNOT | (x[10], x[13])
    CNOT | (x[2], x[13])

    CNOT | (x[3], x[12])
    CNOT | (x[27], x[12])
    CNOT | (x[18], x[12])
    CNOT | (x[10], x[12])
    CNOT | (x[9], x[12])
    CNOT | (x[1], x[12])

    CNOT | (x[2], x[11])
    CNOT | (x[26], x[11])
    CNOT | (x[17], x[11])
    CNOT | (x[9], x[11])
    CNOT | (x[8], x[11])
    CNOT | (x[0], x[11])

    CNOT | (x[1], x[10])
    CNOT | (x[25], x[10])
    CNOT | (x[16], x[10])
    CNOT | (x[8], x[10])
    CNOT | (x[7], x[10])
    CNOT | (x[31], x[10])
    CNOT | (x[22], x[10])
    CNOT | (x[14], x[10])
    CNOT | (x[13], x[10])
    CNOT | (x[29], x[10])
    CNOT | (x[4], x[10])
    CNOT | (x[28], x[10])
    CNOT | (x[20], x[10])
    CNOT | (x[12], x[10])
    CNOT | (x[19], x[10])
    CNOT | (x[27], x[10])
    CNOT | (x[18], x[10])
    CNOT | (x[2], x[10])
    CNOT | (x[9], x[10])
    CNOT | (x[1], x[10])

    CNOT | (x[0], x[9])
    CNOT | (x[24], x[9])
    CNOT | (x[15], x[9])
    CNOT | (x[7], x[9])
    CNOT | (x[6], x[9])
    CNOT | (x[30], x[9])
    CNOT | (x[21], x[9])
    CNOT | (x[13], x[9])
    CNOT | (x[12], x[9])
    CNOT | (x[28], x[9])
    CNOT | (x[3], x[9])
    CNOT | (x[27], x[9])
    CNOT | (x[19], x[9])
    CNOT | (x[11], x[9])
    CNOT | (x[18], x[9])
    CNOT | (x[26], x[9])
    CNOT | (x[17], x[9])
    CNOT | (x[1], x[9])
    CNOT | (x[8], x[9])
    CNOT | (x[0], x[9])

    #8
    CNOT | (x[31], x[8])
    CNOT | (x[22], x[8])
    CNOT | (x[23], x[8])
    CNOT | (x[13], x[8])
    CNOT | (x[5], x[8])
    CNOT | (x[6], x[8])
    CNOT | (x[4], x[8])
    CNOT | (x[28], x[8])
    CNOT | (x[19], x[8])
    CNOT | (x[11], x[8])
    CNOT | (x[10], x[8])
    CNOT | (x[26], x[8])
    CNOT | (x[1], x[8])
    CNOT | (x[25], x[8])
    CNOT | (x[17], x[8])
    CNOT | (x[9], x[8])
    CNOT | (x[16], x[8])
    CNOT | (x[24], x[8])
    CNOT | (x[31], x[8])
    CNOT | (x[15], x[8])
    CNOT | (x[22], x[8])
    CNOT | (x[14], x[8])
    CNOT | (x[6], x[8])
    CNOT | (x[30], x[8])
    CNOT | (x[29], x[8])
    CNOT | (x[21], x[8])
    CNOT | (x[20], x[8])
    CNOT | (x[4], x[8])
    CNOT | (x[11], x[8])
    CNOT | (x[3], x[8])
    CNOT | (x[2], x[8])
    CNOT | (x[26], x[8])
    CNOT | (x[17], x[8])
    CNOT | (x[9], x[8])
    CNOT | (x[24], x[8])
    CNOT | (x[15], x[8])
    CNOT | (x[7], x[8])
    CNOT | (x[6], x[8])
    CNOT | (x[30], x[8])
    CNOT | (x[21], x[8])
    CNOT | (x[13], x[8])
    CNOT | (x[12], x[8])
    CNOT | (x[28], x[8])
    CNOT | (x[3], x[8])
    CNOT | (x[27], x[8])
    CNOT | (x[19], x[8])
    CNOT | (x[2], x[8])
    CNOT | (x[11], x[8])
    CNOT | (x[18], x[8])
    CNOT | (x[2], x[8])
    CNOT | (x[1], x[8])
    CNOT | (x[26], x[8])
    CNOT | (x[17], x[8])
    CNOT | (x[0], x[8])


    #7
    CNOT | (x[30], x[7])
    CNOT | (x[21], x[7])
    CNOT | (x[13], x[7])
    CNOT | (x[12], x[7])
    CNOT | (x[28], x[7])
    CNOT | (x[3], x[7])
    CNOT | (x[27], x[7])
    CNOT | (x[19], x[7])
    CNOT | (x[11], x[7])
    CNOT | (x[18], x[7])
    CNOT | (x[26], x[7])
    CNOT | (x[17], x[7])
    CNOT | (x[8], x[7])
    CNOT | (x[31], x[7])
    CNOT | (x[23], x[7])
    CNOT | (x[1], x[7])
    CNOT | (x[0], x[7])
    CNOT | (x[6], x[7])

    #6
    CNOT | (x[21], x[6])
    CNOT | (x[12], x[6])
    CNOT | (x[27], x[6])
    CNOT | (x[18], x[6])
    CNOT | (x[10], x[6])
    CNOT | (x[9], x[6])
    CNOT | (x[25], x[6])
    CNOT | (x[24], x[6])
    CNOT | (x[16], x[6])
    CNOT | (x[8], x[6])
    CNOT | (x[15], x[6])
    CNOT | (x[23], x[6])
    CNOT | (x[30], x[6])
    CNOT | (x[14], x[6])
    CNOT | (x[21], x[6])
    CNOT | (x[13], x[6])
    CNOT | (x[12], x[6])
    CNOT | (x[28], x[6])
    CNOT | (x[27], x[6])
    CNOT | (x[19], x[6])
    CNOT | (x[11], x[6])
    CNOT | (x[18], x[6])
    CNOT | (x[26], x[6])
    CNOT | (x[17], x[6])
    CNOT | (x[8], x[6])
    CNOT | (x[31], x[6])
    CNOT | (x[23], x[6])
    CNOT | (x[22], x[6])
    CNOT | (x[13], x[6])
    CNOT | (x[28], x[6])
    CNOT | (x[19], x[6])
    CNOT | (x[11], x[6])
    CNOT | (x[10], x[6])
    CNOT | (x[26], x[6])
    CNOT | (x[25], x[6])
    CNOT | (x[17], x[6])
    CNOT | (x[9], x[6])
    CNOT | (x[16], x[6])
    CNOT | (x[24], x[6])
    CNOT | (x[31], x[6])
    CNOT | (x[15], x[6])
    CNOT | (x[22], x[6])
    CNOT | (x[14], x[6])
    CNOT | (x[30], x[6])
    CNOT | (x[29], x[6])
    CNOT | (x[21], x[6])
    CNOT | (x[20], x[6])
    CNOT | (x[11], x[6])
    CNOT | (x[26], x[6])
    CNOT | (x[17], x[6])
    CNOT | (x[9], x[6])
    CNOT | (x[8], x[6])
    CNOT | (x[24], x[6])
    CNOT | (x[31], x[6])
    CNOT | (x[23], x[6])
    CNOT | (x[15], x[6])
    CNOT | (x[7], x[6])
    CNOT | (x[4], x[6])
    CNOT | (x[3], x[6])
    CNOT | (x[2], x[6])


    #5
    CNOT | (x[20], x[5])
    CNOT | (x[11], x[5])
    CNOT | (x[26], x[5])
    CNOT | (x[17], x[5])
    CNOT | (x[9], x[5])
    CNOT | (x[8], x[5])
    CNOT | (x[24], x[5])
    CNOT | (x[31], x[5])
    CNOT | (x[23], x[5])
    CNOT | (x[15], x[5])
    CNOT | (x[7], x[5])
    CNOT | (x[28], x[5])
    CNOT | (x[19], x[5])
    CNOT | (x[11], x[5])
    CNOT | (x[10], x[5])
    CNOT | (x[26], x[5])
    CNOT | (x[25], x[5])
    CNOT | (x[17], x[5])
    CNOT | (x[9], x[5])
    CNOT | (x[16], x[5])
    CNOT | (x[24], x[5])
    CNOT | (x[31], x[5])
    CNOT | (x[15], x[5])
    CNOT | (x[22], x[5])
    CNOT | (x[14], x[5])
    CNOT | (x[6], x[5])
    CNOT | (x[30], x[5])
    CNOT | (x[3], x[5])
    CNOT | (x[2], x[5])
    CNOT | (x[1], x[5])

    #4
    CNOT | (x[19], x[4])
    CNOT | (x[10], x[4])
    CNOT | (x[25], x[4])
    CNOT | (x[16], x[4])
    CNOT | (x[8], x[4])
    CNOT | (x[7], x[4])
    CNOT | (x[23], x[4])
    CNOT | (x[30], x[4])
    CNOT | (x[22], x[4])
    CNOT | (x[14], x[4])
    CNOT | (x[6], x[4])
    CNOT | (x[27], x[4])
    CNOT | (x[18], x[4])
    CNOT | (x[10], x[4])
    CNOT | (x[9], x[4])
    CNOT | (x[25], x[4])
    CNOT | (x[24], x[4])
    CNOT | (x[16], x[4])
    CNOT | (x[8], x[4])
    CNOT | (x[15], x[4])
    CNOT | (x[23], x[4])
    CNOT | (x[30], x[4])
    CNOT | (x[14], x[4])
    CNOT | (x[21], x[4])
    CNOT | (x[13], x[4])
    CNOT | (x[5], x[4])
    CNOT | (x[29], x[4])
    CNOT | (x[2], x[4])
    CNOT | (x[1], x[4])
    CNOT | (x[0], x[4])

    #3
    CNOT | (x[18], x[3])
    CNOT | (x[9], x[3])
    CNOT | (x[24], x[3])
    CNOT | (x[15], x[3])
    CNOT | (x[7], x[3])
    CNOT | (x[6], x[3])
    CNOT | (x[22], x[3])
    CNOT | (x[29], x[3])
    CNOT | (x[21], x[3])
    CNOT | (x[13], x[3])
    CNOT | (x[5], x[3])
    CNOT | (x[1],x[3])
    CNOT | (x[0], x[3])
    CNOT | (x[26], x[3])
    CNOT | (x[17], x[3])
    CNOT | (x[9], x[3])
    CNOT | (x[8], x[3])
    CNOT | (x[24], x[3])
    CNOT | (x[31], x[3])
    CNOT | (x[23], x[3])
    CNOT | (x[15], x[3])
    CNOT | (x[7], x[3])

    #2
    CNOT | (x[17], x[2])
    CNOT | (x[8], x[2])
    CNOT | (x[31], x[2])
    CNOT | (x[23], x[2])
    CNOT | (x[22], x[2])
    CNOT | (x[6], x[2])
    CNOT | (x[13], x[2])
    CNOT | (x[5], x[2])
    CNOT | (x[29], x[2])
    CNOT | (x[21], x[2])
    CNOT | (x[0], x[2])
    CNOT | (x[25], x[2])
    CNOT | (x[16], x[2])
    CNOT | (x[8], x[2])
    CNOT | (x[7], x[2])
    CNOT | (x[23], x[2])
    CNOT | (x[30], x[2])
    CNOT | (x[22], x[2])
    CNOT | (x[14], x[2])
    CNOT | (x[6], x[2])


    #1
    CNOT | (x[16], x[1])
    CNOT | (x[7], x[1])
    CNOT | (x[31], x[1])
    CNOT | (x[30], x[1])
    CNOT | (x[14], x[1])
    CNOT | (x[21], x[1])
    CNOT | (x[13], x[1])
    CNOT | (x[5], x[1])
    CNOT | (x[29], x[1])
    CNOT | (x[24], x[1])
    CNOT | (x[15], x[1])
    CNOT | (x[7], x[1])
    CNOT | (x[6], x[1])
    CNOT | (x[22], x[1])
    CNOT | (x[29], x[1])
    CNOT | (x[21], x[1])
    CNOT | (x[13], x[1])
    CNOT | (x[5], x[1])

    #0
    CNOT | (x[15], x[0])
    CNOT | (x[6], x[0])
    CNOT | (x[30], x[0])
    CNOT | (x[29], x[0])
    CNOT | (x[13], x[0])
    CNOT | (x[20], x[0])
    CNOT | (x[12], x[0])
    CNOT | (x[4], x[0])
    CNOT | (x[28], x[0])
    CNOT | (x[23], x[0])
    CNOT | (x[14], x[0])
    CNOT | (x[6], x[0])
    CNOT | (x[5], x[0])
    CNOT | (x[21], x[0])
    CNOT | (x[28], x[0])
    CNOT | (x[20], x[0])
    CNOT | (x[12], x[0])
    CNOT | (x[4], x[0])


    Swap | (x[0], x[31])
    Swap | (x[1], x[30])
    Swap | (x[2], x[29])
    Swap | (x[3], x[28])
    Swap | (x[4], x[27])
    Swap | (x[5], x[26])
    Swap | (x[6], x[25])
    Swap | (x[7], x[24])
    Swap | (x[8], x[23])
    Swap | (x[9], x[22])
    Swap | (x[10], x[21])
    Swap | (x[11], x[20])
    Swap | (x[12], x[19])
    Swap | (x[13], x[18])
    Swap | (x[14], x[17])
    Swap | (x[15], x[16])



def permutation_P1(eng, x, P1):
    for i in range(32):
        CNOT | (x[i], P1[i])
    for i in range(32):
        CNOT | (P1[(i + 15) % 32], x[i])
    for i in range(32):
        CNOT | (P1[(i + 23) % 32], x[i])





def CF_0(eng, j, W_low, W_high, A, B, C, D, E, F, G, H, AND_value, AND_value0, AND_value1, AND_value2, OR_value0, OR_value1, OR_value2, T, c0):
    with Compute(eng):
        T_0(eng, T, j)
        GG(eng, j, E, F, G, AND_value, AND_value0, OR_value0) #GG = OR_value0
        FF(eng, j, A, B, C, AND_value1, AND_value2, OR_value1, OR_value2) #FF = OR_value2
        SS_1(eng, A, E, T, j, c0) #SS1 = E
        SS_2(eng, E, A) #SS2 = A


    TT_2(eng, OR_value0, H, E, W_low, j, c0)  # TT2 = H
    MSG_Exp_0(eng, W_low, W_high)
    TT_1(eng, OR_value2, D, A, W_low, j, c0) #TT1 = D
    Uncompute(eng)

    permutation_P0(eng, H)

    for i in range(32):
        Swap | (D[i], H[i])

    for k in range(9):
        for i in range(31):
            Swap | (B[i], B[i + 1])

    for k in range(19):
        for i in range(31):
            Swap | (F[i], F[i + 1])

    for i in range(32):
        Swap | (A[i], H[i])
    for i in range(32):
        Swap | (B[i], H[i])
    for i in range(32):
        Swap | (C[i], H[i])
    for i in range(32):
        Swap | (D[i], H[i])
    for i in range(32):
        Swap | (E[i], H[i])
    for i in range(32):
        Swap | (F[i], H[i])
    for i in range(32):
        Swap | (G[i], H[i])


def FF(eng, j, x, y, z, AND_value1, AND_value2, OR_value1, OR_value2):
    if -1 < j and j < 16:
        for i in range(32):
            CNOT | (x[i], OR_value2[i])
            CNOT | (y[i], OR_value2[i])
            CNOT | (z[i], OR_value2[i])
    if 15 < j and j < 64:
        with Compute(eng):
            AND_gate(eng, x, z, AND_value1)
            AND_gate(eng, x, y, AND_value2)
        OR_gate(eng, AND_value1, AND_value2, OR_value1)
        for i in range(32):
            X | AND_value1[i]
        Uncompute(eng)

        AND_gate(eng, y, z, AND_value1)

        OR_gate(eng, OR_value1, AND_value1, OR_value2)





def GG(eng, j, x, y, z, AND_value1, AND_value2, OR_value2):
    if -1 < j and j < 16:
        for i in range(32):
            CNOT | (x[i], OR_value2[i])
            CNOT | (y[i], OR_value2[i])
            CNOT | (z[i], OR_value2[i])
    if 15 < j and j < 64:
        AND_gate(eng, x, y, AND_value1)
        for i in range(32):
            X | x[i]
        AND_gate(eng, x, z, AND_value2)
        OR_gate(eng, AND_value1, AND_value2, OR_value2)
        for i in range(32):
            X | x[i]


def OR_gate(eng, A, B, C):
    for i in range(32):
        X | A[i]
        X | B[i]
        Toffoli | (A[i], B[i], C[i])
        X | C[i]


def AND_gate(eng, B, A, AND_value):
    for i in range(32):
        with Control(eng, B[i]):
            with Control(eng, A[i]):
                X | AND_value[i]


def SM3_main(eng):
    j = 0
    AND_gate_value = eng.allocate_qureg(32)
    AND_gate_value0 = eng.allocate_qureg(32)
    AND_gate_value1 = eng.allocate_qureg(32)
    AND_gate_value2 = eng.allocate_qureg(32)
    OR_gate_value0 = eng.allocate_qureg(32)
    OR_gate_value1 = eng.allocate_qureg(32)
    OR_gate_value2 = eng.allocate_qureg(32)


    T = eng.allocate_qureg(32)
    p = eng.allocate_qureg(32)
    c0 = eng.allocate_qubit()

    A = eng.allocate_qureg(32)
    B = eng.allocate_qureg(32)
    C = eng.allocate_qureg(32)
    D = eng.allocate_qureg(32)
    E = eng.allocate_qureg(32)
    F = eng.allocate_qureg(32)
    G = eng.allocate_qureg(32)
    H = eng.allocate_qureg(32)


    M0 = eng.allocate_qureg(32)
    M1 = eng.allocate_qureg(32)
    M2 = eng.allocate_qureg(32)
    M3 = eng.allocate_qureg(32)
    M4 = eng.allocate_qureg(32)
    M5 = eng.allocate_qureg(32)
    M6 = eng.allocate_qureg(32)
    M7 = eng.allocate_qureg(32)
    M8 = eng.allocate_qureg(32)
    M9 = eng.allocate_qureg(32)
    M10 = eng.allocate_qureg(32)
    M11 = eng.allocate_qureg(32)
    M12 = eng.allocate_qureg(32)
    M13 = eng.allocate_qureg(32)
    M14 = eng.allocate_qureg(32)
    M15 = eng.allocate_qureg(32)
    M16 = eng.allocate_qureg(32)
    M17 = eng.allocate_qureg(32)
    M18 = eng.allocate_qureg(32)
    M19 = eng.allocate_qureg(32)
    M20 = eng.allocate_qureg(32)
    M21 = eng.allocate_qureg(32)
    M22 = eng.allocate_qureg(32)
    M23 = eng.allocate_qureg(32)
    M24 = eng.allocate_qureg(32)
    M25 = eng.allocate_qureg(32)
    M26 = eng.allocate_qureg(32)
    M27 = eng.allocate_qureg(32)
    M28 = eng.allocate_qureg(32)
    M29 = eng.allocate_qureg(32)
    M30 = eng.allocate_qureg(32)
    M31 = eng.allocate_qureg(32)
    M32 = eng.allocate_qureg(32)
    M33 = eng.allocate_qureg(32)
    M34 = eng.allocate_qureg(32)
    M35 = eng.allocate_qureg(32)
    M36 = eng.allocate_qureg(32)
    M37 = eng.allocate_qureg(32)
    M38 = eng.allocate_qureg(32)
    M39 = eng.allocate_qureg(32)
    M40 = eng.allocate_qureg(32)
    M41 = eng.allocate_qureg(32)
    M42 = eng.allocate_qureg(32)
    M43 = eng.allocate_qureg(32)
    M44 = eng.allocate_qureg(32)
    M45 = eng.allocate_qureg(32)
    M46 = eng.allocate_qureg(32)
    M47 = eng.allocate_qureg(32)
    M48 = eng.allocate_qureg(32)
    M49 = eng.allocate_qureg(32)
    M50 = eng.allocate_qureg(32)
    M51 = eng.allocate_qureg(32)
    M52 = eng.allocate_qureg(32)
    M53 = eng.allocate_qureg(32)
    M54 = eng.allocate_qureg(32)
    M55 = eng.allocate_qureg(32)
    M56 = eng.allocate_qureg(32)
    M57 = eng.allocate_qureg(32)
    M58 = eng.allocate_qureg(32)
    M59 = eng.allocate_qureg(32)
    M60 = eng.allocate_qureg(32)
    M61 = eng.allocate_qureg(32)
    M62 = eng.allocate_qureg(32)
    M63 = eng.allocate_qureg(32)
    M64 = eng.allocate_qureg(32)
    M65 = eng.allocate_qureg(32)
    M66 = eng.allocate_qureg(32)
    M67 = eng.allocate_qureg(32)

    # X | A[2]
    # X | A[3]
    # X | A[5]
    # X | A[8]
    # X | A[9]
    # X | A[11]
    # X | A[15]
    # X | A[17]
    # X | A[18]
    # X | A[20]
    # X | A[23]
    # X | A[27]
    # X | A[28]
    # X | A[29]
    # X | A[30]
    #
    # X | B[1]
    # X | B[2]
    # X | B[3]
    # X | B[4]
    # X | B[5]
    # X | B[9]
    # X | B[11]
    # X | B[14]
    # X | B[16]
    # X | B[19]
    # X | B[21]
    # X | B[22]
    # X | B[23]
    # X | B[25]
    # X | B[26]
    # X | B[27]
    # X | B[28]
    #
    # X | C[0]
    # X | C[3]
    # X | C[6]
    # X | C[8]
    # X | C[10]
    # X | C[11]
    # X | C[13]
    # X | C[15]
    # X | C[17]
    # X | C[18]
    # X | C[19]
    # X | C[20]
    # X | C[25]
    # X | C[28]
    # X | C[31]
    #
    # X | D[0]
    # X | D[3]
    # X | D[5]
    # X | D[6]
    # X | D[7]
    # X | D[8]
    # X | D[11]
    # X | D[12]
    # X | D[14]
    # X | D[16]
    # X | D[18]
    # X | D[19]
    # X | D[23]
    # X | D[27]
    # X | D[30]
    # X | D[31]
    #
    # X | E[1]
    # X | E[2]
    # X | E[7]
    # X | E[8]
    # X | E[9]
    # X | E[10]
    # X | E[11]
    # X | E[12]
    # X | E[15]
    # X | E[16]
    # X | E[19]
    # X | E[21]
    # X | E[22]
    # X | E[25]
    # X | E[29]
    # X | E[30]
    #
    # X | F[2]
    # X | F[3]
    # X | F[4]
    # X | F[5]
    # X | F[6]
    # X | F[8]
    # X | F[9]
    # X | F[10]
    # X | F[12]
    # X | F[15]
    # X | F[17]
    # X | F[19]
    # X | F[20]
    # X | F[23]
    # X | F[26]
    # X | F[27]
    # X | F[30]
    # X | F[31]
    #
    # X | G[2]
    # X | G[4]
    # X | G[6]
    # X | G[8]
    # X | G[10]
    # X | G[16]
    # X | G[17]
    # X | G[19]
    # X | G[22]
    # X | G[25]
    # X | G[27]
    # X | G[31]
    #
    # X | H[0]
    # X | H[1]
    # X | H[3]
    # X | H[4]
    # X | H[6]
    # X | H[7]
    # X | H[11]
    # X | H[14]
    # X | H[15]
    # X | H[19]
    # X | H[20]
    # X | H[22]
    # X | H[23]
    # X | H[24]
    # X | H[29]
    # X | H[30]

    # =======
    # padding
    # =======

    init_value(eng, A, B, C, D, E, F, G, H)

    init_MSG_Exp(eng, M16, M0, M7, M13, M3, M10, p)
    init_MSG_Exp(eng, M17, M1, M8, M14, M4, M11, p)
    init_MSG_Exp(eng, M18, M2, M9, M15, M5, M12, p)
    init_MSG_Exp(eng, M19, M3, M10, M16, M6, M13, p)
    init_MSG_Exp(eng, M20, M4, M11, M17, M7, M14, p)
    init_MSG_Exp(eng, M21, M5, M12, M18, M8, M15, p)
    init_MSG_Exp(eng, M22, M6, M13, M19, M9, M16, p)
    init_MSG_Exp(eng, M23, M7, M14, M20, M10, M17, p)
    init_MSG_Exp(eng, M24, M8, M15, M21, M11, M18, p)
    init_MSG_Exp(eng, M25, M9, M16, M22, M12, M19, p)
    init_MSG_Exp(eng, M26, M10, M17, M23, M13, M20, p)
    init_MSG_Exp(eng, M27, M11, M18, M24, M14, M21, p)
    init_MSG_Exp(eng, M28, M12, M19, M25, M15, M22, p)
    init_MSG_Exp(eng, M29, M13, M20, M26, M16, M23, p)
    init_MSG_Exp(eng, M30, M14, M21, M27, M17, M24, p)
    init_MSG_Exp(eng, M31, M15, M22, M28, M18, M25, p)
    init_MSG_Exp(eng, M32, M16, M23, M29, M19, M26, p)
    init_MSG_Exp(eng, M33, M17, M24, M30, M20, M27, p)
    init_MSG_Exp(eng, M34, M18, M25, M31, M21, M28, p)
    init_MSG_Exp(eng, M35, M19, M26, M32, M22, M29, p)
    init_MSG_Exp(eng, M36, M20, M27, M33, M23, M30, p)
    init_MSG_Exp(eng, M37, M21, M28, M34, M24, M31, p)
    init_MSG_Exp(eng, M38, M22, M29, M35, M25, M32, p)
    init_MSG_Exp(eng, M39, M23, M30, M36, M26, M33, p)
    init_MSG_Exp(eng, M40, M24, M31, M37, M27, M34, p)
    init_MSG_Exp(eng, M41, M25, M32, M38, M28, M35, p)
    init_MSG_Exp(eng, M42, M26, M33, M39, M29, M36, p)
    init_MSG_Exp(eng, M43, M27, M34, M40, M30, M37, p)
    init_MSG_Exp(eng, M44, M28, M35, M41, M31, M38, p)
    init_MSG_Exp(eng, M45, M29, M36, M42, M32, M39, p)
    init_MSG_Exp(eng, M46, M30, M37, M43, M33, M40, p)
    init_MSG_Exp(eng, M47, M31, M38, M44, M34, M41, p)
    init_MSG_Exp(eng, M48, M32, M39, M45, M35, M42, p)
    init_MSG_Exp(eng, M49, M33, M40, M46, M36, M43, p)
    init_MSG_Exp(eng, M50, M34, M41, M47, M37, M44, p)
    init_MSG_Exp(eng, M51, M35, M42, M48, M38, M45, p)
    init_MSG_Exp(eng, M52, M36, M43, M49, M39, M46, p)
    init_MSG_Exp(eng, M53, M37, M44, M50, M40, M47, p)
    init_MSG_Exp(eng, M54, M38, M45, M51, M41, M48, p)
    init_MSG_Exp(eng, M55, M39, M46, M52, M42, M49, p)
    init_MSG_Exp(eng, M56, M40, M47, M53, M43, M50, p)
    init_MSG_Exp(eng, M57, M41, M48, M54, M44, M51, p)
    init_MSG_Exp(eng, M58, M42, M49, M55, M45, M52, p)
    init_MSG_Exp(eng, M59, M43, M50, M56, M46, M53, p)
    init_MSG_Exp(eng, M60, M44, M51, M57, M47, M54, p)
    init_MSG_Exp(eng, M61, M45, M52, M58, M48, M55, p)
    init_MSG_Exp(eng, M62, M46, M53, M59, M49, M56, p)
    init_MSG_Exp(eng, M63, M47, M54, M60, M50, M57, p)
    init_MSG_Exp(eng, M64, M48, M55, M61, M51, M58, p)
    init_MSG_Exp(eng, M65, M49, M56, M62, M52, M59, p)
    init_MSG_Exp(eng, M66, M50, M57, M63, M53, M60, p)
    init_MSG_Exp(eng, M67, M51, M58, M64, M54, M61, p)


    #round 0
    # print('round 0')
    CF_0(eng, j, M0, M4, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1, OR_gate_value2, T, c0)
    j+=1

    # round 1
    # print('round 1')
    CF_0(eng, j, M1, M5, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 2
    # print('round 2')
    CF_0(eng, j, M2, M6, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 3
    # print('round 3')
    CF_0(eng, j, M3, M7, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 4
    # print('round 4')
    CF_0(eng, j, M4, M8, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 5
    # print('round 5')
    CF_0(eng, j, M5, M9, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 6
    # print('round 6')
    CF_0(eng, j, M6, M10, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 7
    # print('round 7')
    CF_0(eng, j, M7, M11, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 8
    # print('round 8')
    CF_0(eng, j, M8, M12, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 9
    # print('round 9')
    CF_0(eng, j, M9, M13, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 10
    # print('round 10')
    CF_0(eng, j, M10, M14, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 11
    # print('round 11')
    CF_0(eng, j, M11, M15, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1


    # round 12
    # print('round 12')
    CF_0(eng, j, M12, M16, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 13
    # print('round 13')
    CF_0(eng, j, M13, M17, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 14
    # print('round 14')
    CF_0(eng, j, M14, M18, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 15
    # print('round 15')
    CF_0(eng, j, M15, M19, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1


    #round 16
    # print('round 16')
    CF_0(eng, j, M16, M20, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 17
    # print('round 17')
    CF_0(eng, j, M17, M21, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 18
    # print('round 18')
    CF_0(eng, j, M18, M22, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 19
    # print('round 19')
    CF_0(eng, j, M19, M23, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 20
    # print('round 20')
    CF_0(eng, j, M20, M24, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 21
    # print('round 21')
    CF_0(eng, j, M21, M25, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 22
    # print('round 22')
    CF_0(eng, j, M22, M26, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 23
    # print('round 23')
    CF_0(eng, j, M23, M27, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 24
    # print('round 24')
    CF_0(eng, j, M24, M28, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 25
    # print('round 25')
    CF_0(eng, j, M25, M29, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 26
    # print('round 26')
    CF_0(eng, j, M26, M30, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 27
    # print('round 27')
    CF_0(eng, j, M27, M31, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 28
    # print('round 28')
    CF_0(eng, j, M28, M32, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 29
    # print('round 29')
    CF_0(eng, j, M29, M33, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 30
    # print('round 30')
    CF_0(eng, j, M30, M34, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 31
    # print('round 31')
    CF_0(eng, j, M31, M35, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 32
    # print('round 32')
    CF_0(eng, j, M32, M36, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 33
    # print('round 33')
    CF_0(eng, j, M33, M37, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 34
    # print('round 34')
    CF_0(eng, j, M34, M38, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 35
    # print('round 35')
    CF_0(eng, j, M35, M39, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 36
    # print('round 36')
    CF_0(eng, j, M36, M40, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 37
    # print('round 37')
    CF_0(eng, j, M37, M41, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 38
    # print('round 38')
    CF_0(eng, j, M38, M42, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 39
    # print('round 39')
    CF_0(eng, j, M39, M43, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2, OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 40
    # print('round 40')
    CF_0(eng, j, M40, M44, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2,
         OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 41
    # print('round 41')
    CF_0(eng, j, M41, M45, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2,
         OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 42
    # print('round 42')
    CF_0(eng, j, M42, M46, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2,
         OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 43
    # print('round 43')
    CF_0(eng, j, M43, M47, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2,
         OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 44
    # print('round 44')
    CF_0(eng, j, M44, M48, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2,
         OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 45
    # print('round 45')
    CF_0(eng, j, M45, M49, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2,
         OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 46
    # print('round 46')
    CF_0(eng, j, M46, M50, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2,
         OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 47
    # print('round 47')
    CF_0(eng, j, M47, M51, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2,
         OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 48
    # print('round 48')
    CF_0(eng, j, M48, M52, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2,
         OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 49
    # print('round 49')
    CF_0(eng, j, M49, M53, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2,
         OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 50
    # print('round 50')
    CF_0(eng, j, M50, M54, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2,
         OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 51
    # print('round 51')
    CF_0(eng, j, M51, M55, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2,
         OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 52
    # print('round 52')
    CF_0(eng, j, M52, M56, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2,
         OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 53
    # print('round 53')
    CF_0(eng, j, M53, M57, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2,
         OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 54
    # print('round 54')
    CF_0(eng, j, M54, M58, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2,
         OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 55
    # print('round 55')
    CF_0(eng, j, M55, M59, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2,
         OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 56
    # print('round 56')
    CF_0(eng, j, M56, M60, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2,
         OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 57
    # print('round 57')
    CF_0(eng, j, M57, M61, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2,
         OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 58
    # print('round 58')
    CF_0(eng, j, M58, M62, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2,
         OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 59
    # print('round 59')
    CF_0(eng, j, M59, M63, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2,
         OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 60
    # print('round 60')
    CF_0(eng, j, M60, M64, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2,
         OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 61
    # print('round 61')
    CF_0(eng, j, M61, M65, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2,
         OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 62
    # print('round 62')
    CF_0(eng, j, M62, M66, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2,
         OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)
    j += 1

    # round 63
    # print('round 63')
    CF_0(eng, j, M63, M67, A, B, C, D, E, F, G, H, AND_gate_value, AND_gate_value0, AND_gate_value1, AND_gate_value2,
         OR_gate_value0, OR_gate_value1,
         OR_gate_value2, T, c0)


    # init_value(eng, A, B, C, D, E, F, G, H)


    # All(Measure) | A
    # All(Measure) | B
    # All(Measure) | C
    # All(Measure) | D
    # All(Measure) | E
    # All(Measure) | F
    # All(Measure) | G
    # All(Measure) | H
    # print('Hash value')
    # for i in range(32):
    #     print(int(A[i]), end='')
    # print(' ')
    # for i in range(32):
    #     print(int(B[i]), end='')
    # print(' ')
    # for i in range(32):
    #     print(int(C[i]), end='')
    # print(' ')
    # for i in range(32):
    #     print(int(D[i]), end='')
    # print(' ')
    # for i in range(32):
    #     print(int(E[i]), end='')
    # print(' ')
    # for i in range(32):
    #     print(int(F[i]), end='')
    # print(' ')
    # for i in range(32):
    #     print(int(G[i]), end='')
    # print(' ')
    # for i in range(32):
    #     print(int(H[i]), end='')
    # print(' ')

#
# Resource = ClassicalSimulator()
# eng = MainEngine(Resource)
# SM3_main(eng)
# print(Resource)
