"""[Core functions]

This code snippet is used to  1. [optional] iterate all h5 files and read their lengths, read the last none vector and output the actual length,
                              2. read official_annotations/something-something-v2-train/validation/test.json to map [id] to [template]
                              3. read official_annotations/something-something-v2-labels.json to map [template] to class labels
                              4. repack all information into one single json file                    

sayano
"""

from ast import parse
from io import BytesIO
import os.path as osp

import argparse

import mmcv

import h5py

import cv2

import numpy as np

from tqdm import tqdm
import json
from glob import glob

def map_ids_to_templates(ids_fns):
    with open(ids_fns, 'r') as f:
        ann = json.load(f)
    ann_dict = {} 
    for a in ann:
        ann_dict.update(
            {int(a['id']) : a['template']}
        )
    return ann_dict

def search(real_len, key, lst):
    new_lst = []
    for l in lst:
        if key in l:
            l = repack(real_len, l)
        new_lst.append(l)
    return new_lst

def repack(real_length, old_record):
    old_record = old_record.split(';')
    old_record[1] = str(real_length)
    return ';'.join(old_record)

def sanity_check_class(classes):
    cls_dict = {}
    for cls in classes:
        cls_lst = cls.strip('\n').split(',')
        if len(cls_lst) > 2:
            new_template = ','.join(cls_lst[:len(cls_lst)-1])
            cls_dict.update({
                new_template : int(cls_lst[-1])
            })
        else:
            cls_dict.update({
                cls_lst[0]: int(cls_lst[1])
            })
    return cls_dict

def sanity_check_official_consistence(official, extracted):
    templates = []
    for off in official:
        templates.append(off['template'])
    templates = sorted(list(set(templates)))
    extracted = sorted(extracted)
    # import ipdb; ipdb.set_trace()

if __name__ == '__main__':

    split = 'train'

    ids_fn = 'official_annotations/something-something-v2-{}.json'.format(split)
    template_fn = 'official_annotations/something-something-v2-labels.json'

    h5_files = sorted(glob(osp.join('../ssv2_repack/{}'.format(split), '*')))

    id_template_mapping_dict = map_ids_to_templates(ids_fn)
    with open(template_fn, 'r') as tf:
        template_labels_mapping_dict = json.load(tf)

    counter = 0
    wrong_lst = []
    records = []
    for hf in tqdm(h5_files):
        f = h5py.File(hf, 'r')
        data = f['video']
        naming = int(osp.basename(hf).split('.')[0])

        label = template_labels_mapping_dict[id_template_mapping_dict[naming].replace('[', '').replace(']', '')]
        num_of_frames = data.shape[0]
        if data[data.shape[0]-1].shape[0]==0:
            for cnt in range(data.shape[0]):
                if data[cnt].shape[0] == 0:
                    num_of_frames = cnt
                    break
            counter+=1
            wrong_lst.append(hf)
        new_hf = osp.join(*hf.split('/')[-2:])

        records.append(';'.join([new_hf, str(num_of_frames), str(label)])+'\n')
        f.close()
    print(counter/len(h5_files))
    
    with open('./ssv2_{}_annotations.txt'.format(split), 'w') as fout:
        fout.writelines(records)

