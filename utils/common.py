from datetime import datetime


def calculate_duration(date, start_time, end_time):
    end_datetime = datetime.combine(date, end_time)
    start_datetime = datetime.combine(date, start_time)
    difference = end_datetime - start_datetime
    return difference
