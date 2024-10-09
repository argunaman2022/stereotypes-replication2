from os import environ

SESSION_CONFIGS = [
    dict(name='Study',
         app_sequence=['Introduction','Math_memory', 'Results'],
         num_demo_participants=50, 
         completionlink='https://app.prolific.com/submissions/complete?cc=C1J53ZD8'), 

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

ROOMS = [
    dict( name = 'Survey', display_name = 'Survey'),
]
SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc="", use_browser_bots=False,
)

PARTICIPANT_FIELDS = [
    'Allowed','Comprehension_passed', 'Attention_passed',
    'Treatment',
    'Payment_relevant_round', 'Score', 'Bonus'
]
SESSION_FIELDS = {
                    'Male_quotas':{}, 'Female_quotas':{},
                 }

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '9007113971546'
