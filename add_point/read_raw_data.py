import json
import os

import matplotlib.pyplot as plt


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

                        self.raw_path = dict['path']
                        self.path = img_folder + '/' + \
                            self.raw_path.split('/')[-1]
                        self.keypoint = dict['keypoint']
                        self.hand_side = dict['hand_side']
                        self.gt = int(dict['gt'])
                        self.user = dict['user']
                        self.status = dict['status']

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

                self.data = [DMEImg(d, img_folder) for d in data]
                print(len(self.data))

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

if __name__ == '__main__':
    dme_data = DMERawData()
    aa = dme_data.training_set.data[0].plot(1)
    # aa = dme_data.training_set.data[1].plot(1)
    # aa = dme_data.training_set.data[2].plot(1)
    # for a in aa:
    #     print(a.raw_path)
