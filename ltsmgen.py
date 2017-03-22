import sys
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
# load ascii text and covert to lowercase
filename = "wonderland.txt"
raw_text = open(filename, encoding='utf-8').read()
raw_text = raw_text.lower()

chars = sorted(list(set(raw_text)))
# summarize the loaded data
n_chars = len(raw_text)
n_vocab = len(chars)
print ("Total Characters: ", n_chars)
print ("Total Vocab: ", n_vocab)

# create mapping of unique chars to integers, and a reverse mapping
char_to_int = dict((c, i) for i, c in enumerate(chars))
int_to_char = dict((i, c) for i, c in enumerate(chars))
int_to_hot = numpy.eye(n_vocab)
# prepare the dataset of input to output pairs encoded as integers
seq_length = 100
dataX = []
dataY = []

for i in range(3000, 3500, 1):
    seq_in = raw_text[i:i + seq_length]
    seq_out = raw_text[i + seq_length]
    dataX.append(int_to_hot[[char_to_int[char] for char in seq_in]])
    dataY.append(int_to_hot[char_to_int[seq_out]])
n_patterns = len(dataX)
print("Total Patterns: ", n_patterns)
# reshape X to be [samples, time steps, features]


X = numpy.array(dataX)#, (n_patterns, seq_length, n_vocab))
print(X.shape)
print()


y = numpy.array(dataY)
# define the LSTM model
model = Sequential()
model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2])))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation='softmax'))
# load the network weights
filename = "weights/137000weights-improvement-10-1.7069.hdf5"
model.load_weights(filename)
model.compile(loss='categorical_crossentropy', optimizer='adam')

sss = input().lower()
sss = "{:>100}".format(sss)
sss = sss[len(sss) - 100:]

# pick a random seed
start = numpy.random.randint(0, 50)
pattern = int_to_hot[[char_to_int[char] for char in sss]]
print ("Seed:")
print ("\"", ''.join([int_to_char[value.argmax()] for value in pattern]), "\"")
# generate characters
for i in range(500):
    x = numpy.reshape(pattern, (1, len(pattern), n_vocab))
    prediction = model.predict(x, verbose=0)
    index = numpy.argmax(prediction)
    result = int_to_char[index]
    seq_in = [int_to_char[value.argmax()] for value in pattern]
    sys.stdout.write(result)
    pattern[0:-1] = pattern[1:]
    pattern[-1] = int_to_hot[index]
print ("\nDone.")