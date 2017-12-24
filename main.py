import kivy

kivy.require('1.10.0')

from kivy.app import App
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, StringProperty, ObjectProperty
from kivy.config import Config



Config.set('input', 'mouse', 'mouse,multitouch_on_demand')  # removes multitouch simulation
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

import csv
import time

from stimuli_finder import *  # loads functions for experiment


# # Defining multiple screens to be used throughout experiment.
# # This way, different elements/buttons can be shown/have different functions.
class IntroScreen(Screen):
    def button_response(self):
        App.get_running_app().part_num = int(self.part_num.text)
        App.get_running_app().trials_to_run = int(self.trials_to_run.text)

        name = App.get_running_app().csv_name

        date = time.strftime("%d-%m-%Y") + '_' + time.strftime("%H-%M-%S")
        name = 'data/pilot1_' + date + '_participant_' + self.part_num.text + '.csv'

        App.get_running_app().csv_name = name

        with open(name, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                ['Participant', 'Trial_Num', 'Stimulus_name', 'Response'])

        App.get_running_app().root.current = 'setup'


class SetupTrialScreen(Screen):
    def on_enter(self):
        # Load local variables
        trial = App.get_running_app().trial
        stim_master = App.get_running_app().stim_master

        # perform functions
        stimulus = stim_master[trial-1]

        self.lbl.text = "Trial #" + str(trial) + ", stimulus = " + str(stimulus)

        # upload local variables into properties
        App.get_running_app().trial = trial
        App.get_running_app().stimulus = stimulus

    def go_to_run(self):
        self.lbl.text = ''
        App.get_running_app().root.current = 'run'


class RunTrialScreen(Screen):
    def on_enter(self):
        self.lbl.text = "Does the first or second stimulus sound most similar to the target?"
        play_stim(App.get_running_app().stimulus)



class ResponseScreen(Screen):
    def __init__(self, **kwargs):
        super(ResponseScreen, self).__init__(**kwargs)

    def on_pre_enter(self):
        self.lbl.value = 1
        App.get_running_app().response_made = False

    def save_response(self, *args):
        App.get_running_app().response = round(args[1], 1)
        App.get_running_app().response_made = True

    def gotoExit(self):
        trial = App.get_running_app().trial
        stim_master = App.get_running_app().stim_master
        response = App.get_running_app().response
        part_num = App.get_running_app().part_num

        if App.get_running_app().response_made is True:
            App.get_running_app().response_made = False
            stimulus = stim_master[trial-1]
            #condition, key, transposition = extract_stim_info(stimulus)
            data_row = [part_num, trial, stimulus, response]

            with open(App.get_running_app().csv_name, 'a', newline='') as csvfile:
                rowwriter = csv.writer(csvfile, delimiter=',',
                                       quotechar='|', quoting=csv.QUOTE_MINIMAL)
                rowwriter.writerow(data_row)

                # flip screens to next trial or exit
            App.get_running_app().trial += 1
            if App.get_running_app().trial <= App.get_running_app().trials_to_run:
                App.get_running_app().root.current = 'setup'
            else:
                App.get_running_app().root.current = 'exit'


class ExitScreen(Screen):
    def on_enter(self):  # This code will run when exit screen is entered!
        print("finished!")


class MyScreenManager(ScreenManager):
    pass


root_widget = Builder.load_file("the_konrad.kv")


class ScreenManagerApp(App):
    trial = NumericProperty(1)  # keeps track of current trial #
    trials_to_run = NumericProperty(10)
    stimulus = StringProperty('default')  # Stimulus file name
    response = NumericProperty(0)  # Participant Response via button press
    response_made = ObjectProperty(False)  # checks if response has been made

    stim_master = ObjectProperty(stimuli_list())

    part_num = NumericProperty(1)

    date = time.strftime("%d-%m-%Y") + '_' + time.strftime("%H-%M-%S")
    name = 'data/pilot1_' + date + '_participant_1' + '.csv'

    csv_name = StringProperty(name)


    def build(self):
        return root_widget


ScreenManagerApp().run()
