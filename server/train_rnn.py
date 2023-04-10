from drums_rnn.drums_rnn_train import train_rnn

if __name__ == "__main__":
    train_rnn(run_dir='/logdir/run2', sequence_example_file='/tmp/drums_rnn/sequence_examples/eval_drum_tracks.tfrecord', num_training_steps=20000)
