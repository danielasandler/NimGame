import numpy as np
from Nim import Nim
from MinMaxAgent import MinMaxAgent
# # Sample NumPy array
# my_array = np.array([[1, 2, 0],
#                      [0, 4, 5],
#                      [6, 0, 8],
#                      [0, 10, 0]])

# # Count zeros in all columns using numpy.sum
# zero_counts = np.sum(my_array == 0, axis=0)
# print(zero_counts)
# #print(list(zero_counts))

# #arr2 = my_array==0
# #print(arr2)
# result = np.bitwise_xor.reduce(zero_counts)
# print(result)


env=Nim()
player=MinMaxAgent(player=1)
print(player.evaluate(env.state))
