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

    def show(self):
        self.show_core(self.root)

    def show_core(self, node):
        '''DFS遍历语法树'''
        if not node:
            return
        output = open('parser.txt', 'a')
        output.write('( self: %s %s, father: %s, left: %s, right: %s )\r\n' % (
        node.value, node.type, node.father.value if node.father else None, node.left.value if node.left else None,
        node.right.value if node.right else None))
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