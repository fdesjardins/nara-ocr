import sys, os

for x in range(3099,3122):
	command = 'mv X_' + str(x) + '.png Y_' + str(x-3096) + '.png'
	os.system(command)
