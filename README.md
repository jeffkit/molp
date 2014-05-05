mobile online parameter manager for Django
===============================

install
--------

`pip install molp`

add 'molp' into 'INSTALLED_APPS'

config
------


add APP_DEFINITION to settings. example:

APP_DEFINITION = (('com.changba.ktv', u'唱吧(iOS)'), ('com.changba.ktvadr', u'唱吧(安卓)'))

usage
-------

from molp.models import Parameter

ps = Parameter.get_parameters(app, version, channel, since, last_modify)

data = dict([(p.name, p.value) for p in ps])

