# all data print
import streamlit as st
import pickle
import pandas as pd
import requests
import gzip

# Load data and similarity
with gzip.open('movies_dict_compressed.pkl.gz', 'rb') as f:
    movie_list = pickle.load(f)

with gzip.open('similarity_compressed.pkl.gz', 'rb') as f:
    similarity = pickle.load(f)


# Convert the movie dictionary to a pandas DataFrame
movies = pd.DataFrame(movie_list)

# Function to fetch movie poster from the API
def fetch_poster(movie_id):
    # API call to fetch movie data
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US")
    data = response.json()
    # Return the URL of the movie poster
    return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"

# Function to recommend movies based on the selected movie
def recommend(selected_movie):
    # Get the index of the selected movie
    movie_index = movies[movies['title'] == selected_movie].index[0]
    # Get the similarity scores for the selected movie
    similarity_scores = list(enumerate(similarity[movie_index]))
    # Sort the movies based on similarity scores
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    # Get the indices of the recommended movies
    recommended_indices = [i[0] for i in similarity_scores[1:6]]
    # Get the names and posters of the recommended movies
    recommended_movie_names = movies.iloc[recommended_indices]['title'].values
    recommended_movie_posters = [fetch_poster(movies.iloc[i]['id']) for i in recommended_indices]
    return recommended_movie_names, recommended_movie_posters

# Inject custom CSS code into the Streamlit app
st.markdown("""
    <style>
    .ea3mdgi5 {
        width: 100%;
        padding: 6rem 1rem 10rem;
        max-width: 100%;
            margin-top:20px;
    } .st-emotion-cache-ocqkz7 {
            margin-top:20px;
    }
    </style>
           
    
    """, unsafe_allow_html=True)

col1, col2 = st.columns([1, 6]) 

col1.markdown("<h2 style='color:red; text-align:center'>ND FILMS</h2>", unsafe_allow_html=True)

# Display a search box in the right column
selected_movie = st.selectbox("Type or select a movie from the dropdown", movies['title'].values)

# Flag to track whether the button has been clicked
show_recommendations = False

# Button to show recommendations
if st.button('Show Recommendation'):
    show_recommendations = True
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

# Define the number of columns you want to display in a row for the movies
num_columns = 7

# Iterate over the movies dataset and display them side by side
if show_recommendations:
    # Display recommended movies
    st.write("Recommended Movies:")
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(recommended_movie_names[0]  )
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
        print(movies['title'])
        st.markdown(
        f"<div style='font-size: 15px; margin-bottom:12px; background-color: red; padding: 5px; border-radius: 5px; text-align: center;color:white; justify-content:center; display:flex; align-items: center;margin:auto'>{recommended_movie_names}</div>",
        unsafe_allow_html=True      
    )
       
else:
    # Display all movies
    for index, movie in movies.iterrows():
        # Determine which column to use for the current movie
        if index % num_columns == 0:
            columns = st.columns(num_columns)

        col = columns[index % num_columns]

        poster_url = fetch_poster(movie['id'])
        col.image(poster_url, width=None, use_column_width=True ,)

      

        col.markdown(
        f"<div style='font-size: 15px; margin-bottom:12px; background-color: red; padding: 5px; border-radius: 5px; text-align: center;color:white; height:58px; justify-content:center; display:flex; align-items: center;margin:auto'>{movie['title']}</div>",
        unsafe_allow_html=True      
    )
        
 
     