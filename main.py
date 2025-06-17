import pandas as pd
import random

categories = {
    'Aromatherapy': ['Incense Sticks', 'Essential Oils', 'Scented Candles'],
    'Meditation': ['Meditation Cushion', 'Mantra Cards'],
    'Accessories': ['Prayer Beads', 'Crystal Pendant'],
    'Healing': ['Himalayan Salt Lamp', 'Chakra Stones Set'],
    'Sound Therapy': ['Tibetan Singing Bowl'],
    'Books': ['Spiritual Books'],
    'Yoga': ['Yoga Mat', 'Yoga Strap']
}

products = []
for cat, items in categories.items():
    for item in items:
        products.append({'product': item, 'category': cat})


users = [f'user_{i}' for i in range(1, 7)]

data = []
for user in users:
    wishlist = random.sample(products, 3)
    cart = random.sample(products, 2)
    viewed = random.sample(products, 3)
    last_purchase = random.choice(products)
    data.append({
        'user': user,
        'wishlist': wishlist,
        'cart': cart,
        'recently_viewed': viewed,
        'last_purchase': last_purchase
    })

df = pd.DataFrame(data)
print(df.head())

def recommend_products(user_data, all_products):
   
    interested_categories = set(
        item['category'] for section in ['wishlist', 'cart', 'recently_viewed', 'last_purchase']
        for item in (user_data[section] if isinstance(user_data[section], list) else [user_data[section]])
    )
    

    seen_items = set(item['product'] for section in ['wishlist', 'cart', 'recently_viewed', 'last_purchase']
                     for item in (user_data[section] if isinstance(user_data[section], list) else [user_data[section]]))
    
    recommendations = [p for p in all_products if p['category'] in interested_categories and p['product'] not in seen_items]
    
    return random.sample(recommendations, min(10, len(recommendations)))

for index, row in df.iterrows():
    user_id = row['user']
    recommendations = recommend_products(row, products)
    print(f"\nRecommendations for {user_id}:")
    for rec in recommendations:
        print(f" - {rec['product']} ({rec['category']})")

