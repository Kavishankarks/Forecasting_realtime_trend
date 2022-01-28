import pandas as pd
import streamlit as st
import numpy as np
# from nltk.corpus import stopwords
from pytrends.request import TrendReq
import pandas as pd
import time
import re
startTime = time.time()
from statsmodels.tsa.arima.model import ARIMA
from matplotlib import pyplot
pytrend = TrendReq(hl='en-GB', tz=360)


st.title("Forecasting the furure trending topics")
st.markdown("Future is yours!")

stopWords={'i': 1,'me': 1,'my': 1,'myself': 1,'we': 1,'our': 1,'ours': 1,'ourselves': 1,'you': 1,"you're": 1,"you've": 1,"you'll": 1,"you'd": 1,'your': 1,'yours': 1,'yourself': 1,
 'yourselves': 1,'he': 1,'him': 1,'his': 1,'himself': 1,'she': 1,"she's": 1,'her': 1,'hers': 1,'herself': 1,'it': 1,"it's": 1,'its': 1,'itself': 1,'they': 1,
 'them': 1,'their': 1,'theirs': 1,'themselves': 1,'what': 1,'which': 1,'who': 1,'whom': 1,'this': 1,'that': 1,"that'll": 1,'these': 1,'those': 1,'am': 1,'is': 1,'are': 1,
 'was': 1,'were': 1,'be': 1,'been': 1,'being': 1,'china': 1,'germany': 1,'japan': 1,'russia': 1,'pakistan': 1,'rising': 1,'query': 1,'value': 1,'price': 1,'near': 1,
 'has': 1,'had': 1,'having': 1, 'do': 1,'does': 1, 'did': 1,'doing': 1,'a': 1,'an': 1,'the': 1,'and': 1,'but': 1,'if': 1,'or': 1,'because': 1,
 'as': 1,'until': 1,'while': 1,'of': 1,'at': 1,'by': 1,'for': 1,'with': 1,'about': 1,'against': 1,'between': 1,'into': 1,'through': 1,'during': 1,'before': 1,
 'after': 1,'above': 1,'below': 1,'to': 1,'from': 1,'up': 1,'down': 1,'in': 1,'out': 1,'on': 1,'off': 1,'over': 1,'under': 1,'again': 1,'further': 1,'then': 1,
 'once': 1,'here': 1,'there': 1,'when': 1,'where': 1,'why': 1,'how': 1,'all': 1,'any': 1,'both': 1,'each': 1,'few': 1,'more': 1,'most': 1,'other': 1,'some': 1,
 'such': 1,'no': 1,'nor': 1,'not': 1,'only': 1,'own': 1,'same': 1,'so': 1,'than': 1,'too': 1,'very': 1,'s': 1,'t': 1,'can': 1,'will': 1,'just': 1,'don': 1,"don't": 1,
 'should': 1,"should've": 1,'now': 1,'d': 1,'ll': 1,'m': 1,'o': 1,'re': 1,'ve': 1,'y': 1,'ain': 1,'aren': 1,"aren't": 1,'couldn': 1,"couldn't": 1,'didn': 1,"didn't": 1,
 'doesn': 1,"doesn't": 1,'hadn': 1,"hadn't": 1,'hasn': 1,"hasn't": 1,'haven': 1,"haven't": 1,'isn': 1,"isn't": 1,'ma': 1,'mightn': 1,"mightn't": 1,'mustn': 1,
 "mustn't": 1,'needn': 1,"needn't": 1,'shan': 1,"shan't": 1,'shouldn': 1,"shouldn't": 1,'wasn': 1,"wasn't": 1,'weren': 1,"weren't": 1,'won': 1,"won't": 1,'wouldn': 1,
 "wouldn't": 1,'world': 1,'india': 1,'usa': 1,'us': 1,'mexico': 1,'uk': 1,'france': 1}
# # colnames = ["keywords"]
# # df = pd.read_csv("gtkeywords.csv", names=colnames)
# # df2 = df["keywords"].values.tolist()
# # df2.remove("Keywords")

@st.cache
def genData(Trendkey):
    dataset = []
    for x in range(0,1):
        # keywords = [df2[x]]
         pytrend.build_payload(
         Trendkey,
         cat=0,
         timeframe='2010-01-01 2021-06-06',geo='GB')
         data = pytrend.interest_over_time()
         if not data.empty:
              data = data.drop(labels=['isPartial'],axis='columns')
              dataset.append(data)
    return dataset

