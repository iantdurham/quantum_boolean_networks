#############################################
#                                           #
# Traces out individual qubits from system  #
# to give list of individual states         #
# for each qubits.                          #
#                                           #
#############################################

def state_trace(state,num_qubits):

    delta = 1e-3                                                    # General accuracy bound

    state_list = []

    for num in range(num_qubits):
        qubit = state.ptrace(num)
        qubit_mat = qubit.full()
        if (abs(qubit_mat[0, 0] - 1.0) < delta) and (abs(qubit_mat[1, 1] - 0.0) < delta):
            state_list.append('0')
        elif (abs(qubit_mat[1, 1] - 1.0) < delta) and (abs(qubit_mat[0, 0] - 0.0) < delta):
            state_list.append('1')
        elif (abs(qubit_mat[0, 0] - 0.5) < delta) and (abs(qubit_mat[0, 1] - 0.5) < delta):
            state_list.append('+')
        elif (abs(qubit_mat[0, 0] - 0.5) < delta) and (abs(qubit_mat[0, 1] + 0.5) < delta):
            state_list.append('-')
        elif qubit.purity() < 1:
            state_list.append('M')
        else:
            state_list.append('U')

    return state_list