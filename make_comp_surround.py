# -*- coding: utf-8 -*-
import numpy as np
import random
from PIL import Image
import os

def position_constraint(random_array):
    """
    constraint 2: not 2 identical reflectances next to each other
    """
    n_rep = 0
    cnt = 1
    while cnt > 0:
        cnt = 0
        for j in np.arange(len(random_array)):
            ## check identity of adjacent reflectances for all but last and first
            if j < (len(random_array) - 1):
                if random_array[j] == random_array[j+1]:
                    cnt = cnt + 1
            ## check identity of adjacent reflectances for last and first
            elif j == (len(random_array) - 1):
                if random_array[j] == random_array[0]:
                    cnt = cnt + 1
            
            #print 'idx %d, count %d' %(j, cnt)
        if cnt > 0:
            random.shuffle(random_array)
            n_rep = n_rep + 1
        else:
            break
    print(n_rep)
    return random_array
    
def position_constraint2(ext_surround, dir_surround):
    """
    constraint 2: not 2 identical reflectances next to each other
    """
    a = np.array((1,2,3,5,6,7,9,10,11,13,14,15))
    b = np.array((0,1,2,2,3,4,4,5,6,6,7,0))
    n_rep = 0
    cnt = 1
    while cnt > 0:
        cnt = 0
        cnt2=0
        for j in np.arange(len(ext_surround)):
            ## check identity of adjacent reflectances for all but last and first
            if j < (len(ext_surround) - 1):
                if ext_surround[j] == ext_surround[j+1]:
                    cnt = cnt + 1
            ## check identity of adjacent reflectances for last and first
            elif j == (len(ext_surround) - 1):
                if ext_surround[j] == ext_surround[0]:
                    cnt = cnt + 1
            if j in a:
                if ext_surround[a[cnt2]] == dir_surround[b[cnt2]]:
                    cnt  = cnt  + 1
                
                cnt2 =cnt2+1
                
            
        #print cnt
        #print 'idx %d, count %d' %(j, cnt)
        if cnt > 0:
            random.shuffle(ext_surround)
            n_rep = n_rep + 1
        else:
            print('yes')
            break
    #print n_rep
    
    return ext_surround

def check_match_surrounds(surround_values):
    ext_surround = np.concatenate((surround_values[0,], surround_values[1:4,4], surround_values[4,range(4,-1,-1)], surround_values[range(3,0,-1),0]))
    dir_surround = np.concatenate((surround_values[1,1:4], surround_values[2:4,3], surround_values[3,range(2,0,-1)], surround_values[range(2,1,-1),1]))
    
    dir_surround = position_constraint(dir_surround)
    ext_surround = position_constraint2(ext_surround, dir_surround)
    
    surround_values[0,]               = ext_surround[0:5]
    surround_values[1:4,4]            = ext_surround[5:8]
    surround_values[4,range(4,-1,-1)] = ext_surround[8:13]
    surround_values[range(3,0,-1),0]  = ext_surround[13:16]
    
    surround_values[1,1:4]            = dir_surround[0:3]
    surround_values[2:4,3]            = dir_surround[3:5]
    surround_values[3,range(2,0,-1)]  = dir_surround[5:7]
    surround_values[range(2,1,-1),1]  = dir_surround[7]
    
    return(surround_values)
    





def make_random_array(values=np.array([]), n_checks=5):
    """
    return a side_length x side_length numpy array consisting of nr_int different values between min_in and max_int that are randomly arranged
    :input:
    --------
    values      - array of intensities from which to sample
    side_length - default=10
    
    :output:
    ---------
    numpy array
    """
    
    index = np.random.randint(0, len(values), n_checks*n_checks)
    
    a = map(chr, range(97, 97+n_checks))
    
    positions = {}
    cnt = 0
    ## create dictionary with coordinate (e.g. d4):index pairs
    for letters in a:
        for numbers in np.arange(1, 1+n_checks):
            positions[letters+str(numbers)] = index[cnt]
            cnt = cnt + 1
            
    surround_checks = ['b2','c2','d2','d3','d4','c4','b4','b3']
    
    ## read gray values at surround positions from position dictionary
    surround_int = []
    for surr_name in surround_checks:
        surround_int.append(positions[surr_name])
        
    ## check that no two identical gray values are next to each other
    surround_control = position_constraint(np.array(surround_int))
        
    surround_control_dict = {}
    for idx, surr_name in enumerate(surround_checks):
        positions[surr_name] = surround_control[idx]
        ## sub dictionary for immediate surround only
        surround_control_dict[surr_name] = surround_control[idx]
            
    out = np.zeros((n_checks, n_checks))
    
    for col, letters in enumerate(a):
        for row, numbers in enumerate(np.arange(1, 1+n_checks)):
            out[row, col] = values[positions[letters+str(numbers)]]
    return out, surround_control_dict



