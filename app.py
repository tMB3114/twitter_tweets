from flask import Flask, render_template, request
import pandas as pd
import datetime
import numpy as np
import tensorflow as tf
import keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

# to read csv file
data = pd.read_csv('all_final.csv')



    
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


    
app = Flask(__name__)

@app.route('/')
def hello():
     return render_template('home.html')
 
@app.route('/', methods = ['POST','GET'])
def my_for_post():
     name = request.form['word']
     val = word_index.get(name)
     if str(name) == "":
        information = "Hello You !! Please enter Nepali word  " 
        return render_template('home.html', information = information) 
     elif not val:
         information = "Sorry !! Please enter next word!!"
         return render_template('home.html', information = information)      
     else:
        arr = np.arange(0,max(df.columns)+1)
        np.random.shuffle(arr)
        df.columns = arr

        row_arr = np.arange(0,df.shape[0])
        np.random.shuffle(row_arr)
        df.index = row_arr

        
        for i in range(max_length):
            if (df[i] == val).any():
                mask = df[i] == val
                break
        ll = np.array(df[mask])[0]
        ll.tolist()
        final_array = []
        def filter_array(arr):
            for a in arr:
                if a != 0:
                    final_array.append(a)
            return final_array  
        arr = filter_array(ll)
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