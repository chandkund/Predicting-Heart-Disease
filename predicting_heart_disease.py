# -*- coding: utf-8 -*-
"""Predicting Heart Disease.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ghUGLhZ8lofuIfTYGsRgI4utbRskTOw0

# **Predicting Heart Disease**
## **Project Overview**
The project focuses on predicting heart disease using the UCI Heart Disease dataset. Heart disease remains one of the leading causes of death worldwide, and early prediction and diagnosis can significantly enhance treatment outcomes. This project aims to build a machine learning model that can accurately predict the presence of heart disease based on various clinical and demographic features. By utilizing advanced data preprocessing techniques and various machine learning algorithms, the goal is to create a model that can aid healthcare professionals in identifying patients at risk of heart disease.

## **Dataset Description**
The UCI Heart Disease dataset is a well-known dataset that contains several features related to the diagnosis of heart disease. The dataset includes both categorical and numerical features, which are vital for building predictive models. Here's a detailed description of the features:

## **Feature Descriptions:**
**age:** Age of the patient (integer).

**sex:** Gender of the patient (categorical; 0 = female, 1 = male).

**cp:** Chest pain type (categorical; 0-3 values representing different types of chest pain).

**trestbps:** Resting blood pressure in mm Hg on admission to the hospital (integer).

**chol:** Serum cholesterol in mg/dl (integer).

**fbs:** Fasting blood sugar > 120 mg/dl (categorical; 1 = true, 0 = false).

**restecg:** Resting electrocardiographic results (categorical; 0-2 values representing different results).

**thalach:** Maximum heart rate achieved (integer).

**exang:** Exercise-induced angina (categorical; 1 = yes, 0 = no).

**oldpeak:** ST depression induced by exercise relative to rest (integer).

**slope:** Slope of the peak exercise ST segment (categorical; 0-2 values representing different slopes).

**ca:** Number of major vessels (0-3) colored by fluoroscopy (integer).

**thal:** Thalassemia (categorical; 3 = normal, 6 = fixed defect, 7 = reversible defect).

**num:**Target variable representing the presence of heart disease (integer; 0 = no disease, 1-4 = different levels of disease).
"""

pip install ucimlrepo

"""## **Import Relevant Libraries**"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
## Problem is Classification so use classifiaction algorithm for prediction
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,StackingClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

"""## **Load Dataset**"""

from ucimlrepo import fetch_ucirepo

# fetch dataset
heart_disease = fetch_ucirepo(id=45)

# data (as pandas dataframes)
X = heart_disease.data.features
y = heart_disease.data.targets

# metadata
print(heart_disease.metadata)

# variable information
print(heart_disease.variables)

X.head()



y.head()

## Data Cleaning And Preprocessing

X.info()

y.info()

sns.countplot(x=y['num'])
plt.show()

X.isnull().sum()

"""## **Data Cleaning and Preprocessing**"""

X['ca'].fillna(X['ca'].mean(),inplace=True)
X['thal'].fillna(X['thal'].mode()[0],inplace=True)

X.isnull().sum()

from imblearn.over_sampling import SMOTE
smote =SMOTE()
X,y=smote.fit_resample(X,y)

sns.countplot(x=y['num'])
plt.show()

## Visulization of Data

sns.countplot(x=X['sex'])
plt.show()

X['age'].max()

X['age'].min()

sns.histplot(x=X['age'])
plt.show()

sns.countplot(x=X['cp'])
plt.show()



cols = ['cp','fbs','restecg', 'exang','slope','thal']

fig, ax = plt.subplots(nrows=3, ncols=2, figsize=(12, 12))

ax = ax.flatten()

for i, col in enumerate(cols):
    sns.countplot(x=X[col], ax=ax[i])
    ax[i].set_title(f'Count Plot of {col}')

plt.tight_layout()
plt.show()

sns.pairplot(X)
plt.show()

X.columns

cols = ['age','trestbps','chol','thalach','oldpeak','ca']
fig,ax=plt.subplots(nrows=3,ncols=2,figsize=(12,12))
ax= ax.flatten()
for i,col in enumerate(cols):
  sns.histplot(x=X[col],ax=ax[i],kde = True)
  ax[i].set_title(f'Histogram of {col}')
plt.tight_layout()
plt.show()



cols = ['age','trestbps','chol','thalach','oldpeak','ca']
fig,ax = plt.subplots(nrows=3,ncols = 2, figsize=(12,12))
ax=ax.flatten()
for i,col in enumerate(cols):
  sns.boxplot(y=X[col],ax=ax[i])
  ax[i].set_title(f"Boxplot of {col}")
