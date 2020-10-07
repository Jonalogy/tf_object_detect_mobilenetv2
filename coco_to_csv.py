import argparse
import pandas as pd
from pycocotools.coco import COCO


def coco_to_csv(json_path):
    coco = COCO(json_path)
    cat = coco.getCatIds()

    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    entry_list = []
    for ann in coco.loadAnns(ids=coco.getAnnIds()):
        ann_id = ann["id"]
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

    coco_df = pd.DataFrame(entry_list, columns=column_name)
    return coco_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate csv file from xml annotations')
    parser.add_argument('--annot_dir', help='directory of input COCO JSON files', default='../data/coco_annotations.json')
    parser.add_argument('--out_csv_path', help='path to output csv file', default='../data/train.csv')
    args = parser.parse_args()

    coco_df = coco_to_csv(args.annot_dir)
    coco_df.to_csv(args.out_csv_path, index=False)
    print('Successfully converted COCO JSON to csv.')
