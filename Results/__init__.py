from otree.api import *


doc = """
Your app description
"""
class C(BaseConstants):
    NAME_IN_URL = 'Results'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    
     # Prolific links:
    Completion_redirect = "https://app.prolific.com/submissions/complete?cc=C1J53ZD8" 
    Reject_redirect = "https://app.prolific.com/submissions/complete?cc=CSTJBDWB" 
    Return_redirect = "https://app.prolific.com/submissions/complete?cc=C3ZWW9CZ" 
    
    Instructions_path = "_templates/global/Instructions.html"
    Quit_study_text_path = "_templates/global/Quit_study_text.html"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    blur_event_counts = models.StringField(initial=0, blank=True) # logs how often user clicked out of the page 



# PAGES

#%% Base Pages
class MyBasePage(Page):
    'MyBasePage contains the functions that are common to all pages'
    form_model = 'player'
    form_fields = ['blur_event_counts']
    
    
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.Allowed 
    
    @staticmethod
    def vars_for_template(player: Player):
        return {'hidden_fields': ['bullshit'], #hide the browser field from the participant, see the page to see how this works. #user_clicked_out
                'Instructions': C.Instructions_path} 

#%% Pages

class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        print(player.participant.vars)
        return player.participant.Allowed and player.participant.Comprehension_passed and player.participant.Attention_passed

    @staticmethod   
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)
        
        if player.participant.Payment_relevant_round == '1':
            Bonus_message = f'''The computer has randomly selected Part I to determine your bonus.
            In that round you earned {player.participant.Score} points which translates to a bonus of ${player.participant.Bonus}. 
            This bonus will be paid within a week.
            '''
        else:
            payoff_question = player.participant.Payment_relevant_round.split('_')[1]
            Bonus_message = f'''The computer has randomly selected question {payoff_question} from Part II to determine your bonus.
            Once the study is completed, you will be paid your bonus based on how close your answer in that question was to the correct answer.
            '''
        
        variables['Score'] = player.participant.Score
        variables['Bonus'] = player.participant.Bonus
        variables['Bonus_message'] = Bonus_message
        return variables

class Failed_screening(MyBasePage):
    'This page is displayed if the player failed the comprehension checks'
    @staticmethod
    def is_displayed(player: Player):
        return not player.participant.Comprehension_passed 

    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)
        failure_message = '''Unfortunately, you did not pass the comprehension check successfully. Because of this, we cannot use your data. 
                                As we do not want to reject you, we kindly ask you to <strong>return the study on Prolific</strong>. '''
        # Add or modify variables specific to ExtendedPage
        variables['failure_message'] = failure_message
        return variables

    @staticmethod
    def js_vars(player):
        return dict(
            completion_link = C.Return_redirect
        )

class Failed_attention(MyBasePage):
    @staticmethod
    def is_displayed(player: Player):
        return not player.participant.Attention_passed  # player failed both attention checks
    @staticmethod
    def js_vars(player):
        return dict(
            completion_link = C.Reject_redirect
        )

page_sequence = [Results, Failed_screening, Failed_attention]
