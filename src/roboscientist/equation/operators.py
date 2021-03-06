import numpy as np
import torch
from scipy.special import lambertw

class Operator:
    def __init__(self, func, name, repr, arity, complexity):
        self.func = func
        self.name = name
        self.repr = repr
        self.arity = arity
        self.complexity = complexity


def _SAFE_LOG_FUNC(x):
    if isinstance(x, torch.Tensor):
        return torch.where(x > 0.0001, torch.log(torch.abs(x)), torch.tensor(0.0))
    else:
        with np.errstate(divide='ignore', invalid='ignore'):
            return np.where(x > 0.0001, np.log(np.abs(x)), 0.0)


def _SAFE_DIV_FUNC(x, y):
    if isinstance(x, torch.Tensor) or isinstance(y, torch.Tensor):
        x = torch.as_tensor(x)
        y = torch.as_tensor(y)
        return torch.where(torch.abs(y) > 0.001, torch.divide(x, y), torch.tensor(0.0))
    else:
        with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
            return np.where(np.abs(y) > 0.001, np.divide(x, y), 0.0)


def _SAFE_SQRT_FUNC(x):
    if isinstance(x, torch.Tensor):
        return torch.where(x > 0, torch.sqrt(torch.abs(x)), torch.tensor(0.0))
    else:
        with np.errstate(divide='ignore', invalid='ignore'):
            return np.where(x > 0, np.sqrt(np.abs(x)), 0.0)


def _SAFE_EXP_FUNC(x):
    if isinstance(x, torch.Tensor):
        return torch.where(x < 10, torch.exp(x), torch.exp(torch.tensor(10.0)))
    else:
        with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
            return np.where(x < 10, np.exp(x), np.exp(10))


def _SAFE_POW_FUNC(x, y):
    if isinstance(x, torch.Tensor) or isinstance(y, torch.Tensor):
        x = torch.as_tensor(x)
        y = torch.as_tensor(y)
        coeff = torch.where(torch.eq(torch.fmod(y, 1), 0), (-1) ** y, 0.0)
        return torch.where(x > 0, _SAFE_EXP_FUNC(y * _SAFE_LOG_FUNC(x)),
                           coeff * _SAFE_EXP_FUNC(y * _SAFE_LOG_FUNC(torch.abs(x))))
    else:
        with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
            coeff = np.where(np.equal(np.mod(y, 1), 0), (-1) ** y, 0.0).astype(np.float64)
            return np.where(x > 0, _SAFE_EXP_FUNC(y * _SAFE_LOG_FUNC(x)),
                            coeff * _SAFE_EXP_FUNC(y * _SAFE_LOG_FUNC(np.abs(x))))


