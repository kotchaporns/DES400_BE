from flask import Blueprint, request, jsonify, Response
import boto3, botocore
import tempfile
import json
import os
import tensorflow as tf
import numpy as np
from itertools import groupby
import librosa
import librosa.display
from pydub import AudioSegment
from entity.recordEntity import db,Record
from dotenv import load_dotenv

from .modelService import predictModel

load_dotenv()
s3 = boto3.client("s3")
bucketname = os.getenv("S3_BUCKET_NAME")

# s3 = boto3.client(
#    "s3",
#    aws_access_key_id="ASIAU6Y6O34M7ZYK65GO",
#    aws_secret_access_key="WgkJSILBSNjDtf+BEY9OU7tPbey1TCx8fNDEK2w7",
#    aws_session_token="FwoGZXIvYXdzEPj//////////wEaDJjdm9jxn/xPQ0UXwyLLAWQyege+0P53O+PDiUhGCxEmzmspIP32vwWD0HgVf5IVkVETYwxBrez7U+ZiezFwqIPV6b3kE1KxgQ9QsBeSvfkkcStedzRGxuDPu0kwJ0Pyns4nUQQO8agU1RPwt06jBgNr1vEDLCi30UkAsA9tDlt9rzs1WJxVJlD8oIKmxEipJdzaMeGpLSVhtVr5bkOvUET583K91sgJm8zUJYud/ex+fNDCs8XuOXIMU9/9fAVJZfxsGd0Kw2VVBYwHXbNOqjKJp1B+avfqhv1QKL7l+6oGMi0+gWElnUnMDhsACRIpv5qpKG997hc+gK9hHEPUFLZrc3+ZqAlItz6jwCpuuoU="
# )

def predictSnore(file, user_id, date, time_start, time_stop):
    audio_stream = file.stream
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
        temp_audio_path = temp_audio_file.name
        temp_audio_file.write(audio_stream.read())
        
    try:
        yhat, calls = predictModel(temp_audio_path)
    except Exception as e:
        print(f"Model predict error: {e}")

    try:
        with open(temp_audio_path,'rb') as temp_audio_file:
            s3.upload_fileobj(temp_audio_file, bucketname, file.filename)
            s3_path = f"https://{bucketname}.s3.amazonaws.com/" + file.filename
    except Exception as e:
        print(f"S3 upload error {e}")

    record = Record(user_id=user_id, date=date, time_start=time_start, time_stop=time_stop, path=s3_path, model_result=str(yhat), calls=str(calls))
    db.session.add(record)
    db.session.commit()

    return record
