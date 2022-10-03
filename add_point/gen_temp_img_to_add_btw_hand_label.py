from read_raw_data import DMERawData

def gen_temp():
    dme_data = DMERawData()
    data = dme_data.validation_set.data
    for dat in data:
        dat.save_img('temp/' + dat.img_name)
    print('saved', len(data))

if __name__ == '__main__':
    gen_temp()
