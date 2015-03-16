import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, preprocessing
import pandas as pd
from matplotlib import style
style.use("ggplot")

Features = ["Author-Followers", "Market Cap", "Direction_Num", "Editor-Picks"]

def build_data_set(features = Features):
	data_df = pd.DataFrame.from_csv("seeking_alpha_stats_enhanced.csv")

	X = np.array(data_df[features].values)

	y = (data_df["status10"].values.tolist())

	X = preprocessing.scale(X)

	#plt.scatter(X,y)
	#plt.show()

	print X

	return X,y

def analysis():

	test_size = 200
	X, y = build_data_set()

	print len(X)
	print len(y)

	clf = svm.SVC(kernel="linear", C=1.0)

	clf.fit(X[:-test_size],y[:-test_size])

	correct_count = 0

	for x in range(1,test_size+1):
		if clf.predict(X[-x])[0] == y[-x]:
			correct_count +=1

	print "Accuracy: ", (float(correct_count)/float(test_size))*100.00


analysis()
