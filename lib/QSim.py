import numpy as np
from scipy.linalg import kron
from IPython.display import Markdown as md

class Tools:
    def basis(self, string='00010'):
        '''string: the qubits sequence'''
        spin_up = np.array([[1, 0]]).T
        spin_down = np.array([[0, 1]]).T
        # bit[0] = |0>, bit[1] = |1>
        bit = [spin_up, spin_down]
        res = np.array([[1]])
        # 从最后一位开始往前数，做克罗内克积
        for idx in string[::-1]:
            res = kron(bit[int(idx)], res)
        return np.matrix(res)

    def hilbert_space(self, nbit=5):
        nspace = 2 ** nbit
        for i in range(nspace):
            # bin(7) = 0b100
            binary = bin(i)[2:]
            nzeros = nbit - len(binary)
            yield '0' * nzeros + binary

    def wave_func(self, coef=[], seqs=[]):
        '''返回由振幅和几个Qubit序列表示的叠加态波函数，
           sum_i coef_i |psi_i> '''
        res = 0
        for i, a in enumerate(coef):
            res += a * self.basis(seqs[i])
        return np.matrix(res)

    def project(self, wave_func, direction):
        '''<Psi | phi_i> to get the amplitude '''
        return wave_func.H * direction

    def decompose(self, wave_func):
        '''将叠加态波函数分解'''
        nbit = int(np.log2(len(wave_func)))
        amplitudes = []
        direct_str = []
        for seq in self.hilbert_space(nbit):
            direct = self.basis(seq)
            amp = self.project(wave_func, direct).A1[0]  #A1 属性将矩阵转化为 1 维 numpy 数组
            if np.linalg.norm(amp) != 0:
                amplitudes.append(amp)
                direct_str.append(seq)
        return amplitudes, direct_str

    def print_wf(self, wf):
        coef, seqs = self.decompose(wf)
        latex = ""
        for i, seq in enumerate(seqs):
            latex += r"%s$|%s\rangle$" % (coef[i], seq)
            if i != len(seqs) - 1:
                latex += "+"
        return md(latex)

# Define the one-qubit and 2-qubit operation gates
Gates = {
    'I': np.matrix("1 0; 0 1"),
    'X': np.matrix("0 1; 1 0"),
    'Y': np.matrix("0 -1j; 1j 0"),
    'Z': np.matrix("1 0; 0 -1"),
    'H': np.matrix("1 1; 1 -1") / np.sqrt(2),
    'CNOT': np.matrix("1 0 0 0; 0 1 0 0; 0 0 0 1; 0 0 1 0"),
    'SWAP': np.matrix("1 0 0 0; 0 0 1 0; 0 1 0 0; 0 0 0 1")
}

class QuantumRegister:
    def __init__(self, numQubits):
        self.numQubits = numQubits
        self.amplitudes = np.zeros(2**numQubits)
        self.amplitudes[0] = 1
        self.value = False

    # generate Matrix by given gates
    def generateMatrix(self, gate, numQubits, q1, q2=-1):
        res = np.array([[1]])
        if q2 == -1:
            for i in range(self.numQubits):
                if(i == q1):
                    res = kron(res, Gates[gate])
                else:
                    res = kron(res, Gates['I'])
        else:
            for i in range(self.numQubits-1):
                if (i == q1):
                    res = kron(res, Gates[gate])
                    i = i+1
                else:
                    res = kron(res, Gates['I'])
        return res

    def add(self, gate, q1, q2=-1):
        if self.value:
            raise ValueError('Cannot add Gate to Measured Register')
        if gate not in Gates:
            raise Exception('Gate {} is not defined in Gates'.format(gate))
        # 暂时只考虑相邻的门
        gateMatrix = self.generateMatrix(gate, self.numQubits, q1, q2)
        self.amplitudes = np.dot(self.amplitudes, gateMatrix)

    def measure(self):
        if(self.value):
            return print_wf(self.value)
        self.probabilities = []
        for amp in np.nditer(self.amplitudes):
            probability = np.absolute(amp) ** 2
            self.probabilities.append(probability)
        results = list(range(len(self.probabilities)))
        self.value = np.binary_repr(
            np.random.choice(results, p=self.probabilities),
            self.numQubits
        )
        return self.value