plt.tight_layout()
plt.show()

"""## **Remove Outlier**"""

trestbps_q1 = X['trestbps'].quantile(0.25)
trestbps_q3=X['trestbps'].quantile(0.75)
trestbps_iqr = trestbps_q3-trestbps_q1
trestbps_lower_bound = trestbps_q1-(1.5*trestbps_iqr)
trestbps_upper_bound=trestbps_q3+(1.5*trestbps_iqr)
X=X[(X['trestbps']>=trestbps_lower_bound) & (X['trestbps']<=trestbps_upper_bound)]


chol_q1 = X['chol'].quantile(0.25)
chol_q3=X['chol'].quantile(0.75)
chol_iqr = chol_q3-chol_q1
chol_lower_bound = chol_q1-(1.5*chol_iqr)
chol_upper_bound=chol_q3+(1.5*chol_iqr)
X=X[(X['chol']>=chol_lower_bound) & (X['chol']<=chol_upper_bound)]


thalach_q1 = X['thalach'].quantile(0.25)
thalach_q3=X['thalach'].quantile(0.75)
thalach_iqr = thalach_q3-thalach_q1
thalach_lower_bound = thalach_q1-(1.5*thalach_iqr)
thalach_upper_bound=thalach_q3+(1.5*thalach_iqr)
X=X[(X['thalach']>=thalach_lower_bound) & (X['thalach']<=thalach_upper_bound)]


oldpeak_q1 = X['oldpeak'].quantile(0.25)
oldpeak_q3=X['oldpeak'].quantile(0.75)
oldpeak_iqr = oldpeak_q3-oldpeak_q1
oldpeak_lower_bound = oldpeak_q1-(1.5*oldpeak_iqr)
oldpeak_upper_bound=oldpeak_q3+(1.5*oldpeak_iqr)
X=X[(X['oldpeak']>=oldpeak_lower_bound) & (X['oldpeak']<=oldpeak_upper_bound)]


cp_q1 = X['cp'].quantile(0.25)
cp_q3=X['cp'].quantile(0.75)
cp_iqr = cp_q3-cp_q1
cp_lower_bound = cp_q1-(1.5*cp_iqr)
cp_upper_bound=cp_q3+(1.5*cp_iqr)
X=X[(X['cp']>=cp_lower_bound) & (X['cp']<=cp_upper_bound)]

cols = ['age','trestbps','chol','thalach','oldpeak','ca']
fig,ax = plt.subplots(nrows=3,ncols = 2, figsize=(12,12))
ax=ax.flatten()
for i,col in enumerate(cols):
  sns.boxplot(y=X[col],ax=ax[i])
  ax[i].set_title(f"After removal of outlier Boxplot of {col}")
plt.tight_layout()
plt.show()

import numpy as np

X['oldpeak'] = np.log(X['oldpeak'] + 1)
X['chol'] = np.log(X['chol'] + 1)

X.isnull().sum()

"""## **feature Selection**"""

# Keep the indices where outliers were not removed
indices_to_keep = X.index

# Filter `y` based on the indices of the filtered `X`
y_filtered = y.loc[indices_to_keep]

# Now `X` and `y_filtered` should have the same number of samples
X_train, X_test, y_train, y_test = train_test_split(X, y_filtered, test_size=0.2, random_state=42)

# Check the shapes to confirm
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

"""## **Standardization**"""

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

"""## **Model**"""

models = [
    LogisticRegression(random_state=42),
    AdaBoostClassifier(random_state=11),
    DecisionTreeClassifier(),
    RandomForestClassifier(random_state=42,
        n_estimators=200,
        max_depth=15,
        min_samples_split=10,
        min_samples_leaf=4,
        bootstrap=True,
        max_features='sqrt'),
    GradientBoostingClassifier(random_state=20),
    GaussianNB(),
    SVC(),
]

for model in models:

    model.fit(X_train, y_train)


    train_preds = model.predict(X_train)
    test_preds = model.predict(X_test)

    # Accuracy
    train_acc = accuracy_score(y_train, train_preds)
    test_acc = accuracy_score(y_test, test_preds)

    # Print results
    print(f"{model.__class__.__name__}:")
    print(f"Train Accuracy: {train_acc:.4f}")
    print(f"Test Accuracy: {test_acc:.4f}")
    print("_" * 50)

