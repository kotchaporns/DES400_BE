from flask import Blueprint, request, jsonify, Response
from entity.recordEntity import db,Record
from entity.userEntity import User
from entity.dailyEntity import Daily
from sqlalchemy import and_, func
from sqlalchemy.orm import aliased

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import  Table, TableStyle
from datetime import datetime
from io import BytesIO




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
    
def getSound(user_id, start_date, end_date):
    try:
        # result = Record.query.filter(
        #     Record.user_id == user_id,
        #     Record.date >= start_date,
        #     Record.date <= end_date
        # ).all()


        record_alias = aliased(Record)

        # Subquery to get the time_start corresponding to the max intensity
        subquery = (
            db.session.query(
                Record.date,
                func.max(Record.calls).label('max_intensity')
            )
            .filter(
                    Record.user_id == user_id,
                    Record.date >= start_date,
                    Record.date <= end_date
                 )
            .group_by(Record.date)
            .subquery()
        )

        # Main query to retrieve results
        records = (
            db.session.query(
                subquery.c.date,
                subquery.c.max_intensity,
                record_alias.path,
                record_alias.record_id,
                record_alias.user_id
            )
            .join(record_alias, and_(
                record_alias.user_id == user_id,
                record_alias.date == subquery.c.date,
                record_alias.calls == subquery.c.max_intensity
            ))
            .all()
        )
        if records:
            results = [{'record_id': entry.record_id, 'user_id': entry.user_id,
                    'date': entry.date.strftime('%Y-%m-%d'),
                    'path': entry.path,
                    } for entry in records]

            return results
        else:
            return 'No Record Found'

       
        

    except Exception as e:
        return {"error": 'Invalid input'}


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
    

    
def getPdf(user_id, start_date, end_date):
    try:
        header_image = './assets/logo.png'

        buffer = BytesIO()

        user = User.query.filter_by(user_id=user_id).first()

        # Check if the user exists
        if user is None:
            raise Exception("User not found.")

        user_fName = user.firstname
        user_lName = user.lastname
        current_date = datetime.now()
        user_age = current_date.year - user.birthday.year - ((current_date.month, current_date.day) < (user.birthday.month, user.birthday.day))
        # Create a PDF document with A4 page size
        pdf_canvas = canvas.Canvas(buffer,pagesize=A4)

        # Draw the image in the header
        pdf_canvas.drawImage(header_image, 30, A4[1] - 80, width=50, height=50)

        # Draw heading
        pdf_canvas.setFont("Helvetica-Bold", 16)

        # Calculate x-coordinate for the middle of the page
        title = "SNORING SUMMARY RESULT"
        title_width = pdf_canvas.stringWidth(title, "Helvetica-Bold", 16)
        x_middle = (pdf_canvas._pagesize[0] - title_width) / 2

        pdf_canvas.drawString(x_middle, A4[1] - 80, title)

        # Convert start_date and end_date to datetime objects
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        # Draw user name and date range on the left side
        pdf_canvas.setFont("Helvetica", 12)
        pdf_canvas.drawString(30, A4[1] - 120, f"Name: {user_fName} {user_lName}            Age: {user_age}")
        pdf_canvas.drawString(30, A4[1] - 140, f"Medical Condition: {user.medical_condition}")
        pdf_canvas.drawString(30, A4[1] - 160, f"Height: {user.height}    Weight: {user.weight}")
        pdf_canvas.drawString(30, A4[1] - 180, f"Date: {start_date.strftime('%d/%m/%Y')}  to {end_date.strftime('%d/%m/%Y')}")


        # Run the query to get the highest intensity for each record date
        # Subquery to get the time_start corresponding to the max intensity
        # Create an alias for the Record table to use in the subquery
        record_alias = aliased(Record)

        # Subquery to get the time_start corresponding to the max intensity
        subquery = (
            db.session.query(
                Record.date,
                func.max(Record.calls).label('max_intensity')
            )
            .filter(Record.user_id == user_id,                    
                    Record.date >= start_date,
                    Record.date <= end_date)
            .group_by(Record.date)
            .subquery()
        )

        # Main query to retrieve results
        records = (
            db.session.query(
                subquery.c.date,
                subquery.c.max_intensity,
                record_alias.time_start
            )
            .join(record_alias, and_(
                record_alias.user_id == user_id,
                record_alias.date == subquery.c.date,
                record_alias.calls == subquery.c.max_intensity
            ))
            .all()
        )
        if records:
    
            row_height = 12

            # Table data, including headers
            table_data = [
                ["date", "total_sleeptime", "snoring", "highest_intensity","timestamp","factor"]
            ]

            for record in records:
                date_str = record.date.strftime('%d/%m/%Y')
                daily = Daily.query.filter_by(user_id=user_id, date=record.date).first()
                if daily:
                    sleep_time_min = round(daily.sleep_time / 60, 2)
                    snoring_time_min = round(daily.snoring / 60, 2)
                    factors = []

                    if daily.alcohol:
                        factors.append("alcohol")

                    if daily.stress:
                        factors.append("stress")

                    if daily.exercise:
                        factors.append("exercise")

                    factors_string = ",".join(factors)
                    if factors_string == "":
                         factors_string = "-"
                    table_data.append([date_str, str(sleep_time_min),str(snoring_time_min) ,str(record.max_intensity), str(record.time_start),factors_string])

        # Create the Table object
        table = Table(table_data, colWidths=[80, 80, 60, 80, 80, 180], rowHeights=[row_height] * len(table_data))

        # Apply style to add borders and center-align text
        style = TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),  # Add border to the entire table
            ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),  # Gray background for headers
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center-align text
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Center-align vertically within each cell
        ])
        table.setStyle(style)

        # Calculate x-coordinate for the middle of the page
        table_width, table_height = table.wrap(0, 0)
        x_table_middle = (pdf_canvas._pagesize[0] - table_width) / 2

        # Draw the table on the canvas
        table.drawOn(pdf_canvas, x_table_middle, A4[1] - 230)

        # Save the PDF document
        pdf_canvas.showPage()
        pdf_canvas.save()
        buffer.seek(0)

        return buffer

    except Exception as e:
        return {"error": f'{e}'}