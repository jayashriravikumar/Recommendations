import pandas as pd

products_df = pd.read_csv("D:\\Recommendations\\Products.csv")
categories_df = pd.read_csv("D:\\Recommendations\\category.csv")
viewed_df = pd.read_csv(r"D:\\Recommendations\\viewed.csv")
wishlist_df = pd.read_csv("D:\\Recommendations\\wishlist.csv")
cart_df = pd.read_csv("D:\\Recommendations\\cart_table.csv")
purchase_df = pd.read_csv("D:\\Recommendations\\purchase.csv")

products_df = products_df.merge(categories_df, left_on='single_category', right_on='id', suffixes=('_product', '_category'))
products_df = products_df[['id_product', 'title', 'category']]  
products_df.columns = ['product_id', 'title', 'category']

def recommend_products(user_id, products_df, viewed_df, wishlist_df, cart_df, purchase_df):

    weights = {
        'viewed': 1,
        'wishlist': 2,
        'cart': 3,
        'purchase': 4
    }

    category_scores = {}


    def update_scores(df, user_id, weight):
        user_prods = df[df['user_id'] == user_id]['pro_id'].tolist()
        for pid in user_prods:
            category = products_df[products_df['product_id'] == pid]['category'].values
            if len(category) == 0:
                continue
            category = category[0]
            category_scores[category] = category_scores.get(category, 0) + weight

    update_scores(viewed_df, user_id, weights['viewed'])
    update_scores(wishlist_df, user_id, weights['wishlist'])
    update_scores(cart_df, user_id, weights['cart'])
    update_scores(purchase_df, user_id, weights['purchase'])

    sorted_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
    top_categories = [cat for cat, score in sorted_categories]

    user_product_ids = set(
        viewed_df[viewed_df['user_id'] == user_id]['pro_id'].tolist() +
        wishlist_df[wishlist_df['user_id'] == user_id]['pro_id'].tolist() +
        cart_df[cart_df['user_id'] == user_id]['pro_id'].tolist() +
        purchase_df[purchase_df['user_id'] == user_id]['pro_id'].tolist()
    )

    recommendations = products_df[
        (products_df['category'].isin(top_categories)) &
        (~products_df['product_id'].isin(user_product_ids))
    ]

    return recommendations.sample(n=min(10, len(recommendations)))

user_id = int(input("Enter user id:"))
recs = recommend_products(user_id, products_df, viewed_df, wishlist_df, cart_df, purchase_df)


print(f"Recommendations for user {user_id}:\n")
for _, row in recs.iterrows():
    print(f" - {row['title']} ({row['category']})")
