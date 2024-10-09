from otree.api import *
import random
from itertools import product

doc = '''
This is the first app - the Introduction app. It contains
1. Demgraphics page
2. Instructions that participants can always access
3. Comprehension checks 
4. and the first attention checks
Following are saved to the participant level
- Allowed: if they didnt fail the comprehension checks
- Comprehension_passed: whether they passed the comprehension checks
- Attention_1: whether they passed the first attention check
'''


#%% Classes
class C(BaseConstants):
    NAME_IN_URL = 'Introduction'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    
    # Payment infos
    Completion_fee = 1.05 # adjust
    Piece_rate = 0.05 #  Adjust #Average person had solved 16 problems in 2 minutes in a previous experiment. 16*0.03 = 0.5
    Max_score = 40 #TODO: adjust. 5 boxes and each box has 8 scores -> 5*8 = 40
    Max_bonus = 2 #TODO: adjust   40 *0.05
    Max_bonus_beliefs = 2 #TODO: adjust  
    
    # picture
    MathMemory_pic = 'https://raw.githubusercontent.com/argunaman2022/stereotypes-replication2/master/_static/pics/MathMemory_pic.png'
    
    
    # Prolific links:
    Completion_redirect = "https://www.wikipedia.org/" #TODO:  ADJUST.  completion redirect
    Reject_redirect = "https://www.wikipedia.org/" #TODO:  ADJUST.  reject redirect
    Return_redirect = "https://www.wikipedia.org/" #TODO: adj ADJUST. ust return redirect
    
    Instructions_path = "_templates/global/Instructions.html"
    Quit_study_text_path = "_templates/global/Quit_study_text.html"
        
    Female_quotas = {
    'Math': 0,
    'Memory': 0,
    }
    Male_quotas = {
    'Math': 0,
    'Memory': 0,
    } 
    
class Subsession(BaseSubsession):
    pass        

def creating_session(subsession):
    '''
    1. initialize the Allowed status to True and Comprehension_passed to False. 
    '''       
    
    subsession.session.Male_quotas = C.Male_quotas.copy()
    subsession.session.Female_quotas = C.Female_quotas.copy()
    
    for player in subsession.get_players():
        player.participant.Allowed = True
        player.participant.Comprehension_passed = False 
        player.participant.vars['Attention_passed'] = True
        player.participant.Treatment = False


            

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    # Demographics
    prolific_id = models.StringField(default=str("None")) #prolific id, will be fetched automatically.
    Age = models.IntegerField(label="Age", min=18, max=100)
    Gender = models.StringField(label='Gender at birth',
                                choices=['Male', 'Female',], widget=widgets.RadioSelect)
    
    # Data quality. 
    #browser used by the participant This variable is saved in the demographics page.
    browser = models.StringField(blank=True) 
    # logs how often user clicked out of the page #TODO: ensure that this is added to all the new pages
    blur_event_counts = models.StringField(initial=0, blank=True) 
    
    'Comprehension and attention checks'
    #whether the player got the comprehension questions rigt at the first try
    Comprehension_1 = models.BooleanField(initial=True) 
    #In the first comprehension check, the questions the player has answered wrong are stored as a string below.
    Comprehension_wrong_answers = models.StringField(initial='') 
    Comprehension_2 = models.BooleanField(initial=True) 
    
    Comprehension_question_1 = models.BooleanField(choices=[
            [False,'My bonus does not depend on how well I do in the game.'], # Correct answer here
            [False, 'To maximize my bonus, I must solve the game as quickly as I can.'],
            [True, 'To maximize my bonus, I must find as many matching pairs as I can in the game.'],],
        label = '<strong>Bonus</strong>. Which of the following is correct?',
        widget=widgets.RadioSelect)
    Comprehension_question_2 = models.BooleanField(choices=[
            [False,'10 minutes.'], 
            [True, '2 minutes.'],
            [False, 'There is no time limit and I must solve as many problems as I can.'],],
        label = '<strong>Time limit</strong>. How much time will you have in the game?',
        widget=widgets.RadioSelect)
    
    Attention_1 = models.BooleanField(choices=[
            [False, 'Austria'],
            [False, 'Germany'],
            [False, 'Switzerland'],
            [True, 'Russia'], 
            [False, 'India'] ],
        label='<strong>Choose the country that was described in the instructions above.</strong>',
        widget=widgets.RadioSelect)
    

    
  
