import os 

if __name__ == '__main__':
    root = '../data_from_dme'
    path = root + '/dme_raw/testing_set'
    gt_path = root + '/testing_json'
    for root, __, fname in os.walk(path):
        break
    
    with open(gt_path, 'r') as f:
        data = f.read()
    print(data)
    # print(root)