import tensorflow as tf


def open_sharded_output_tfrecords(exit_stack, base_path, num_shards):
    """
    Opens all TFRecord shards for writing and adds them to an exit stack.

    Taken from: https://github.com/tensorflow/models/blob/b9ef963d1e84da0bb9c0a6039457c39a699ea149/research/object_detection/dataset_tools/tf_record_creation_util.py

    :param exit_stack:  A context2.ExitStack used to automatically closed
                        the TFRecords opened in this function.
    :param base_path:   The base path for all shards.
    :param num_shards:  The number of shards.
    :return:            The list of opened TFRecords. Position k in the list
                        corresponds to shard k.
    """
    tf_record_output_filenames = [
        '{}-{:05d}-of-{:05d}'.format(base_path, idx, num_shards)
        for idx in range(num_shards)
    ]

    tfrecords = [
        exit_stack.enter_context(tf.io.TFRecordWriter(file_name))
        for file_name in tf_record_output_filenames
    ]

    return tfrecords
