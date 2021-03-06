# -*- coding: utf-8 -*-
"""Spam_sorting_Machine_Learning-IPWK9_Angela_Njogu.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vGrZGdXnxKSewqky7u4ZLG3eJWNS0rWV

# E-mail sort: Spam or non-spam: Machine Learning Project

## Defining the question

### Specifying the question

Classifying email data as either spam or email.

### Defining the metrics of success

To consider my project successful, I should have been able to build a Naive Bayes model that predicts whether an email is either spam or not.

### Understanding the context

The data records each represent an email, and the columns detail the counts for different words and punctuations found in the emails, information about capital letter sequences and whether an email is a spam or not

## Reading the data

Importing relevant libraries:
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import metrics, model_selection, naive_bayes, preprocessing

"""Loading the data:"""

data =pd.read_csv("/content/spambase.data")
names =pd.read_csv("/content/spambase.names", sep='|', header=27)

plt.rcParams['figure.figsize'] = (10,8)
plt.rcParams['axes.titleweight'] = 700
plt.rcParams['axes.titlesize'] = 16

"""## Checking the data"""

# displaying the shape of the dataset.

data.shape

# checking the column data types
data.dtypes

# previewing the head of the dataset

data.head()

# previewing the tail of the dataframe

data.tail()

# previewing the names dataset

names

"""## Data cleaning"""

# checking for missing values and duplicates

print(data.isnull().any().any())
print(data.duplicated().any())

# dropping duplicates

data.drop_duplicates(inplace=True)

# cleaning the names dataset

# the column names begin from row index 2
columns =names.iloc[2:]

# splitting the column into two
columns =columns['Unnamed: 0'].str.split(expand= True)

# naming my columns
columns.columns = ['column_name', 'variable_type']
columns

naming = list(columns.column_name)
naming.append('spam')

data.columns = naming
data.head()

"""## Exploratory Data Analysis

### Univariate analysis
"""

# plotting the number of spams and not spams

sns.countplot(x=data['spam'])
plt.title("Number of records that are spam and non-spam")

"""- A majority of the emails in the records are not spam.
- The frequency margin between the two categories is not very large.

### Multivariate analysis
"""

# displaying the most frequently used words in non-spam emails
# punctuation character values are not going to be included

# picking only non-spam email records
non = data[data['spam']==0]

# picking only the word frequency columns
words_non = non.iloc[:, 0:-10]

# creating a dataframe and selecting the top ten most frequently used words
word_n =pd.DataFrame(words_non.sum().sort_values(ascending=False).head(10))

# plotting the data
sns.barplot(x= word_n.index, y= word_n[0], palette='cubehelix')
plt.xticks(rotation=90)
plt.title("Most frequent words in non-spam emails")

"""- The most frequently used word in non- spam emails is you.
- The other nine appear in this order of frequency:
   1. hp
   2. george
   3. will
   4. hpl
   5. re
   6. your
   7. edu
   8. meeting
   9. all 
"""

# displaying the least frequently used words in spam emails

spam = data[data['spam']==1]

# only picking spam email records
words_spam = spam.iloc[:, 0:-10]

word_s = pd.DataFrame(words_spam.sum().sort_values(ascending=False).head(10))


sns.barplot(x= word_s.index, y= word_s[0], palette='cubehelix')
plt.xticks(rotation=90)
plt.title("Most frequent words in spam emails")

"""- The most frequently used word in spam emails is you as well.
- The following nine appear as follows in terms of frequency:
   1. your
   2. will
   3. free
   4. our
   5. all
   6. mail
   7. email
   8. business
   9. remove

## Naive Bayes Model building
"""

# splitting the data into train and test sets

X= data.drop(['spam'], axis=1)
y= data['spam']

X_train, X_test, y_train, y_test= model_selection.train_test_split(X,y, test_size=0.2, random_state=98)

# instatiating Multinomial naive bayes

Mnb = naive_bayes.MultinomialNB()

# training my raw data
model= Mnb.fit(X_train, y_train)

pred = model.predict(X_test)

# computing the accuracy of my model
metrics.accuracy_score(y_test, pred)

# displaying the confusion matrix
metrics.confusion_matrix(y_test, pred)

"""#### Standardizing my data

I will be using MinMaxScaler to standardize my data. The values will range from 1 to 0.
"""

# calling the scaling method MinMaxScaler
sc = preprocessing.MinMaxScaler()

# transforming our target and predictor variables
x_train = sc.fit_transform(X_train)
x_test = sc.transform(X_test)

# training my data
std_model= Mnb.fit(x_train, y_train)

pred_std = std_model.predict(x_test)

# computing the accuracy score
metrics.accuracy_score(y_test, pred_std)

"""- The accuracy of my model has greatly increased after standardizing my data."""

# displaying the confusion matrix
metrics.confusion_matrix(y_test, pred_std)

"""#### Hyperparameter tuning"""

# creating a for loop to compute the accuracies across different alpha values 
vals = list(np.arange(0.01,1,0.02))
scores = []
alpha = []

for i in vals:
  model = naive_bayes.MultinomialNB(alpha=i)
  model = model.fit(x_train, y_train)

  predicted = model.predict(x_test)
  acc = metrics.accuracy_score(y_test, predicted)

  scores.append(acc)
  alpha.append(i)

# converting the two lists into dataframes and then combining them.
Scores =pd.DataFrame(scores,)
Alpha =pd.DataFrame(alpha,)

accuracy_scores= pd.concat([Scores, Alpha], axis=1)

# naming the columns of the dataframe
accuracy_scores.columns= ['accracy_scores', 'alpha_values']

# displaying the first ten alpha values with the largest accuracy score
accuracy_scores.sort_values(by=['accracy_scores'],ascending=False).head(10)

"""- The ten best alpha values all have an accuracy score of 89.07 which is slightly higher than the previous models."""

# instatiating my model and setting alpha to 0.01
best_model = naive_bayes.MultinomialNB(alpha=0.01)

# training my data and generating predictions
best_model = best_model.fit(x_train, y_train)
pred_vals =best_model.predict(x_test)

# computing the accuracy score
metrics.accuracy_score(y_test, pred_vals)

# displaying the final confusion matrix
metrics.confusion_matrix(y_test, pred_vals)