import gym
import numpy as np
import cPickle as pickle
from tutorial import *
from pymongo import MongoClient

col = MongoClient("mongodb://localhost:27017").RL.m_car

env = gym.make("CartPole-v0")
obs = env.reset()
state_length = obs.shape[0]
action_space = env.action_space.n
episodes = 0
tau_reward = 0
gamma = 0.99
decay_rate = 0.99
learning_rate = 1e-3
render = False
resume = False

def discount_rewards(r):
  """ take 1D float array of rewards and compute discounted reward """
  discounted_r = np.zeros_like(r)
  running_add = 0
  for t in reversed(xrange(0, r.size)):
    if r[t] != -200: running_add = 0 # reset the sum, since this was a game boundary (pong specific!)
    running_add = running_add * gamma + r[t]
    discounted_r[t] = running_add
  return discounted_r

if resume:
  W = pickle.load(open('save.p','rb'))
else:
  W = {}
  W['1'] = np.random.rand(state_length,20) / np.sqrt(state_length)
  W['2'] = np.random.rand(20,action_space) / np.sqrt(20)

grad_buffer = { k: np.zeros_like(v) for k,v in W.iteritems() }
rmsprop_cache = { k : np.zeros_like(v) for k,v in W.iteritems() }

obs_,h_,dif_,r_ = [],[],[],[]

while True:
  if render: env.render()
  # sample action from distribution
  y,h = feedforward(obs,W)
  action = np.argmax(y) if np.argmax(y) > np.random.uniform() \
			else np.random.choice(action_space)
  # get info from the environment after performing an action
  obs, reward, done, info = env.step(action)
  tau_reward += reward
  # fake labels
  targets = np.zeros(action_space)
  targets[action] = 1
  dif = y - targets
  # store relevant information for estimating the gradient
  obs_.append(obs)
  h_.append(h)
  dif_.append(dif)
  r_.append(reward)
  # when episode is finished ... 
  if done:
    episodes += 1
    # ... vertically stack all info ...
    episode_obs = np.vstack(obs_)
    episode_h = np.vstack(h_)
    episode_dif = np.vstack(dif_)
    episode_r = np.vstack(r_)
    # ... reset memory ...
    obs_,h_,dif_,r_ = [],[],[],[]

    discounted_epr = discount_rewards(episode_r)
    # standardize the rewards to be unit normal (helps control the gradient estimator variance)
    discounted_epr -= np.mean(discounted_epr)
    discounted_epr /= np.std(discounted_epr)

    # ... scale a component to the gradient according to the reward ...
    episode_dif *= (episode_r - np.mean(episode_r))
    # ... perform backpropagation ...
    grad = backprop(episode_h,episode_dif,episode_obs,W)
    # ... sum grad over the entire trajectory ...
    for k,v in W.iteritems(): grad_buffer[k] += grad[k]
    print "Episode: ",episodes, "Total reward: ", tau_reward
#      col.insert_one({ 'episode':episodes ,'reward':tau_reward })
    if episodes % 10 == 0:
      for k,v in W.iteritems():
	grad[k] /= 10
	W[k] -= 0.0001*grad[k]
#        g = grad_buffer[k]
#        rmsprop_cache[k] = decay_rate * rmsprop_cache[k] + (1 - decay_rate) * g**2
#        W[k] += learning_rate * g / (np.sqrt(rmsprop_cache[k]) + 1e-5)
#	grad_buffer[k] = np.zeros_like(v)
#    if tau_reward != -200: 
#      print "!!!!!!! ", tau_reward
#      col.insert_one({ 'episode':episodes ,'reward':tau_reward })
      
#    if episodes % 100 == 0: pickle.dump(W, open('save.p', 'wb'))

    tau_reward = 0
    obs = env.reset()
