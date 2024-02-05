from random import randint
import numpy as np

moves = {'@':0,'#':1,'%':2}

scoreboard = {'Player':0,'Computer':0}

first = randint(0,2)

def game(play,com): #Lets simplify: now this func takes only [0:2] as arg
    
    rival_move = list(moves.keys())[list(moves.values()).index(com)]
    print ('Computer :' + rival_move + '\n')
    if play == com:
        print ('Tie')
        return 2
    elif play == 1:
        if com == 2:
            print ('Scissor cuts paper \n ')
            return 1
        else:
            print ('Paper covers rock \n ')
            return 0
    elif play == 2:
        if com == 0:
            print ('Rock smashes scissors \n ')
            return 1
        else:
            print ('Scissor cuts paper \n ')
            return 0
    else:
        if com == 1:
            print ('Paper covers rock \n ')
            return 1
        else:
            print ('Rock smashes scissors \n ')
            return 0
    # Now this returns 0 if Player wins, 1 if Com wins and 2 if they tie
    
    ######################
    
    # The next function just updates and prints the scoreboard

def update_score(res):
    if res == 0:
        scoreboard['Player'] = scoreboard['Player'] + 1
    elif res == 1:
        scoreboard['Computer'] = scoreboard['Computer'] + 1
    for i in scoreboard:
        print (i, scoreboard[i])

    ######################
    
    # The next function defines a match, asking the player its choice, making sure it's valid, calls a game, calls a scoreboard update and returns a list with the winner and the player's choice

def match(Ai):
    ask = str(input('\n Rock (@), Paper(#), Scissors(%) \nPlayer:'))
    if ask in ('%','#','@'):
        choice = moves[ask]
        result = game(choice,Ai)
    else:
        invalid = True
        while invalid:
            ask = str(input('You must enter any of these symbols: @ (Rock), # (Paper) or % (Scissors) \nPlayer:'))
            if ask in ('%','#','@'):
                invalid = False
                choice = moves[ask]
                result = game(choice,Ai)                
            else:
                invalid = True
    update_score(result)
    return[result,choice]
    
    ######################
    
    # This is the simplest AI you can have that barely improves a random choice

def fai(mat):
    if mat[0] in (0,2):
        if mat[1] == 0:
            return 2
        else:
            return(mat[1]-1)
    elif mat[0] == 1:
        return mat[1]
        
    ######################
    
    # This function calls all other functions to start the game and determines when to stop playing. It returns the playlog for research purposes.


def championship():
    print(" Let's play Rock, Paper, Scisors! \n ")
    playing = True
    playlog=[[3,3]]
    log=match(first)
    while playing:
        while log[0] == 2:            
            playlog=np.append(playlog,[log],axis=0)
            log=match(fai(log))
        winner = (scoreboard['Player'] - scoreboard['Computer'])
        matches = (scoreboard['Player'] + scoreboard['Computer'])
        if abs(winner) >= 2:
            playing = False
            if winner > 0:
                print('Player wins!')
            else:
                print('AI wins!')
            playlog=np.append(playlog,[log],axis=0)
        elif abs(winner) == 1:
            follow = str(input('Best out of %s ? (Y/N) \n ' % (matches + 2)))
            if follow.upper() == 'N':
                playing = False
                if winner > 0:
                    print('Player wins!')
                else:
                    print('AI wins!')
                playlog=np.append(playlog,[log],axis=0)
            else:
                print('Thats a YES!')
                playlog=np.append(playlog,[log],axis=0)
                log=match(fai(log))                
        else:
            playlog=np.append(playlog,[log],axis=0)
            log=match(fai(log))
    np.savetxt('playlog.txt',playlog,fmt='%i')
                    
championship()