def resize_array(arr, factor):
    """
    from Torsten Betz' utils.py
    Return a copy of an array, resized by the given factor. Every value is
    repeated factor[d] times along dimension d.
    
    Parameters
    ----------
    arr : 2D array
          the array to be resized
    factor : tupel of 2 ints
             the resize factor in the y and x dimensions
    
    Returns
    -------
    An array of shape (arr.shape[0] * factor[0], arr.shape[1] * factor[1])
    """
    x_idx = np.arange(0, arr.shape[1], 1. / factor[1]).astype(int)
    y_idx = np.arange(0, arr.shape[0], 1. / factor[0]).astype(int)
    return arr[:, x_idx][y_idx, :]


def replace_image_part(stimulus=None, replacement=None, position=None):
    """
    :Input:
    ----------
    stimulus    - numpy array of original stimulus
    increment   - numpy array of to be added increment
    position    - tuple of center coordinates within stimulus where increment should be placed
    :Output:
    ----------
    """
    
    inc_y, inc_x  = replacement.shape
    pos_y, pos_x  = position
    
    x1 = int(pos_x - inc_x/2)
    x2 = int(pos_x + inc_x/2)
    y1 = int(pos_y - inc_y/2)
    y2 = int(pos_y + inc_y/2)
    
    new_stimulus = stimulus.copy()
    
    for k, c in enumerate(range(x1, x2)):
        for l, r in enumerate(range(y1, y2)):
            new_stimulus[r, c] = replacement[l, k]
    return new_stimulus


def array_to_image(stimulus_array = None, outfile_name = None, out_format = 'bmp'):
    """
    convert numpy array into image (default = '.bmp') in order to display it with vsg.vsgDrawImage
    input:
    ------
    stimulus_array  -   numpy array
    outfile_name    -   ''
    out_format      -   'bmp' (default) or 'png'
    output:
    -------
    image           -   outfile_name.out_format
    """
    im_row, im_col = stimulus_array.shape
    im_new = Image.new("L",(im_col, im_row))
    im_new.putdata(stimulus_array.flatten())
    im_new.save('%s.%s' %(outfile_name, out_format), format = out_format)


def image_to_array(fname, in_format = 'png'):
    """
    read specified image file (default: png), converts it to grayscale and into numpy array
    input:
    ------
    fname       - name of image file
    in_format   - extension (png default)
    output:
    -------
    numpy array
    """
    im = Image.open('%s.%s' %(fname, in_format)).convert('L')
    im_matrix = [ im.getpixel(( y, x)) for x in range(im.size[1]) for y in range(im.size[0])]
    im_matrix = np.array(im_matrix).reshape(im.size[1], im.size[0])
    
    return im_matrix


def load_matching_field(cnt):
    TRM = open("matchsurround.txt") # open Text-File
    
    A = np.zeros((5,5))
    cnt_A=-1
    for line in TRM:
        cnt_A=cnt_A+1
        line=line.rstrip() # remove end of line
        parts=line.split() # without an argument splits after white space
        values=[float(P) for P in parts] # transforms each string in the line in a float
        A[cnt_A,] =values
    
    if cnt== 1:
        surround_values = np.fliplr(A)
    if cnt== 2:
        surround_values = np.flipud(A)
    if cnt== 3:
        surround_values2 = np.flipud(A)
        surround_values = np.fliplr(surround_values2)
    if cnt== 4:
        surround_values = A
    
    return(surround_values)

def make_life_matches(trl_nr):
    center_size = 50
    resolution  = 24
    cnt_idx= np.array((1,2,3,4))
    random.shuffle(cnt_idx)
    cnt = cnt_idx[0]
    surround_values = load_matching_field(cnt)
    
    surround = resize_array(surround_values, (resolution, resolution))
        
    pos = np.round(surround.shape[0]/2)-1
            
    matches = {}
            
    ## modify match intensity on constant surround
    for center_int in np.arange(256):
        center = np.ones((center_size, center_size)) * center_int
        matches[center_int] = replace_image_part(surround, center, (pos, pos))

    ## returns an extra image where the center target region has -1
    ## in that way we can easily replace the values with the actual match value
    center = np.ones((center_size, center_size)) * -1
    matches[-1] = replace_image_part(surround, center, (pos, pos))
    
    return matches, surround_values



