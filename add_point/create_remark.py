from read_raw_data import DMERawData

import cv2

def append_remark(dat, is_full):
    if is_full:
        t = 'full'
    else:
        t = 'only_hands'
    save_text = ';'.join([str(dat.index), dat.img_name, t]) + '\n'
    with open('temp.txt', 'a') as f:
        f.write(save_text)

def handle_key(key, dat):
    # print('key num --- ',key)
    if key == 27:
        print('esc... exit')
        return True
    elif key == 59:
        print('z')
    elif key == 32:
        print('space')
        append_remark(dat, is_full=True)
    elif key == 13:
        print('enter')
        append_remark(dat, is_full=False)
    print('img.name =',dat.img_name)
    return False

def cv2_show_img(dat):
    img = cv2.imread(dat.raw_path)
    cv2.imshow('my img', img)

    key = cv2.waitKey(0)
    is_break = handle_key(key, dat)
    cv2.destroyAllWindows()
    return is_break

def run(data):
    for i, dat in enumerate(data):
        # if i <= 592: continue
        dat.index = i
        is_break = cv2_show_img(dat)
        if is_break: break

if __name__ == '__main__':
    dme_data = DMERawData()
    # run(dme_data.training_set.data)
    # run(dme_data.validation_set.data)
    run(dme_data.testing_set.data)



    # with open('temp.txt', 'r') as f:
    #     data = f.read()
    
    # data = data.split('\n')
    # print(len(data))
    # print(data[0])
    # print(data[-1])



