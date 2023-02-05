
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from textblob import TextBlob
import geopandas as gpd
from pathlib import Path
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
from googletrans import Translator
import openpyxl
import pyproj
from folium.features import GeoJsonTooltip
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import advertools as adv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import io
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



st.set_page_config(layout="wide")

global dataframe_append #dataframe global variable

#menu
def main():

    hidefooter()
    mapresize()
    
    # sidebar menu
    
    with st.sidebar:
        selected = option_menu(
            menu_title = "Main Menu",
            options=["Home Page", "Text Translator", "Text Analysis", "Data Visualization", "Laguna Geo-Graphic Visualization", "Word Cloud"],
            icons= ["house", "translate", "book", "bar-chart-line-fill", "map", "cloud"],
            )

    #selected menu


    if(selected=="Home Page"):
            homepage()         
    if(selected=="Text Translator"):
            texttranslate()
    if(selected=="Text Analysis"):
            textanalysis()
    if(selected=="Data Visualization"):
            datavisual()
    if(selected=="Laguna Geo-Graphic Visualization"):
            geographic()
    if(selected=="Word Cloud"):
            wordcloud()

        

#home page

def homepage():
    
    st.markdown("<h1 style ='text-align: center;'>Welcome to Laguna Sentiment Analyzer Web Application</h1>", unsafe_allow_html=True) #title center
    st.text("")
    st.text("")
    st.text("")
    
#centering logo
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text("")
    with col2:
        lagunalogo = Image.open("SentimentWebapp/images/lagunalogo.png")
        logoresize = lagunalogo.resize((675,675))
        st.image(logoresize)
    with col3:
        st.text("")
   


    st.text("")
    st.text("")
#centering text
    st.markdown("<p style ='text-align: center; font-size: 22px'>This web application is a sentiment analysis tools that essentially to detect and understand the feelings of their citizen per municipalities.</p>", unsafe_allow_html=True)
    st.markdown("<p style ='text-align: center; font-size: 22px'>This tools generate insights into how the LGU (Local Government Units) can enhance or improve the experiences and services of their citizens.</p>", unsafe_allow_html=True)
    st.markdown("<p style ='text-align: center; font-size: 22px'>The web app includes those functionalities such as sentiment analysis, data visualitzation, geo-graphic visualization and wordcloud.</p>", unsafe_allow_html=True)
    
    #sentiment analysis short description
    
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    
    
    col5, col6 = st.columns(2)
    with col5:
         st.markdown("<p style ='text-align: justify; font-size: 22px'>Sentiment Analysis</p>", unsafe_allow_html=True)
         st.markdown("<p style ='text-align: justify; font-size: 16px'>Sentiment analysis (or opinion mining) is a natural language processing (NLP) technique used to determine whether data is positive, negative or neutral.</p>", unsafe_allow_html=True)
    with col6:
        senti = Image.open("SentimentWebapp/images/sentiment.jpg")
        resize = senti.resize((375,375))
        st.image(resize)
        
    #datavisual short description    
        
    st.text("")
    st.text("")
    
    col7, col8 = st.columns(2)
    with col7:
         st.markdown("<p style ='text-align: justify; font-size: 22px'>Data Visualization</p>", unsafe_allow_html=True)
         st.markdown("<p style ='text-align: justify; font-size: 16px'>Data visualization is the graphical representation of different pieces of information or data, using visual elements such as charts, graphs, or maps.</p>", unsafe_allow_html=True) 
         st.markdown("<p style ='text-align: justify; font-size: 16px'>Data visualization tools provide the ability to see and understand data trends, outliers, and patterns in an easy, intuitive way.</p>", unsafe_allow_html=True)
     
    with col8:
        dataimage = Image.open("SentimentWebapp/images/datavisual.png")
        resize = dataimage.resize((375,375))
        st.image(resize)
       
        
    #geovisual short description    
        
    st.text("")
    st.text("")
    
    col9, col10 = st.columns(2)
    with col9:
         st.markdown("<p style ='text-align: justify; font-size: 22px'>Geovisualization or “Geographic Visualization”</p>", unsafe_allow_html=True)
         st.markdown("<p style ='text-align: justify; font-size: 16px'>Geovisualization or “Geographic Visualization”</p>", unsafe_allow_html=True)
         st.markdown("<p style ='text-align: justify; font-size: 16px'>concerns the visual representations of geospatial data and the use of cartographic techniques to support visual analytics.</p>", unsafe_allow_html=True)
    with col10:
        geo = Image.open("SentimentWebapp/images/geovisual.png")
        geologo = geo.resize((375,375))
        st.image(geologo)
        
      #wordcloud short description    
        
    st.text("")
    st.text("")
    
    col11, col12 = st.columns(2)
    with col11:
         st.markdown("<p style ='text-align: justify; font-size: 22px'>“WordCloud”</p>", unsafe_allow_html=True)
         st.markdown("<p style ='text-align: justify; font-size: 16px'>A word cloud is a data visualization technique that shows the most used words in large font and the least used words in small font.</p>", unsafe_allow_html=True)
         st.markdown("<p style ='text-align: justify; font-size: 16px'>It helps to get an idea about your text data, especially when working on problems based on natural language processing.</p>", unsafe_allow_html=True)
    with col12:
        wordpic = Image.open("SentimentWebapp/images/wordcloud.png")
        cloudpic = wordpic.resize((375,375))
        st.image(cloudpic)
        
        
        
    
    

