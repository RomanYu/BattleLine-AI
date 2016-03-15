# TouchPal Internship Hack Marathon 2015 summer

### Introduction

1.  You should prepare an executable application for this game.
2.  Modify config.json and indicate the application runtime.
3.  run ./judge.py to play the game.

### Protocol

Card Name:
There are 60 cards:
{A..F} * {1..10} (letter means color)

There are 9 regions:
R * {0..8}

There is only one action for player to exetute:
act $region $card
(please make sure do flush after write)

Player will receive 3 kinds of message:

1.  cardget $card        #You got a new card $card.
2.  rival $region $card  #Your rival put a $card on $region
3.  youwin / youlose

In each turn, you will receive a line containing an integer N whitch indicates the number of messages you will be sent.

And the following N lines describe the messages.

(Judge will choose the offensive player randomly. So if the first number you get if 7, it means you are on the offensive, 8 means defensive.)

Once you read the message, you have 30 secs to give the action.
No tolerance for timeout or error output.

