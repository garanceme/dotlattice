#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### In the experimental room Labb 5:
# - Need a system for which 4 buttons to press for the corners!
# - I marked the spots in pencil where the monitor and chinrest should be. I'm
# leaving them there anyways but in case they get moved. With this setup,  the 
# viewer's eyes are 57 cm from the screen, I measured it.
# - The person should be in the dark so that I can recreate more easily elsewhere.
# - I left a little roll of toilet paper behind the screen to lay a sheet down on 
# the chinrest. 
# - The keyboard has a weird layout, I took a pic on my phone.
# - The screen is a large ASUS - Republic of Gamers so my guess is that it's great,
# but the resolution doesn't look great. According to the Windows 10 settings it's
# set to 1920x1080 which seems dumb on such a large screen but ok. Scale is set to 100%. 
# - don't think online using Replit works because I'd need an online place to store the data then


"""
Dot lattice to create stimuli in which observers search for a specific orientation. 

Methods: 
    https://docs.google.com/document/d/1K1D_PBbofxpclgBuswPIPoTwnx4d6uB4th5EJhUCI58/edit

Created by: Garance Merholz - gmerholz@gmail.com
10 April 2022
"""

# The script that glues together some functions for making the whole
# experiment. 

import pygame

# initialize pygame modules
pygame.init()

import src.nt_utilities as utils # should import after pygame.init() I think
# import os
# from psychopy import event, data, core # logging, visual,
import numpy as np
from itertools import permutations
import src.create_stim as cst
import src.parameters as params
from time import perf_counter
import random

# start a timer
starttime = perf_counter()

penrose0_dots1 = 1

expInfo = {} # initiate experiment info dict
# expInfo['dateStr'] = data.getDateStr()  # add the current time to expInfo dict

## Set the logging to critical only, to avoid getting all minor alerts
# logging.console.setLevel(logging.CRITICAL)
# print("PSYCHOPY LOGGING set to: CRITICAL")
# print(expInfo['dateStr'])

if penrose0_dots1:
    print("********************************************")
    print("DOTLATTICE ORIENTATION EXTRACTION EXPERIMENT")
    print("********************************************")
else:
    print("*****************************************")
    print("NOISETILE TEXTURE SEGMENTATION EXPERIMENT")
    print("*****************************************")

ntvars = utils.NtVars

# Open the exp window
pixelator_pix, nul = utils.calculate_pixel_length_from_dva(params.size_pixelatingunit_dva[0])
pixelunit_pix = round( (5/6) * pixelator_pix) # make the pixel unit just a bit smaller than the pixelator
                                              # to preserve structure without making obvious cuts thru pixrs
scaling_factor = pixelunit_pix
original_width, original_height = utils.winsize[0]//scaling_factor, utils.winsize[1]//scaling_factor
depth = 4*8 # I don't know where this calc came from
# screen = pygame.Surface((original_width,original_height), pygame.DOUBLEBUF, depth)
screen = pygame.Surface(utils.winsize, pygame.DOUBLEBUF, depth)
# fullwindow = pygame.display.set_mode((scaling_factor*original_width, scaling_factor*original_height), display=params.screennum)
fullwindow = pygame.display.set_mode(utils.winsize, display=params.screennum)

# Welcome to the exp, check that keyboard is getting recorded
utils.open_window_welcome(fullwindow)

# Ask if real participant or debug
real1_or_debug0, chinrest1_0, subject_sex, subj_righthandYN = utils.ask_if_real_participant(fullwindow)
if real1_or_debug0: 
    savefolder = "realparticipants_results"
    checkparamsmessage = "Please ensure src/parameters.py are accurate. Press to continue."
    utils.draw_text_wait_resp(fullwindow, checkparamsmessage, None, 9)
else: savefolder = "results"

# Get response keys keylist (it saves to utils.NtVars)
respkeys = utils.get_nt_response_keys(fullwindow)
print(respkeys.response_keys_codes) # this is the dict containing the response keycodes

# Will need instructions here

#!!! THere is an issue with the rescale. The PNG shows that the process is making a whole image with way
# smaller pixel units than it should, and takes 20 minutes to do it, and then only shows a small corner
# of it in the Pygame window.

if penrose0_dots1:
    zooms_entropyconds = params.lattice_entropy_conds # displacement vector length in percent of dot radius
    lattice_arrangements = list(permutations(range(1, 5))) # [(1,2,3,4), (1,2,4,3), (1,3,2,4), ..., (4,3,2,1)]
    # 1: horizontal(0pi), 2: 45° cw from vert (pi/4), 3: vert (pi/2), 4: 45° ccw from vert (3pi/4)
    # ind0 is top left, ind1 top right, ind2 bottom left, ind3 bottom right
    targcodes = np.arange(len(lattice_arrangements))
    ors_to_attend = random.choice(lattice_arrangements)
else:
    # This will need to be in an experimental loop but just make it show stims for now
    targcodes = [11,12,13,14,21,22,23,24,31,32,33,34,41,42,43,44,51,52,53,54,
                 61,62,63,64,71,72,73,74,81,82,83,84]
    targcodes = [11] # test with 1 first
    zooms_entropyconds = [0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1] # ??? why 7? should be 5?
    zooms_entropyconds = [0.5] # test with 1 first
    ors_to_attend = (np.nan,np.nan,np.nan,np.nan)
