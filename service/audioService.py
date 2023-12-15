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
from entity.recordEntity import db,Record
from entity.dailyEntity import Daily
from dotenv import load_dotenv
from sqlalchemy import func

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
    
    num_snoring = yhat.count(1)
    num_sleeptime = len(yhat)
    num_non_snoring = num_sleeptime - num_snoring

    
    exist_record = Daily.query.filter_by(user_id=user_id, date=date).first()
    if exist_record:
        print(exist_record)
        exist_record.snoring = (exist_record.snoring or 0) + num_snoring
        exist_record.non_snoring = (exist_record.non_snoring or 0) + num_non_snoring
        exist_record.intensity = (exist_record.intensity or 0) + calls
        exist_record.sleep_time = (exist_record.sleep_time or 0) + num_sleeptime
        db.session.commit()
    
    else:
        daily = Daily(user_id=user_id, date=date, alcohol=False, exercise=False, stress=False, snoring=num_snoring, non_snoring=num_non_snoring, intensity=calls, sleep_time=num_sleeptime)
        db.session.add(daily)
        db.session.commit()

    record = Record(user_id=user_id, date=date, time_start=time_start, time_stop=time_stop, path=s3_path, model_result=str(yhat), calls=str(calls))
    db.session.add(record)
    db.session.commit()

    return record

def getDaily(user_id, date):
        exist_daily = Daily.query.filter_by(user_id=user_id, date=date).first()
        if exist_daily:
            return {
                'user_id': exist_daily.user_id,
                'factor_id': exist_daily.factor_id,
                'date': exist_daily.date,
                'alcohol':exist_daily.alcohol,
                'exercise':exist_daily.exercise,
                'stress':exist_daily.stress,
                'snoring':exist_daily.snoring,
                'non_snoring':exist_daily.non_snoring,
                'intensity':exist_daily.intensity,
                'sleep_time':exist_daily.sleep_time
                }
        
        return {'Error':'Data not exist'}


def updateDailyFactor(data):
    try:
        user_id = data.get('user_id')
        date = data.get('date')
        if(not user_id or not date):
             return {'error': 'No user_id or date'}
        exist_daily = Daily.query.filter_by(user_id=user_id, date=date).first()
        if not exist_daily:
                    return {'error': 'Daily not found'}

        exist_daily.alcohol = data.get('alcohol', exist_daily.alcohol)
        exist_daily.exercise = data.get('exercise', exist_daily.exercise)
        exist_daily.stress = data.get('stress', exist_daily.stress)
    
        db.session.commit()
        return {
                'user_id': exist_daily.user_id,
                'factor_id': exist_daily.factor_id,
                'date': exist_daily.date,
                'alcohol':exist_daily.alcohol,
                'exercise':exist_daily.exercise,
                'stress':exist_daily.stress,
                'snoring':exist_daily.snoring,
                'non_snoring':exist_daily.non_snoring,
                'intensity':exist_daily.intensity,
                'sleep_time':exist_daily.sleep_time
            }

    except Exception as e:
        return {"Error update factor": f"{e}"}
    



def cal_notification(user_id):
    try:
        # Query from table Daily
        result = db.session.query(
            Daily.date,
            func.sum(Daily.intensity).label('total_intensity')
        ).filter_by(user_id=user_id).group_by(Daily.date).all()

        notification_data = []

        for date, total_intensity in result:
            # Convert date to string for better JSON serialization
            formatted_date = date.strftime('%d/%m/%Y')
            notification_data.append({'date': formatted_date, 'intensity': total_intensity})

        return notification_data

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None  

