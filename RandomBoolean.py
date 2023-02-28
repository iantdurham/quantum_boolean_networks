# Program to create autonomous, random Boolean networks of specifically K=2 inputs.
#
# Author: Ian Durham
#
# Package requires the following:
# input_states.py
# boolean_gates.py
# state_list.py
#
####################################################################################

# Import packages

from numpy import prod
from numpy.fft import fft
from qutip import tensor,entropy_vn,sigmax,sigmaz,qeye
from random import choice
from math import log
from pylab import plot,show,xlabel,ylabel,table,title
from boolean_gates import *
from input_states import *
from state_list import *

delta = 1e-3                                                    # General accuracy bound

#############################################
#                                           #
# User input (sets size and time)           #
#                                           #
#############################################

#N = int(input("Please input the number of gates:"))
#t = int(input("Please input the number of time steps:"))
#I = int(input("Press 1 for purely classical inputs and press 2 for general inputs:"))

N = 2
t = 40
I = 2

#############################################
#                                           #
# Generate network and initial state        #
#                                           #
#############################################

# Randomly select N gates from list func[] and
# check for number of qubits in each gate in order
# to store logical qubit indices

# Lists to hold functions and their names for random call
#func = [I,NOR,f3,f4,AND,XNOR,f7,f8,f9,f10,XOR,OR,f13,f14,NAND,f16]
func = [f1,NOR,AND,XNOR,XOR,OR,NAND]
#func_names = ['I','NOR','f3','f4','AND','XNOR','f7','f8','f9','f10','XOR','OR','f13','f14','NAND','f16']
func_names = ['I','NOR','AND','XNOR','XOR','OR','NAND']

gates = []
gates_names = []
index = 0
ancilla_list = []                                   # Keeps track of ancilla qubits
for i in range(N):
    n = randrange(7)
    gates.append(func[n])
    gates_names.append(func_names[n])
    gate_size = prod(func[n].dims[0])
    gate_qubits = int(log(gate_size,2))
    index += gate_qubits
    if abs(gate_qubits - 3.0) < delta:
        ancilla_list.append(index-1)

gates = [XNOR,NOR] # <-- fill this manually and uncomment to specify exact gates
gates_names = ['XNOR','NOR'] # <-- use this to name manually entered gates for printing
ancilla_list = [4] # <-- use this to manually enter the ancilla qubits
print("Gates: ",gates_names)

# Tensor the gates to create full network

network = gates[0]
for j in range(1,N):
    network = tensor(network,gates[j])

# Check network size to determine number of qubits in system and create index list

size = prod(network.dims[0])
num_qubits = int(log(size,2))
qubit_index = []
for w in range(num_qubits):
    qubit_index.append(w)

# Randomly choose input qubit states by calling input_random() but ensuring any acillas are set to 0

states = []                                             # QuTiP objects
for k in range(num_qubits):
    if k in ancilla_list:
        states.append(ancilla)
    else:
        if I==1:
            state, state_name = class_random()
        else:
            state, state_name = input_random()
        states.append(state)

states = [plus,one,one,minus,zero] # <-- uncomment this to specify initial input states

# Check the number of states in the system (not necessarily the same as the number of qubits)

num_states = len(states)

# Tensor input qubit states to create initial system state

initial_state = states[0]
for l in range(1,num_states):
    initial_state = tensor(initial_state,states[l])

states_in = state_trace(initial_state,num_states)
print("Initial states: ",states_in)

# Generate a random permutation wiring for the network

wiring = []
for m in range(num_qubits):
    p = choice(list({x for x in range(0, num_qubits)} - set(wiring)))      # Random number not previously chosen
    wiring.append(p)
wiring = [2,1,0,4,3] #<-- fill this manually and uncomment to specify exact wiring
print('Wiring: ',wiring)

# Permute initial state using wiring to create network input state.
# This is required in order to find consistency in state cycles.

input_state = initial_state.permute(wiring)

# Create associated list

input_state_list = state_trace(input_state,num_qubits)

print("Input: ",input_state_list)

#############################################
#                                           #
# Evolve network forward in time            #
#                                           #
#############################################

entropy = []
time = []
data = []

# Store system states

data_file = open("unperturb.txt","w")
data_file.writelines(input_state_list)
data_file.write("\n")

for v in range(0,t+1):

# Perform network operation

    output_state = network * input_state * network.dag()

# Apply perturbation (currently not random -- comment out if no perturbation)

#    if v == 11:
#        pert = tensor(sigmax(),qeye(2),qeye(2),qeye(2),qeye(2),qeye(2),qeye(2),qeye(2))
#        out_pert = pert * output_state * pert.dag()
#        output_state = out_pert

# Trace out each qubit state

    output_state_list = state_trace(output_state,num_qubits)

    data_file.writelines(output_state_list)
    data_file.write(" ")
    data_file.writelines(str(v))
    data_file.write("\n")

#    print(output_state_list, " ", v)

# Calculate the multipartite mutual information of the network

    SA = 0
    for g in range(num_qubits):
        SA += entropy_vn(output_state.ptrace(g))
    S = entropy_vn(output_state)
    QMI = SA - S

    entropy.append(QMI)
    time.append(v)
    data.append([v,entropy])

# Set next input step -- comment out if resetting ancillas

    input_state = output_state.permute(wiring)

# Reset ancilla qubits

#    next_state = output_state.permute(wiring)
#    input_state = next_state.ptrace(0)
#    for s in range(1,num_qubits):
#        if s in ancilla_list:
#            input_state = tensor(input_state,ancilla)
#        else:
#            input_state = tensor(input_state,next_state.ptrace(s))

data_file.close()

if I==2:
    plot(time,entropy)
    xlabel("Time step")
    ylabel("Multipartite mutual information")
    cell_text = [["Initial input states:",states_in],["Gates in network:",gates_names],["Wiring:",wiring]]
    table(cellText=cell_text,cellLoc='left',loc='top',edges='open')
    show()

    c = fft(entropy)
    plot(abs(c))
    xlabel("Frequency")
    ylabel("Multipartite mutual information, frequency domain")
    cell_text = [["Initial input states:", states_in],
                 ["Gates in network:", gates_names], ["Wiring:", wiring]]
    table(cellText=cell_text, cellLoc='left', loc='top', edges='open')
    show()
else:
    print("Gates in network:",gates_names)