import tkinter as tk
from tkinter import ttk
from tkinter import Canvas
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import ImageTk,Image


window= tk.Tk()
window.title=("Movierecommendationsystem")
window.geometry('600x400')
window.configure(bg='grey')

# creating label for first name

Movie_label = ttk.Label(window, text="Please Enter the  Movie Name                    ")
#Movie_label.grid(row=600, column=200)
Movie_label.place(relx = 0.4,
                   rely = 0.4,
                   anchor = 'center')

# entry box
m_var = tk.StringVar()
m_entrybox = ttk.Entry(window, width=30, textvariable=m_var)
#m_entrybox.grid(row=600, column=201)
m_entrybox.place(relx = 0.7,
                   rely = 0.4,
                   anchor = 'center')

m_entrybox.focus()


# define a function that creates similarity matrix
# if it doesn't exist

def create_sim():
    data = pd.read_csv('main_data.csv')
    # creating a count matrix
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(data['comb'])
    # creating a similarity score matrix
    sim = cosine_similarity(count_matrix)
    return data,sim

def action1():
    movie= m_var.get()
    m = movie.lower()
    data, sim = create_sim()
    # check if the movie is in our database or not
    if m not in data['movie_title'].unique():
        msg = tk.Message(window, text="Movie is not Present in our data base. \n Or please check your spelling ")
        msg.config(bg='lightgrey', font=('times', 9, 'italic'),borderwidth=25,aspect=1800,fg='black')
        msg.grid(row=18, column=1, columnspan=1, rowspan=5)
        msg.place(relx=0.5,
                         rely=0.7,
                         anchor='center')
    else:
        # getting the index of the movie in the dataframe
        i = data.loc[data['movie_title'] == m].index[0]
        print(i)
        # fetching the row containing similarity scores of the movie
        # from similarity matrix and enumerate it
        lst = list(enumerate(sim[i]))
        #print(lst)

        # sorting this list in decreasing order based on the similarity score
        lst = sorted(lst, key=lambda x: x[1], reverse=True)
        #print(lst)


        # not taking the first index since it is the same movie
        lst = lst[1:11]

        # making an empty list that will containg all 10 movie recommendations
        l_movie = []
        for i in range(len(lst)):
            a = lst[i][0]
            l_movie.append(data['movie_title'][a])
            #print(l_movie)
        openNewWindow(l_movie)
"""  for i in range(len(l_movie)):
            msg = tk.Message(window, text= l_movie[i])
            msg.config(bg='lightgrey', font=('times', 9, 'italic'), borderwidth=0,aspect=1800,fg='black')
            #msg.grid(row=18+i, column=1)
            msg.place(relx=0.5/i,
                      rely=0.6)
        #return l_movie

"""
def openNewWindow(l_movie):
    newWindow = tk.Tk()
    newWindow.title("New Window")
    newWindow.geometry("600x400")
    newWindow.configure(bg='grey')
    ne_label = ttk.Label(newWindow, text="Recommended movies for YOU... ENJOY")
    ne_label.grid(row=6, column=8)

    for i in range(len(l_movie)):
        msg = tk.Message(newWindow , text=l_movie[i])
        msg.config(bg='lightgrey', font=('times', 9, 'italic'), borderwidth=2, aspect=1800, fg='black')
        msg.grid(row=18+i, column=8)

first_button= ttk.Button(window, text='Search', command= action1)
first_button.grid(row=2500, column=2)
first_button.place(relx = 0.5,
                   rely = 0.5,

                   anchor = 'center')
window.mainloop()



