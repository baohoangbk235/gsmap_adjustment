import numpy as np
from model import common_util


def create_data(**kwargs):

    data_npz = kwargs['data'].get('dataset')
    time = np.load(data_npz)['time']
    lon = np.load(data_npz)['input_lon']
    lat = np.load(data_npz)['input_lat']
    precip = np.load(data_npz)['input_precip']

    target_lon = np.load(data_npz)['output_lon']
    target_lat = np.load(data_npz)['output_lat']
    target_precip = np.load(data_npz)['output_precip']

    channels = 3  # Two channels are lon, lat and precip

    input_conv2d_gsmap = np.zeros(shape=(len(time), len(lat), len(lon),
                                         channels))
    target_conv2d_gsmap = np.zeros(shape=(len(time), len(target_lat),
                                          len(target_lon), channels))
    """fill input_data"""
    # preprocessing data
    lon_res = lon.reshape(1, lon.shape[0])
    lat_res = lat.reshape(lat.shape[0], 1)
    lon_dup = np.repeat(lon_res, len(lat), axis=0)
    lat_dup = np.repeat(lat_res, len(lon), axis=1)

    # because lon and lat are the same over the period, therefore we duplicate
    lon_dup = np.repeat(lon_dup[np.newaxis, :, :], len(time), axis=0)
    lat_dup = np.repeat(lat_dup[np.newaxis, :, :], len(time), axis=0)

    # fill channels
    input_conv2d_gsmap[:, :, :, 0] = lat_dup
    input_conv2d_gsmap[:, :, :, 1] = lon_dup

    # input for conv2d is (batch_size, (H,W), channels)
    for i in range(0, len(time)):
        input_conv2d_gsmap[i, :, :, 2] = precip[i]
    """fill target_data"""
    # preprocessing data
    target_lon_res = target_lon.reshape(1, target_lon.shape[0])
    target_lat_res = target_lat.reshape(target_lat.shape[0], 1)
    target_lon_dup = np.repeat(target_lon_res, len(target_lat), axis=0)
    target_lat_dup = np.repeat(target_lat_res, len(target_lon), axis=1)

    # because lon and lat are the same over the period, therefore we duplicate
    target_lon_dup = np.repeat(target_lon_dup[np.newaxis, :, :],
                               len(time),
                               axis=0)
    target_lat_dup = np.repeat(target_lat_dup[np.newaxis, :, :],
                               len(time),
                               axis=0)

    # fill channels
    target_conv2d_gsmap[:, :, :, 0] = target_lat_dup
    target_conv2d_gsmap[:, :, :, 1] = target_lon_dup

    # target for conv2d is (batch_size, (H,W), channels)
    for i in range(0, len(time)):
        target_conv2d_gsmap[i, :, :, 2] = target_precip[i]

    return input_conv2d_gsmap, target_conv2d_gsmap


def load_dataset(**kwargs):
    # get preprocessed input and target
    input_conv2d_gsmap, target_conv2d_gsmap = create_data(**kwargs)

    # get test_size, valid_size from config
    test_size = kwargs['data'].get('test_size')
    valid_size = kwargs['data'].get('valid_size')

    # split data to train_set, valid_set, test_size
    input_train, input_valid, input_test = common_util.prepare_train_valid_test(
        input_conv2d_gsmap, test_size=test_size, valid_size=valid_size)
    target_train, target_valid, target_test = common_util.prepare_train_valid_test(
        target_conv2d_gsmap, test_size=test_size, valid_size=valid_size)
    data = {}
    for cat in ["train", "valid", "test"]:
        x, y = locals()["input_" + cat], locals()["target_" + cat]
        data["input_" + cat] = x
        data["target_" + cat] = y

    return data