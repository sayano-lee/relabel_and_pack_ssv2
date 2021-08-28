""" [Core functions]

This code snippet is used to encode video files into h5py file

Possible errors happen when you read video frames using opencv, 
some void frames might be read into the h5 files,
therefore, an empty array might appear in the h5 file.

The problem is that, the length of the encoded h5 file is inconsistent with the number of actual data

sayano
"""

from io import BytesIO
import os.path as osp

import argparse

import mmcv

import h5py

import cv2

import numpy as np

from tqdm import tqdm

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--split', required=True, type=str, default=None)
    args = parser.parse_args()

    with open(args.split, 'r') as f:
        data = f.readlines()

    h5_out = '../ssv2_repack/train'
    
    for video in tqdm(data, leave=False):
        video = video.strip('\n')
        vi = mmcv.VideoReader(video)
        vih5 = h5py.File(osp.join(h5_out, osp.basename(video).replace('webm', 'hdf5')), 'w')
        dtype = h5py.special_dtype(vlen='uint8')
        video_h5 = vih5.create_dataset(
            'video',
            (len(vi),),
            dtype=dtype
        )
        for ii, im in enumerate(vi):
            video_h5[ii] = np.frombuffer(cv2.imencode('.jpg', im)[1], dtype='uint8')
        vih5.close()
    