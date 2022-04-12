#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 19:35:49 2021

@author: mbialoncz
"""

import os
import requests
import re
import pandas as pd

png_dictionary = {
 'game_url' : re.compile(r'\[Site \"(?P<url>.*)\"\]'),
 'white_player': re.compile(r'\[White \"(?P<user>.*)\"\]'),
 'black_player': re.compile(r'\[Black \"(?P<user>.*)\"\]'),
 'white_elo' : re.compile(r'\[WhiteElo \"(?P<white_elo>\d+)\"\]'),
 'black_elo' : re.compile(r'\[BlackElo \"(?P<black_elo>\d+)\"\]'),
 'result' :re.compile(r'\[Result \"(?P<result>(1|0|1/2)\-(1|0|1/2))\"\]'),
 'moves': re.compile(r'(?P<moves>(1.) .*)'),
 'date' : re.compile(r'\[UTCDate \"(?P<date>.*)\"\]'),
 'time' : re.compile(r'\[UTCTime \"(?P<time>.*)\"\]'),
 
}

class LichessGame(object) :
    
    def LichessGame(self) :
        pass
    

def downloadGames(user, max_number) :
    url = "http://lichess.org/games/export/"+user+"?max="+str(max_number)
    print(url)
    r = requests.get(url, allow_redirects=True, verify=False)
    open(user,"wb").write(r.content)
    
def parse_line(line) :
    for key, reg_obj in png_dictionary.items() :
        match = reg_obj.search(line)
        if match :
            return key, match
    return None, None
    
def processFile(pgn_file, user) :
    
    data = []
    row_dict={}
    features = 8
    with open(pgn_file,"r") as file_obj :
        line = file_obj.readline() 
        
        while line :
            key, match = parse_line(line)

            if key == 'game_url' :
                row_dict['url'] = match.group('url')
            
            elif key == 'white_player' :
                row_dict['white_player'] = match.group('user')
            
            elif key == 'black_player' :
                row_dict['black_player'] = match.group('user')
                
            elif key == 'result' :
                res = match.group('result')
                if res =='1-0' :
                    row_dict['white_result'] = 1
                    row_dict['black_result'] = 0
                elif res == '0-1' :
                    row_dict['white_result'] = 0
                    row_dict['black_result'] = 1
                
                else :
                    row_dict['white_result'] = 0.5
                    row_dict['black_result'] = 0.5
            elif key == 'date' :
                row_dict['date'] = match.group('date')
                

            elif key == 'time' :
                row_dict['time'] = match.group('time')
                
            elif key == 'moves' :
                row_dict['moves'] = match.group('moves')
                

            if len(row_dict) == features :
                data.append(row_dict)
                row_dict = {}
                
            
            line = file_obj.readline()
    
    return pd.DataFrame(data)

def checkBegin(begin, moves) :
    if len(begin) > len(moves) :
        raise ValueException("Length of beginning bigger then length of game!")
    
    return moves[:len(begin)] == begin
    

def listAllOpeningsWhite(user, begin, pd) :
    pass
    
    
    
    

#downloadGames("lfceline", 2000)

#data = processFile("lsmolin", 'lsmolin')


    