from read_raw_data import DMERawData
import json

TEMP_FOLDER = 'add_point/temp/'
JSON_PATH = 'add_point/name_map.json'

def gen_temp():
    dme_data = DMERawData()
    data = dme_data.training_set.full 
    assert len(data) == dme_data.training_set.get_n_full()
    '''
    1. write img
    2. create name map

    {
        'namexxx': 1,
        'namexxx': 2,
        'namexxx': 3,
        ...
    }
    '''
    name_map = {}
    for i, dat in enumerate(data):
        pth = TEMP_FOLDER + str(i) + '.jpg'
        suc = dat.save_img(pth)
        assert suc == True
        if i > 6:break
        name_map[str(i)] = pth + ' ---> ' + dat.img_name
    with open(JSON_PATH, 'w') as f:
        f.write(json.dumps(name_map))
    
    print('saved', len(data))


def read_name_map():
    with open(JSON_PATH, 'r') as f:
        dat = json.loads(f.read())
    print([dat['0']])

if __name__ == '__main__':
    gen_temp()
    read_name_map()
