import numpy as np
import os
import pandas as pd
import scanpy.api as sc
import tensorflow as tf
import keras.optimizers as opt
from keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from keras import backend as K
from sklearn.model_selection import train_test_split
from model import ZINBAutoencoder

def train(adata, network, output_dir=None, optimizer='rmsprop', learning_rate=None,
          epochs=300, reduce_lr=10, output_subset=None, use_raw_as_output=True,
          early_stop=15, batch_size=32, clip_grad=5., save_weights=False,
          validation_split=0.1, tensorboard=False, verbose=True, threads=None,
          **kwds):

    K.set_session(tf.Session(config=tf.ConfigProto(intra_op_parallelism_threads=threads, inter_op_parallelism_threads=threads)))
    model = network.model
    loss = network.loss
    if output_dir is not None:
        os.makedirs(output_dir, exist_ok=True)

    if learning_rate is None:
        optimizer = opt.__dict__[optimizer](clipvalue=clip_grad)
    else:
        optimizer = opt.__dict__[optimizer](lr=learning_rate, clipvalue=clip_grad)

    model.compile(loss=loss, optimizer=optimizer)

    # Callbacks
    callbacks = []

    if save_weights and output_dir is not None:
        checkpointer = ModelCheckpoint(filepath="%s/weights.hdf5" % output_dir,
                                       verbose=verbose,
                                       save_weights_only=True,
                                       save_best_only=True)
        callbacks.append(checkpointer)
    if reduce_lr:
        lr_cb = ReduceLROnPlateau(monitor='val_loss', patience=reduce_lr, verbose=verbose)
        callbacks.append(lr_cb)
    if early_stop:
        es_cb = EarlyStopping(monitor='val_loss', patience=early_stop, verbose=verbose)
        callbacks.append(es_cb)
    if tensorboard:
        tb_log_dir = os.path.join(output_dir, 'tb')
        tb_cb = TensorBoard(log_dir=tb_log_dir, histogram_freq=1, write_grads=True)
        callbacks.append(tb_cb)

    if verbose: model.summary()

    inputs = {'count': adata.X, 'size_factors': adata.obs.size_factors}


    output = adata.X

    loss = model.fit(inputs, output,
                     epochs=epochs,
                     batch_size=batch_size,
                     shuffle=True,
                     callbacks=callbacks,
                     validation_split=validation_split,
                     verbose=verbose,
                     **kwds)

    return loss

def train_model(data_path):
    K.set_session(tf.Session())
    # load data
    adata = sc.read(data_path, first_column_names=True)
    adata = adata.transpose()
    # delete gene and cell with all 0 value
    sc.pp.filter_genes(adata, min_counts=1)
    sc.pp.filter_cells(adata, min_counts=1)
    # split test dataset
    train_idx, test_idx = train_test_split(np.arange(adata.n_obs), test_size=0.1, random_state=42)
    spl = pd.Series(['train'] * adata.n_obs)
    spl.iloc[test_idx] = 'test'
    adata.obs['dca_split'] = spl.values
    adata.obs['dca_split'] = adata.obs['dca_split'].astype('category')
    # calculate side factors
    sc.pp.normalize_per_cell(adata)
    adata.obs['size_factors'] = adata.obs.n_counts / np.median(adata.obs.n_counts)
    # log transfer and normalization
    sc.pp.log1p(adata)
    sc.pp.scale(adata)

    output_size = adata.n_vars
    input_size = adata.n_vars
    hidden_size = [64,32,64]
    hidden_dropout = 0

    net = ZINBAutoencoder(input_size=input_size,
            output_size=output_size,
            hidden_size=hidden_size,
            l2_coef=0.0,
            l1_coef=0.0,
            l2_enc_coef=0.0,
            l1_enc_coef=0.0,
            ridge=0.0,
            hidden_dropout=0.0,
            input_dropout=0.0,
            batchnorm=True,
            activation='relu',
            init='glorot_uniform',
            debug=False,
            file_path=False)
    net.build()
    losses = train(adata[adata.obs.dca_split == 'train'], net,
                   output_dir="./result",)

