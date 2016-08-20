import colander

from kotti_controlpanel.util import add_settings
from kotti_controlpanel.util import get_setting
from kotti_google_analytics import _, controlpanel_id, AnayticsDefault


class AnalyticsSchema(colander.MappingSchema):
    client_id = colander.SchemaNode(
        colander.String(),
        name="client_id",
        title=_(u'Client ID'),
    )
    client_secret = colander.SchemaNode(
        colander.String(),
        name="client_secret",
        title=_(u'Client Secret'),
    )
    identity = colander.SchemaNode(
        colander.String(),
        name="identity",
        title=_(u'Identity'),
    )
    access_token = colander.SchemaNode(
        colander.String(),
        name="access_token",
        title=_(u'Access Token'),
    )
    refresh_token = colander.SchemaNode(
        colander.String(),
        name="refresh_token",
        title=_(u'Refresh Token'),
    )


GAControlPanel = {
    'name': controlpanel_id,
    'title': _(u'Google Analytics Settings'),
    'description': _(u"Settings for google_analytics"),
    'success_message': _(u"Successfully saved google_analytics settings."),
    'schema_factory': AnalyticsSchema,
}


def populate():
    add_settings(GAControlPanel)

    AnayticsDefault.client_id = get_setting("client_id")
    AnayticsDefault.client_secret = get_setting("client_secret")
    AnayticsDefault.access_token = get_setting("access_token")
    AnayticsDefault.refresh_token = get_setting("refresh_token")
    AnayticsDefault.identity = get_setting("identity")