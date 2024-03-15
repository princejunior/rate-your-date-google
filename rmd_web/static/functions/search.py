import firebase_admin
from firebase_admin import firestore

def search_users(query):
    db = firestore.client()
    users_ref = db.collection('users')
    results = []

    # Search by first name
    query_first = users_ref.where('name', '>=', query).where('name', '<=', query + u'\uf8ff').stream()
    results.extend([doc.to_dict() for doc in query_first])

    # Search by last name
    query_last = users_ref.where('name', '>=', query).where('name', '<=', query + u'\uf8ff').stream()
    results.extend([doc.to_dict() for doc in query_last])

    return results
