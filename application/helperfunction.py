from datetime import datetime
import pytz
  
# get the standard UTC time 
UTC = pytz.utc

# it will get the time zone 
# of the specified location
IST = pytz.timezone('Asia/Kolkata')
  
# print the date and time in
# standard format
# print("UTC in Default Format : ", 
#       datetime.now(UTC))
  
# print("IST in Default Format : ", 
#       datetime.now(IST))
  
# # print the date and time in 
# # specified format
# datetime_utc = datetime.now(UTC)
# print("Date & Time in UTC : ",
#       datetime_utc.strftime('%Y:%m:%d %H:%M:%S %Z %z'))
  
# datetime_ist = datetime.now(IST)
# print("Date & Time in IST : ", 
#       datetime_ist.strftime('%d:%m:%Y-%H:%M:%S'))
# datetimeist = datetime_ist.strftime('%d:%m:%Y-%H:%M:%S')


# def timeconversion(UTC_datetime):
#     UTC_datetime_timestamp = float(UTC_datetime.strftime("%s"))
#     local_datetime_converted = datetime.fromtimestamp(UTC_datetime_timestamp)
#     return local_datetime_converted

# def totalsecs(local_time):
#     local_time_string = local_time.split()[1]
#     local_time_li = local_time_string.split(':')
#     total = local_time_li[0]*3600+local_time_li[1]*60+local_time_li[2]
#     return total
    
# def secdiff(before_datetime):
#     local_now = timeconversion(datetime.utcnow())
#     total_now = totalsecs(local_now)
#     total_before = totalsecs(before_datetime)
    
def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(IST)
    datetime_ist = IST.normalize(local_dt)
    return datetime_ist.strftime('%d:%m:%Y-%H:%M:%S')

    
    