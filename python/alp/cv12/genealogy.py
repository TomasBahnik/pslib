import sys


class Person:
    def __init__(self, name, sex):
        self.name = name
        self.sex = sex
        self.children = []
        self.parents = []  # parents of this node
        self.partner = None  # partner (=husband/wife of this node)

    def add_child(self, node):
        self.children.append(node)

    def add_parent(self, node):
        self.parents.append(node)

    def set_partner(self, node):
        self.partner = node

    def __str__(self):
        s = "Female" if self.sex == 'F' else "Male"
        return self.name + " " + s

    def __repr__(self):
        s = "Female" if self.sex == 'F' else "Male"
        return self.name + " " + s


def findPerson(name, family):  # name is string
    for person in family:
        if person == name:
            return person
    return None


def loadFamily():
    f = open(sys.argv[1], "r")
    family = []
    for line in f:
        typ, name1, name2, sex1, sex2 = line.strip().split()
        p1 = findPerson(name1, family)
        if p1 == None:
            p1 = Person(name1, sex1)
            family.append(p1)
        p2 = findPerson(name2, family)
        if p2 == None:
            p2 = Person(name2, sex2)
            family.append(p1)

        if typ == "M":
            p1.set_partner(p2)
            p2.set_partner(p1)
        elif typ == "P":
            p1.add_child(p2)
            p2.add_child(p1)
    return family


def findChildren(name, family):  # name is string
    person = findPerson(name, family)
    if person == None:
        return []
    res = []
    for child in person.children:
        res.append(child)
    if person.partner != None:
        for child in person.partner.children:
            res.append(child)
    return res


def findGC(name, family):  # name is string
    children = findChildren(name, family)
    res = []
    for person in children:
        res += findChildren(person.name, family)
    return res


# family = loadFamily()
# print(family)

for person in loadFamily():
    print(person)

"""
nevali to !!!!
"""
family = loadFamily()
print(family)


# for person in findGC("Jan", family):
#     print(person)

sys.exit(1)
