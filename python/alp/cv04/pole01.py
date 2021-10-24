def find(where, what):
    for i in range(len(where)), len(what) + 1:
        j = 0
        while j < len(what):
            if where[i + j] == what[j]:
                j += 1
            else:
                break
        if len(what) == j:
            return i
    return None


print(find('abcdf', 'BB'))
#nefunguje
