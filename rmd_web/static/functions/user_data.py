class UserData:
    def __init__(self, friend_requests=None, conversations=None, interests=None, profile_picture='', 
                 friends=None, privacy_settings=None, professional_background=None, sent_friend_request=None, 
                 events=None, social_media=None, first_name='', email='', connections=None, last_name=''):
        self.friend_requests = friend_requests or []
        self.conversations = conversations or {}
        self.interests = interests or []
        self.profile_picture = profile_picture
        self.friends = friends or []
        self.privacy_settings = privacy_settings or {}
        self.professional_background = professional_background or []
        self.sent_friend_request = sent_friend_request or []
        self.events = events or []
        self.social_media = social_media or []
        self.first_name = first_name
        self.email = email
        self.connections = connections or []
        self.last_name = last_name
    
    def to_dict(self):
        # Convert UserData object to a dictionary
        return {
            'friend_requests': self.friend_requests,
            'conversations': self.conversations,
            'interests': self.interests,
            'profile_picture': self.profile_picture,
            'friends': self.friends,
            'privacy_settings': self.privacy_settings,
            'professional_background': self.professional_background,
            'sent_friend_request': self.sent_friend_request,
            'events': self.events,
            'social_media': self.social_media,
            'first_name': self.first_name,
            'email': self.email,
            'connections': self.connections,
            'last_name': self.last_name
        }
    def is_empty(self):
        return all(value == '' or value == [] or value == {} for value in self.__dict__.values())

    # Getter methods
    def get_friend_requests(self):
        return self.friend_requests

    def get_conversations(self):
        return self.conversations

    def get_interests(self):
        return self.interests

    def get_profile_picture(self):
        return self.profile_picture

    def get_friends(self):
        return self.friends

    def get_privacy_settings(self):
        return self.privacy_settings

    def get_professional_background(self):
        return self.professional_background

    def get_sent_friend_request(self):
        return self.sent_friend_request

    def get_events(self):
        return self.events

    def get_social_media(self):
        return self.social_media

    def get_first_name(self):
        return self.first_name

    def get_email(self):
        return self.email

    def get_connections(self):
        return self.connections

    def get_last_name(self):
        return self.last_name

    # Setter methods
    def set_friend_requests(self, friend_requests):
        self.friend_requests = friend_requests

    def set_conversations(self, conversations):
        self.conversations = conversations

    def set_interests(self, interests):
        self.interests = interests

    def set_profile_picture(self, profile_picture):
        self.profile_picture = profile_picture

    def set_friends(self, friends):
        self.friends = friends

    def set_privacy_settings(self, privacy_settings):
        self.privacy_settings = privacy_settings

    def set_professional_background(self, professional_background):
        self.professional_background = professional_background

    def set_sent_friend_request(self, sent_friend_request):
        self.sent_friend_request = sent_friend_request

    def set_events(self, events):
        self.events = events

    def set_social_media(self, social_media):
        self.social_media = social_media

    def set_first_name(self, first_name):
        self.first_name = first_name

    def set_email(self, email):
        self.email = email

    def set_connections(self, connections):
        self.connections = connections

    def set_last_name(self, last_name):
        self.last_name = last_name
        
   