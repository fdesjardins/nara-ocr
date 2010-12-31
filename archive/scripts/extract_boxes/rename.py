import sys, os

for x in range(721,733):
    os.rename('X_' + str(x) + ".png", 'W_' + str(x-721) + ".png")
