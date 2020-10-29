import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #当前程序上上一级目录，这里为QSim
sys.path.append(BASE_DIR) #添加环境变量
from lib.GateManager import GateManager
import numpy as np
from scipy.linalg import kron
from sklearn.preprocessing import normalize

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
        '''
        返回由振幅和几个Qubit序列表示的叠加态波函数，
        sum_i coef_i |psi_i>
        '''
        res = 0
        for i, a in enumerate(coef):
            res += a * self.basis(seqs[i])
        return np.matrix(res)

    # @param wave_func: np.martix
    def project(self, wave_func, direction):
        '''
        <Psi | phi_i> to get the amplitude
        '''
        return wave_func.H * direction

    def decompose(self, wave_func):
        '''
        将叠加态波函数分解
        :param wave_func: np.martix
        '''
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
        '''
        :param wf: np.martix
        :return: sr
        '''
        coef, seqs = self.decompose(wf)
        str = '|psi> = '
        for i, seq in enumerate(seqs):
            str += '{}|{}>'.format(coef[i], seq)
            if i != len(seqs) - 1:
                str += '+'
        return str

    def normalization(self, coef):
        '''
        将输入参数归一化，如：[0.1, 0.4] => [0.2, 0.8]
        :param coef:
        :return:
        '''
        return coef / np.linalg.norm(coef)

