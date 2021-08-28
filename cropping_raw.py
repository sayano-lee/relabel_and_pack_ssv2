"""[Help functions]

Help function to chunk all files in both train and val into small segments,
in order to open multiple processes to crop and encode videos into h5py files


sayano
"""


import mmcv
import os.path as osp

from glob import glob
import json

import h5py

from itertools import islice

def chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())

if __name__ == '__main__':
    # testing_fn = 'ssv2_val_annotations_v2.txt'
    # training_fn = 'ssv2_train_annotations_v2'
    raw_videos = '../ssv2_raw/20bn-something-something-v2'

    training_split = 'official_annotations/something-something-v2-train.json'

    with open(training_split, 'r') as f:
        # records = f.readlines()
        records = json.load(f)
    
    videos = []
    for record in records:
        # import ipdb; ipdb.set_trace()
        path = osp.join(raw_videos, record['id']+'.webm')
        # naming = record.split(';')[0].split('/')[-1].split('.')[0]
        videos.append(path)
    
    # import ipdb; ipdb.set_trace()
    
    splits = list(chunk(videos, 3000))

    for cnt, split in enumerate(splits):
        split = list(map(lambda x: x+'\n', split))
        with open(osp.join('train_split/{:05d}.txt'.format(cnt)), 'w') as f:
            f.writelines(split)

    