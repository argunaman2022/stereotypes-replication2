from os import environ

SESSION_CONFIGS = [
    dict(name='Study',
         app_sequence=['Introduction','Math_memory', 'Results'],
         num_demo_participants=1000, #TODO: adjust number
         completionlink='prolific completion link!!!!!!'), #TODO: ADJUST. add the proper completion link from prolific

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

ROOMS = [
    dict( name = 'Survey', display_name = 'Survey'),
]

#TODO:  ADJUST.  add use use_browser_bots=True, to test with website bots. Alternatively use otree test Study --export to test with the otree bots. Make sure to delete database first
SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc="", use_browser_bots=False,
)
#TODO:  ADJUST. add the relevant participant fields if you wanna pass them thourgh apps
PARTICIPANT_FIELDS = [
    'Allowed','Comprehension_passed', 'Attention_passed',
    'Covariate_categories', #this is the dictionary of covariates that we stratify over
    'Treatment'
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
