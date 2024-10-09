from . import *
import random

class PlayerBot(Bot):


    def play_round(self):

        # Assume demographics data is fixed for simplicity
        yield Consent
        yield Demographics, {
            'Age': random.randint(18, 70),
            'Gender': random.choice(['Male', 'Female', ]), 
            'browser': 'Chrome'
        }
        yield Instructions

        yield Comprehension_check_1, {
            'Comprehension_question_1': True,
            'Comprehension_question_2': True,
        }
        yield Attention_check_1, {'Attention_1': True}

    

    # Optionally define any helper methods here if needed for complex operations
