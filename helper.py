import emoji
import emoji.unicode_codes
from urlextract import URLExtract
extract = URLExtract()
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import seaborn as sns

def fetch_stats(selected_user,df):

    if selected_user!="Overall":
        df=df[df['user']==selected_user]
        
    # Number of messages
    num_messages = df.shape[0]
        
    # Fetch number of words
    words=[]
    for messages in df['message']:
        words.extend(messages.split())
        
    #Fetch number of media messages
    keywords = ["omitted"]
    pattern = '|'.join(keywords)
    num_media_messages = df[df['message'].str.contains(pattern, case=False, na=False)].shape[0]
        
    #Fetch number of Sticker messages
    num_sticker = df[df['message']=="sticker omitted"].shape[0]

    # Fetch Number of Links
    links = []
    for messages in df['message']:
        links.extend(extract.find_urls(messages))

    
    return num_messages,len(words) , num_media_messages,num_sticker,len(links)  
    

def most_busy_user(df):
    x = df['user'].value_counts().head()
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percentage'})
    return x,df


def create_wordcloud(selected_user , df):
        
    if selected_user!="Overall":
        df=df[df['user']==selected_user]
    
    f = open('stop_hinglish.txt' , 'r')
    stopwords=f.read()

    temp=df[df['user']!='group_notification']
    keywords = ["omitted"]
    pattern = '|'.join(keywords)
    temp=temp[~temp['message'].str.contains(pattern, case=False, na=False)]

    # remove stopwords
    def remove_sw(message):
        y = []
        for word in message.lower().split():
            if word not in stopwords:
                y.append(word)
        return " ".join(y)
        
    wc= WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] =temp['message'].apply(remove_sw)
    df_wc=wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user , df):
    if selected_user!='Overall':
        df = df[df['user']==selected_user]
    
    f = open('stop_hinglish.txt' , 'r')
    stopwords=f.read()

    temp=df[df['user']!='group_notification']
    keywords = ["omitted"]
    pattern = '|'.join(keywords)
    temp=temp[~temp['message'].str.contains(pattern, case=False, na=False)]

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)
    

    most_common_df = pd.DataFrame(Counter(words).most_common(20))

    return most_common_df

def emoji_helper(selected_user,df):

    if selected_user!='Overall':
        df = df[df['user']==selected_user]


    emojis = []

    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.unicode_codes.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df


def monthly_timeline(selected_user,df):
    
    if selected_user!='Overall':
        df = df[df['user']==selected_user]

    timeline= df.groupby(['year','month_num','month']).count()['message'].reset_index()

    time=[]

    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))

    timeline['time']=time

    return timeline 


def daily_timeline(selected_user,df):

    if selected_user!='Overall':
        df = df[df['user']==selected_user]

    daily_timeline= df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline


def week_activity_maps(selected_user,df):

    if selected_user!='Overall':
        df = df[df['user']==selected_user]
    

    return df['day_name'].value_counts()
    
def month_activity_name(selected_user ,df):

    if selected_user !='Overall':
        df = df[df['user']==selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    
    if selected_user!='Overall':
        df = df[df['user']==selected_user]

    user_heatmap= df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)

    return user_heatmap