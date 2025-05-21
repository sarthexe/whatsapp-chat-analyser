import streamlit as st
import data_preprocessing,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp chat analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=data_preprocessing.preprocess(data)


    #fetch unique users

    userlist = df['user'].unique().tolist()
    userlist.remove('group_notification')
    userlist.sort()
    userlist.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt" ,userlist)


    if st.sidebar.button("Show Analysis"):

        #Stats area

        num_messages,words ,num_media_messages,num_sticker,num_links= helper.fetch_stats(selected_user,df)
        st.title("Top statistics")        
        col1, col2, col3 , col4 ,col5 = st.columns(5)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total words")
            st.title(words)

        with col3:
            st.header("Media shared")
            st.title(num_media_messages)
        
        with col4:
            st.header("Stickers shared")
            st.title(num_sticker)
        
        with col5:
            st.header("Links shared")
            st.title(num_links)

        # monthly timeline
        st.title("Monthly timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax= plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)  

        # daily timeline

        st.title("Daily timeline")
        daily_timeline=helper.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'],color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity map

        st.title("Activity Map")
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_maps(selected_user,df)
            fig,ax= plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_name(selected_user,df)
            fig,ax= plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Heatmap")
        user_heatmap= helper.activity_heatmap(selected_user,df)
        fig,ax= plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)




        #finding the busiest user in the group chat

        if selected_user == "Overall":
            st.title('Most Busy User')
            x,new_df=helper.most_busy_user(df)
            fig,ax=plt.subplots()

            col1,col2 =st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        #Wordcloud
        st.title('Worcloud')
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words

        most_common_df = helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        #plt.xticks(rotation='vertical')
        st.title("Most Common words")
        st.pyplot(fig)

        #emoji analysis

        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji analysis")
        col1,col2 =st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1],labels=emoji_df[0],autopct="%0.2f")
            st.pyplot(fig)