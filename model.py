import pandas as pd
from sklearn.neighbors import NearestNeighbors
import pickle
import os


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

def create_user_category_scores(viewed_df, wishlist_df, cart_df, purchase_df, products_df):
    weights = {'viewed': 1, 'wishlist': 2, 'cart': 3, 'purchase': 4}
    all_data = []

    for name, df in [('viewed', viewed_df), ('wishlist', wishlist_df), 
                     ('cart', cart_df), ('purchase', purchase_df)]:
        df = df.copy()
        df['interaction_type'] = name
        df['weight'] = weights[name]
        all_data.append(df[['user_id', 'pro_id', 'weight']])

    interactions = pd.concat(all_data)
    interactions = interactions.merge(products_df, left_on='pro_id', right_on='product_id')

    user_category_scores = interactions.groupby(['user_id', 'category'])['weight'].sum().reset_index()
    return user_category_scores

def train_recommender(user_category_scores):
    user_cat_matrix = user_category_scores.pivot(index='user_id', columns='category', values='weight').fillna(0)
    model = NearestNeighbors(metric='cosine', algorithm='brute')
    model.fit(user_cat_matrix.values)
    return model, user_cat_matrix





user_category_scores = create_user_category_scores(viewed_df, wishlist_df, cart_df, purchase_df, products_df)

model, user_cat_matrix = train_recommender(user_category_scores)



with open(os.path.join(BASE_DIR, "model_knn.pkl"), "wb") as f:
    pickle.dump(model, f)


with open(os.path.join(BASE_DIR, "user_matrix.pkl"), "wb") as f:
    pickle.dump(user_cat_matrix, f)






