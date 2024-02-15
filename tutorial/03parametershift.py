import pennylane as qml
from pennylane import numpy as np

dev = qml.device('default.qubit', wires = 2)

# A qnode takes a circuit (gates and measurement)
# and a device: either a simulator or a real device

#@qml.qnode(dev, diff_method = 'finite-diff')
@qml.qnode(dev, diff_method = 'parameter-shift')

def circuit(params):
    qml.RY(params[0], wires = 0)
    qml.RX(params[1], wires = 1)
    return qml.expval(qml.PauliZ(0)+qml.PauliZ(1))

params = np.array([np.pi/4, np.pi/3], requires_grad =  True)

def finite_diff_grad(params, h=1.0e-7):
    '''
    This is a classical finite difference differentiation
    '''
    gradient = np.zeros_like(params)

    for i in range(len(params)):
        # x+h
        params[i] += h
        # f(x+h)
        gradient[i] =+ circuit(params)

        # x-h
        params[i] -= 2*h
        # f(x-h)
        gradient[i] -= circuit(params)

        # (f(x+h)-f(x-h))/2h
        gradient[i] /= 2*h

        params += h

    return gradient
    
def parameter_shift_grad(params, s=np.pi/3):
    '''
    This is a classical finite difference differentiation
    '''
    gradient = np.zeros_like(params)

    for i in range(len(params)):
        # x+s
        params[i] += s
        # f(x+s)
        gradient[i] =+ circuit(params)

        # x-s
        params[i] -= 2*s
        # f(x-s)
        gradient[i] -= circuit(params)

        # (f(x+s)-f(x-s))/2s
        gradient[i] /= 2*np.sin(s)

        params += s

        return gradient
    
print(parameter_shift_grad(params))
print(qml.grad(circuit)(params))