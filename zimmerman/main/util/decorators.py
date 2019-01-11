def uniq(a_list):
    encountered = set()
    result = []
    for elem in a_list:
        if elem not in encountered:
            result.append(elem)
        encountered.add(elem)
    return result