def make_single_trial_matches(trl_nr):
    """
    generate all possible matches for LUT of [0,255]
    returns:
    - reflectance index [1,12] for the checks adjacent to match
    - 256 bmps with match intensities on constant surround
    """
    resolution  = 24
    n_checks    = 5
    center_size = 50
    
    gray_values = np.array([5,10,17,27,41,57,74,92,124,150,176,200])

    surround_values, direct_surround = make_random_array(gray_values, n_checks)
    
    ## draw to scale
    surround = resize_array(surround_values, (resolution, resolution))

    pos = np.round(surround.shape[0]/2)-1
    
    if not os.path.exists('stimuli/match/trl_%03d' %trl_nr):
        os.mkdir('stimuli/match/trl_%03d' %trl_nr)

    ## modify match intensity on constant surround
    for center_int in np.arange(256):
        center = np.ones((center_size, center_size)) * center_int
        match_stimulus = replace_image_part(surround, center, (pos, pos))
    
        array_to_image(match_stimulus, 'stimuli/match/trl_%03d/match_%03d' %(trl_nr, center_int), 'bmp')
    return direct_surround


def make_life_single_trial_matches(trl_nr):
    """
    generate all possible matches for LUT of [0,255]
    returns:
    - reflectance index [1,12] for the checks adjacent to match
    - numpy array
    """
    resolution  = 24
    n_checks    = 5 # Marianne hatte 5 als Parameter
    center_size = 50
    ind         = 0
    #gray_values = np.array([5,10,17,27,41,57,74,92,124,150,176,200])
    gray_values = np.array([5,10,17,27,42,57,75,96,118,137,152,178,202])
    while ind < 1.0:
       surround_values, direct_surround = make_random_array(gray_values, n_checks)
       surround_values = check_match_surrounds(surround_values)
       # the center check should not add to the mean, therefore it is replaced by the mean
       adj_surr = np.array((surround_values[1,1], surround_values[1,2],surround_values[1,3],surround_values[2,1],surround_values[2,3],surround_values[3,1],surround_values[3,2],surround_values[3,3] ))
       surround_values[2,2] = round(np.mean(gray_values))
       match_mean    = round(np.mean(surround_values))
       surround_mean = round(np.mean(adj_surr))
       if match_mean == round(np.mean(gray_values)) and surround_mean == round(np.mean(gray_values)) :
          ind=1
       if ind==1:
          break
    
    return surround_values
    #surround_values = check_match_surrounds(surround_values)
    
    ## draw to scale
    surround = resize_array(surround_values, (resolution, resolution))
        
    pos = np.round(surround.shape[0]/2)-1
            
    matches = {}
            
    ## modify match intensity on constant surround
    for center_int in np.arange(256):
        center = np.ones((center_size, center_size)) * center_int
        matches[center_int] = replace_image_part(surround, center, (pos, pos))
    return matches, direct_surround, surround_values


def read_surround_checks(fname):
    """
    read out surround indices for matches which were not saved upon generation
    """
    surround_pos = {'b2':(30,30),'c2':(30,60),'d2':(30,90),'d3':(60,90),'d4':(90,90),'c4':(90,60),'b4':(90,30),'b3':(60,30)}
    curr_stim = image_to_array(fname, 'bmp')
    direct_surround = {}
    for idx, pos in surround_pos.iteritems():
        direct_surround[idx] = curr_stim[pos[0],pos[1]]
    return direct_surround


if __name__ == "__main__":

    fid = open('design/mm_1_matchsurr.txt', 'w')
    fid.write('b2\tc2\td2\td3\td4\tc4\tb4\tb3\n')

    for trl_nr in np.arange(240):
        match_surr = make_single_trial_matches(trl_nr)
        #match_surr = read_surround_checks('stimuli/match/%03d_match_000' %trl_nr)
        fid.write('%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\n' %(match_surr['b2'], match_surr['c2'], match_surr['d2'], match_surr['d3'], match_surr['d4'], match_surr['c4'], match_surr['b4'], match_surr['b3']))
    fid.close()

    
#    resolution  = 24
#    n_checks    = 5
#    center_size = 50
    
#    gray_values = np.array([5,10,17,27,41,57,74,92,124,150,176,200])
    
#    center_int = gray_values[np.random.randint(0,12)]

#    surround_values, direct_surround = make_random_array(gray_values, n_checks)
    
    ## draw to scale
#    surround = resize_array(surround_values, (resolution, resolution))

#    pos = np.round(surround.shape[0]/2)-1

#    center = np.ones((center_size, center_size)) * center_int
#    match_stimulus = replace_image_part(surround, center, (pos, pos))
    
#    array_to_image(match_stimulus, 'test_surround', 'bmp')

