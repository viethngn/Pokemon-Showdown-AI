import argparse
import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
import math
from datetime import datetime


def model(X_train):
    # determine the number of input features
    n_features = X_train.shape[1]

    # estimate number of neurons in hidden layer
    n_hidden = math.ceil(X_train.shape[0] / (2 * (X_train.shape[1] + 1)))

    model = Sequential()
    model.add(Dense(n_hidden, activation='relu', kernel_initializer='he_normal', input_shape=(n_features,)))
    model.add(Dense(1, activation='sigmoid'))

    # compile the model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    return model


def _load_training_data(base_dir):
    x_train = pd.read_csv(f"{base_dir}/train_data.csv")
    y_train = pd.read_csv(f"{base_dir}/train_label.csv")
    return x_train, y_train


def _load_testing_data(base_dir):
    x_test = pd.read_csv(f"{base_dir}/test_data.csv")
    y_test = pd.read_csv(f"{base_dir}/test_label.csv")
    return x_test, y_test


def _load_val_data(base_dir):
    x_val = pd.read_csv(f"{base_dir}/val_data.csv")
    y_val = pd.read_csv(f"{base_dir}/val_label.csv")
    return x_val, y_val


def parse_args():
    parser = argparse.ArgumentParser()

    # Data, model, and output directories
    # model_dir is always passed in from SageMaker. By default this is a S3 path under the default bucket.
    parser.add_argument("--model_dir", type=str)
    parser.add_argument("--sm_model_dir", type=str, default=os.environ.get("SM_MODEL_DIR"))
    parser.add_argument('--train', type=str, default=os.environ.get('SM_CHANNEL_TRAIN'))
    parser.add_argument('--eval', type=str, default=os.environ.get('SM_CHANNEL_EVAL'))
    parser.add_argument('--epochs', type=int, default=1)
    parser.add_argument('--batch_size', type=int, default=64)

    # give existing model param
    parser.add_argument('--retrain_model', type=str, default='')

    return parser.parse_known_args()


if __name__ == '__main__':
    # load arguments
    args, _ = parse_args()

    # print args
    print(args)

    # load data
    print(f"Loading training data from {args.train}")
    X_train, y_train = _load_training_data(args.train)
    X_test, y_test = _load_testing_data(args.train)
    X_val, y_val = _load_val_data(args.train)

    # create and train the model
    print(f"Creating and training the model")
    if args.retrain_model and os.path.exists(args.retrain_model):
        model = tf.keras.models.load_model(args.retrain_model)
    else:
        model = model(X_train)
    model.fit(X_train, y_train, epochs=args.epochs, batch_size=args.batch_size, validation_data=(X_val, y_val))

    # save the entire model as a `.keras` zip archive.
    # print(f"Saving trained model to: {args.sm_model_dir}/my_model.keras")
    # model.save(f'{args.sm_model_dir}/my_model.keras')

    # print(f"Saving trained model to: {args.sm_model_dir}")
    # tf.saved_model.save(model, f"{args.sm_model_dir}/{datetime.now().strftime('%Y%m%d%H%M')}")

    print(f"Saving trained model to: {args.sm_model_dir}/{datetime.now().strftime('%Y%m%d')}")
    model.save(f"{args.sm_model_dir}/{datetime.now().strftime('%Y%m%d')}")