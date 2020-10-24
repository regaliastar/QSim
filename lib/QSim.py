import numpy as np
from scipy.linalg import kron
from IPython.display import Markdown as md

spin_up = np.array([[1, 0]]).T
spin_down = np.array([[0, 1]]).T
# bit[0] = |0>, bit[1] = |1>
bit = [spin_up, spin_down]
def basis(string='00010'):
    '''string: the qubits sequence'''
    res = np.array([[1]])
    # 从最后一位开始往前数，做直积
    for idx in string[::-1]:
        res = kron(bit[int(idx)], res)
    return np.matrix(res)
# Define the one-qubit and 2-qubit operation gates
I = np.matrix("1 0; 0 1")
X = np.matrix("0 1; 1 0")
Y = np.matrix("0 -1j; 1j 0")
Z = np.matrix("1 0; 0 -1")
H = np.matrix("1 1; 1 -1") / np.sqrt(2)
CNOT = np.matrix("1 0 0 0; 0 1 0 0; 0 0 0 1; 0 0 1 0")
SWAP = np.matrix("1 0 0 0; 0 0 1 0; 0 1 0 0; 0 0 0 1")
gates = {'I':I,  'X':X, 'Y':Y, 'Z':Z, 'H':H, 'CNOT':CNOT, 'SWAP':SWAP}
def hilbert_space(nbit=5):
    nspace = 2**nbit
    for i in range(nspace):
        #bin(7) = 0b100
        binary = bin(i)[2:]
        nzeros = nbit - len(binary)
        yield '0'*nzeros + binary
def wave_func(coef=[], seqs=[]):
    '''返回由振幅和几个Qubit序列表示的叠加态波函数，
       sum_i coef_i |psi_i> '''
    res = 0
    for i, a in enumerate(coef):
        res += a * basis(seqs[i])
    return np.matrix(res)
def project(wave_func, direction):
    '''<Psi | phi_i> to get the amplitude '''
    return wave_func.H * direction
def decompose(wave_func):
    '''将叠加态波函数分解'''
    nbit = int(np.log2(len(wave_func)))
    amplitudes = []
    direct_str = []
    for seq in hilbert_space(nbit):
        direct = basis(seq)
        amp = project(wave_func, direct).A1[0]
        if np.linalg.norm(amp) != 0:
            amplitudes.append(amp)
            direct_str.append(seq)
    return amplitudes, direct_str
def print_wf(wf):
    coef, seqs = decompose(wf)
    latex = ""
    for i, seq in enumerate(seqs):
        latex += r"%s$|%s\rangle$"%(coef[i], seq)
        if i != len(seqs) - 1:
            latex += "+"
    return md(latex)

if __name__ == '__main__':

