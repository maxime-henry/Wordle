#!/usr/bin/.venv python
# -*- coding: utf-8 -*- 

import pandas as pd
import collections
import math
from itertools import product
from tqdm import tqdm




def filter_possible_words(first_letter= None, nbletters=None):
    data = pd.read_csv('listemots.csv',index_col=False)
    newdata = data[data['nblettres']== nbletters]
    if first_letter!=None:
        filter_words = [word for word in newdata['ortho'] if word.lower()[0] == first_letter.lower()]
        newdata = newdata[newdata['ortho'].isin(filter_words)]
    newdata=newdata[['ortho','freqlivres']].reset_index()
    return(newdata)



def pattern_combinaisons(nbletters):
    pattern =[]
    hey = product(range(3), repeat=nbletters)
    for i in list(hey):
        pattern.append(i)
    return(pattern)

# Filtre basé sur la réponse de SUTOM
def filter_words(words, guess, score):
    new_words = []
    for word in words:
        # The pool of characters that account for the PRESENT ones is all the characters
        # that do not correspond to CORRECT positions.
        pool = collections.Counter(c for c, sc in zip(word, score) if sc != 2)
        for char_w, char_g, sc in zip(word, guess, score):
            if sc == 2 and char_w != char_g:
                break  # Word doesn't have the CORRECT character.
            elif char_w == char_g and sc != 2:
                break  # If the guess isn't CORRECT, no point in having equal chars.
            elif sc == 1:
                if not pool[char_g]:
                    break  # Word doesn't have this PRESENT character.
                pool[char_g] -= 1
            elif sc == 0 and pool[char_g]:
                break  # ABSENT character shouldn't be here.
        else:
            new_words.append(word)  # No `break` was hit, so store the word.

    return (new_words)

def lets_think(data, pattern):
    result=data.copy()
    suivi = 0 
    resume = []
    for mot, popularite in zip(tqdm(data.ortho), data.freqlivres):
        #print("Mot : ",mot," ",round(suivi/len(data)*100,2)," %")
        suivi += 1
        stat = []
        for pat in range(len(pattern)):
            avant=len(data)
            mot_filtre=filter_words(  data['ortho']  ,  mot , pattern[pat])
            apres=len(mot_filtre)
            fraction = apres/avant
            if fraction==0:
                bit=0
                info=0
            else:
                bit = -math.log(fraction, 2)
                info = fraction * bit * sigmoid(popularite)
            stat.append(info)
        entropie = sum(stat)
        resume.append(entropie)
        #print("Mot :",mot," ",round(suivi/len(data)*100,2)," % - Score = ", entropie)
    result['info']=resume
    print(result.sort_values(['info', 'freqlivres'], ascending = False).head())
    return(result)



import math

def sigmoid(x):
  return 1 / (1 + math.exp(-x))