OPERATORS = {


    'log**2': Operator(
        func=lambda x: _SAFE_LOG_FUNC(x) * _SAFE_LOG_FUNC(x) ,
        name='log**2',
        repr=lambda x: f'(log**2({x}))',
        arity=1,
        complexity=3,
    ),

    'X**-2': Operator(
        func=lambda x: _SAFE_DIV_FUNC(_SAFE_DIV_FUNC(1 , x), x ),
        name='X**-2',
        repr=lambda x: f'(X**-2({x}))',
        arity=1,
        complexity=3,
    ),


    'sin**2': Operator(
        func=lambda x: np.sin(x) * np.sin(x) ,
        name='sin**2',
        repr=lambda x: f'(sin**2({x}))',
        arity=1,
        complexity=3,
    ),

    'cos**2': Operator(
        func=lambda x: np.cos(x) * np.cos(x) ,
        name='cos**2',
        repr=lambda x: f'(cos**2({x}))',
        arity=1,
        complexity=3,
    ),


    'add_oscil': Operator(
        func=lambda x,y,z,r:   _SAFE_DIV_FUNC(np.cos(x) * np.cos(x) , z) + r*_SAFE_EXP_FUNC(-y) ,
        name='add_oscil',
        repr=lambda x,y,z,r: f'(add_oscil({x,y,z,r}))',
        arity=4,
        complexity=5,
    ),


    'OSCE': Operator(
        func=lambda x,y,z: _SAFE_DIV_FUNC(np.cos(x) * np.cos(x) * _SAFE_EXP_FUNC(-y) , z*z),
        name='OSCE',
        repr=lambda x,y,z: f'(OSCE({x,y,z}))',
        arity=3,
        complexity=5,
    ),

    'OSCL': Operator(
        func=lambda x,y,z: _SAFE_DIV_FUNC(np.cos(x) * np.cos(x) * _SAFE_LOG_FUNC(y) * _SAFE_LOG_FUNC(y), z*z),
        name='OSCL',
        repr=lambda x,y,z: f'(OSCL({x,y,z}))',
        arity=3,
        complexity=5,
    ),

    'LWF': Operator(
        func=lambda x: lambertw(x, k=0).real,
        name='LWF',
        repr=lambda x: f'(LWF({x}))',
        arity=1,
        complexity=3,
    ),
    'add': Operator(
        func=lambda x, y: x + y,
        name='add',
        repr=lambda x, y: f'({x} + {y})',
        arity=2,
        complexity=1,
    ),
    'sub': Operator(
        func=lambda x, y: x - y,
        name='sub',
        repr=lambda x, y: f'({x} - {y})',
        arity=2,
        complexity=1,
    ),
    'mul': Operator(
        func=lambda x, y: x * y,
        name='mul',
        repr=lambda x, y: f'({x} * {y})',
        arity=2,
        complexity=1,
    ),
    'sin': Operator(
        func=lambda x: np.sin(x),
        name='sin',
        repr=lambda x: f'(sin({x})',
        arity=1,
        complexity=3,
    ),
    'cos': Operator(
        func=lambda x: np.cos(x),
        name='cos',
        repr=lambda x: f'(cos({x})',
        arity=1,
        complexity=3,
    ),
    'log': Operator(
        func=lambda x: _SAFE_LOG_FUNC(x),
        name='safe_log',
        repr=lambda x: f'(log({x})',
        arity=1,
        complexity=4,
    ),
    'sqrt': Operator(
        func=lambda x: _SAFE_SQRT_FUNC(x),
        name='safe_sqrt',
        repr=lambda x: f'(sqrt({x})',
        arity=1,
        complexity=2,
    ),
    'div': Operator(
        func=lambda x, y: _SAFE_DIV_FUNC(x, y),
        name='safe_div',
        repr=lambda x, y: f'({x} / {y})',
        arity=2,
        complexity=2,
    ),
    'exp': Operator(
        func=lambda x: _SAFE_EXP_FUNC(x),
        name='safe_exp',
        repr=lambda x: f'(e^{x})',
        arity=1,
        complexity=4,
    ),
    'pow': Operator(
        func=lambda x, y: _SAFE_POW_FUNC(x, y),
        name='safe_pow',
        repr=lambda x, y: f'({x}^{y})',
        arity=2,
        complexity=4,
    ),
    'pow2': Operator(
        func=lambda x: _SAFE_POW_FUNC(x, 2),
        name='safe_pow2',
        repr=lambda x: f'({x}^{2})',
        arity=1,
        complexity=3,
    ),
    'e': Operator(
        func=lambda: np.e,
        name='e',
        repr=lambda: f'e',
        arity=0,
        complexity=1,
    ),
    'pi': Operator(
        func=lambda: np.e,
        name='pi',
        repr=lambda: f'pi',
        arity=0,
        complexity=1,
    ),
    '0.5': Operator(
        func=lambda: 0.5,
        name='half',
        repr=lambda: f'0.5',
        arity=0,
        complexity=1
    ),
}


VARIABLES = {
    'x1': 0,
    'x2': 1,
    'x3': 2,
    'x4': 3,
    'x5': 4
}
CONST_SYMBOL = 'const'

FLOAT_CONST = ['-1.0', '1.0', '2.0', '3.0', '4.0', '5.0', '6.0', '7.0', '8.0', '9.0', '10.0']

VAR_CONST_COMPLEXITY = 1

if __name__ == '__main__':
    print(_SAFE_LOG_FUNC(np.array([0, 1, -1, 3])))
