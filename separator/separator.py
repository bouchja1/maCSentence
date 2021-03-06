#!/usr/bin/env python
#encoding=utf-8 (pep 0263)

#Copyright (c) 2015, Petr Machovec
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#
#2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
#3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

""" This module includes 'separate' function, which reads the text given as the first parameter and separates it into the list of sentences. This list is then returned. It also provides main function to execute separation from the bash or command line. """

import argparse
import sys
import os

from formate_result import formate_result

def separate(input_string):
    file_not_found = False
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    message = ""
    #abbreviations set - common czech abbreviations:
    try:
        with open("separator_data/abbreviations.txt", 'r') as abbreviations_file:
            abbreviations = frozenset(line.strip().decode("utf-8") for line in abbreviations_file)

    except IOError:
        message += "Soubor abbreviations.txt nenalezen"
        file_not_found = True

    #separators set - symbols that separate sentences:
    try:
        with open("separator_data/separators.txt", 'r') as separators_file:
            separators = frozenset(line.strip().decode("utf-8") for line in separators_file)

    except IOError:
        message += "; Soubor separators.txt nenalezen"
        file_not_found = True

    #starters set - symbols that can appear at the beginning of a sentence:
    try:
        with open("separator_data/starters.txt", 'r') as starters_file:
            starters = frozenset(line.strip().decode("utf-8") for line in starters_file)

    except IOError:
        message += "; Soubor starters.txt nenalezen"
        file_not_found = True

    #terminators set - symbols that can appear at the end of a sentence (after a separator)
    try:
        with open("separator_data/terminators.txt", 'r') as terminators_file:
            terminators = frozenset(line.strip().decode("utf-8") for line in terminators_file)

    except IOError:
        message += "; Soubor terminators.txt nenalezen"
        file_not_found = True

    if file_not_found:
        message = message.strip(";").strip()
        raise IOError(message)

    input_string = input_string.strip().decode("utf-8")
    sentences = list()
    begin = 0
    end = 0
    help_begin = 0
    help_end = 0
    sep_pos = 0
    help_string = ""
    make_sentence = False
    upper = False

    while (end < len(input_string)): #Big while-cycle reading the whole input_string char after char and performing all the magic
        if input_string[end] == '\n': #New line - end of a paragraph
            sentence = input_string[begin:end].strip()
            if len(sentence) > 0:
                sentences.append(sentence)
            begin = end+1

            #The last word of the paragraph can be a sign (one word with small letter at the beginning), this must be checked, but only if the sentence was really added (i.e. if it's length is bigger than 0)
            if len(sentence) > 0:
                help_begin = end-1
                help_end = end-1

                while (input_string[help_end].isspace()): #Moving help_end to the end of the paragraph text
                    help_end -= 1

                if not input_string[help_end] in separators: #Text of the paragraph is not finished by a separator, there can be a sign
                    help_begin = help_end

                    while (help_begin >= 0 and not input_string[help_begin].isspace()): #Moving help_begin before the beginning of the last word before the new line (possible sign)
                        help_begin -= 1

                    sign = input_string[help_begin+1:help_end+1] #Last word of the paragraph - possible sign

                    if sign[0].islower(): #First char of the possible sign is lower - it was not separated as a sentence before

                        while (input_string[help_begin].isspace()): #Moving help_begin to the end of the text before the possible sign
                            help_begin -= 1

                        if input_string[help_begin] in separators: #There is a separator before the possible sign - it really is a sign and must be separated
                            sentences.pop()
                            sentence = sentence[0:(len(sentence)-len(sign))].strip()
                            sentences.append(sentence)
                            sentences.append(sign)



        elif input_string[end] in separators: #Sentence separating char (separator) was detected, it depends what follows in the text
            sep_pos = end

            while (end < len(input_string)-1 and
                   input_string[end+1] in terminators): #Skipping terminators
                end += 1

            help_end = end+1
            make_sentence = False

            while (help_end < len(input_string) and
                   (input_string[help_end].isspace() or (input_string[help_end] in starters)) and
                   input_string[help_end] != '\n'):
                help_end += 1 #Moves help_end to the first 'sentence-begin-deciding' char behind the separator (starters act like whitespaces, but they are not trimmed when at the beginning of a sentence)

            if help_end >= len(input_string): #There are only whitespaces or starters mesh after the separator - end of the text
                sentence = input_string[begin:end+1].strip()
                if len(sentence) > 0:
                    sentences.append(sentence)
                end = help_end-1

            elif input_string[help_end] == '\n': #There is a new line after the separator - will be solved in next round
                end = help_end-1

            elif (input_string[help_end].isupper() or
                  input_string[help_end].isdigit()): #There is an upper char or digit after the separator

                upper = input_string[help_end].isupper()
                if input_string[end] != '.': #The separator is not a dot, it is the end of the sentence
                    make_sentence = True

                else: #The separator is a dot, it can be the end of an abbreviation or a part of an order number
                    help_begin = sep_pos-1
                    help_end = sep_pos-1

                    while (input_string[help_end].isspace()): #Skipping whitespaces before the dot
                        help_begin -= 1
                        help_end -=1

                    while (help_begin >= 0 and
                           not input_string[help_begin].isspace() and
                           input_string[help_begin] != '.'): #Moving help_begin to the beginning of the word before the dot
                        help_begin -= 1

                    help_begin += 1

                    #The word before the dot is to be extracted, it can start with any of the starters and these must be ommited
                    while (help_begin < help_end and input_string[help_begin] in starters):
                        help_begin += 1

                    help_string = input_string[help_begin:help_end+1] #The word before the dot

                    if ((len(help_string) != 1 or help_string.isdigit() or help_string in terminators) and
                        not help_string.lower() in abbreviations): #The word before the dot is not an abbreviation

                        if upper: #There is an upper char after the dot, all prerequisities to make a sentence are satisfied
                            make_sentence = True
                        elif (len(help_string) > 0 and
                              not help_string[len(help_string)-1].isdigit()): #There is a digit after the dot, the word before the dot  cannot end with a digit to make a sentence
                            make_sentence = True

            if make_sentence:
                sentence = input_string[begin:end+1].strip()
                if len(sentence) > 0:
                    sentences.append(sentence)
                begin = end+1

        end += 1 #End of the big while-cycle

    help_end = end-1 #When the whole text is not ended by a separator, last sentence is not included. This must be solved separately.
    while (help_end >= 0 and
           (input_string[help_end] in terminators or input_string[help_end].isspace())):
        help_end -= 1

    if help_end >= 0 and not input_string[help_end] in separators:
        sentence = input_string[begin:end].strip()
        if len(sentence) > 0:
            sentences.append(sentence)

    return sentences

if __name__ == "__main__":
    text = sys.argv[1]
    output_texts = separate(text)

    result = formate_result(output_texts, "\SEPARATOR", 2)
    try:
        print result.encode("utf-8")
    except IOError: #This is not nice, but it makes the program work properly on Windows
        pass
    exit(1)

