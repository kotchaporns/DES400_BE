from flask import Blueprint, request, jsonify, Response
import boto3, botocore
import json
import os
import tensorflow as tf
import numpy as np
from itertools import groupby
import librosa
import librosa.display
from pydub import AudioSegment

from .modelService import predictModel


s3 = boto3.client(
   "s3",
   aws_access_key_id="ASIAU6Y6O34M7ZYK65GO",
   aws_secret_access_key="WgkJSILBSNjDtf+BEY9OU7tPbey1TCx8fNDEK2w7",
   aws_session_token="FwoGZXIvYXdzEPj//////////wEaDJjdm9jxn/xPQ0UXwyLLAWQyege+0P53O+PDiUhGCxEmzmspIP32vwWD0HgVf5IVkVETYwxBrez7U+ZiezFwqIPV6b3kE1KxgQ9QsBeSvfkkcStedzRGxuDPu0kwJ0Pyns4nUQQO8agU1RPwt06jBgNr1vEDLCi30UkAsA9tDlt9rzs1WJxVJlD8oIKmxEipJdzaMeGpLSVhtVr5bkOvUET583K91sgJm8zUJYud/ex+fNDCs8XuOXIMU9/9fAVJZfxsGd0Kw2VVBYwHXbNOqjKJp1B+avfqhv1QKL7l+6oGMi0+gWElnUnMDhsACRIpv5qpKG997hc+gK9hHEPUFLZrc3+ZqAlItz6jwCpuuoU="
)

def predictSnore(file):
     # upload_data =  s3.upload_fileobj(file, "snorewisebucket", file.filename)
    audio_stream = file.stream
    yhat, calls = predictModel(audio_stream)
    return  yhat, calls


    