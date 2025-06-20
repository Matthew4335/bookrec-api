from fastapi import FastAPI
import pandas as pd
import numpy as np
from recommender import recommend_books

app = FastAPI()
df = pd.read_csv("../data/cleaned_books.csv")
sim_matrix = np.load("../models/semantic_sim_matrix.npy")

@app.get("/recommend")
def recommend(title: str, top_n: int = 5):
    return recommend_books(title, df, sim_matrix)