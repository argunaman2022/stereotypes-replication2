from otree.api import *
from . import *
import random

class PlayerBot(Bot):


    def play_round(self):
        # Provide responses for the main survey
        yield Round_1_Explanation
        yield Round_1_Play, {'Piece_rate': random.choice([1, 2, 3, 4]), 'Attempts_Piece_rate': random.choice([1, 2, 3, 4])}
        yield PartII
        yield FOB, {'FOB_Male_score': random.choice([1, 2, 3, 4]), 'FOB_Female_score': random.choice([1, 2, 3, 4])}
        yield SOB, {'SOB_Male_score': random.choice([1, 2, 3, 4]), 'SOB_Female_score': random.choice([1, 2, 3, 4])}
        yield Attention_check_2, {'Attention_2_question': '1234'}




    # Optionally define any helper methods here if needed for complex operations