#sentiment scores

def score(x):

    vadertext = SentimentIntensityAnalyzer()
    return vadertext.polarity_scores(x)

#sentiment analyzer
        
def analyze(x):
    if x['compound'] >= 0.05:
        return 'Positive'
    elif x['compound'] <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'
    
    

#text translator

def texttranslate():
    st.title(f"Tagalog to English Translator")
    
    translator = Translator()
    dataframe_append = pd.DataFrame()
    cols = {'Municipalities', 'Comments','Scores', 'Analysis', 'Category'}
    multiple_files = st.file_uploader('Translate CSV',type="csv", accept_multiple_files=True)
    for file in multiple_files:
        file.seek(0)
        df = pd.read_csv(file)

        colsname = df.axes[1] #headername/column names

#validating if the file has the same column
        
        if any(i for i in colsname if i not in cols):
            st.error("Please make it sure your column name in your csv file is the same")
            
        else:
            dataframe_append = pd.concat([dataframe_append, df], ignore_index=True)        
            dataframe_append['Translations'] = dataframe_append['Comments'].apply(translator.translate, src='tl', dest='en').apply(getattr, args=('text',)) 
        
       

#checking is file not empty before display it
        
    if dataframe_append.empty == False:
        st.write(dataframe_append)

        @st.cache
    #raw_data = pd.concat(df)
        def convert_df(dataframe_append):
            #IMPORTANT: Cache the conversion to prevent computation on every rerun
            return dataframe_append.to_csv(index=False).encode('utf-8')
        csv = convert_df(dataframe_append)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='translated.csv',
            mime='text/csv',
            )         
                            
       
#text analyzer
             
def textanalysis():
    
     st.title(f"Sentiment Analyzer")
     dataframe_append = pd.DataFrame()
     cols = {'Municipalities', 'Comments','Scores', 'Analysis', 'Category', 'Translations'}
     
     multiple_files = st.file_uploader('Analyze CSV',type="csv", accept_multiple_files=True)
     for file in multiple_files:
         file.seek(0)
         df = pd.read_csv(file)

            
         colsname = df.axes[1] #headername/column names
         
#validating if the file has the same column
        
         if any(i for i in colsname if i not in cols):
             st.error("Please make it sure your column name in your csv file is the same")
             
         else:
             dataframe_append = pd.concat([dataframe_append, df], ignore_index=True)
         
         #del['Unnamed: 0']
             dataframe_append['Scores'] = dataframe_append['Translations'].apply(score)
             dataframe_append['Analysis'] = dataframe_append['Scores'].apply(analyze)

         

         #checking is file not empty before display it
     if dataframe_append.empty == False:
         

         @st.cache
        #coverting the data
         
         def convert_df(dataframe_append):
             #IMPORTANT: Cache the conversion to prevent computation on every rerun
             return dataframe_append.to_csv(index=False).encode('utf-8')
            
         st.write(dataframe_append)  

         #download the data
         csv = convert_df(dataframe_append)
         st.download_button(
             label="Download data as CSV",
             data=csv,
             file_name='sentiment.csv',
             mime='text/csv',
             )
         
                     
             
#data representation
         
def datavisual():
    
     st.title(f"Data Visualization")
     dataframe_append = pd.DataFrame()
     cols = {'Municipalities', 'Comments','Scores', 'Analysis', 'Category', 'Translations'}
     
     multiple_files = st.file_uploader('Upload CSV',type="csv", accept_multiple_files=True)
     for file in multiple_files:
         file.seek(0)
         df = pd.read_csv(file)

         colsname = df.axes[1] #headername/column names
         
         
         
#validating if the file has the same column
        
         if any(i for i in colsname if i not in cols):
             st.error("Please make it sure your column name in your csv file is the same")
               
         else:
             dataframe_append = pd.concat([dataframe_append, df], ignore_index=True)
         

