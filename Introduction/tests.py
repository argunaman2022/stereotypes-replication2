from . import *
import random

class PlayerBot(Bot):


    def play_round(self):
        case = self.case

        # Assume demographics data is fixed for simplicity
        yield Consent
        yield Demographics, {
            'Age': random.randint(18, 70),
            'Gender': random.choice(['Male', 'Female', ]),
            'Education': random.choice(['Haven’t graduated high school','GED','High school graduate','Bachelors','Masters','Professional degree (JD, MD, MBA)','Doctorate']),
            'Employment': random.choice(['Employed full-time', 'Student', 'Out of work, or seeking work']),
            'Income': random.choice(['$0-$10.000', '$10.000-$20.000','$20.000-$30.000','$30.000-$40.000','$40.000-$50.000','$50.000-$60.000',
                                     '$50.000-$75.000', '$75.000-$100.000', '$100.000-$150.000', '$150.000-$200.000', '$200.000+',]),
            'browser': 'Chrome'
        }
        yield Instructions

        yield Comprehension_check_1, {
            'Comprehension_question_1': True,
            'Comprehension_question_2': True,
            'Comprehension_question_3': True
        }
        yield Attention_check_1, {'Attention_1': True}

    

    # Optionally define any helper methods here if needed for complex operations
