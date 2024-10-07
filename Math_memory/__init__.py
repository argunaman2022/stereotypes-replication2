from otree.api import *
import random

doc = '''
This is the main survey app. It contains
1. Main survey 
2. One attention check.
- You can additionally calculate payoffs and save them at a participant field.
'''

class C(BaseConstants):
    NAME_IN_URL = 'Study_Name'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    
    # Payment infos
    Completion_fee = 0.5 #TODO: adjust
    Piece_rate = 0.03 # TODO: Adjust
    Max_score = 10 #TODO: adjust
    Max_bonus = 0.5 #TODO: adjust 
    
    # Round length
    Round_length = 3600 #TODO: adjust
    Timer_text = "Time left to complete this round:"  
    
    
    Instructions_path = "_templates/global/Instructions.html"
    Quit_study_text_path = "_templates/global/Quit_study_text.html"

    Return_redirect = "https://www.wikipedia.org/" #TODO:  ADJUST.  redirect

    #TODO: update this pic
    MathMemory_pic = 'https://raw.githubusercontent.com/argunaman2022/stereotypes-replication/master/_static/pics/MathMemory_pic.png'
    
    
    
class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer): 
    bonus_payoff = models.FloatField(initial=0)
  
    # Attention check 2, 1 was in introduction 
    Attention_2 = models.BooleanField(choices=[
            [True, 'I disagree.'],
            [False, 'I think both are possible.'],
            [False, 'I agree.'],], 
        label= 'A 20 year old man can eat 500kg meat and 2 tons of vegetables in one meal.', widget=widgets.RadioSelect)
            
    # Player answers
    # Scores and trials from each game. There are 6 games but each player plays only 2. See treatment for the order.
    ## First game
    Piece_rate = models.IntegerField(initial=0) #correct answers


    ## Extra fields for certain tasks
    Attempts_Piece_rate = models.IntegerField(initial=0) # logs the number of attempts in the math memory game
    
    # Whether the player clicked out of the page
    blur_event_counts = models.StringField(initial=0, blank=True) # logs how often user clicked out of the page 
 
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
        if player.participant.Treatment:
            Treatment = player.participant.Treatment
            Skill = Treatment.lower()
        else:
            Treatment, Skill = '', ''
        return {
            'Treatment': Treatment,
            'Skill': Skill,
            'hidden_fields': ['blur_event_counts'], #fields to be hidden from the participant e.g. browser, blur_event_counts, see the page to see how this works. #user_clicked_out
                } 


class Round_1_Explanation(MyBasePage):
    extra_fields = []
    form_fields = MyBasePage.form_fields + extra_fields
    
    
class Round_1_Play(MyBasePage):
    extra_fields = ['Piece_rate','Attempts_Piece_rate'] 
    form_fields = MyBasePage.form_fields + extra_fields
    
    timeout_seconds = C.Round_length
    timer_text = C.Timer_text
    


class Attention_check_2(MyBasePage):         
    extra_fields = ['Attention_2']
    form_fields = MyBasePage.form_fields + extra_fields
    
    def before_next_page(player: Player, timeout_happened=False):
        if (not player.Attention_2 and not player.participant.vars['Attention_1']):
            player.participant.vars['Allowed'] = False
            player.participant.vars['Attention_passed'] = False



                
page_sequence = [
    Round_1_Explanation, Round_1_Play,
    Attention_check_2,
    ]
