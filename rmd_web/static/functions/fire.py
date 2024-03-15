# Initialize Firebase Admin SDK
cred = credentials.Certificate('path/to/serviceAccountKey.json')  # Update with your service account key file
firebase_admin.initialize_app(cred)
db = firestore.client()

def add_group_date(group_date_data):
    doc_ref = db.collection('group_dates').document()
    doc_ref.set({
        'creator_id': group_date_data['creator_id'],
        'details': group_date_data['details'],
        'maxParticipants': group_date_data['maxParticipants'],
        'participants': group_date_data['participants'],
        'privacy': group_date_data['privacy'],
        'status': group_date_data['status'],
    })
    return doc_ref.id

def get_group_date(group_date_id):
    doc_ref = db.collection('group_dates').document(group_date_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        print(f"No group date found with ID: {group_date_id}")
        return None

# Example usage:
group_date_data = {
    'creator_id': 'example_creator_id',
    'details': {
        'date': '2024-03-20',
        'time': '15:00',
        'location': 'Central Park',
        'interests': ['Hiking', 'Picnic']
    },
    'maxParticipants': 10,
    'participants': ['user1_id', 'user2_id'],
    'privacy': 'public',
    'status': 'planned'
}

group_date_id = add_group_date(group_date_data)
print("Group date added with ID:", group_date_id)

retrieved_group_date = get_group_date(group_date_id)
if retrieved_group_date:
    print("Retrieved Group Date:")
    print(retrieved_group_date)
