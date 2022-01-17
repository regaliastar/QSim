import numpy as np
from sklearn.preprocessing import normalize
import sys
from lib.Noisy import Noisy

noisy = Noisy()

class GateManager:
    Gates = {
        'I': np.array([[1.0, 0], [0, 1]]),
        'X': np.array([[0.0, 1], [1, 0]]),
        'Y': np.array([[0.0, -1j], [1j, 0]]),
        'Z': np.array([[1.0, 0], [0, -1]]),
        'P': np.array([[1.0, 0], [0, 1j]]),
        'H': np.array([[1 / np.sqrt(2), 1 / np.sqrt(2)], [1 / np.sqrt(2), -1 / np.sqrt(2)]]),
        'S': np.array([[1.0, 0], [0, 1j]]),
        'T': np.array([[1.0, 0], [0, np.exp(1j * np.pi / 4)]]),
        'V': np.array([[(1 + 1j) / 2, -1j * (1 + 1j) / 2], [-1j * (1 + 1j) / 2, (1 + 1j) / 2]]),
        'V_H': np.array([[(1 - 1j) / 2, 1j * (1 - 1j) / 2], [1j * (1 - 1j) / 2, (1 - 1j) / 2]]),
        'SWAP': np.array([[1.0, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
    }

    def getGate(gate):
        if gate in GateManager.Gates:
            result = noisy.getNoisyGate(GateManager.Gates[gate])
            return result
        if gate[0] == 'R':
            k = int(gate[1:])
            result = noisy.getNoisyGate(np.array([[1, 0], [0, np.exp(2j * np.pi / 2**k)]]))
            return result
        raise ValueError('Failed to GateManager.getGate!')

    def has(gate):
        if gate in GateManager.Gates:
            return True
        if gate[0] == 'R':
            return True
        return False

    def getGates():
        return GateManager.Gates

    def setGates(name, matrix):
        if name in GateManager.Gates:
            raise ValueError('Gate {} is already defined in GateManager.Gates'.format(name))
        if not isinstance(matrix,np.ndarray):
            raise ValueError('matrix must be np.ndarray instance!')
        GateManager.Gates[name] = matrix

    def gate2Matrix(gate, q1, q2=-1):
        '''
        将gate转化成矩阵
        适用于跨线路门
        控制位在上下都可以
        CNOT, C-Z, C-U
        :return np.ndarray
        '''
        if not GateManager.has(gate):
            raise ValueError('Gate {} is not defined in Gates'.format(gate))
        gate_matrix = GateManager.getGate(gate)
        if q2 == -1:
            return gate_matrix
        if q2 > q1:
            m_size = 2 ** (q2 - q1 + 1)
            base = np.identity(m_size)
            for i in range(int(m_size / 4)):
                # base[m_size/2+i*2][m_size/2+i*2]
                for j in range(2):
                    for k in range(2):
                        base[int(m_size / 2 + i * 2 + j)][int(m_size / 2 + i * 2 + k)] = gate_matrix[j][k]
            return base
        elif q2 < q1:
            m_size = 2 ** (q1 - q2 + 1)
            base = np.identity(m_size)
            for i in range(int(m_size / 4)):
                # 1+2*i, 1+2*i+m_size/2
                for j in range(2):
                    for k in range(2):
                        base[int(1 + 2 * i + j * m_size / 2)][int(1 + 2 * i + k * m_size / 2)] = gate_matrix[j][k]
            return base
        else:
            raise ValueError('Failed to input args!')

