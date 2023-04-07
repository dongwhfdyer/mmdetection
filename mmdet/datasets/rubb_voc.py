# Copyright (c) OpenMMLab. All rights reserved.
from collections import OrderedDict

from mmcv.utils import print_log
from mmdet.datasets import VOCDataset

from mmdet.core import eval_map, eval_recalls
from .builder import DATASETS
from .xml_style import XMLDataset


@DATASETS.register_module()
class rubb_voc(VOCDataset):
    CLASSES = ("dog", "cat", "pig")