targcode_assignment = np.tile(np.array(targcodes),len(zooms_entropyconds)) 
# cst.rng.shuffle(targcode_assignment)
entrop_assignment = np.tile(np.array(zooms_entropyconds),len(targcodes))
# cst.rng.shuffle(entrop_assignment)
# w/ 2 shuffles you weren't using the same shuffled order for zooms and targtypes, 
# which is stupid. should use the same shuffled order for both, so that each 
# entropy level has all of the targtypes and vice-versa
shuff_order = np.random.permutation(len(targcode_assignment))
targcode_assignment = targcode_assignment[shuff_order]
entrop_assignment = entrop_assignment[shuff_order]

# prepare data text file, to save results and info
pixels_per_dva, screen_res_pix = utils.calculate_pixel_length_from_dva(1)
filename, filename_otherinfo = utils.make_save_files(savefolder, 
   chinrest1_0, penrose0_dots1, respkeys.response_keys_codes, subject_sex,
   ors_to_attend,targcode_assignment,entrop_assignment,subj_righthandYN,
   pixels_per_dva, screen_res_pix)
responses = []

# start a timer for the stim generation
starttimeexp_afterwelcome = perf_counter()

if params.display1_or_savesvg0:
    response_keys_list = list(respkeys.response_keys_codes.values())
    
texlist = []
# breakcounter = 0
breaks = np.empty((1,100))
breaks[:] = np.nan
# showed_or_to_attend = np.empty(len(ors_to_attend))
# showed_or_to_attend[:] = np.nan
ortoattendcounter = 0
orchange_trials = np.linspace(0,params.num_trials_per_entropandarrangecond * 
            len(zooms_entropyconds) * len(targcodes), 5)
for block in range(params.num_trials_per_entropandarrangecond):
    for trial in range(len(zooms_entropyconds)*len(targcodes)):
        if (block)*(len(zooms_entropyconds)*len(targcodes))+trial == round(orchange_trials[ortoattendcounter]):
                utils.show_orientationtoattend(fullwindow,ors_to_attend[ortoattendcounter])
                # showed_or_to_attend[ortoattendcounter] = 1
                ortoattendcounter += 1
        # 1: horizontal(0pi), 2: 45° cw from vert (pi/4), 3: vert (pi/2), 4: 45° ccw from vert (3pi/4)
        # ind0 is top left, ind1 top right, ind2 bottom left, ind3 bottom right
        targcode, entroplevel = targcode_assignment[trial], entrop_assignment[trial]
        correct_respcode = response_keys_list[lattice_arrangements[targcode].index(ors_to_attend[ortoattendcounter-1])]
        if penrose0_dots1:
            bnt_pgtex = cst.make_dotlattices_tex(screen, fullwindow, lattice_arrangements[targcode], entroplevel)
        else:
            bnt_pgtex, bk_pgtex, t_pgtex = \
                cst.make_bk_and_target(screen, fullwindow, targcode, entroplevel)
    
            # # let's see what those 2 sheets look like
            # utils.display_to_window_collect_response(screen, bk_pgtex)
            # utils.display_to_window_collect_response(screen, t_pgtex)
        
        # this here used to be separate, first did all stims and then showed them at each trial (separate for loop)
        texlist.append(bnt_pgtex)
        if params.display1_or_savesvg0:
            utils.display_to_window_limited_time(screen, fullwindow, texlist[trial], 300)
            screen.fill(params.dot_bkgd_color)
            cst.fixation_cross(screen)
            response, reactiontime_ms = utils.display_to_window_collect_response(screen,fullwindow,screen,response_keys_list,2)
            # response_outline = utils.display_to_window_collect_response(screen,imtex_outlined)
            responses.append(response)
        
            # save the data at each trial
            timestamp = perf_counter()
            textfile = open(f"{filename}", "a")
            textfile.write(f"{response}\t")
            textfile.write(f"{reactiontime_ms}\t")
            textfile.write(f"{targcode_assignment[trial]}\t")
            textfile.write(f"{entrop_assignment[trial]}\t")
            textfile.write(f"{correct_respcode}\t")
            textfile.write(f"{ors_to_attend[ortoattendcounter-1]}\t")
            textfile.write(f"{timestamp}\n")
            textfile.close()
        
        # Have a break every x trials
        if trial%params.num_trials_bw_breaks == 0 and\
            trial !=0:
                    utils.make_break(fullwindow, ors_to_attend[ortoattendcounter-1])
                    # breaks[0,breakcounter] = nowtime
                    # breakcounter += 1
        
# # Tell me how long it took to generate stimuli
endtimeexp = perf_counter()
print(f"Experiment completed in {endtimeexp-starttimeexp_afterwelcome:0.4f} sec")
        

end_message = "Thank you for your participation. Please call the experimenter to RECORD YOUR AGE in otherinfo.txt"
utils.draw_text_wait_resp(fullwindow, end_message)

# close
pygame.display.quit()

