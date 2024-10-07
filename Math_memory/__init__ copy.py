from otree.api import *
import random
import numpy as np

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
    
    Participation_fee = 1.87 ## TODO: Adjust
    Bonus_fee_max = 2 ## TODO: Adjust
    
    Piece_rate = 0.03 # TODO: Adjust    
    
    # Paths
    Instructions_path = "_templates/global/Instructions.html"
    Quit_study_text_path = "_templates/global/Quit_study_text.html"

    # Prolific links:
    Completion_redirect = 'Wikipedia.com' #TODO: ADJUST
    Reject_redirect = 'Wikipedia.com' #TODO: ADJUST
    Return_redirect = 'Wikipedia.com' #TODO: ADJUST
    
        
    Math_memory_template_path = "_templates/global/Math_memory.html"
        
    Round_length = 120 
    Timer_text = "Time left to complete this round:"
    
    
    # Game explanation texts
    #TODO: adjust times in thees descriptions. Currently: 2 minutes
    MathMemory_text_Math = '''
    You will see a box with 16 cells.
    Behind each cell, there is a simple addition of two one-digit numbers (e.g. 1+2) and a red or black heart.
    Your task is to find the matching pairs by clicking on the corresponding cells. 
    For two cells to be a match two conditions must be met: first, the addition must be the same, and second, the hearts must be the same color.
    When you find a matching pair, these cells will disappear. Once you finish one box, another will appear. 
    <br>
    When you find a matching pair, these cells will disappear. 
    Once you find all matching pairs in one box, another box with 16 cells will appear.
    Each pair found counts as one problem correctly solved! 
    <br>
    An example is depicted below. 
    In this picture, 1+2 and 3+0 are matching pairs, since they both equal 3 and they both have a red heart.
    Clicking on these two cells leads to a correct solution
    
    <br>
    For this round you will be given <b>2 minutes</b> to solve as many <b>Math task problems</b> as you can.
    We expect that those with stronger <b>math skills</b> will perform better. Good luck!
    '''
    MathMemory_text_Memory = '''
    You will see a box with 16 cells.
    Behind each cell, there is a simple addition of two one-digit numbers (e.g. 1+2) and a red or black heart.
    Your task is to find the matching pairs by clicking on the corresponding cells. 
    For two cells to be a match two conditions must be met: first, the addition must be the same, and second, the hearts must be the same color.
    When you find a matching pair, these cells will disappear. Once you finish one box, another will appear. 
    <br>
    When you find a matching pair, these cells will disappear. 
    Once you find all matching pairs in one box, another box with 16 cells will appear.
    Each pair found counts as one problem correctly solved! 
    <br>
    An example is depicted below. 
    In this picture, 1+2 and 3+0 are matching pairs, since they both equal 3 and they both have a red heart.
    Clicking on these two cells leads to a correct solution
    
    <br>
    For this round you will be given <b>2 minutes</b> to solve as many <b>Memory task problems</b> as you can.
    We expect that those with stronger <b>memory skills</b> will perform better. Good luck!
    '''
    
   
       
    # Game explanation pics
    #TODO: Adjust the paths to the pic
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
            
    # Scores and trials from each game. There are 6 games but each player plays only 2. See treatment for the order.
    ## First game
    Piece_rate = models.IntegerField(initial=0) #correct answers


    ## Extra fields for certain tasks
    Attempts_Piece_rate = models.IntegerField(initial=0) # logs the number of attempts in the math memory game
    
    # Whether the player clicked out of the page
    blur_event_counts = models.StringField(initial=0, blank=True) # logs how often user clicked out of the page 

 
#%% Functions

#TODO: delete these functions if not needed
# def get_game(player):
#     Treatment = player.participant.Treatment
#     # split treatment based on _
#     First_part, Second_part = Treatment.split('_')[0], Treatment.split('_')[1]
#     Treatment_math_or_memory = First_part
    
#     Game1 = 'MathMemory'
    
#     Game1_Page_title = Treatment_math_or_memory + ' game'

#     return Game1, Second_part, Treatment_math_or_memory, Game1_Page_title, Game2_Page_title
        
