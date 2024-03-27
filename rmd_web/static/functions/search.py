import firebase_admin
from firebase_admin import credentials, firestore, storage
from google.cloud.firestore_v1.base_query import FieldFilter
import datetime
from google.cloud.firestore_v1 import ArrayUnion
# Initialize Firebase Admin SDK
db = firestore.client()


######################################################################################################################
# SEARCH
def search_profiles_single_term(term):
    profiles_ref = db.collection("profiles")
    id_ref = profiles_ref.where(filter=FieldFilter("id", "==", term))
    first_name_ref = profiles_ref.where(filter=FieldFilter("first_name", "==", term))
    last_name_ref = profiles_ref.where(filter=FieldFilter("last_name", "==", term))
    email_ref = profiles_ref.where(filter=FieldFilter("email", "==", term))
    
    id_results = id_ref.stream()
    first_name_results = first_name_ref.stream()
    last_name_results = last_name_ref.stream()
    email_results = email_ref.stream()

    profiles = []

    # Add profiles from id_results
    for profile in id_results:
        profile_dict = profile.to_dict()
        if profile_dict not in profiles:
            profiles.append(profile_dict)

    # Add profiles from first_name_results
    for profile in first_name_results:
        profile_dict = profile.to_dict()
        if profile_dict not in profiles:
            profiles.append(profile_dict)

    # Add profiles from last_name_results
    for profile in last_name_results:
        profile_dict = profile.to_dict()
        if profile_dict not in profiles:
            profiles.append(profile_dict)

    # Add profiles from email_results
    for profile in email_results:
        profile_dict = profile.to_dict()
        if profile_dict not in profiles:
            profiles.append(profile_dict)

        
    # Collect the matching profiles
    # profiles = remove_duplicates(profiles)

    # print('profiles', profiles)
    return profiles

def search_profiles(query):
   
    profiles_ref = db.collection("profiles")

    # Construct the query dynamically based on the provided parameters
    for field, value in query.items():
        profiles_ref = profiles_ref.where(field, "==", value)

    # Execute the query
    results = profiles_ref.stream()

    # Collect the matching profiles
    profiles = []
    for profile in results:
        profiles.append(profile.to_dict())

    return profiles

######################################################################################################################
