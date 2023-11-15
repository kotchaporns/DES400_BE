from flask import Blueprint, request, jsonify, Response
import boto3, botocore
import json
import os
import tensorflow as tf
import numpy as np
from itertools import groupby
import librosa
import librosa.display

audio_api = Blueprint('audio_api', __name__)


s3 = boto3.client(
   "s3",
   aws_access_key_id="",
   aws_secret_access_key="",
   aws_session_token=""
)
@audio_api.route("/send-audio", methods=['POST'])
def audio():
    file = request.files['audioFile']
    print(file)

    file.save(os.path.join("./tmp", file.filename))

    upload_data =  s3.upload_fileobj(file, "snorewisebucket", file.filename)
     # Load the model

    model_path = "./MobileNetV2_size224_bs16"

    model = load_model(model_path)
    wav, sequence_stride, min_wav = preprocess_audio("./tmp/"+file.filename, SNR_dB=0)
    audio_slices = preprocess_audio_for_model(wav, sequence_stride)
    yhat, calls = perform_inference(model, audio_slices)

    print("Inference Results:")
    print("Predicted Labels:", yhat)
    print("Total Calls:", calls)

    os.remove("./tmp/"+file.filename)


    return "https://snorewisebucket.s3.amazonaws.com/" + file.filename


def load_model(model_path):
        return tf.keras.models.load_model(model_path)

def load_wav_16k_mono(filename):
        """ Load an MP3/WAV file, convert it to a float tensor, resample to 16 kHz single-channel audio. """
        # Load audio using librosa
        y, sr = librosa.load(filename, sr=16000, mono=True)

        # Convert audio to float tensor
        wav = np.asarray(y, dtype=np.float64)

        return wav

    # Preprocess the audio
def preprocess_audio(audio_path, SNR_dB=0):
        wav = load_wav_16k_mono(audio_path)
        avg_power_of_signal = sum(wav**2) / len(wav)

        SNR_linear = 10 ** (SNR_dB / 10)
        avg_power_of_noise = avg_power_of_signal / SNR_linear
        noise = np.random.normal(0, avg_power_of_noise ** 0.5, wav.shape)
        wav = wav + noise
        min_wav = (min(wav))

        sequence_stride = 16000 if len(wav) > 16000 else 16000 - 1

        return wav, sequence_stride, min_wav

    # Preprocess the audio for model input
def preprocess_audio_for_model(wav, sequence_stride):
        def preprocess_mp3(sample, index):
            sample = sample[0]
            zero_padding = tf.zeros([16000] - tf.shape(sample), dtype=tf.float64)
            wav = tf.concat([zero_padding, sample], 0)
            spectrogram = tf.signal.stft(wav, frame_length=320, frame_step=32)
            spectrogram = tf.abs(spectrogram)
            spectrogram = tf.expand_dims(spectrogram, axis=2)
            spectrogram = tf.image.resize(spectrogram, size=(224, 224))
            spectrogram = tf.image.grayscale_to_rgb(spectrogram)
            spectrogram /= tf.reduce_max(spectrogram)
            return spectrogram

        audio_slices = tf.keras.utils.timeseries_dataset_from_array(wav, wav, sequence_length=16000, sequence_stride=sequence_stride, batch_size=1)
        audio_slices = audio_slices.map(preprocess_mp3)
        audio_slices = audio_slices.batch(16)

        return audio_slices

    # Perform inference with the model
def perform_inference(model, audio_slices):
        yhat = model.predict(audio_slices)
        yhat = [1 if prediction > 0.75 else 0 for prediction in yhat]

        yhat1 = [key for key, group in groupby(yhat)]
        calls = tf.math.reduce_sum(yhat1).numpy()

        return yhat, calls