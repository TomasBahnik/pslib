# Implementace insertion sort (třídění vkládáním) pomocí spojových seznamů
#
# Jan Kybic, 2016

from linkedlistqueue import Node, ListQueue

""" OrderedList keeps the list sorted in a descending order, elements are inserted only using insert """


class OrderedList(ListQueue):

    def insert(self, x):
        """ inserts item x in the right position into a sorted list"""
        newnode = Node(x)
        prev = None
        node = self.head
        while node is not None and x < node.data:
            prev = node
            node = node.next
        if node is None:  # newnode patří na konec
            if self.head is None:  # seznam je prázdný
                self.head = newnode
            else:
                self.last.next = newnode
            self.last = newnode
        else:
            if prev is None:  # newnode patří na začátek
                self.head = newnode
            else:  # newnode patří mezi prev a node
                prev.next = newnode
            newnode.next = node
        self.count += 1


def insertion_sort_linkedlist(a):
    """ sorts array a inplace in ascending order """
    q = OrderedList()
    for x in a:
        q.insert(x)
    for i in range(len(a) - 1, -1, -1):
        a[i] = q.pop()  # from the highest value


# ----------------------- testing ----------------------------

def main():
    import random
    a = [random.randrange(100) for i in range(10)]
    print(a)
    insertion_sort_linkedlist(a)
    print(a)


def test():
    # kontrola na mnoha náhodných vstupech
    import sorting_experiments
    sorting_experiments.test_sort(f=insertion_sort_linkedlist)


def timing():
    # měření času
    import sorting_experiments
    from sorting_experiments import insertion_sort as insertion_sort_array
    # a=[random.randrange(1000000) for i in range(10000)]
    # t0=time.clock()
    # a1=insertion_sort_array(a)
    # t1=time.clock()
    # t2=time.clock()
    # a2=insertion_sort(a)
    # t3=time.clock()
    # print("insertion_sort_array: ",t1-t0, "  insertion_sort:", t3-t2)

    sorting_experiments.time_sorting_algorithms(algs=[  # sorting_experiments.bubble_sort,
        sorting_experiments.selection_sort,
        insertion_sort_array,
        insertion_sort_linkedlist],
        # merge_sort_experiments.merge_sort,
        # quick_sort_experiments.quick_sort,
        # sorting_experiments.python_sort
        prefix="time_with_insertion_sort_linkedlist")


if __name__ == "__main__":
    main()
    test()
    timing()
