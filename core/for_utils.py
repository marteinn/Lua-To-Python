def get_for_range(start, end, step=1):
    if step > 0:
        comp = lambda x, y: x <= y
    else:
        comp = lambda x, y: x >= y

    index = start
    while comp(index, end):
        yield index
        index = index + step
