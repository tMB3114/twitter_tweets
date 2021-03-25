from flask import Flask, render_template, request
import pandas as pd

import numpy as np
import tensorflow as tf
import keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

# to read csv file
data = pd.read_csv('all_final.csv')

# for random tweet 
def random_tweet(dataframe):
    val = np.random.randint(1,dataframe.shape[0])
    return dataframe['tweet'][val]

    
#main code  
tokenizer = Tokenizer(90000)
tokenizer.fit_on_texts(data['tweet'])
word_index = tokenizer.word_index
tweet_search = []
for a in data['tweet']:
    token_list = tokenizer.texts_to_sequences([a])[0]
    tweet_search.append(token_list)    
    
max_length = max(len(i) for i in tweet_search)    
a = np.array(pad_sequences(tweet_search,max_length))    
df = pd.DataFrame(a)

# to filter array
def filter_array(arr):
    final_array = [] 
    for a in arr:
            if a!=0:
                final_array.append(a)
    
app = Flask(__name__)

@app.route('/')
def hello():
     return render_template('home.html')
 
@app.route('/', methods = ['POST','GET'])
def my_for_post():
     name = request.form['word']
     user_input = name.lower()
     word_array = user_input.split()
     v = []
     hiss = 0
     for i in range(len(word_array)):
            val = word_index.get(word_array[i])
            v.append(val)    
            if not val:
                hiss = 1  
     if 'mamba' in word_array:  
         information = random_tweet(data)
         return render_template('home.html', information = information)        
                
     elif hiss == 1:
         information = "Hello Kale Dai !! Please enter other Nepali words  "
         return render_template('home.html', information = information)
                      
     else:
        #to shuffle row index   
        row_arr = np.arange(0,df.shape[0])
        np.random.shuffle(row_arr)
        df.index = row_arr
        value = 0  
        a = 0
        for ind in row_arr:  
            for i in range(len(v)):
                if v[i]  in df.values[ind]:
                    value = 1 + value
                else:
                    value = 0 
                    continue
     
            if value == len(v):
                a = ind
                break     
    
    
        if a == 0:
            information = "Enter next word"
            return render_template('home.html', information = information)
            
        else:            
            arr = filter_array((df.iloc[a,:].values).tolist())
            final = ""
            word = ''
            for a in arr:
                for key,value in tokenizer.word_index.items():
                    if a == value:
                        word = key
                        break
                final = final + word + " " 
            information = final
            return render_template('home.html', information = information)
        
    
           
if __name__ == "__main__":
    app.run(debug = True)
