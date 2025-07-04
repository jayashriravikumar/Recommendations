import os
import pandas as pd
import pickle
import faiss


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

products_df = pd.read_csv(os.path.join(BASE_DIR, "Products.csv"))
categories_df = pd.read_csv(os.path.join(BASE_DIR, "category.csv"))
viewed_df = pd.read_csv(os.path.join(BASE_DIR, "viewed.csv"))
wishlist_df = pd.read_csv(os.path.join(BASE_DIR, "wishlist.csv"))
cart_df = pd.read_csv(os.path.join(BASE_DIR, "cart_table.csv"))
purchase_df = pd.read_csv(os.path.join(BASE_DIR, "purchase.csv"))


products_df = products_df.merge(categories_df, left_on='single_category', right_on='id', suffixes=('_product', '_category'))
products_df = products_df[['id_product', 'title', 'category']]
products_df.columns = ['product_id', 'title', 'category']

# with open(os.path.join(BASE_DIR, "model_knn.pkl"), "rb") as f:
#     model = pickle.load(f)

# with open(os.path.join(BASE_DIR, "user_matrix.pkl"), "rb") as f:
#    user_cat_matrix = pickle.load(f)

# Load FAISS IVF index
index = faiss.read_index(os.path.join(BASE_DIR, "model_faiss_ivf.index"))

# Set nprobe (must match model.py or can be tuned per request)
index.nprobe = 10  # higher = better accuracy, lower = faster

# Load user matrix and ID mappings
with open(os.path.join(BASE_DIR, "user_matrix.pkl"), "rb") as f:
    user_cat_matrix = pickle.load(f)

with open(os.path.join(BASE_DIR, "user_index_map.pkl"), "rb") as f:
    user_index_map = pickle.load(f)


# def recommend_from_model(user_id):
#     if user_id not in user_cat_matrix.index:
#         return []

#     user_vector = user_cat_matrix.loc[user_id].values.reshape(1, -1)
#     distances, indices = model.kneighbors(user_vector, n_neighbors=5)
#     similar_users = user_cat_matrix.index[indices.flatten()].tolist()
#     similar_user_scores = user_cat_matrix.loc[similar_users].mean().sort_values(ascending=False)
#     top_categories = similar_user_scores.head(3).index.tolist()

#     user_product_ids = set(
#         viewed_df[viewed_df['user_id'] == user_id]['pro_id'].tolist() +
#         wishlist_df[wishlist_df['user_id'] == user_id]['pro_id'].tolist() +
#         cart_df[cart_df['user_id'] == user_id]['pro_id'].tolist() +
#         purchase_df[purchase_df['user_id'] == user_id]['pro_id'].tolist()
#     )

#     recommendations = products_df[
#         (products_df['category'].isin(top_categories)) &
#         (~products_df['product_id'].isin(user_product_ids))
#     ]

#     # Optional: rank by popularity using purchase count (if available)
#     popularity = purchase_df.groupby('pro_id').size().reset_index(name='popularity')
#     recommendations = recommendations.merge(popularity, how='left', left_on='product_id', right_on='pro_id')
#     recommendations['popularity'] = recommendations['popularity'].fillna(0)

#     # Sort by popularity (descending), then by product_id (ascending)
#     recommendations = recommendations.sort_values(by=['popularity', 'product_id'], ascending=[False, True])

#     return recommendations.head(10)[['product_id', 'title', 'category']].to_dict(orient='records')

def recommend_from_model(user_id):
    if user_id not in user_cat_matrix.index:
        return []

    # Get and normalize user's vector
    user_vector = user_cat_matrix.loc[user_id].values.astype('float32').reshape(1, -1)
    faiss.normalize_L2(user_vector)

    # Search for nearest neighbors
    D, I = index.search(user_vector, k=5)

    # Convert indices to user IDs
    similar_users = [user_index_map[i] for i in I.flatten() if i < len(user_index_map)]

    # Average their category preferences
    similar_user_scores = user_cat_matrix.loc[similar_users].mean().sort_values(ascending=False)
    top_categories = similar_user_scores.head(3).index.tolist()

    # Gather user's seen products
    user_product_ids = set(
        viewed_df[viewed_df['user_id'] == user_id]['pro_id'].tolist() +
        wishlist_df[wishlist_df['user_id'] == user_id]['pro_id'].tolist() +
        cart_df[cart_df['user_id'] == user_id]['pro_id'].tolist() +
        purchase_df[purchase_df['user_id'] == user_id]['pro_id'].tolist()
    )

    # Filter products in top categories and not seen by user
    recommendations = products_df[
        (products_df['category'].isin(top_categories)) &
        (~products_df['product_id'].isin(user_product_ids))
    ]

    # Rank by purchase popularity
    popularity = purchase_df.groupby('pro_id').size().reset_index(name='popularity')
    recommendations = recommendations.merge(popularity, how='left', left_on='product_id', right_on='pro_id')
    recommendations['popularity'] = recommendations['popularity'].fillna(0)
    recommendations = recommendations.sort_values(by=['popularity', 'product_id'], ascending=[False, True])

    return recommendations.head(10)[['product_id', 'title', 'category']].to_dict(orient='records')
