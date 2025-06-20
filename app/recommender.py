import re
from rapidfuzz import fuzz, process

def extract_series_name(title):
    """Extracts the series name from a title like 'Book Title (Series Name, #2)'."""
    match = re.search(r'\(([^,]+),\s?#\d+\)', title)
    if match:
        return match.group(1).strip().lower()
    return None

def recommend_books(user_input_title, df, sim_matrix, top_n=5, score_threshold=60):
    titles = df['title'].tolist()
    best_match = process.extractOne(user_input_title, titles, scorer=fuzz.token_set_ratio)

    if best_match is None or best_match[1] < score_threshold:
        return [f"No close match found for: '{user_input_title}'"]

    matched_title = best_match[0]
    print(f"Best match: {matched_title}")
    idx = df[df['title'] == matched_title].index[0]
    original_series = extract_series_name(matched_title)

    sim_scores = list(enumerate(sim_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    exclusion_keywords = ['boxset', 'box set', 'guide', 'parody', 'authors on', 'world of']
    recommendations = []

    for i in sim_scores:
        candidate_title = df.iloc[i[0]]['title']
        if candidate_title == matched_title:
            continue
        if any(kw in candidate_title.lower() for kw in exclusion_keywords):
            continue
        if original_series and extract_series_name(candidate_title) == original_series:
            continue

        recommendations.append(candidate_title)
        if len(recommendations) == top_n:
            break

    return recommendations