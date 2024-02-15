import pennylane as qml
from pennylane import numpy as np


# In this code we are going to optimize a function
dev = qml.device('default.qubit', wires = 1)

@qml.qnode(dev)

def circuit(theta):
    qml.PauliX(wires = 0)
    qml.RY(theta, wires = 0)
    return qml.expval(qml.PauliZ(wires = 0))

# We want to get the angle that minimizes the expected
# value. It starts at -2

theta = np.array([-2.], requires_grad = True)

# we can use different optimizers

opt = qml.GradientDescentOptimizer(stepsize = 0.1)

# For each iteration we find a new value of theta
n_it = 100
for it in range(n_it):
    theta, prev_cost = opt.step_and_cost(circuit,theta)
    if it%10==0 : 
        print('Theta: ', theta, 'Cost: ', circuit(theta))

# Note that the cost of our optimization is the circuit,
# as it gives the expected value of Z, and that's what
# we want to optimize