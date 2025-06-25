import pandas as pd
# from sklearn.neighbors import NearestNeighbors
import pickle
import os
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

    ctr_df = calculate_ctr(log_path=os.path.join(BASE_DIR, "logs"))
    products_df = products_df.merge(ctr_df, on="product_id", how="left")
    products_df["ctr"] = products_df["ctr"].fillna(0.0)
    

    # Multiply category scores by CTR so more engaging products get higher influence
    interactions = interactions.merge(products_df, left_on='pro_id', right_on='product_id')
    interactions['ctr'] = interactions['ctr'].fillna(0.0)
    interactions['weighted_score'] = interactions['weight'] * (1 + interactions['ctr'])  # scale by CTR

    user_category_scores = interactions.groupby(['user_id', 'category'])['weighted_score'].sum().reset_index()
    return user_category_scores



def calculate_ctr(log_path="logs"):
    rec_log = pd.read_csv(os.path.join(log_path, "recommendation_logs.csv"), header=None)
    rec_log.columns = ['timestamp', 'user_id', 'product_id', 'title', 'category', 'action']

    click_log = pd.read_csv(os.path.join(log_path, "click_logs.csv"), header=None)
    click_log.columns = ['timestamp', 'user_id', 'product_id', 'title', 'category', 'action']

    

    total_recs = rec_log.groupby("product_id").size()
    total_clicks = click_log.groupby("product_id").size()

    ctr_df = (total_clicks / total_recs).fillna(0).reset_index()
    ctr_df.columns = ["product_id", "ctr"]

    return ctr_df



# def train_recommender(user_category_scores):
#     user_cat_matrix = user_category_scores.pivot(index='user_id', columns='category', values='weighted_score').fillna(0)
#     model = NearestNeighbors(metric='cosine', algorithm='brute')
#     model.fit(user_cat_matrix.values)
#     return model, user_cat_matrix

def train_faiss_ivf_index(user_category_scores, nlist=100, nprobe=10):
    user_cat_matrix = user_category_scores.pivot(index='user_id', columns='category', values='weighted_score').fillna(0)
    user_vectors = user_cat_matrix.values.astype('float32')
    faiss.normalize_L2(user_vectors)

    d = user_vectors.shape[1]
    quantizer = faiss.IndexFlatIP(d)
    index = faiss.IndexIVFFlat(quantizer, d, nlist, faiss.METRIC_INNER_PRODUCT)
    index.train(user_vectors)
    index.add(user_vectors)
    index.nprobe = nprobe  

    return index, user_cat_matrix


user_category_scores = create_user_category_scores(viewed_df, wishlist_df, cart_df, purchase_df, products_df)
index, user_cat_matrix = train_faiss_ivf_index(user_category_scores)

# Save FAISS IVF index
faiss.write_index(index, os.path.join(BASE_DIR, "model_faiss_ivf.index"))

# Save user index mappings
with open(os.path.join(BASE_DIR, "user_matrix.pkl"), "wb") as f:
    pickle.dump(user_cat_matrix, f)

with open(os.path.join(BASE_DIR, "user_index_map.pkl"), "wb") as f:
    pickle.dump(user_cat_matrix.index.tolist(), f)






# with open(os.path.join(BASE_DIR, "model_knn.pkl"), "wb") as f:
#     pickle.dump(model, f)

# with open(os.path.join(BASE_DIR, "user_matrix.pkl"), "wb") as f:
#     pickle.dump(user_cat_matrix, f)










