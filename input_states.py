#############################################
#                                           #
# Possible input states and function for    #
# randomly selecting from list.             #
#                                           #
#############################################

# Import packages
from qutip import basis, bell_state, ghz_state, w_state
from random import randrange

# Basis states (for both classical and quantum)
zero = basis(2,0) * basis(2,0).dag()
one = basis(2,1) * basis(2,1).dag()

# Normalized fully general quantum state
plus0 = (basis(2,0) + basis(2,1)).unit()
plus = plus0 * plus0.dag()
minus0 = (basis(2,0) - basis(2,1)).unit()
minus = minus0 * minus0.dag()

# Ancilla qubit
ancilla = zero

# GHZ state
ghz0 = ghz_state(N=3)
ghz = ghz0 * ghz0.dag()

# W state
w0 = w_state(N=3)
w = w0 * w0.dag()

# Function for randomly returning a classical state
def class_random():
    q = randrange(2)
    if q == 0:
        in_state = zero
        state_name = '0'
    else:
        in_state = one
        state_name = '1'
    return in_state, state_name

# Function for randomly returning a general state
def input_random():
    q = randrange(4)
    if q == 0:
        in_state = zero
        state_name = '0'
    elif q == 1:
        in_state = one
        state_name = '1'
    elif q == 2:
        in_state = plus
        state_name = '+'
    else:
        in_state = minus
        state_name = '-'
    return in_state, state_name

# Function to return a Bell state
def input_bell():
    q = randrange(4)
    if q == 0:
        in_state = bell_state(state='00')
        state_name = 'B_00'
    elif q == 1:
        in_state = bell_state(state='01')
        state_name = 'B_01'
    elif q == 2:
        in_state = bell_state(state='10')
        state_name = 'B_10'
    else:
        in_state = bell_state(state='11')
        state_name = 'B_11'
    return in_state, state_name