#checking is file not empty before display it
     if dataframe_append.empty == False:
         st.write(dataframe_append)

         try:

             st.write("Pie Chart")

             muni_option  = dataframe_append['Municipalities'].unique().tolist()
             options = st.selectbox("Municipalities: ", muni_option, 0)

             category_option  = dataframe_append['Category'].unique().tolist()
             cate_options = st.selectbox("Category: ", category_option, 0)
        
        
        
             pos = dataframe_append.loc[(dataframe_append['Analysis']== "Positive") & (dataframe_append['Category']==cate_options) & (dataframe_append['Municipalities']==options)  ]
             neg = dataframe_append.loc[(dataframe_append['Analysis']== "Negative")  & (dataframe_append['Category']==cate_options) & (dataframe_append['Municipalities']==options)]
             neu = dataframe_append.loc[(dataframe_append['Analysis']== "Neutral") & (dataframe_append['Category']==cate_options) & (dataframe_append['Municipalities']==options)]
       
           
#chart
        #pie chart
              

             Labels = ['Positive', 'Negative', 'Neutral'] 
             sentvalues = [pos['Analysis'].count(), neg['Analysis'].count(), neu['Analysis'].count()]

             fig = go.Figure(data=[go.Pie(labels=Labels, values = sentvalues)])
             fig.update_layout(title=options + ' Covid-19 Responsed Sentiment Analysis' +"\t\t"+"(Category: " + cate_options +")")
             st.plotly_chart(fig)

        #bar chart
              
             st.write("Bar Chart")
        
         
        
             dataframe_append = dataframe_append.loc[(dataframe_append['Category']==cate_options)]
         
             figbar = px.histogram(dataframe_append,x='Municipalities', color='Analysis', title = "Laguna Covid-19 Responsed Sentiment Analysis"+"\t\t"+"(Category: "+cate_options+")" , text_auto=True,  barmode="group", color_discrete_sequence=["#C0EEE4","#F8F988", "#FFCAC8"] )
             
             st.plotly_chart(figbar)


         except:
             st.error("Make it sure all the rows values from Municipalities , Comments, Category and Translations is not blank or NaN! Please check your uploaded file carefully")    
                             
                       
     
#geo-graphic visual

def geographic():


#Biñan

#OpenStreetMap lagunamap
    lagunamap = folium.Map(location = [14.2888,121.2892], zoom_start = 11)
    folium.TileLayer('OpenStreetMap').add_to(lagunamap)
   

#uploadfile
    st.title(f"Laguna Geo-Graphic Visualization")
    dataframe_append = pd.DataFrame()
    cols = {'Municipalities', 'Comments','Scores', 'Analysis', 'Category', 'Translations'}

    
    multiple_files = st.file_uploader('Upload CSV',type="csv", accept_multiple_files=True)
    for file in multiple_files:
        file.seek(0)
        df = pd.read_csv(file)

        colsname = df.axes[0] #headername/column names
         
#validating if the file has the same column
        
        if all(i for i in colsname if i not in cols):
            st.error("Please make it sure your column name in your csv file is the same")
        else:
            dataframe_append = pd.concat([dataframe_append, df], ignore_index=True)
    

#checking is file not empty before display it
    if dataframe_append.empty == False:
        st.write(dataframe_append)

        #municipalities
        
#category options
        
        category_option  = dataframe_append['Category'].unique().tolist()
        cate_options = st.selectbox("Category: ", category_option, 0)


        lagunalocate = pd.read_csv('SentimentWebapp/lagunaloc/lagunamap.csv')
        lagunalocate = lagunalocate[['name', 'lat', 'long']]

       #tooltip=folium.Tooltip(location_info['name'], permanent=True)
       
#plotting map
        
        for index, location_info in lagunalocate.iterrows():

