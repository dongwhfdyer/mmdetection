_base_ = [
    '../_base_/models/ssd300.py', '../_base_/datasets/openimages_detection.py',
    '../_base_/default_runtime.py', '../_base_/schedules/schedule_1x.py'
]
model = dict(
    bbox_head=dict(
        num_classes=601,
        anchor_generator=dict(basesize_ratio_range=(0.2, 0.9))))
# dataset settings
dataset_type = 'OpenImagesDataset'
data_root = 'data/OpenImages/'
img_norm_cfg = dict(mean=[123.675, 116.28, 103.53], std=[1, 1, 1], to_rgb=True)
train_pipeline = [
    dict(type='LoadImageFromFile', to_float32=True),
    dict(type='LoadAnnotations', with_bbox=True, normed_bbox=True),
    dict(
        type='PhotoMetricDistortion',
        brightness_delta=32,
        contrast_range=(0.5, 1.5),
        saturation_range=(0.5, 1.5),
        hue_delta=18),
    dict(
        type='Expand',
        mean=img_norm_cfg['mean'],
        to_rgb=img_norm_cfg['to_rgb'],
        ratio_range=(1, 4)),
    dict(
        type='MinIoURandomCrop',
        min_ious=(0.1, 0.3, 0.5, 0.7, 0.9),
        min_crop_size=0.3),
    dict(type='Resize', img_scale=(300, 300), keep_ratio=False),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='RandomFlip', flip_ratio=0.5),
    dict(type='DefaultFormatBundle'),
    dict(type='Collect', keys=['img', 'gt_bboxes', 'gt_labels']),
]
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='MultiScaleFlipAug',
        img_scale=(300, 300),
        flip=False,
        transforms=[
            dict(type='Resize', keep_ratio=False),
            dict(type='Normalize', **img_norm_cfg),
            dict(type='ImageToTensor', keys=['img']),
            dict(type='Collect', keys=['img']),
        ])
]
data = dict(
    samples_per_gpu=8,  # using 32 GPUS while training.
    workers_per_gpu=0,  # workers_per_gpu > 0 may occur out of memory
    train=dict(
        _delete_=True,
        type='RepeatDataset',
        times=3,
        dataset=dict(
            type=dataset_type,
            ann_file=data_root +
                     'annotations/oidv6-train-annotations-bbox.csv',
            img_prefix=data_root + 'OpenImages/train/',
            label_file=data_root +
                       'annotations/class-descriptions-boxable.csv',
            hierarchy_file=data_root +
                           'annotations/bbox_labels_600_hierarchy.json',
            pipeline=train_pipeline)),
    val=dict(pipeline=test_pipeline),
    test=dict(pipeline=test_pipeline))
# optimizer
optimizer = dict(type='SGD', lr=0.04, momentum=0.9, weight_decay=5e-4)
optimizer_config = dict()
# learning policy
lr_config = dict(
    policy='step',
    warmup='linear',
    warmup_iters=20000,
    warmup_ratio=0.001,
    step=[8, 11])

# NOTE: `auto_scale_lr` is for automatically scaling LR,
# USER SHOULD NOT CHANGE ITS VALUES.
# base_batch_size = (32 GPUs) x (8 samples per GPU)
auto_scale_lr = dict(base_batch_size=256)
