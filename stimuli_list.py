import os
import random

def play_stim(stimulus):
    from kivy.core.audio import audio_pygame
    path = 'stimuli/'+stimulus

    #audio_pygame.mixer.music.load(path)
    #audio_pygame.mixer.music.play()

    #while audio_pygame.mixer.music.get_busy():
        #continue

def stimuli_list():

    #Read a folder of stimuli
    stimulus_files = os.listdir("stimuli/")

    experiment_order = []
    target = []
    D7 = []
    voicing = []
    mode = []
    order = []
    key = []

    #Add various components into their respective lists
    for file in stimulus_files:
        stimuli = file.strip('.wav')
        stim_parts = stimuli.split('_')
        if stim_parts[0] not in target:
            target.append(stim_parts[0])
        if stim_parts[1] not in D7:
            D7.append(stim_parts[1])
        if stim_parts[2] not in voicing:
            voicing.append(stim_parts[2])
        if stim_parts[3] not in mode:
            mode.append(stim_parts[3])
        if stim_parts[4] not in order:
            order.append(stim_parts[4])
        if stim_parts[5] not in key:
            key.append(stim_parts[5])

    key = key * 18
    random.shuffle(key)

    for targ in target:
        for d7 in D7:
            for voice in voicing:
                for mod in mode:
                    for orde in order:
                        for k in key:
                            current_combo = targ + '_' + d7 + '_' + voice + '_' + mod + '_' + orde + '_' + k + '.wav'

                            if current_combo not in stimulus_files:
                                print("% not in folder" % current_combo)
                            else: experiment_order.append(current_combo)

    shuffle_numb = random.randint(1,9)
    for i in range(shuffle_numb):
        random.shuffle(experiment_order)

    return experiment_order
                            
def extract_stim_info(stimulus):
    stimulus = stimulus.strip('.wav')
    stim_parts = stimulus.split('_')
    return stim_parts
