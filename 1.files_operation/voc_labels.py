
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

sets = ['train', 'test', 'val']
# classes = ['parrester_28','arrester_36','pressure_8','oil_temperature_2','arrester_11','pressure_13','arrester_26','arrester_35','arrester_1','arrester_27']
#classes = ['wcgz', 'xy', 'head', 'bpmh', 'bpps', 'gbps', 'nc', 'gkxfw', 'xmbhyc', 'dmyw', 'gjtbs', 'gjtps', 'hxqyfywyc', 'wkps', 'dsyc', 'helmet', 'jyzps','bjzc']
classes = ['wcgz', 'xy', 'wdaqm', 'bpmh', 'bpps', 'gbps', 'nc', 'gkxfw', 'xmbhyc', 'dmyw', 'gjbs', 'gjtps', 'hxqyfywyc', 'wkps', 'dsyc', 'helmet', 'jyzps','bjzc']
replace_dict = {'jytpl':'jyzps', 'bjps':'bpps', 'hxjyfywyc':'hxqyfywyc', 'bjduyc':'dsyc', 'bjmh':'bpmh', 'bpdsyc':'dsyc', 'gkxw':'gkxfw', 'bpdsyc':'dsyc', 'smbhyc':'xmbhyc', 'jyzpl':'jyzps', 'bjdsyc':'dsyc', 'gjtbs':'gjbs', 'head':'wdaqm'}

device_class = ['', '']
output_class = ['wcgz', 'xy', 'wdaqm']


def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def convert_annotation(image_id):
    in_file = open('data/wugaosuo_xml/%s.xml' % (image_id), 'rb')
    out_file = open('data/labels/%s.txt' % (image_id), 'w')
    try:
        tree = ET.parse(in_file)
    except Exception:
        print(image_id)
        return
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls in replace_dict.keys():
            cls = replace_dict[cls]
        if cls not in classes:# or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()
print(wd)
for image_set in sets:
    if not os.path.exists('data/labels/'):
        os.makedirs('data/labels/')
    image_ids = open('data/ImageSets/%s.txt' % (image_set)).read().strip().split()
    list_file = open('data/%s.txt' % (image_set), 'w')
    for image_id in image_ids:
        list_file.write('data/wugaosuo_pic/%s.jpg\n' % (image_id))
        # try:
        convert_annotation(image_id)
        # except ZeroDivisionError:
        #     print(image_id)
    list_file.close()
