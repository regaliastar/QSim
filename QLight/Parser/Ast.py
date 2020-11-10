class SyntaxTree(object):
    '''
    实现抽象语法树
    '''
    def __init__(self):
        self.root = None
        self.current = None

    def add_child_node(self, new_node, father=None):
        if not father:
            father = self.current
        new_node.father = father
        if not father.first_son:
            father.first_son = new_node
        else:
            current_node = father.first_son
            while current_node.right:
                current_node = current_node.right
            current_node.right = new_node
            new_node.left = current_node
        self.current = new_node

    def find_all_child(self, node):
        """
        遍历node子节点
        :return list
        """
        if node.first_son:
            res = []
            child = node.first_son
            while child:
                res.append(child)
                child = child.right
            return res
        else:
            return []

    def show(self):
        self.show_core(self.root)

    def show_core(self, node):
        '''DFS遍历语法树'''
        if not node:
            return
        output = open('log/parser.txt', 'a', encoding = 'utf-8')
        output.write(node.format())
        output.close()
        child = node.first_son
        while child:
            self.show_core(child)
            child = child.right

class SyntaxTreeNode(object):
    '''语法树节点'''
    def __init__(self, value=None, _type=None, extra_info=None):
        self.value = value
        self.type = _type
        self.extra_info = extra_info
        self.father = None
        self.left = None
        self.right = None
        self.first_son = None

    def set_value(self, value):
        self.value = value
    def set_type(self, _type):
        self.type = _type
    def set_extra_info(self, extra_info):
        self.extra_info = extra_info

    def format(self):
        '''格式化输出'''
        return '( self: %s %s,first_son: %s, father: %s, left: %s, right: %s )\r\n' % (
            self.value, self.type, self.first_son.value if self.first_son else None, self.father.value if self.father else None, self.left.value if self.left else None,
            self.right.value if self.right else None)
