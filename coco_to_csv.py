import argparse
import pandas as pd
import math
from pycocotools.coco import COCO


def coco_to_csv(json_path):
    coco = COCO(json_path)

    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    entry_list = []
    for ann in coco.loadAnns(ids=coco.getAnnIds()):
        img = coco.loadImgs(ids=[ann['image_id']])[0]
        cat_id = ann["category_id"]
        coco_bbox = ann["bbox"]

        bottom_left_X = coco_bbox[0]
        bottom_left_Y = coco_bbox[1]
        bbox_width = coco_bbox[2]
        bbox_height = coco_bbox[3]

        xmin = bottom_left_X
        ymin = bottom_left_Y
        xmax = bottom_left_X + bbox_width
        ymax = bottom_left_Y + bbox_height

        filename = img['file_name']
        img_height = img['height']
        img_width = img['width']
        class_name = coco.loadCats(ids=[cat_id])[0]["name"]

        entry = (filename, img_width, img_height, class_name, xmin, ymin, xmax, ymax)
        entry_list.append(entry)

    return pd.DataFrame(entry_list, columns=column_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate csv file from xml annotations')
    parser.add_argument('--annot_dir', help='directory of input COCO JSON files',
                        default='../data/coco_annotations.json')
    parser.add_argument('--out_csv_path', help='path to output csv file', default='../data/train.csv')
    parser.add_argument('--test_size', help="enter '0.2' for a 80% train and 20% test split", default=0)
    args = parser.parse_args()

    coco_df = coco_to_csv(args.annot_dir)

    test_size_ratio = float(args.test_size)
    print("Total records found:", len(coco_df.index))

    if test_size_ratio > 0:
        test_amt = round(test_size_ratio, 2)
        train_amt = round(1 - test_size_ratio, 2)
        print(f'train to test split ratio at {(train_amt, test_amt)}')
        train_till = math.floor(len(coco_df.index) * train_amt)
        train_df = coco_df.iloc[:train_till]
        test_df = coco_df.iloc[train_till:]
        print("train_size:", len(train_df.index), ", test_size:", len(test_df.index))
        train_df.to_csv('train.csv', index=None)
        test_df.to_csv('test.csv', index=None)
    else:
        coco_df.to_csv(args.out_csv_path, index=False)

    print('Successfully converted COCO JSON to csv.')
