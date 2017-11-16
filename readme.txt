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


### To run the random neural net:
In the rnn_generator directory…

1. Set the textfile you want to use to train the network in the code ("with open('data/shakespeare.txt', 'r') as f:")

2. Run the network
    $ python rnn_tf.py

3. Run the network with the starting prefix you want to use to generate text:
    $ python rnn_tf.py saved/model.ckpt "The "

### To run the CFG:


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

We are using lyrics .csv data from https://github.com/walkerkq/musiclyrics.
