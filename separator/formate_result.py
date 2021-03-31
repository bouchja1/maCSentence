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

""" This module includes 'formate_result' function, which transforms list of strings (first parameter) to one string. Strings are separated by string given as the second parameter and other symbols are added according to the third parameter. If the third parameter has forbidden value, the fourth parameter is returned. """

def formate_result(sentences, sentence_separator, switch):
    if switch < 1 or switch > 3: #Switch has forbidden value
        raise ValueError("Switch has forbidden value")    
    
    result = ""
    number = 1
    
    for sentence in sentences:
        if switch != 3 and number > 1:
            result = result + sentence_separator
        
        if switch == 1: #Numbered list
            result = result + str(number) + ". " + sentence
        elif switch == 2: #Non-numbered list
            result = result + sentence
        elif switch == 3: #Continuous text
            result = result + sentence + " "
    
        number += 1
    
    return result.strip()
