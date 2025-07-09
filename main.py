from fastapi import FastAPI, Query
from recommender import recommend_books
import pandas as pd
import numpy as np

app = FastAPI()

df = pd.read_csv("data/cleaned_books.csv")
sim_matrix = np.load("models/semantic_sim_matrix.npy")

@app.get("/")
def root():
    return {"message": "Welcome to the BookRec API"}

@app.get("/recommend")
def recommend(title: str = Query(..., description="Book title to base recommendations on")):
    results = recommend_books(title, df, sim_matrix)
    return {"input": title, "recommendations": results}