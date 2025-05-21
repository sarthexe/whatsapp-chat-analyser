import pandas as pd
import re

def preprocess(data):
    pattern = r'\[\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}:\d{2}\s(?:AM|PM)\]'
    messages = re.split(pattern,data)
    messages = [re.sub(r'[\u200e\u202f]', '', msg).strip() for msg in messages if msg.strip()]
    dates=re.findall(pattern,data)
    dates = [re.sub(r'[\[\]\u200e\u202f]', '', date).strip() for date in dates if date.strip()]
    df= pd.DataFrame({'user_message':messages, 'message_date':dates})
    df['message_date']=pd.to_datetime(df['message_date'],format = '%d/%m/%y, %I:%M:%S%p')
    df.rename(columns={'message_data':'date'},inplace=True)
    users=[]
    messages= []

    for message in df['user_message']:
        entry=re.split(r'([\w\W]+?):\s',message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user']=users
    df['message']=messages
    df.drop(columns=['user_message'],inplace=True)

    df['only_date']=df['message_date'].dt.date
    df['year']=df['message_date'].dt.year
    df['month']=df['message_date'].dt.month_name()
    df['month_num']=df['message_date'].dt.month
    df['day']=df['message_date'].dt.day
    df['day_name']=df['message_date'].dt.day_name()
    df['hour']=df['message_date'].dt.hour
    df['minute']=df['message_date'].dt.minute
    df['second']=df['message_date'].dt.second
    df['user'] = df['user'].replace('😝 TOESGOTNOHOES (WP-ED)', 'group_notification')
    

    period = []
    
    for hour in df[['day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour)+'-'+str('00'))
        elif hour == 0:
            period.append(str(00)+"-"+str(hour+1))

        else:
            period.append(str(hour)+"-"+str(hour+1))
    df['period']= period

    return df        
