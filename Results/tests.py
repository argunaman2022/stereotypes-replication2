from otree.api import *
from . import *
import random

class PlayerBot(Bot):

    cases = ['pass', 'fail_comprehension', 'fail_attention']

    def play_round(self):
        pass

    # Optionally define any helper methods here if needed for complex operations
