# 🎬 CineMatch AI – Intelligent Movie Recommendation System

A content-based Movie Recommendation System built using **Python, Machine Learning, NLP, and Streamlit**. The application recommends movies similar to the one selected by the user and displays their posters using the TMDB API.

---


## 🚀 Live Demo

**Streamlit App:** *https://raqrnhctz2woajjprgtnon.streamlit.app/*

---

## 📌 Features

* 🎥 Recommend Top 5 similar movies
* 🖼️ Display movie posters using TMDB API
* 🔍 Search and select movies from a dropdown
* ⚡ Fast recommendations using precomputed cosine similarity
* 🌐 Interactive web interface built with Streamlit

---

## 🛠️ Tech Stack

* Python
* Pandas
* NumPy
* Scikit-learn
* Natural Language Processing (NLP)
* CountVectorizer (Bag of Words)
* Cosine Similarity
* Streamlit
* TMDB API
* Pickle

---

## 📂 Dataset

Dataset Source:

* TMDB Movie Metadata
* TMDB Credits Dataset

Downloaded using:

```python
import kagglehub

path = kagglehub.dataset_download("tmdb/tmdb-movie-metadata")
```

---

## 🧠 How It Works

1. Merge movie and credits datasets.
2. Select important features:

   * Overview
   * Genres
   * Keywords
   * Cast
   * Director
3. Clean and preprocess the text.
4. Combine all features into a single **tags** column.
5. Apply **CountVectorizer** to convert text into numerical vectors.
6. Compute similarity using **Cosine Similarity**.
7. Recommend the top 5 most similar movies.
8. Fetch movie posters using the TMDB API.

---

## 📁 Project Structure

```
Movie-Recommendation-System/
│
├── app.py
├── MOVIE RECOMMENDER.ipynb
├── movie_list.pkl
├── similarity.pkl
├── requirements.txt
├── README.md
├── .gitignore
├── .env                 # Not uploaded to GitHub
```

---


## 📊 Machine Learning Pipeline

* Data Collection
* Data Cleaning
* Feature Engineering
* Text Preprocessing
* Bag of Words (CountVectorizer)
* Cosine Similarity
* Recommendation Engine
* Streamlit Deployment

---

## 📚 Concepts Used

* Content-Based Recommendation System
* Natural Language Processing
* Bag of Words
* CountVectorizer
* Cosine Similarity
* Feature Engineering
* Pickle Serialization
* REST API Integration

---

## 📦 Requirements

```
streamlit
pandas
numpy
scikit-learn
requests
python-dotenv
```

---

## 🌟 Future Improvements

* Search by actor or director
* Hybrid recommendation system
* Genre-based filtering
* Movie ratings integration
* User authentication
* Personalized recommendations
* IMDb and trailer integration
* Recommendation history
* Responsive UI improvements

---

## 👨‍💻 Author

**Abhideepta**

MCA Student | Machine Learning | Data Science | AI Enthusiast

LinkedIn: https://www.linkedin.com/in/abhideepta-mishra-557249244/

---

## ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.
*

---

## 📌 Features

* 🎥 Recommend Top 5 similar movies
* 🖼️ Display movie posters using TMDB API
* 🔍 Search and select movies from a dropdown
* ⚡ Fast recommendations using precomputed cosine similarity
* 🌐 Interactive web interface built with Streamlit

---

## 🛠️ Tech Stack

* Python
* Pandas
* NumPy
* Scikit-learn
* Natural Language Processing (NLP)
* CountVectorizer (Bag of Words)
* Cosine Similarity
* Streamlit
* TMDB API
* Pickle

---

## 📂 Dataset

Dataset Source:

* TMDB Movie Metadata
* TMDB Credits Dataset

Downloaded using:

```python
import kagglehub

path = kagglehub.dataset_download("tmdb/tmdb-movie-metadata")
```

---

## 🧠 How It Works

1. Merge movie and credits datasets.
2. Select important features:

   * Overview
   * Genres
   * Keywords
   * Cast
   * Director
3. Clean and preprocess the text.
4. Combine all features into a single **tags** column.
5. Apply **CountVectorizer** to convert text into numerical vectors.
6. Compute similarity using **Cosine Similarity**.
7. Recommend the top 5 most similar movies.
8. Fetch movie posters using the TMDB API.

---

## 📁 Project Structure

```
Movie-Recommendation-System/
│
├── app.py
├── MOVIE RECOMMENDER.ipynb
├── movie_list.pkl
├── requirements.txt
├── README.md
├── .gitignore
├── .env                 # Not uploaded to GitHub
```

---


## 📊 Machine Learning Pipeline

* Data Collection
* Data Cleaning
* Feature Engineering
* Text Preprocessing
* Bag of Words (CountVectorizer)
* Cosine Similarity
* Recommendation Engine
* Streamlit Deployment

---

## 📚 Concepts Used

* Content-Based Recommendation System
* Natural Language Processing
* Bag of Words
* CountVectorizer
* Cosine Similarity
* Feature Engineering
* Pickle Serialization
* REST API Integration

---

## 📦 Requirements

```
streamlit
pandas
numpy
scikit-learn
requests
python-dotenv
```

---

## 🌟 Future Improvements

* Search by actor or director
* Hybrid recommendation system
* Genre-based filtering
* Movie ratings integration
* User authentication
* Personalized recommendations
* IMDb and trailer integration
* Recommendation history
* Responsive UI improvements

---

## 👨‍💻 Author

**Abhideepta**

MCA Student | Machine Learning | Data Science | AI Enthusiast

LinkedIn: https://www.linkedin.com/in/abhideepta-mishra-557249244/

---

## ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.
