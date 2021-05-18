

def handle__unregistered(message):
    """
Actually, this can be 'in' for no context, not registered
    """
    pass

def handle__whats_your_name(message):
    """
A CONTEXT IS TIED TO THIS IN METHOD
    """
    pass

def handle__menu(message):
    """
    Can fan out to either choices

the fanning out logic can be done here
context switching codes can also be moved here










A CONTEXT IS TIED TO THIS IN METHOD - in a dictionary, so we know there's just 1 context per method


OUT METHODS ARE TIED TO CHOICES, OR if there are no choices, then we have only
one out method


    what if the user abandons? the context will expire after some time

    what if the user has more than 1 active context? the protocol is to have
    the user confirm which context is he referring to
    """
    pass

# ----- Start: Flow following menu option 1 (find buyer) -----

# depending on the choice of menu, I want to send the right messages

def OUT__what_sell(message):
    pass

def OUT__what_sell_availability(message):
    pass

def OUT__what_sell_location(message):
    pass

def OUT__confirm_sell_packing(message):
    pass

def OUT__what_sell_packing(message):
    pass


# ----- End: Flow following menu option 1 (find buyer) -----



# Can I have data structures
# graph structure

# a points to b
"""


lambda conditions for options is passed to each handle
THIS MAKES IT HARDER TO DEBUG










A CONTEXT IS TIED TO THIS IN METHOD
OUT METHODS ARE TIED TO CHOICES, OR if there are no choices, then we have only
one out method



handler is configured to handle a context - one to one
when a message comes in
a handler has 0 or more choices















say, a points to b
b points to c or d


the graph has a set of inputs to get started
let this be the message object

the graph has a starting point - say node a

a has conditions
b has conditions
c has conditions


a's condition is that either ph or usr is new
b's condition is that the user has an active context


what if 2 nodes are in conflict?, the one with the shortest path 


















I know the user's context


What is a 'context'
Messages I have sent the user, and is awaiting a reply

What if the user has 2 running contexts? how do I ascertain which context
is the user replying to?
- I can classify the user's message body
- I can verify with the user - by sending a testing question
- the same can be applied to 









"""