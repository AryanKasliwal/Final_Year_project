
import hashlib
import os
from tqdm import tqdm

from note_seq import abc_parser
from note_seq import midi_io
from note_seq import musicxml_reader
import tensorflow._api.v2.compat.v1 as tf


FLAGS = tf.flags.FLAGS

tf.flags.DEFINE_string('input_dir', None,
                           'Directory containing files to convert.')
tf.flags.DEFINE_string('output_file', None,
                           'Path to output TFRecord file. Will be overwritten '
                           'if it already exists.')
tf.flags.DEFINE_bool('recursive', False,
                         'Whether or not to recurse into subdirectories.')
tf.flags.DEFINE_string('log', 'INFO',
                           'The threshold for what messages will be logged '
                           'DEBUG, INFO, WARN, ERROR, or FATAL.')

def generate_note_sequence_id(filename, collection_name, source_type):
	"""Generates a unique ID for a sequence.

	The format is:'/id/<type>/<collection name>/<hash>'.

	Args:
		filename: The string path to the source file relative to the root of the
			collection.
		collection_name: The collection from which the file comes.
		source_type: The source type as a string (e.g. "midi" or "abc").

	Returns:
		The generated sequence ID as a string.
	"""
	filename_fingerprint = hashlib.sha1(filename.encode('utf-8'))
	return '/id/%s/%s/%s' % (
		source_type.lower(), collection_name, filename_fingerprint.hexdigest())


def convert_files(root_dir, sub_dir, writer, recursive=False):
  """Converts files.

  Args:
    root_dir: A string specifying a root directory.
    sub_dir: A string specifying a path to a directory under `root_dir` in which
        to convert contents.
    writer: A TFRecord writer
    recursive: A boolean specifying whether or not recursively convert files
        contained in subdirectories of the specified directory.

  Returns:
    A map from the resulting Futures to the file paths being converted.
  """
  dir_to_convert = os.path.join(root_dir, sub_dir)
  tf.logging.info("Converting files in '%s'.", dir_to_convert)
  files_in_dir = tf.gfile.ListDirectory(dir_to_convert)#os.path.join(dir_to_convert))
  recurse_sub_dirs = []
  written_count = 0
  for file_in_dir in tqdm(files_in_dir):
    tf.logging.log_every_n(tf.logging.INFO, '%d files converted.',
                           1000, written_count)
    full_file_path = os.path.join(dir_to_convert, file_in_dir)
    if (full_file_path.lower().endswith('.mid') or
        full_file_path.lower().endswith('.midi')):
      try:
        sequence = convert_midi(root_dir, sub_dir, full_file_path)
      except Exception as exc:  # pylint: disable=broad-except
        tf.logging.fatal('%r generated an exception: %s', full_file_path, exc)
        continue
      if sequence:
        writer.write(sequence.SerializeToString())
    elif (full_file_path.lower().endswith('.xml') or
          full_file_path.lower().endswith('.mxl')):
      try:
        sequence = convert_musicxml(root_dir, sub_dir, full_file_path)
      except Exception as exc:  # pylint: disable=broad-except
        tf.logging.fatal('%r generated an exception: %s', full_file_path, exc)
        continue
      if sequence:
        writer.write(sequence.SerializeToString())
    elif full_file_path.lower().endswith('.abc'):
      try:
        sequences = convert_abc(root_dir, sub_dir, full_file_path)
      except Exception as exc:  # pylint: disable=broad-except
        tf.logging.fatal('%r generated an exception: %s', full_file_path, exc)
        continue
      if sequences:
        for sequence in sequences:
          writer.write(sequence.SerializeToString())
    else:
      if recursive and tf.gfile.IsDirectory(full_file_path):
        recurse_sub_dirs.append(os.path.join(sub_dir, file_in_dir))
      else:
        tf.logging.warning(
            'Unable to find a converter for file %s', full_file_path)

  for recurse_sub_dir in recurse_sub_dirs:
    convert_files(root_dir, recurse_sub_dir, writer, recursive)


def convert_midi(root_dir, sub_dir, full_file_path):
	"""Converts a midi file to a sequence proto.

	Args:
		root_dir: A string specifying the root directory for the files being
			converted.
		sub_dir: The directory being converted currently.
		full_file_path: the full path to the file to convert.

	Returns:
		Either a NoteSequence proto or None if the file could not be converted.
	"""
	try:
		sequence = midi_io.midi_to_sequence_proto(
			tf.gfile.GFile(full_file_path, 'rb').read())
	except midi_io.MIDIConversionError as e:
		tf.logging.warning(
			'Could not parse MIDI file %s. It will be skipped. Error was: %s',
			full_file_path, e)
		return None
	else:
		sequence.collection_name = os.path.basename(root_dir)
		sequence.filename = os.path.join(sub_dir, os.path.basename(full_file_path))
		sequence.id = generate_note_sequence_id(
			sequence.filename, sequence.collection_name, 'midi')
		tf.logging.info('Converted MIDI file %s.', full_file_path)
	return sequence


if __name__ == "__main__":
	root_dir = "C:/Users/akasliwal2/Documents/FYP/Final_Year_project/Dataset/FinalData/train/"
	sub_dir = "c/"
	writer = tf.io.TFRecordWriter("C:/Users/akasliwal2/Documents/FYP/Final_Year_project/Dataset/noteSequences.tfrecord")
	full_file_path = "C:/Users/akasliwal2/Documents/FYP/Final_Year_project/Dataset/FinalData/test/c/1_funk_80_beat_4-4_6.midi"
	convert_files(root_dir, sub_dir, writer, recursive=False)