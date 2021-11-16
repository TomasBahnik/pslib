# Implementace binárního stromu
#
# Jan Kybic, 2016


class BinaryTree:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


# převod výrazu na řetězec
def to_string_preorder(tree):
    return (str(tree.data) + " " +
            to_string_preorder(tree.left) +
            to_string_preorder(tree.right)
            if tree else "")


def to_string_postorder(tree):
    return (to_string_postorder(tree.left) +
            to_string_postorder(tree.right) + " " + str(tree.data)
            if tree else "")


def to_string_inorder(tree):
    if not tree:  # prázdný strom
        return ""
    if tree.left:  # binární operátor
        return ("(" + to_string_inorder(tree.left) + str(tree.data)
                + to_string_inorder(tree.right) + ")")
    return str(tree.data)  # jen jedno číslo


def evaluate(tree):
    """ Vyhodnotí aritmetický výraz zadaný ve formě binárního stromu """
    if tree.data == '+':
        return evaluate(tree.left) + evaluate(tree.right)
    if tree.data == '-':
        return evaluate(tree.left) - evaluate(tree.right)
    if tree.data == '*':
        return evaluate(tree.left) * evaluate(tree.right)
    if tree.data == '/':
        return evaluate(tree.left) / evaluate(tree.right)
    return tree.data  # jen jedno číslo


# one more implementation using a dictionary
import operator

operators = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}


def evaluate2(tree):
    if tree.left:
        fn = operators[tree.data]
        return fn(evaluate(tree.left), evaluate(tree.right))
    else:
        return tree.data


# příklad stromu reprezentujícího aritmetický výraz
def test_expression():
    t = BinaryTree('*',
                   BinaryTree('+',
                              BinaryTree(7),
                              BinaryTree(3)),
                   BinaryTree('-',
                              BinaryTree(5),
                              BinaryTree(2)))
    print(to_string_preorder(t))
    print(to_string_postorder(t))
    print(to_string_inorder(t))
    print(evaluate(t))
    print(evaluate2(t))


if __name__ == "__main__":
    test_expression()
