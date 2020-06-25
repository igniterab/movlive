from django.shortcuts import render


import pandas as pd
import numpy as np


user_ratings = pd.read_csv("C:\\Users\\Ashish Bhardwaj\\Desktop\\m\\movie\\movie\\ratings.csv")
tags = pd.read_csv("C:\\Users\\Ashish Bhardwaj\\Desktop\\m\\movie\\movie\\tags.csv")
movies_title = pd.read_csv("C:\\Users\\Ashish Bhardwaj\\Desktop\\m\\movie\\movie\\movies.csv")
#Using regular expressions to find a year stored between parentheses
#We specify the parantheses so we don't conflict with movies that have years in their titles
movies_title['year'] = movies_title.title.str.extract('(\(\d\d\d\d\))',expand=False)
#Removing the parentheses
movies_title['year'] = movies_title.year.str.extract('(\d\d\d\d)',expand=False)
#Removing the years from the 'title' column
movies_title['title'] = movies_title.title.str.replace('(\(\d\d\d\d\))', '')
#Applying the strip function to get rid of any ending whitespace characters that may have appeared
movies_title['title'] = movies_title['title'].apply(lambda x: x.strip())

links = pd.read_csv("C:\\Users\\Ashish Bhardwaj\\Desktop\\m\\movie\\movie\\links.csv")
df = pd.merge(user_ratings , movies_title , on="movieId")

#sns.set_style = 'white' #this will give me a white background
df.groupby('title')['rating'].mean().sort_values(ascending=False)
ratings = pd.DataFrame(df.groupby('title')['rating'].mean())
ratings['No. of rating'] = pd.DataFrame(df.groupby('title')['rating'].count())
movie_mat = df.pivot_table(index="userId",columns='title',values='rating')




def home(request):
    return render(request,'index.html')

def check(request):
    text_name = request.POST.get('text','default')
    movie_name = text_name
    movie_name_user_ratings = movie_mat[movie_name]
    similar_to_movie_name = movie_mat.corrwith(movie_name_user_ratings)
    corr_movie_name = pd.DataFrame(similar_to_movie_name,columns=['corelation'])
    corr_movie_name.dropna(inplace=True)
    corr_movie_name = corr_movie_name.join(ratings['No. of rating'])
    a = pd.DataFrame(corr_movie_name[corr_movie_name['No. of rating']>100].sort_values('corelation',ascending=False).head())
    b = list(a.index[0:5])

    punct = {"data":text_name,'a':b[0],'b':b[1],'c':b[2],'d':b[3],'e':b[4]}
       
    return render(request,'movie.html',punct)



