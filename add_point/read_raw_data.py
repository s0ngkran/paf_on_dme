import json
import os

import matplotlib.pyplot as plt
import cv2

class DMERawData:
    def __init__(
        self,
        root='../data_from_dme',
        img_folder_training_set='/dme_raw/training_set',
        img_folder_validation_set='/dme_raw/validation_set',
        img_folder_testing_set='/dme_raw/testing_set',
        gt_path_training_set='/training_json',
        gt_path_validation_set='/validation_json',
        gt_path_testing_set='/testing_json',
    ):
        class DMESet:
            def __init__(self, img_folder, gt_path):
                self.img_folder = img_folder
                self.gt_path = gt_path

                with open(self.gt_path, 'r') as f:
                    data = json.load(f)

                class DMEImg:
                    def __init__(self, dict, img_folder):
                        # exampla data in dict
                        # {'path': 'testing_set/0IMG_1789.jpg',
                        #  'keypoint': [[271.8, 216.8, '0', '0'], [234.8, 185.30000000000004, '0', '0'], [222.3, 173.8, '0', '0'], [210.3, 161.8, '1', '1'], [270.8, 183.29999999999998, '0', '0'], [256.3, 150.3, '0', '0'], [252.3, 135.8, '0', '0'], [250.3, 120.8, '0', '0'], [246.3, 109.3, '0', '0'], [269.3, 148.3, '0', '0'], [271.3, 131.3, '0', '0'], [272.3, 114.8, '0', '0'], [272.8, 97.3, '0', '0'], [282.3, 152.3, '0', '0'], [284.8, 134.3, '0', '0'], [284.8, 116.3, '0', '0'], [287.3, 101.80000000000001, '0', '0'], [294.3, 161.3, '0', '0'], [301.3, 146.8, '0', '0'], [305.3, 136.8, '0', '0'], [313.3, 124.30000000000001, '0', '0'], [161.29999999999998, 160.8, '0', '0'], [180.8, 160.8, '0', '0'], [193.8, 160.8, '0', '0'], [206.3, 158.8, '0', '0']],
                        #   'hand_side': 'L',
                        #    'gt': '2\n',
                        #    'user': 'DMW',
                        #    'status': 'testing',
                        #    'gts': 'testing_set/0IMG_1789.jpg.gts',
                        #    'gtl': 'testing_set/0IMG_1789.jpg.gtl',
                        #    'covered_point': ['0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
                        #     'covered_link': [False, False, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]}

                        self.img_path = dict['path']
                        self.img_name = self.img_path.split('/')[-1]
                        self.path = img_folder + '/' + self.img_name
                        self.replica_num = self.img_name[0]
                        self.raw_path = os.path.join(
                            '../dme_data_raw/hand', self.img_name[1:])
                        self.keypoint = dict['keypoint']
                        self.hand_side = dict['hand_side']
                        self.gt = int(dict['gt'])
                        self.user = dict['user']
                        self.status = dict['status']
                        assert self.hand_side in ['R', 'L']

                        # do not use these old gts
                        # self.gts = dict['gts']
                        # self.gtl = dict['gtl']
                        # self.covered_point = dict['covered_point']
                        # self.covered_link = dict['covered_link']

                    def plot(self, show=False):
                        img = plt.imread(self.path)
                        plt.imshow(img)
                        for kp in self.keypoint:
                            x, y, c_point, c_link = kp
                            # green if no covered
                            # red if covered
                            color = 'og' if c_point == '0' else 'or'
                            plt.plot(x, y, color)

                        if show:
                            plt.show()

                    def plot_raw(self, show=False, save=False):
                        img = plt.imread(self.raw_path)
                        plt.imshow(img)
                        for kp in self.keypoint:
                            x, y, c_point, c_link = kp
                            # scale from 360 to 720
                            thres = 720/360
                            x, y = x*thres, y*thres

                            if self.hand_side == 'L':
                                plt.title('real-side = ' + str(self.hand_side))
                                # swap x = -x
                                x = 720 - x
                            # green if no covered
                            # red if covered
                            color = 'og' if c_point == '0' else 'or'
                            plt.plot(x, y, color)

                        if save:
                            plt.axis('off')
                            plt.savefig('out.png', bbox_inches='tight',transparent=True , pad_inches=0)
                            return
                        if show:
                            plt.show()
                            return
                    def save_img(self, path):
                        img = cv2.imread(self.raw_path)
                        for kp in self.keypoint:
                            x, y, c_point, c_link = kp
                            # scale from 360 to 720
                            thres = 720/360
                            x, y = x*thres, y*thres

                            if self.hand_side == 'L':
                                # plt.title('real-side = ' + str(self.hand_side))
                                # swap x = -x
                                x = 720 - x
                            # green if no covered
                            # red if covered
                            color = (0,255,0) if c_point == '0' else (0,0,255)

                            if self.hand_side == 'L':
                                img = cv2.flip(img, 1)
                                cv2.circle(img, (int(x), int(y)), 5, color, -1)
                        return cv2.imwrite(path, img)

                self.data = [DMEImg(d, img_folder) for d in data]
                data = []
                for dat in self.data:
                    if dat.replica_num == str(0):
                        data.append(dat)
                self.data = data
                print('len data =', len(self.data))

        self.training_set = DMESet(
            root+img_folder_training_set,
            root+gt_path_training_set,
        )
        self.validation_set = DMESet(
            root+img_folder_validation_set,
            root+gt_path_validation_set,
        )
        self.testing_set = DMESet(
            root+img_folder_testing_set,
            root+gt_path_testing_set,
        )
        print(
            'tr + va + te =',
            len(self.training_set.data) +
            len(self.validation_set.data) +
            len(self.testing_set.data)
        )


if __name__ == '__main__':
    dme_data = DMERawData()
    # for i in range(10):
    #     aa = dme_data.training_set.data[i].plot_raw(save=1)
    aa = dme_data.training_set.data[0]
    aa.save_img('temp/' + aa.img_name)
    # aa = dme_data.training_set.data[1].plot(1)
    # aa = dme_data.training_set.data[2].plot(1)
    # for a in aa:
    #     print(a.raw_path)
