from split_settings.tools import optional, include
include(
    'base.py',
    'database.py',
    optional('local_settings.py')
)

