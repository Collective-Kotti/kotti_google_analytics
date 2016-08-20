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
from kotti_controlpanel.util import set_setting, get_setting
from kotti_google_analytics import _, AnayticsDefault
from kotti_google_analytics.fanstatic import css_and_js
from kotti_google_analytics.views import BaseView


@view_config(
    name='analytics-code',
    renderer='kotti_google_analytics:templates/tracking_code.pt')
class CartView(BaseView):

    def __call__(self):
        return {
            "tracking_id": AnayticsDefault.tracking_id
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
            self.__credentials = self.flow.step2_exchange(AnayticsDefault.refresh_token)
        return self.__credentials

    @property
    def flow(self):
        return ga.auth.Flow(
            AnayticsDefault.client_id,
            AnayticsDefault.client_secret,
            redirect_uri=self.request.resource_url(
                self.context, "google-analytics-callback"))

    @property
    def profile(self):
        if not hasattr(self, "__profile"):
            data = {
                "access_token": AnayticsDefault.access_token,
                "client_email": None,
                "refresh_token": AnayticsDefault.refresh_token,
                "client_id": AnayticsDefault.client_id,
                "client_secret": AnayticsDefault.client_secret,
                "identity": AnayticsDefault.identity}
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
        jcred = credentials.serialize()
        set_setting("client_id", jcred.get("client_id"))
        set_setting("client_secret", jcred.get("client_secret"))
        set_setting("access_token", jcred.get("access_token"))
        set_setting("refresh_token", jcred.get("refresh_token"))
        set_setting("identity", jcred.get("identity"))
        return jcred
