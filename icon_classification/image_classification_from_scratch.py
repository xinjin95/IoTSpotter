#!/usr/bin/env python
# encoding: utf-8
"""
@author: xxx xxx
@license: (C) Copyright 2013-2019.
@contact: xxx.xxx0010@gmail.com
@software: pycharm
@file: image_classification_from_scratch.py
@time: 5/3/21 10:17 PM
@desc:
"""
import os
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pandas as pd

training_app_list_path = "../data/final_dataset/package_label_list.csv"

iot_apps = set()
non_iot_apps = set()

image_size = (512, 512)
batch_size = 32


def get_apps():
    df = pd.read_csv(training_app_list_path)
    for i, pkg_name in enumerate(df["app_id"]):
        label = int(df["label"][i])
        if label == 1:
            iot_apps.add(pkg_name)
        elif label == 0:
            non_iot_apps.add(pkg_name)


def move_imgs():
    for fname in os.listdir("data/"):
        if not fname.endswith('.png'):
            continue
        # fpath = os.path.join("data/", fname)
        pkg_name = fname.replace('.png', '')
        if pkg_name in iot_apps:
            os.rename("data/{}".format(fname), "data/raw_data/iot/{}".format(fname))
        elif pkg_name in non_iot_apps:
            os.rename("data/{}".format(fname), "data/raw_data/non_iot/{}".format(fname))


def split_dataset():
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        "data/raw_data/",
        validation_split=0.2,
        subset="training",
        seed=1337,
        image_size=image_size,
        batch_size=batch_size,
    )
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        "data/raw_data/",
        validation_split=0.2,
        subset="validation",
        seed=1337,
        image_size=image_size,
        batch_size=batch_size,
    )
    return train_ds, val_ds


def visualize_data():

    plt.figure(figsize=(10, 10))
    train_ds, val_ds = split_dataset()
    for images, labels in train_ds.take(1):
        for i in range(9):
            ax = plt.subplot(3, 3, i + 1)
            plt.imshow(images[i].numpy().astype("uint8"))
            plt.title(1 - int(labels[i]))
            plt.axis("off")
    plt.show()

    # plt.figure(figsize=(10, 10))
    # for images, _ in train_ds.take(1):
    #     for i in range(9):
    #         augmented_images = data_augmentation(images)
    #         ax = plt.subplot(3, 3, i + 1)
    #         plt.imshow(augmented_images[0].numpy().astype("uint8"))
    #         plt.axis("off")
    # plt.show()


def make_model(input_shape, num_classes):

    data_augmentation = keras.Sequential(
        [
            layers.experimental.preprocessing.RandomFlip("horizontal"),
            layers.experimental.preprocessing.RandomRotation(0.1),
        ]
    )

    inputs = keras.Input(shape=input_shape)
    # Image augmentation block
    x = data_augmentation(inputs)

    # Entry block
    x = layers.experimental.preprocessing.Rescaling(1.0 / 255)(x)
    x = layers.Conv2D(32, 3, strides=2, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    x = layers.Conv2D(64, 3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    previous_block_activation = x  # Set aside residual

    for size in [128, 256, 512, 728]:
        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(size, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(size, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.MaxPooling2D(3, strides=2, padding="same")(x)

        # Project residual
        residual = layers.Conv2D(size, 1, strides=2, padding="same")(
            previous_block_activation
        )
        x = layers.add([x, residual])  # Add back residual
        previous_block_activation = x  # Set aside next residual

    x = layers.SeparableConv2D(1024, 3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    x = layers.GlobalAveragePooling2D()(x)

    if num_classes == 2:
        activation = "sigmoid"
        units = 1
    else:
        activation = "softmax"
        units = num_classes

    x = layers.Dropout(0.5)(x)
    outputs = layers.Dense(units, activation=activation)(x)
    return keras.Model(inputs, outputs)


def main():
    model = make_model(input_shape=image_size + (3,), num_classes=2)
    keras.utils.plot_model(model, show_shapes=True)

    epochs = 50

    callbacks = [
        keras.callbacks.ModelCheckpoint(
            "data/model/save_at_{epoch}.h5",
            monitor='val_accuracy',
            verbose=1,
            save_best_only=True,
            save_weights_only=False, mode='auto'
        ),
    ]
    model.compile(
        optimizer=keras.optimizers.Adadelta(),
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )

    train_ds, val_ds = split_dataset()
    train_ds = train_ds.prefetch(buffer_size=32)
    val_ds = val_ds.prefetch(buffer_size=32)
    history = model.fit(
        train_ds, epochs=epochs, callbacks=callbacks, validation_data=val_ds,
    )

    return history


def classify():
    test_ds = tf.keras.preprocessing.image_dataset_from_directory(
        "data/test_data/",
        image_size=image_size,
        batch_size=batch_size,
    )
    # for images, labels in test_ds.take(1):
    #     for i in range(9):
    #         ax = plt.subplot(3, 3, i + 1)
    #         plt.imshow(images[i+18].numpy().astype("uint8"))
    #         if int(labels[i+18]) == 0:
    #             plt.title("iot")
    #         else:
    #             plt.title("non-iot")
    #         # plt.title(1 - int(labels[i+9]))
    #         plt.axis("off")
    # plt.show()
    test_labels = np.concatenate([y for x, y in test_ds], axis=0)
    test_labels = list(test_labels)
    test_labels = [1-label for label in test_labels]
    test_ds = test_ds.prefetch(buffer_size=32)
    model = keras.models.load_model("data/model/save_at_50.h5")
    predictions = model.predict(test_ds)
    predictions = np.reshape(predictions, newshape=(600,))
    predictions = list(predictions)
    predictions = [int(p < 0.5) for p in predictions]
    # predictions = int(predictions)
    from sklearn import metrics
    print("f1-score:", metrics.f1_score(test_labels, predictions))
    print("accuracy:", metrics.accuracy_score(test_labels, predictions))
    print("precision:", metrics.precision_score(test_labels, predictions))
    print("recall:", metrics.recall_score(test_labels, predictions))
    print("(tn, fp, fn, tp): {}\n".format(metrics.confusion_matrix(test_labels, predictions).ravel()))

    # print(predictions.shape)
    # print(predictions)


if __name__ == '__main__':
    # main()
    # visualize_data()
    classify()
    # tf.get_logger().setLevel('INFO')
    # tf.debugging.set_log_device_placement(False)
    # strategy = tf.distribute.MirroredStrategy()
    # with strategy.scope():
    #     main()