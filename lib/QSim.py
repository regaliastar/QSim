import numpy as np
from scipy.linalg import kron
import sys

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

    # @param wave_func: np.martix
    def project(self, wave_func, direction):
        '''<Psi | phi_i> to get the amplitude '''
        return wave_func.H * direction

    # @param wave_func: np.martix
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

    # @param wf: np.martix
    def print_wf(self, wf):
        coef, seqs = self.decompose(wf)
        str = ''
        for i, seq in enumerate(seqs):
            str += '{}|{}>'.format(coef[i], seq)
            if i != len(seqs) - 1:
                str += '+'
        return str

# Define the one-qubit and 2-qubit operation gates
Gates = {
    # 'I': np.matrix("1 0; 0 1"),
    # 'X': np.matrix("0 1; 1 0"),
    # 'Y': np.matrix("0 -1j; 1j 0"),
    # 'Z': np.matrix("1 0; 0 -1"),
    # 'H': np.matrix("1 1; 1 -1") / np.sqrt(2),
    # 'CNOT2_01': np.matrix("1 0 0 0; 0 1 0 0; 0 0 0 1; 0 0 1 0"),
    # 'CNOT2_10': np.matrix("1 0 0 0; 0 0 0 1; 0 0 1 0; 0 1 0 0"),
    # 'SWAP2_01': np.matrix("1 0 0 0; 0 0 1 0; 0 1 0 0; 0 0 0 1")
    'I': np.array([[1, 0], [0, 1]]),
    'X': np.array([[0, 1], [1, 0]]),
    'Y': np.array([[0, -1j], [1j, 0]]),
    'Z': np.array([[1, 0], [0, -1]]),
    'H': np.array([[1 / np.sqrt(2), 1 / np.sqrt(2)], [1 / np.sqrt(2), -1 / np.sqrt(2)]]),
    'CNOT2_01': np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]), #控制位在第一个
    'CNOT2_10': np.array([[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]]), #控制位在第二个
    'SWAP2_01': np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
}

class QuantumRegister:
    def __init__(self, numQubits=-1, coef = '-1', basis='-1'):
        tools = Tools()
        if type(numQubits)==type(int(numQubits)) and numQubits>0 :  #判断 numQubits 是否为正整数
            self.numQubits = numQubits
            # self.amplitudes = np.zeros(2**numQubits)
            dim_1 = ['0' for index in range(numQubits)]
            basisStr = ''.join(dim_1)
            self.amplitudes = tools.basis(basisStr).A1
            self.amplitudes[0] = '1'                    # 因为默认的输入是 '00000...0'
            self.value = False
        elif basis is not '-1' and isinstance(basis,str): #生成初态如 '0110...'
            self.amplitudes = tools.basis(basis).A1
            self.numQubits = len(basis)
            self.value = False
        elif coef is not '-1':  #生成初态如 '1/2|00>+1/2|01>+1/2|10>+1/2|11>'
            # 验证输入
            if not isinstance(coef,list) or not isinstance(basis,list):
                raise Exception('Failed to excuse coef {}, basis {}'.format(coef, basis))
            self.amplitudes = tools.wave_func(coef, basis).A1
            self.numQubits = len(basis[0])
            self.value = False
        else:
            raise ValueError('Failed to import arguments: {}'.format(sys.argv))

    # get current amplitudes
    # @return np.ndarray
    def getAmplitudes(self):
        return self.amplitudes

    # 将 self.amplitudes 转为能被 print_wf 函数解析的 wave_func 格式
    # ndarray 转为 matrix，
    # 一维 转为 二维
    # @return np.matrix
    def a2wf(self):
        return np.mat(self.amplitudes.reshape(2 ** self.numQubits, 1))

    # generate Matrix by given gates
    # 暂时只考虑相邻的门
    # @return np.ndarray
    def generateMatrix(self, gate, q1, q2=-1):
        res = np.array([[1]])
        if q2 == -1:    # 单比特门
            for i in range(self.numQubits):
                if i == q1:
                    res = kron(res, Gates[gate])
                else:
                    res = kron(res, Gates['I'])
        else:           # 双比特门
            for i in range(self.numQubits-1):
                if i == q1:
                    res = kron(res, Gates[gate])
                    i = i+1
                else:
                    res = kron(res, Gates['I'])
        return res

    # 将gate转化成矩阵
    # 适用于跨线路门
    # 控制位在上
    # CNOT, C-Z, C-U
    # @return np.ndarray
    def gate2Matrix(self, gate, q1, q2=-1):
        if gate not in Gates:
            raise ValueError('Gate {} is not defined in Gates'.format(gate))
        if q2 == -1:
            return Gates[gate]
        if q2 > q1:
            m_size = 2 ** (q2 - q1 + 1)
            base = np.identity(m_size)
            for i in range(int(m_size/4)):
                # base[m_size/2+1+i*2][m_size/2+1+i*2]
                for j in range(2):
                    for k in range(2):
                        base[int(m_size / 2 + i * 2 + j)][int(m_size / 2  + i * 2 + k)] = Gates[gate][j][k]
            return base

    def applyGate(self, gate, q1, q2=-1):
        if self.value:
            raise ValueError('Cannot add Gate to Measured Register')
        if gate not in Gates:
            raise ValueError('Gate {} is not defined in Gates'.format(gate))
        gateMatrix = self.generateMatrix(gate, q1, q2)
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