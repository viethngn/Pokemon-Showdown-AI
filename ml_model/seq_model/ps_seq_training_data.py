import argparse

import pandas as pd
from sklearn.model_selection import train_test_split


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--program_path')
    parser.add_argument('-f', '--file_path')
    args = parser.parse_args()

    df = pd.read_csv(args.file_path)
    # create label & feature data
    features = df.copy()
    labels = features.pop('p1_win')

    # ensure all data are floating point values
    features = features.astype('float32')
    labels = labels.astype('float32')

    # split into train and test datasets
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=12)
    print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

    # Reserve 200 samples for validation
    X_val = X_train[-200:]
    y_val = y_train[-200:]
    X_train = X_train[:-200]
    y_train = y_train[:-200]

    # Use 'csv' format to store the data
    X_train.to_csv(f'{args.program_path}/ml_model/seq_model/train_data.csv', index=False)
    y_train.to_csv(f'{args.program_path}/ml_model/seq_model/train_label.csv', index=False)
    X_test.to_csv(f'{args.program_path}/ml_model/seq_model/test_data.csv', index=False)
    y_test.to_csv(f'{args.program_path}/ml_model/seq_model/test_label.csv', index=False)
    X_val.to_csv(f'{args.program_path}/ml_model/seq_model/val_data.csv', index=False)
    y_val.to_csv(f'{args.program_path}/ml_model/seq_model/val_label.csv', index=False)