class QuantumRegister:
    def __init__(self, numQubits=-1, coef = '-1', basis='-1'):
        '''
        定义了3种构造方法：QuantumRegister()
        :param numQubits: number
        :param coef: list
        :param basis: str or list
        '''
        tools = Tools()
        if type(numQubits)==type(int(numQubits)) and numQubits>0 :  #判断 numQubits 是否为正整数
            self.numQubits = numQubits
            dim_1 = ['0' for index in range(numQubits)]
            basisStr = ''.join(dim_1)
            self.amplitudes = tools.basis(basisStr).A1
            self.amplitudes[0] = '1'                    # 因为默认的输入是 '00000...0'
            self.value = False
            self.measured = np.zeros(self.numQubits)
        elif basis is not '-1' and isinstance(basis,str): #生成初态如 '0110...'
            self.amplitudes = tools.basis(basis).A1
            self.numQubits = len(basis)
            self.value = False
            self.measured = np.zeros(self.numQubits)
        elif coef is not '-1':  #生成初态如 '1/2|00>+1/2|01>+1/2|10>+1/2|11>'
            # 验证输入
            if not isinstance(coef,list) or not isinstance(basis,list):
                raise Exception('Failed to excuse coef {}, basis {}'.format(coef, basis))
            self.amplitudes = tools.wave_func(coef, basis).A1
            self.numQubits = len(basis[0])
            self.value = False
            self.measured = np.zeros(self.numQubits)
        else:
            raise ValueError('Failed to import arguments: {}'.format(sys.argv))

    def getAmplitudes(self):
        '''
        get current amplitudes
        :return np.ndarray
        '''
        return self.amplitudes

    def getBasicInfo(self):
        info = {
            'numQubits': self.numQubits,
            'measured': self.measured,
            'value': self.value,
            'amplitudes': self.getAmplitudes()
        }
        return info

    def a2wf(self):
        '''
        将 self.amplitudes 转为能被 print_wf 函数解析的 wave_func 格式
        ndarray 转为 matrix，一维 转为 二维
        :return np.matrix
        '''
        return np.mat(self.amplitudes.reshape(2 ** self.numQubits, 1))

    def getCurrentIndex(self, q1, q2=-1):
        '''
        由于测试单个比特，导致Index和线路模型中的Index不同
        根据self.measured表来生成符合波函数的index，如对于3比特系统:
        q0 ---H---*---M    此时波函数有q1,q2，因此若输入位置1，需转换为当前Index = 0
                  |
        q1 -------C------M 此时波函数只有q2，因此若输入位置2，需转换为当前Index = 0

        q2 ----------------
        :param q1:
        :param q2:
        :return:
        '''
        [index_1, index_2] = [0, 0]
        if q2 == -1:
            for i in range(q1):
                if self.measured[i] == 1:
                    index_1 += 1
            index_1 = q1 - index_1
            return index_1
        else:
            [index_1, index_2] = [0, 0]
            for i in range(q1):
                if self.measured[i] == 1:
                    index_1 += 1
            index_1 = q1 - index_1
            for i in range(q2):
                if self.measured[i] == 1:
                    index_2 += 1
            index_2 = q2 - index_2
            return [index_1, index_2]

    def generateMatrix(self, gate, q1, q2=-1):
        '''
        generate Matrix by given gates
        暂时不考虑并行，每添加一个门就进行一次波函数的运算
        :return np.ndarray
        '''
        res = np.array([[1]])
        if q2 == -1:    # 单比特门
            index_1 = self.getCurrentIndex(q1, q2)
            for i in range(self.numQubits):
                if i == index_1:
                    res = kron(res, GateManager.Gates[gate])
                else:
                    res = kron(res, GateManager.Gates['I'])
        else:           # 双比特门
            [index_1, index_2] = self.getCurrentIndex(q1, q2)
            length = index_1-index_2 if index_1>index_2 else index_2-index_1
            min = index_1 if index_1<index_2 else index_2
            matrix = GateManager.gate2Matrix(gate, index_1, index_2)
            for i in range(self.numQubits-length):
                if i == min:
                    res = kron(res, matrix)
                else:
                    res = kron(res, GateManager.Gates['I'])
        return res

    def applyGate(self, gate, q1, q2=-1):
        if self.value:
            raise ValueError('Cannot add Gate to Measured Register')
        if gate not in GateManager.Gates:
            raise ValueError('Gate {} is not defined in Gates'.format(gate))
        gateMatrix = self.generateMatrix(gate, q1, q2)
        self.amplitudes = np.dot(self.amplitudes, gateMatrix)

    def measure(self, place=-1, count=1):
        '''
        若 place 为空，则测量全局
        否则测量第place个比特
        :param: place 测量第place个比特
        :param: count 全局测试的次数
        :return: str
        '''
        if(self.value):
            return print_wf(self.value)
        if place == -1:
            _v = {'value':{}}
            _v['count'] = count
            for i in range(count):
                self.probabilities = []
                for amp in np.nditer(self.amplitudes):
                    probability = np.absolute(amp) ** 2
                    self.probabilities.append(probability)
                results = list(range(len(self.probabilities)))
                v = np.binary_repr(
                    np.random.choice(results, p=self.probabilities),
                    self.numQubits
                )
                if v in _v['value']:
                    _v['value'][v] += 1
                else:
                    _v['value'][v] = 1
            self.value = _v
            return _v
        elif type(place)==type(int(place)) and place>=0:
            if self.measured[place] == 1:
                raise ValueError('{} is measured already!'.format(place))
            index = self.getCurrentIndex(place)
            tools = Tools()
            coef, seqs = tools.decompose(self.a2wf())
            [prob_0, prob_1] = [0, 0]
            probabilities = np.zeros(2)
            for i, seq in enumerate(seqs):
                prob_0 += np.square(coef[i]) if seq[index] == '0' else 0
            probabilities[0] = prob_0
            probabilities[1] = 1 - prob_0
            ls = [0, 1]
            selected = np.random.choice(ls, p=probabilities)
            self.measured[place] = 1
            # 重新生成状态
            co = []
            ba = []
            for i, seq in enumerate(seqs):
                if seq[index] == str(selected):
                    co.append(coef[i])
                    ba.append(seq[0:index] + seq[index+1:len(seq)])
            co = tools.normalization(co)
            self.amplitudes = tools.wave_func(co, ba).A1
            self.numQubits = len(ba[0])
            return selected
        else:
            raise ValueError('Failed to import arguments: {}'.format(sys.argv))
