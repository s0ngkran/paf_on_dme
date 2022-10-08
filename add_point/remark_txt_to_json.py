def run(fname):
    with open(fname, 'r') as f:
        data = f.readlines()
    return data

if __name__ == '__main__':
    fname = 'add_point/training_set_only_hands.txt'
    data = run(fname)
    print([data[0].strip()])
    # print(data[:2])
