
def querySet_to_list(query_set,field):
    query_list = []
    for event in query_set:
        query_list.append(event[field])
    return query_list