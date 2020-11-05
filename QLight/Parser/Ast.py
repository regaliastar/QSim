class SyntaxTree(object):
    '''
    实现抽象语法树
    '''
    def __init__(self):
        # 树的根节点
        self.root = None
        # 现在遍历到的节点
        self.current = None

    # 添加一个子节点，必须确定father在该树中
    def add_child_node(self, new_node, father=None):
        if not father:
            father = self.current
        # 认祖归宗
        new_node.father = father
        # 如果father节点没有儿子，则将其赋值为其第一个儿子
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

    # 交换相邻的两棵兄弟子树
    def switch(self, left, right):
        left_left = left.left
        right_right = right.right
        left.left = right
        left.right = right_right
        right.left = left_left
        right.right = left
        if left_left:
            left_left.right = right
        if right_right:
            right_right.left = left

class SyntaxTreeNode(object):
    '''语法树节点'''
    def __init__(self, value=None, _type=None, extra_info=None):
        # 节点的值，为文法中的终结符或者非终结符
        self.value = value
        # 记录某些token的类型
        self.type = _type
        # 语义分析中记录关于token的其他一些信息，比如关键字是变量，该变量类型为int
        self.extra_info = extra_info
        self.father = None
        self.left = None
        self.right = None
        self.first_son = None
    # 设置value
    def set_value(self, value):
        self.value = value
    # 设置type
    def set_type(self, _type):
        self.type = _type
    # 设置extra_info
    def set_extra_info(self, extra_info):
        self.extra_info = extra_info