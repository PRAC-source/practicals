#importing the required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
#importing the dataset
df=pd.read_csv("uber.csv")
#importing the dataset
df=pd.read_csv("uber.csv")
#1 preprocess the dataset
df.head()
df.info()  #To get the required information of the dataset
df.columns  #TO get number of columns in the dataset 
df=df.drop(['Unnamed: 0','key'], axis= 1)
df.head()
df.shape  #To get the total (Rows,Columns)
df.dtypes #To get the type of each column
#Column pickup_datetime is in wrong format (Object). Convert it to DateTime Format
df.pickup_datetime=pd.to_datetime(df.pickup_datetime)
df.dtypes
#Filling the Missing Values
df.isnull().sum()
df['dropoff_latitude'].fillna(value=df['dropoff_latitude'].mean(),inplace=True)
df['dropoff_longitude'].fillna(value=df['dropoff_longitude'].median(),inplace=True)
df.isnull().sum()
 # To segregate each time of date and time
df= df.assign(hour = df.pickup_datetime.dt.hour, 
             day= df.pickup_datetime.dt.day, 
             month = df.pickup_datetime.dt.month, 
             year = df.pickup_datetime.dt.year, 
             dayofweek = df.pickup_datetime.dt.dayofweek) 
df.head()
# Here we are going to use Heversine formula to calculate the distance between two points and journey, using the longitude and latitude values
from math import * 
# function to calculate the travel distance from the longitudes and latitudes 
def distance_transform(longitude1, latitude1, longitude2, latitude2): 
    travel_dist = [] 
     
    for pos in range(len(longitude1)): 
        long1,lati1,long2,lati2 = map(radians,[longitude1[pos],latitude1[pos],longitude2[pos],latitude2[pos]]) 
        dist_long = long2 - long1 
        dist_lati = lati2 - lati1 
        a = sin(dist_lati/2)**2 + cos(lati1) * cos(lati2) * sin(dist_long/2)**2 
        c = 2 * asin(sqrt(a))*6371 
        travel_dist.append(c) 
        
    return travel_dist 

df['dist_travel_km'] = distance_transform(df['pickup_longitude'].to_numpy(),
                                                df['pickup_latitude'].to_numpy(), 
                                                df['dropoff_longitude'].to_numpy(), 
                                                df['dropoff_latitude'].to_numpy() 
                                              )
df.head()
df.head()
# Checking outliers and filling them
df.plot(kind = "box",subplots = True,layout = (7,2),figsize=(15,20))
#  #Using the InterQuartile Range to fill the values
def remove_outlier(df1 , col): 
    Q1 = df1[col].quantile(0.25) 
    Q3 = df1[col].quantile(0.75) 
    IQR = Q3 - Q1 
    lower_whisker = Q1-1.5*IQR 
    upper_whisker = Q3+1.5*IQR 
    df[col] = np.clip(df1[col] , lower_whisker , upper_whisker) 
    return df1 
 
def treat_outliers_all(df1 , col_list): 
    for c in col_list: 
        df1 = remove_outlier(df , c) 
    return df1
df = treat_outliers_all(df , df.iloc[: , 0::])
 df.plot(kind = "box",subplots = True,layout = (7,2),figsize=(15,20))
 #Uber doesn't travel over 130 kms so minimize the distance  
df= df.loc[(df.dist_travel_km >= 1) | (df.dist_travel_km <= 130)] 
print("Remaining observastions in the dataset:", df.shape)
 #Finding inccorect latitude (Less than or greater than 90) and longitude (greater than or less than 180) 
incorrect_coordinates = df.loc[(df.pickup_latitude > 90) |(df.pickup_latitude < -90) | 
                                   (df.dropoff_latitude > 90) |(df.dropoff_latitude < -90) | 
                                   (df.pickup_longitude > 180) |(df.pickup_longitude < -180) | 
                                   (df.dropoff_longitude > 90) |(df.dropoff_longitude < -90) 
                                    ]


 df.drop(incorrect_coordinates, inplace = True, errors = 'ignore') 
  df.head() 
  df.isnull().sum() 
  sn.heatmap(df.isnull()) #Free for null values 
  corr = df.corr() #Function to find the correlation 
  corr
   fig,axis = plt.subplots(figsize = (10,6)) 
sn.heatmap(df.corr(),annot = True) #Correlation Heatmap (Light values means highly correlated) 
# Dividing the dataset into feature and target values
x = df[['pickup_longitude','pickup_latitude','dropoff_longitude','dropoff_latitude','passenger_count','hour','day','month','year','dayofweek','dist_travel_km']] 
y = df['fare_amount'] 
# Dividing the dataset into training and testing dataset
from sklearn.model_selection import train_test_split 
X_train,X_test,y_train,y_test = train_test_split(x,y,test_size = 0.33) 
# Linear Regression
from sklearn.linear_model import LinearRegression 
regression = LinearRegression()
regression.fit(X_train,y_train) 
regression.intercept_ #To find the linear intercept 
regression.coef_ #To find the linear coeeficient 
prediction = regression.predict(X_test) #To predict the target values 
print(prediction)
y_test 
# Metrics Evaluation using R2, Mean Squared Error, Root Mean Sqared Error
from sklearn.metrics import r2_score  
r2_score(y_test,prediction)
 from sklearn.metrics import mean_squared_error
 MSE = mean_squared_error(y_test,prediction) 
MSE
RMSE = np.sqrt(MSE)
RMSE
# random forest regression
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor(n_estimators=100) #Here n_estimators means number of trees you want to build before making the prediction
rf.fit(X_train,y_train)
y_pred = rf.predict(X_test) 
y_pred
# Metrics evaluatin for Random Forest
R2_Random = r2_score(y_test,y_pred) 
R2_Random

 MSE_Random = mean_squared_error(y_test,y_pred) 
MSE_Random 
RMSE_Random = np.sqrt(MSE_Random) 
RMSE_Random