#filtering to get specific positive negative and neutral count
            
            pos = dataframe_append.loc[(dataframe_append['Analysis']== "Positive") & (dataframe_append['Municipalities']==location_info['name']) & (dataframe_append['Category']==cate_options) ]
            neg = dataframe_append.loc[(dataframe_append['Analysis']== "Negative")  & (dataframe_append['Municipalities']==location_info['name']) & (dataframe_append['Category']==cate_options) ]
            neu = dataframe_append.loc[(dataframe_append['Analysis']== "Neutral") & (dataframe_append['Municipalities']==location_info['name'])& (dataframe_append['Category']==cate_options)]

 #marking a map
            
            if pos['Analysis'].count() > 0 or neg['Analysis'].count() > 0 or  neu['Analysis'].count() > 0:
                
                if pos['Analysis'].count() > neg['Analysis'].count() and  pos['Analysis'].count() > neu['Analysis'].count():
                    iconemote = folium.features.CustomIcon('SentimentWebapp/images/happy.png', icon_size=(45,45))
                    folium.Marker([location_info['lat'],location_info['long']], tooltip=folium.Tooltip(location_info['name']), icon=iconemote).add_to(lagunamap)
        
                elif neg['Analysis'].count() > pos['Analysis'].count() and  neg['Analysis'].count() > neu['Analysis'].count():
                    iconemote = folium.features.CustomIcon('SentimentWebapp/images/sad.png', icon_size=(45,45))
                    folium.Marker([location_info['lat'],location_info['long']] ,tooltip=folium.Tooltip(location_info['name']), icon=iconemote).add_to(lagunamap)
                
                else:
                    iconemote = folium.features.CustomIcon('SentimentWebapp/images/neutral.png', icon_size=(45,45))
                    folium.Marker([location_info['lat'],location_info['long']] ,tooltip=folium.Tooltip(location_info['name']), icon=iconemote).add_to(lagunamap)

            else:
                iconemote = folium.features.CustomIcon('SentimentWebapp/images/na.png', icon_size=(45,45))
                folium.Marker([location_info['lat'],location_info['long']] ,tooltip=folium.Tooltip(location_info['name']),icon=iconemote).add_to(lagunamap)

         #download as png folium map
        #img_data = lagunamap._to_png(2)
    #img = Image.open(io.BytesIO(img_data))
        #img.save('lagunegeovisual.png')
     
        #st.download_button(
         #   label="Download as png",
          #  data= img_data,
           # file_name= cate_options+'_lagunageovisual.png',
            #mime='image/png',
         #)
    

            
    #st.set_option('deprecation.showPyplotGlobalUse', False)
    #lagunamapping = gpd.read_file("shapefilemap/Laguna Mapping.shp")

   
    #gdf = gpd.GeoDataFrame(lagunamapping)
    #folium.PolyLine(lagunamapping['geometry'])
    #folium.GeoJson(data=gdf["geometry"]).add_to(lagunamap)
    #st.write(lagunamapping)
    #st.pyplot()
    #st.map(lagunamap)
    
    
    #folium.GeoJson(data=gdf["geometry"]).add_to(lagunamap)
                

    st_folium(lagunamap, width = 1500, height= 800)

  

    #legend

    st.write("Legend:")
    legend = Image.open("SentimentWebapp/images/legend.png")
    legendresize = legend.resize((375,275))
    st.image(legendresize)


#wordcloud

def wordcloud():
    #stopwords

    adv.stopwords.keys()
    
    stopwords = set(adv.stopwords['tagalog'])
    #wordlocud pic
    
    maskpic = np.array(Image.open('SentimentWebapp/images/thumbs.png'))


    cols = {'Municipalities', 'Comments','Scores', 'Analysis', 'Category', 'Translations'}

    st.title(f"Word Cloud")
    dataframe_append = pd.DataFrame()    
    multiple_files = st.file_uploader('Upload CSV',type="csv", accept_multiple_files=True)
    for file in multiple_files:
        
        file.seek(0)
        df = pd.read_csv(file)

        colsname = df.axes[0] #headername/column names
         
#validating if the file has the same column
        
        if all(i for i in colsname if i not in cols):
            st.error("Please make it sure your column name in your csv file is the same")
        else:
          dataframe_append = pd.concat([dataframe_append, df], ignore_index=True)
         
    

#checking is file not empty before display it


    if dataframe_append.empty == False:


#options positive negative neutral
        category_option  = dataframe_append['Analysis'].unique().tolist()
        cate_options = st.selectbox("Category: ", category_option, 0)
        
        words = dataframe_append.loc[(dataframe_append['Analysis'])==cate_options]
        
            

#displaying those comment into wordcloud
        st.set_option('deprecation.showPyplotGlobalUse', False)
        wordcloud_text = WordCloud(stopwords = stopwords, max_words=6000, contour_color='steelblue', random_state=1, width=900, height=600, collocations=False,mask=maskpic, background_color="black")
        wordcloud_text.generate(''.join(str(words['Comments'].values)))
        plt.figure(figsize=(20,10),facecolor='k')
        plt.imshow(wordcloud_text,interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout (pad=0)
        #plt.savefig("cloud.png", format="png")
        st.pyplot()


#hiding footer

def hidefooter():
    hide_st_style = """
   <style>
   #MainMenu {visibility: hidden;}
    footer {visibility:hidden;}

   </style>   """
    st.markdown(hide_st_style, unsafe_allow_html=True)

#resizing width folium map

def mapresize():
    make_map_responsive = """
    <style>
    [title~="st.iframe"]{width: 100%}
    </style>
    """
    st.markdown(make_map_responsive, unsafe_allow_html=True)
    

#run start
if __name__=='__main__':
    main()
