#!/usr/bin/env python3
"""SessionDBAuth module
"""


from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from flask import request
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class
    """
    def __init__(self):
        super().__init__()
        self.user_session = UserSession()

    def create_session(self, user_id=None):
        """ Overloads SessionExpAuth create_session
        """
        if user_id is None:
            return None
        session_id = super().create_session(user_id)
        self.user_session.session_id = session_id
        self.user_session.user_id = user_id
        self.user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Overloads method in SessionExpAuth
            Returns User ID by requesting UserSession in DB using session_id
        """
        if session_id is None:
            return None
        session_list = UserSession.search({'session_id': session_id})
        if len(session_list) < 1:
            return None
        current_session = session_list[0]
        local_session_dict = self.user_id_by_session_id
        created_at = local_session_dict.get(session_id).get('created_at')
        expiration = created_at + timedelta(seconds=self.session_duration)
        if expiration < datetime.now():
            current_session.remove()
            return None
        return current_session.user_id

    def destroy_session(self, request=None):
        """ Overloads method in SessionExpAuth
            Destroys UserSession based on the Session ID from user cookie
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        session_list = UserSession.search({'session_id': session_id})
        if len(session_list) < 1:
            return False
        current_session = session_list[0]
        current_session.remove()
        return True
