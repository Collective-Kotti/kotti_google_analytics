# -*- coding: utf-8 -*-

"""
Created on 2016-06-18
:author: Oshane Bailey (b4.oshany@gmail.com)
"""
import os
import json

from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid import httpexceptions as httpexc

import googleanalytics as ga
from kotti_google_analytics import _, tracking_id
from kotti_google_analytics.fanstatic import css_and_js
from kotti_google_analytics.views import BaseView


@view_config(
    name='analytics-code',
    renderer='kotti_google_analytics:templates/tracking_code.pt')
class CartView(BaseView):

    def __call__(self):
        return {
            "tracking_id": tracking_id
        }



class Analytics(BaseView):
    
    @property
    def client_id(self):
        return os.environ.get('GOOGLE_ANALYTICS_CLIENT_ID')

    @property
    def client_secret(self):
        return os.environ.get('GOOGLE_ANALYTICS_CLIENT_SECRET')
        
    @property
    def credentials(self):
        if not hasattr(self, "__credentials"):
            self.__credentials = self.flow.step2_exchange("4/iEQV69seHV0JarE5pGkPMRQzIsaBAB6a_Pv1VcW4RpA#")
        return self.__credentials

    @property
    def flow(self):
        return ga.auth.Flow(
            "187255482175-q01b8ltg5biq3vffh8qiulsbjov3n5ci.apps.googleusercontent.com",
            "ADaoG02rqSNt4QihuZFbcRFm",
            redirect_uri=self.request.resource_url(
                self.context, "google-analytics-callback"))

    @property
    def profile(self):
        if not hasattr(self, "__profile"):
            data = {
                "access_token": "ya29.Ci9FA84qFRGWanIS7ZsW8MyVHVYPnUpafadcsrVCbgh2HLtoLAHfhUBvaQZ8Dcp-Zg",
                "client_email": None,
                "refresh_token": "1/2eN7Q18KsKrpyqh6YVH5XYruW4tIHJLgY6IwiSCgzHk",
                "client_id": "187255482175-q01b8ltg5biq3vffh8qiulsbjov3n5ci.apps.googleusercontent.com",
                "client_secret": "ADaoG02rqSNt4QihuZFbcRFm",
                "identity": "187255482175-q01b8ltg5biq3vffh8qiulsbjov3n5ci.apps.googleusercontent.com"}
            self.__profile = ga.authenticate(
                account='dpk.alteroo.com',
                webproperty="UA-82860015-1",
                **data
            )
        return self.__profile

    @view_config(name='analytics-report', root_only=True,
                 permission="admin",
                 renderer="kotti_google_analytics:templates/analytics.pt")
    def view(self):
        return {}

    @view_config(name='analytics-setup', root_only=True, permission="admin")
    def setup_analytics(self):
        authorize_url = self.flow.step1_get_authorize_url()
        return httpexc.HTTPFound(location=authorize_url)

    @view_config(name="google-analytics-callback", root_only=True,
                 permission="admin", renderer="json")
    def callback(self):
        credentials = self.flow.step2_exchange(self.request.params['code'])
        return credentials.serialize()