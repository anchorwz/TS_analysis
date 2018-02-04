
def WindowSliding(data, gen_lines, compute_error, data_range=None, max_error=0.005):
    ''' Return list of lines by sliding window'''
    if not data_range:
        data_range = (0, len(data)-1)
    start = data_range[0]
    end = start 
    lines = gen_lines(data, (data_range[0], data_range[1]))
    a = 0 
    while end < data_range[1]:
        end += 1
        tmp_line = gen_lines(data, (start, end))
        error = compute_error(data, tmp_line)
        if error <= max_error:
            lines = tmp_line
        else:
            a += error
            break
    if end == data_range[1]:
        return [lines]
    else:
        return [lines] + WindowSliding(data, gen_lines, compute_error, (end-1, data_range[1]), max_error=0.005)
