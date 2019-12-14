# PokerAssistant
Program which will help you monitor the game.

### Overview
This program is suited to [*No Limit Texas Holdem*](https://www.poker-king.com/dictionary/no-limit-texas-holdem/).
It can show your wining chance wrt **cards in your hand**, **cards on
the table** and **number of your opponents** (not implemented yet).

### Starting working
To start using this program you just need to call `game.start()` method
(Game class is located in **poker/game_stages.py**).  
Once you do it program will offer you to enter info about cards which are in your **hand**.

**Example :**  

*--- Hand ---  
Card 1, val : 12  
Card 1, suit : 1  
Card 2, val : 4  
Card 2, suit : 2*  

Here every card is defined by 2 numbers :
- **Val**, which is card rank. Can be one of [2, 14] int interval. Meaning:
    - *2 <= val <= 10* : card rank is actually val
    - *val == 11* : card rank is J
    - *val == 12* : card rank is Q
    - *val == 13* : card rank is K
    - *val == 14* : card rank is A
- **Suit**, which is card suit. Can be one of [0, 3] int interval. There is no 
strict definition that concrete number represent concrete suit, so you define it by
yourself. The most important here is that if you define :hearts: as 0, then 
in this game you should define **all** :hearts: as 0. Of course you can use this standard
definition if you don`t want to think up your own definition. I will use this
definition in my examples.
    - *suit == 0* : heart :hearts:
    - *suit == 1* : diamond :diamonds:
    - *suit == 2* : club :clubs:
    - *suit == 3* : spade :spades:

So, in example from above we can see **Q**:diamonds: and **4**:clubs:.
After that we will enter into **pre-flop** section.  

**Example :**  

*--- Pre-flop ---  
Win prob: 47.70%  
Opening flop  
Card 1, val :*  

You can see estimation of your winning chance wrt cards in your hand.
Now you can enter 3 flop cards and we will continue in **flop** section.  

**Example :**  

*Opening flop  
Card 1, val : 2  
Card 1, suit : 0  
Card 2, val : 12  
Card 2, suit : 0  
Card 3, val : 4  
Card 3, suit : 0  
--- Flop ---  
Win prob: 73.47%  
Opening turn  
Card val :*  

As you can see we have 2 pairs now (Q and 4) and win prob is increased significantly.
Let`s move on to **turn** section.  

**Example :**  

*Opening turn  
Card val : 7  
Card suit : 0  
--- Turn ---  
Win prob: 55.24%  
Opening river  
Card val :*  

Not good for us. We have 4 :hearts: cards on the table. This leads to increasing
flush chance and, because our 2 pairs is weaker than opponent`s possible flush,
our winning chance is decreasing. Howbeit, we move on to **river** section.

**Example :**  

*Opening river  
Card val : 4  
Card suit : 3  
--- River ---  
Win prob: 99.24%* 

What a luck! We have full house. It is stronger then any flush, so you can forget
about this danger. 99.24% winning chance means that you now are the absolute favorite.