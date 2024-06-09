import pandas as pd

#In this exercise, we're going to create a program that allows us do
#cross-cultural cinematic research. A tool that prints the percentage of movie
#descriptions containing a certain word (scraped from Wikipedia),
#for different cultures. First we will practice a little with Pandas.
#Then, follow the steps to create the program.
#As a challenge, you can also ignore these steps and code it without help.
#1. First, download the movie_plots.csv file from Canvas and open it
#2. Let's inspect the data. Display the first rows and get the summary (.info)

movies = pd.read_csv("movie_plots-1.csv")

print(movies.head(1))

print(movies.info)


#3. Print out the number of movies for each Origin/Ethnicity
print(movies["Origin/Ethnicity"].value_counts())

#4. Subsetting: select only the rows with Bollywood movies
Bollywood_movies = movies[movies["Origin/Ethnicity"] == "Bollywood"]

#5. Subsetting: select only the rows with Turkish movies released after 2000
Turkish_movies = movies[movies["Origin/Ethnicity"] == "Turkish"]

Turkish_movies_2000plus = Turkish_movies[Turkish_movies["Release Year"] > 2000]

#6. Subsetting: create a new df with only Title, Release Year, Origin/Ethnicity, Plot
new_df = movies[["Title", "Release Year",  "Origin/Ethnicity", "Plot"]]

#7. Change the column names to Title, Year, Origin, Plot. Find online how to this.
renamed_new_df = new_df.rename(columns = {'Title':'Title','Release Year':'Year','Origin/Ethnicity':'Origin','Plot':'Plot'}) 




##This is where the basic section ends.##




##Advanced section: for a more challenging assignment, try (some of) the steps below##
#8. Create a new column "kimono" that is True if the Plot contains the word
"kimono"
#and false if not (tip: find a suitable Pandas string method).
#Tip: use Pandas .astype(int) to convert the resulting Boolean in 0 or 1.
#9. Using your new column, pd.groupby() and another Pandas function, count the number of movies
#with "kimono" in the plot, for the different origins.
#10. Using your earlier code, create a function add_word_present() with one argument (word),
#that adds a column df[word] with a 1 if the word occurs in the plot,
#and 0 if not.
#Extra challenge: make sure that it's not counted if it's inside another word.
#11. Write another function compare_origins() with one argument (word), that:
#1. adds a column to your data frame (simply call your earlier function)
#2. prints the proportion of movies for different origins containing that word
#12. We need one more tweak: to really compare different cultures,
#we need to account for the fact that the total number of movies is not the same.
#Write another, better function that calculates a percentage rather than a count.
#Hint: note that df.groupby(["Origin"])[word].count() will get you the number of movies, grouped by origin.
#Also sort the result so that the percentage is descending.
#Finally, make it user-friendly: print the word and what the numbers mean
#You're done! Try out your function and paste your most interesting result
#as a comment