# def get_game_text(player, game2, Tournament_for_Change_detection=False):
#     if game2 == 'VisualMemory':
#         game2_explanation_text = C.Visual_memory_text
#         game2_explanation_pic = C.Visual_memory_pic
#         game2_path = C.Visual_memory_template_path
#     elif game2 == 'Quiz':
#         game2_explanation_text = C.Quiz_text
#         game2_explanation_pic = C.Quiz_pic
#         game2_path = C.Quiz_template_path
#     elif game2 == 'SpotTheDifference':
#         game2_explanation_text = C.SpotTheDifference_text
#         game2_explanation_pic = C.SpotTheDifference_pic
#         game2_path = C.SpotTheDifference_template_path
#         if Tournament_for_Change_detection:
#             game2_path = C.SpotTheDifference_template_Tournament_path
    
#     return game2_explanation_text, game2_explanation_pic, game2_path

 
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
        return {'hidden_fields': ['blur_event_counts'], #hide the browser field from the participant, see the page to see how this works. #user_clicked_out
                'Instructions': C.Instructions_path,
                'Treatment': player.participant.Treatment,} 
  
# Pages
class Attention_check_2(MyBasePage):         
    extra_fields = ['Attention_2']
    form_fields = MyBasePage.form_fields + extra_fields
    
    def before_next_page(player: Player, timeout_happened=False):
        if (not player.Attention_2 and not player.participant.vars['Attention_1']):
            player.participant.vars['Allowed'] = False
            player.participant.vars['Attention_passed'] = False
          

class Round_1_Explanation(MyBasePage):
    extra_fields = []
    form_fields = MyBasePage.form_fields + extra_fields
    
    @staticmethod
    def vars_for_template(player: Player):
        # _, _, Treatment_math_or_memory, Game1_title, _ = get_game(player)
        
        # if Treatment_math_or_memory == 'Math':
        #     game1_explanation_text = C.MathMemory_text_Math
        # elif Treatment_math_or_memory=='Memory':
        #     game1_explanation_text = C.MathMemory_text_Memory
        # game1_explanation_pic = C.MathMemory_pic
        
        # variables = MyBasePage.vars_for_template(player)
        # variables['Game_explanation_text'] = game1_explanation_text
        # variables['Game_explanation_pic'] = game1_explanation_pic
        # variables['Game_title'] = Game1_title
        # variables['Payment_info'] = Payment_info(player, 'MathMemory')
        # return variables
    
class Round_1_Play(MyBasePage):
    extra_fields = ['Piece_rate','Attempts_Piece_rate'] 
    form_fields = MyBasePage.form_fields + extra_fields
    
    timeout_seconds = C.Round_length
    timer_text = C.Timer_text
    
    @staticmethod
    def vars_for_template(player: Player):
        # game1, game2, Treatment_math_or_memory, Game1_title, Game2_title = get_game(player)
        
        # if Treatment_math_or_memory == 'Math':
        #     game1_explanation_text = C.MathMemory_text_Math
        # elif Treatment_math_or_memory=='Memory':
        #     game1_explanation_text = C.MathMemory_text_Memory
        # game1_explanation_pic = C.MathMemory_pic
        
        # variables = MyBasePage.vars_for_template(player)
        # variables['Game_explanation_text'] = game1_explanation_text
        # variables['Game_explanation_pic'] = game1_explanation_pic
        
        # variables['Game_path'] = C.Math_memory_template_path
        # variables['Game_title'] = Game1_title

        # return variables
    
    @staticmethod
    def js_vars(player):
        game1, _, Treatment_math_or_memory, _, _ = get_game(player)
        return dict(
            game_name = game1,
            game_field_name = 'id_Piece_rate',
        )

        

page_sequence = [
    Round_1_Explanation, Round_1_Play, Page3_G1_R1_R,
    Attention_check_2,
    Page4_G1_R2_E, Page5_G1_R2, Page6_G1_R2_R,
    Page7_G2_R1_E, Page8_G2_R1, Page9_G2_R1_R,
    Page10_G2_R2_E, Page11_G2_R2, Page12_G2_R2_R,
    Page13_G1_Choice, Page14_G2_Choice,
    ]