def showSingleKeyTrend(key):
    result = pd.concat(genData(key), axis=1)
    result.to_csv('trends.csv')

    # executionTime = (time.time() - startTime)
    # print('Execution time in sec.: ' + str(executionTime))

    df=pd.read_csv("trends.csv")
    st.write("Displaying data")

    st.write(df.size)
    st.write(df.head(10))

    st.line_chart(df)

keys=['deep learning', 'machine learning','python','artificial intelligence','covaxin']

option = st.selectbox('Which topic do you like?',keys)

'You selected: ', option
key=[]
key.append(option)


@st.cache
def ARIMA_MODEL():
    series = pd.read_csv('trends.csv', header=0, index_col=0, parse_dates=True, squeeze=True)
    X = series.values
    size = int(len(X) * 0.70)
    train, test = X[0:size], X[size:len(X)]
    history = [x for x in train]
    predictions = list()
    # walk-forward validation
    for t in range(len(test)):
        model = ARIMA(history, order=(5,2,0))
        model_fit = model.fit()
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
        #print('predicted=%f, expected=%f' % (yhat, obs))
    # evaluate forecasts
    # rmse = sqrt(mean_squared_error(test, predictions))
    # print('Test RMSE: %.3f' % rmse)
    # plot forecasts against actual outcomes
    tp=pd.DataFrame(test,columns=['test'])
    tp['prediction']=predictions
    return tp

if(st.button("Click to get trend of "+key[0])):
    showSingleKeyTrend(key)
    st.title("Displaying plot of arima mode predictions")
    tp=ARIMA_MODEL()
    
    st.line_chart(tp)
    
#----------------------------------------------------------------------------------------------------------------
#trend of many keywords
st.title("Generating whole list of data")

txt=st.text_area("Enter key words to search:(seperate with ,)")
multiKeys=txt.split(",")
st.write(*multiKeys)

if(st.button("Click to generate result")):
    MultiRes = pd.concat(genData(multiKeys), axis=1)
    MultiRes.to_csv('Multitrends.csv')

    dfMulti=pd.read_csv("Multitrends.csv")
    st.write("Displaying data")

    st.write(dfMulti.size)
    st.write(dfMulti.head(10))

    st.line_chart(dfMulti)

#-----------------------------------------------------------------------------------
#related key words and there data

q_rel=st.text_area("Enter key word to search related keywords:")
q_rel=q_rel.split(",")
countries=['world','india','usa','us','mexico','uk','france','china','germany','japan','france','russia','pakistan','rising', 'query', 'value','price','near']

def get_related_queries(query):
    pytrend.build_payload(query)
    related_queries=pytrend.related_queries()
    a=related_queries.values()
    a=str(a)
    a=(a.split('\n'))
    # a.remove(a[0])
    a=a[1:100]
    st.write("Found related queris:")
    for i in range(1,10):
        st.write(a[i])
    rel_keys=[]
    kwords=[]
    #removing all characters and digits and retainign only alpha's
    for i in a:
        txt = i
        txt.strip("")
        #print(txt)
        #Find all lower case characters alphabetically between "a" and "m":

        x = re.findall("[a-z]+", txt)
        for i in x:
            kwords.append(i)
    #splitting the key word if two words are present(ex: deep learning)
    query=query[0].split(' ')
    #removing stop words running twice remove all things which are remained in first iteration
    for _ in range(2):
        for i in kwords:
            if(i==query[0]):
                kwords.remove(query[0])
            if(len(query)>1 and i==query[1] ):
                kwords.remove(query[1]) 
    st.title("Generated Related  list of keywords")
    st.write(*kwords)

    #removing stop words 
    # en_stops = set(stopwords.words('english'))
    for _ in range(2):
        for i in kwords:
            if(i==query[0]):
                kwords.remove(query[0])
            if(len(query)>1 and i==query[1] ):
                kwords.remove(query[1])
    for word in kwords: 
        if word not in rel_keys and word not in en_stops and word not in countries:
            rel_keys.append(word)

    st.write("Keys after removing stop words:")
    st.write(*rel_keys)
    return rel_keys


if(st.button("Get related queries of "+q_rel[0],help="Click on the button to get all the queries related to"+q_rel[0])):
    rel_topics=get_related_queries(q_rel)
    rel_topics.insert(0,q_rel[0])
    rel_topics=rel_topics[:5]
    df_rel_topics_res = pd.concat(genData(rel_topics), axis=1)
    df_rel_topics_res.to_csv('rel_topics_trends.csv')

    df_rel_topics=pd.read_csv("rel_topics_trends.csv")
    st.write("Displaying data")

    st.write(df_rel_topics.size)
    st.write(df_rel_topics.head(10))

    st.line_chart(df_rel_topics)

    st.write(df_rel_topics.corr())


