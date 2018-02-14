from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, precision_score, recall_score


# GET DATA
X = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/iris/bezdekIris.data")

# PRE-PROCESSING
X = X.values

X = pd.DataFrame({ 'sepal_length':X[:,0], 'sepal_width':X[:,1], 'petal_length':X[:,2], 'petal_width':X[:,3], 'class':X[:,4] })

T = pd.get_dummies(X["class"]).values
X = X[["sepal_length","sepal_width","petal_length","petal_width"]].values.astype("float")

hidden_size = 40

# FEATURE NORMALIZATION
for i in range(X.shape[1]):
  X[:,i] = ( X[:,i] - np.mean(X[:,i]) ) / np.std(X[:,i])

# TRAIN-TEST SPLIT
x_train, x_test = train_test_split(X,test_size=0.2)
t_train, t_test = train_test_split(T,test_size=0.2)


# NEURAL NETWORK WEIGHTS (XAVIER INITIALIZATION)
W = {}
W['1'] = np.random.rand(X.shape[1],hidden_size) / np.sqrt(X.shape[1])
W['2'] = np.random.rand(hidden_size,3) / np.sqrt(hidden_size)


def sigmoid(x):
  return 1.0 / (1.0 + np.exp(-x))


#def softmax(x):
  #return np.exp(x) / np.sum(np.exp(x))

def softmax(w):
    a = np.max(w)
    e = np.exp(np.array(w) - a)
    dist = e / np.sum(e)
    return dist


def feedforward(X,W):
  z1 = np.dot(X,W['1'])
#  h1 = sigmoid(z1)
  h1 = z1
  h1[h1<0] = 0
  z2 = np.dot(h1,W['2'])
  y = np.array(map(softmax,z2)) if len(z2.shape) != 1 else softmax(z2)
  return y,h1


def backprop(h,d,X,W):
  dW2 = np.dot(h.T,d)
#  dW1 = np.dot( X.T,np.multiply( h*(1-h) , np.dot(d,W["2"].T) ) )
  dW1 = np.dot( X.T,np.multiply( h , np.dot(d,W["2"].T) ) )
  return { '1':dW1, '2':dW2 }


def loss(y,t):
   logProb = np.log(y)
   tagProd = t * logProb
   sums = map(lambda x:np.sum(x),tagProd) if len(tagProd.shape) != 1 else sum(tagProd)
   loss = -1 * np.mean(sums)
   return loss


def gradientDescent(alpha=0.01,iters=100000):
  history = []
  for i in range(iters):
    y,h = feedforward(x_train,W)
    dW = backprop(h,(y - t_train),x_train,W)
    W['2'] -= alpha * dW['2']
    W['1'] -= alpha * dW['1']
    if( i % 10 == 0 ):
      print np.mean(f1_score(t_test,np.around(predict(x_test,W)),average=None))
      history.append(loss(y,t_train))
  return history


def sgd(alpha=0.001,iters=10):
  history = []
  sgd_data = np.column_stack((x_train,t_train))
  np.random.shuffle(sgd_data)
  for i in xrange(iters):
   for d in sgd_data:
     X_l = x_train.shape[1]
     T_l = X_l + t_train.shape[1]
     X_ = d[0:X_l]
     T_ = d[X_l:T_l]
     y_,h_ = feedforward(X_,W)
     dif = (y_ - T_)
     dif = dif.reshape(1,dif.shape[0])
     h_ = h_.reshape(1,h_.shape[0])
     X_ = X_.reshape(1,X_.shape[0])
     dW = backprop(h_,dif,X_,W)
     W['2'] -= alpha * dW['2']
     W['1'] -= alpha * dW['1']
     history.append(loss(y_,T_))
  return history


def sgd_(alpha=0.001,iters=10):
  history = []
  sgd_data = np.column_stack((x_train,t_train))
  for i in xrange(iters):
     batch = sgd_data[np.random.randint(sgd_data.shape[0],size=20),:]
     X_l = x_train.shape[1]
     T_l = X_l + t_train.shape[1]
     X_ = d[0:X_l]
     T_ = d[X_l:T_l]
     y_,h_ = feedforward(X_,W)
     dif = (y_ - T_)
     dif = dif.reshape(1,dif.shape[0])
     h_ = h_.reshape(1,h_.shape[0])
     X_ = X_.reshape(1,X_.shape[0])
     dW = backprop(h_,dif,X_,W)
     W['2'] -= alpha * dW['2']
     W['1'] -= alpha * dW['1']
     history.append(loss(y_,T_))
  return history


def predict(x,w):
#  return np.around(feedforward(x,w)[0]).astype(int)
  return feedforward(x,w)[0]
