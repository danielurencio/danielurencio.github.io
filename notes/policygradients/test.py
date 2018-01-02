import gym
import numpy as np
import cPickle as pickle
from tutorial import *
from pymongo import MongoClient
import matplotlib.pyplot as plt

col = MongoClient("mongodb://localhost:27017").RL.m_car

env = gym.make("CartPole-v0")#gym.make("MountainCar-v0")
obs = env.reset()
state_length = obs.shape[0]
action_space = env.action_space.n
episodes = 0
tau_reward = 0
learning_rate = 0.1
batch = 5
gamma = 0.99
hidden = 20
render = False
resume = False
t = 0
B1 = 0.9
B2 = 0.999
decay_rate = 0.99

def discount_rewards(r):
    """ take 1D float array of rewards and compute discounted reward """
    discounted_r = np.zeros_like(r)
    running_add = 0
    for t in reversed(xrange(0, r.size)):
        running_add = running_add * gamma + r[t]
        discounted_r[t] = running_add
    return discounted_r

if resume:
  W = pickle.load(open('save.p','rb'))
else:
  W = {}
  W['1'] = np.random.rand(state_length,hidden) / np.sqrt(state_length)
  W['2'] = np.random.rand(hidden,action_space) / np.sqrt(hidden)

grad_buffer = { k: np.zeros_like(v) for k,v in W.iteritems() }
ADAM_m_t = { k: np.zeros_like(v) for k,v in W.iteritems() }
ADAM_v_t = { k: np.zeros_like(v) for k,v in W.iteritems() }

rmsprop_cache = { k : np.zeros_like(v) for k,v in W.iteritems() } # rmsprop memory

obs_,h_,dif_,r_ = [],[],[],[]

REWARDS = []
Rewards_Mean = []

while True:
  if render: env.render()
  # sample action from distribution
  y,h = feedforward(obs,W)
  action = np.argmax(y) if np.max(y) > np.random.uniform() \
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
    REWARDS.append(tau_reward)
    episodes += 1
    # ... vertically stack all info ...
    episode_obs = np.vstack(obs_)
    episode_h = np.vstack(h_)
    episode_dif = np.vstack(dif_)
    episode_r = np.vstack(r_)
    # ... reset memory ...
    obs_,h_,dif_,r_ = [],[],[],[]

    dis_R = discount_rewards(episode_r)
    normalized_R = (dis_R - np.mean(dis_R)) / dis_R
 
#    normalized_R = (episode_r - np.mean(episode_r))  / np.std(episode_r)
    # ... scale a component to the gradient according to the reward ...
    episode_h *= normalized_R
    # ... perform backpropagation ...
    grad = backprop(episode_h,episode_dif,episode_obs,W)
    # ... sum grad over the entire trajectory ...
    for k,v in W.iteritems(): grad_buffer[k] += grad[k]
#    print "Episode: ",episodes, "Total reward: ", tau_reward
    if episodes % batch == 0:
      t += 1
      for k,v in W.iteritems():
        g = grad_buffer[k] # gradient
        rmsprop_cache[k] = decay_rate * rmsprop_cache[k] + (1 - decay_rate) * g**2
        W[k] += learning_rate * g / (np.sqrt(rmsprop_cache[k]) + 1e-5)
        grad_buffer[k] = np.zeros_like(v) # reset batch gradient buffer


        g_hat = (grad_buffer[k] / batch)
	ADAM_m_t[k] = B1* ADAM_m_t[k] + (1-B2)*g_hat
	ADAM_v_t[k] = B1* ADAM_v_t[k] + (1-B2)*g_hat**2

	m_hat = ADAM_m_t[k] / (1 - (B1**t))
	v_hat = ADAM_v_t[k] / (1 - (B2**t))

	adam_quotient = learning_rate / (np.sqrt(v_hat) + 1e-08)
#ADAM
#	W[k] -= adam_quotient * m_hat
#Normal Gradient Descent	
#	W[k] -= learning_rate * (grad_buffer[k] / batch)
        grad_buffer[k] = np.zeros_like(v)
 
    if episodes % 1000 == 0:
	print "Episode: ",episodes, "Total reward: ",np.mean(REWARDS)
        Rewards_Mean.append(np.mean(REWARDS))
        REWARDS = []
        if episodes % 10000 == 0:
	  t = 0
    #      plt.plot(Rewards_Mean); plt.show()
    tau_reward = 0
    obs = env.reset()
