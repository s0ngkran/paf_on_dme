from read_raw_data import DMERawData
import json
import os
TEMP_FOLDER = 'add_point/temp'
JSON_PATH = 'add_point/name_map.json'

def gen_temp(
    training_set=False,
    validation_set=False,
    testing_set=False,
):
    dme_data = DMERawData()

    if training_set:
        data = dme_data.training_set.build_full() 
        assert len(data) == dme_data.training_set.get_n_full()
    elif validation_set:
        data = dme_data.validation_set.build_full() 
        assert len(data) == dme_data.validation_set.get_n_full()
    elif testing_set:
        data = dme_data.testing_set.build_full() 
        assert len(data) == dme_data.testing_set.get_n_full()
    else:
        assert False

    '''
    Steps
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
    if not os.path.exists(TEMP_FOLDER):
        os.mkdir(TEMP_FOLDER)
    for i, dat in enumerate(data):
        pth = TEMP_FOLDER +'/'+ str(i) + '.jpg'
        suc = dat.save_img(pth)
        assert suc == True
        name_map[str(i)] = pth + ' ---> ' + dat.img_name
    with open(JSON_PATH, 'w') as f:
        f.write(json.dumps(name_map))
    print('saved', len(data))

def read_name_map():
    with open(JSON_PATH, 'r') as f:
        dat = json.loads(f.read())
    print([dat['0']])

if __name__ == '__main__':
    # gen_temp(training_set=True)
    # gen_temp(validation_set=True)
    gen_temp(testing_set=True)
    read_name_map()
    # after run this file, you need to 
    #       rename temp/ -> temp_training_set/
    #       rename name_map.json/ -> name_map_training_set.json
