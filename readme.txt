README.TXT

# Lyrics Generator
Veronica Child, Maryam Hedayati, Chelsea Ying, and Sasha Mayn

A program that generates pop lyrics through templates, CFG, and random neural net.

## Running the Programs

Using the command line…

### To run the templates:
In the template_generator directory…

1. Run the program
‘’’
$ python2 lyricsGenerator.py
‘’’

2. Follow the prompts as specified


### To run the recurrent neural net:
In the rnn_generator directory…

To train and run your own trained model:
1. Set the textfile you want to use to train the network in the code by substituting ‘shakespeare.txt’ with your own textile with the correct path:
‘’’
with open(‘../billboard_lyrics_1964-2015.csv’, ‘r’, errors=‘ignore’) as f:
‘’’

2. Train and run your network:
‘’’
$ python3 rnn_tf.py
‘’’

To run our model, trained on billboard lyrics:
1. Run the network with the starting prefix you want to use to generate text:
‘’’
$ python3 rnn_tf.py saved/model.ckpt "The "
‘’’

### To run the CFG:
In the cfg_generator

1. Run the program:
‘’’
python3 cfg.py
‘’’

## Libraries

Below is a list of all the Python libraries we used:

- nltk
- nltk.corpus
- pickle
- random
- re
- sys
- son
- pattern.en *only compatible with Python 2
- tensor flow
- bumpy
- csv
- time

## Data

Our CFG and RNN use 50 years of Pop Music Lyrics as our data from a .csv that is available on Github (https://github.com/walkerkq/musiclyrics).