#%% Functions
def treatment_assignment(player):
    session=player.subsession.session
    
    if player.Gender == 'Male':
        Quotas = session.Male_quotas
    elif player.Gender == 'Female':
        Quotas = session.Female_quotas

    
    #the line below does: splits the Quotas into two halves, picks one of them randomly from the bottom half.
    '''
    Quota/Treatment assignment works as follows:
    1. get the current quotas
    2. assign a random treatment from the bottom half of the quotas (i.e. the treatment with the lowest quota)
    3. update quotas accordingly.
    '''
    treatment = random.choice([key for key, value in Quotas.items() if value in sorted(Quotas.values())[:1]])
    # print('Treatment:', treatment)
    player.participant.Treatment = treatment
    if player.Gender == 'Male':
        Quotas.update({treatment: Quotas[treatment]+1})
        session.Male_quotas = Quotas
        # print('incrementing male quotas: ', Quotas)
    elif player.Gender == 'Female':
        Quotas.update({treatment: Quotas[treatment]+1})
        # print('incrementing female quotas: ', Quotas)
        session.Female_quotas = Quotas  
        


    
            
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
        
        

#%% Pages

#Consent, Demographics, Introduction, Comprehension checks and attention check 1
class Consent(Page):   
    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):
        # TODO: in prolific use https://.../room/your_prolific_study?participant_label={{%PROLIFIC_PID%}}
        player.prolific_id = player.participant.label #save prolific id

class Demographics(MyBasePage):
    extra_fields = ['Age', 'Gender', 'browser'] 
    form_fields = MyBasePage.form_fields + extra_fields
        
    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)

        variables['hidden_fields'].append('browser') 
        return variables
        
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        treatment_assignment(player)

    
class Instructions(MyBasePage):
    pass
    
            
class Comprehension_check_1(MyBasePage):
    extra_fields = ['Comprehension_question_1', 'Comprehension_question_2',]
    form_fields = MyBasePage.form_fields + extra_fields    

    @staticmethod   
    def before_next_page(player: Player, timeout_happened=False):
        player_passed_comprehension = player.Comprehension_question_1 and player.Comprehension_question_2
        # if player has answered a question wrong then I save it in a string
        wrong_answers = ''
        if not player.Comprehension_question_1:
            player.Comprehension_question_1 = None #reset player answer so it doesnt show up in the next page
            wrong_answers+= 'first question'
        if not player.Comprehension_question_2:
            if not wrong_answers =='': wrong_answers += ', '
            player.Comprehension_question_2 = None
            wrong_answers+= 'second question'
        
        player.Comprehension_wrong_answers = wrong_answers
        player.Comprehension_1 = player_passed_comprehension
        # save at the participant level
        if player_passed_comprehension:
            player.participant.vars['Comprehension_passed'] = True

        
class Comprehension_check_2(MyBasePage):
    extra_fields = ['Comprehension_question_1', 'Comprehension_question_2',]
    form_fields = MyBasePage.form_fields + extra_fields    

    @staticmethod
    def is_displayed(player: Player):
        condition = MyBasePage.is_displayed(player) and not player.Comprehension_1
        return condition
    
    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)

        # Add or modify variables specific to ExtendedPage
        variables['Comprehension_wrong_answers'] = player.Comprehension_wrong_answers
        return variables

    @staticmethod   
    def before_next_page(player: Player, timeout_happened=False):
        player_passed_comprehension = (player.Comprehension_question_1 and
                                       player.Comprehension_question_2)
        #failing two compr. checks player is not allowed to continue
        player.participant.Allowed = player_passed_comprehension
        player.Comprehension_2 = player_passed_comprehension
        # save at the participant level if they passed
        if player_passed_comprehension:
            player.participant.vars['Comprehension_passed'] = True
            player.participant.vars['Allowed']=True
        else:
            player.participant.vars['Allowed']=False
            player.participant.vars['Comprehension_passed'] = False

class Attention_check_1(MyBasePage):
    extra_fields = ['Attention_1']
    form_fields = MyBasePage.form_fields + extra_fields    
    #save at  the participant level
    @staticmethod   
    def before_next_page(player: Player, timeout_happened=False):
        player.participant.vars['Attention_1'] = player.Attention_1
        
    

page_sequence = [Consent, Demographics, Instructions,
                 Comprehension_check_1, Comprehension_check_2,
                 Attention_check_1,
                 ]