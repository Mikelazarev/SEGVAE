import numpy as np
import torch


class Operator:
    def __init__(self, func, name, repr, arity):
        self.func = func
        self.name = name
        self.repr = repr
        self.arity = arity


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
        return _SAFE_EXP_FUNC(y * _SAFE_LOG_FUNC(x))
    else:
        with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
            return _SAFE_EXP_FUNC(y * _SAFE_LOG_FUNC(x))


OPERATORS = {
    'add': Operator(
        func=lambda x, y: x + y,
        name='add',
        repr=lambda x, y: f'({x} + {y})',
        arity=2,
    ),
    'sub': Operator(
        func=lambda x, y: x - y,
        name='sub',
        repr=lambda x, y: f'({x} - {y})',
        arity=2,
    ),
    'mul': Operator(
        func=lambda x, y: x * y,
        name='mul',
        repr=lambda x, y: f'({x} * {y})',
        arity=2,
    ),
    'sin': Operator(
        func=lambda x: np.sin(x),
        name='sin',
        repr=lambda x: f'sin({x})',
        arity=1,
    ),
    'cos': Operator(
        func=lambda x: np.cos(x),
        name='cos',
        repr=lambda x: f'cos({x})',
        arity=1,
    ),
    'safe_log': Operator(
        func=lambda x: _SAFE_LOG_FUNC(x),
        name='safe_log',
        repr=lambda x: f'log({x})',
        arity=1,
    ),
    'safe_sqrt': Operator(
        func=lambda x: _SAFE_SQRT_FUNC(x),
        name='safe_sqrt',
        repr=lambda x: f'sqrt({x})',
        arity=1,
    ),
    'safe_div': Operator(
        func=lambda x, y: _SAFE_DIV_FUNC(x, y),
        name='safe_div',
        repr=lambda x, y: f'({x} / {y})',
        arity=2,
    ),
    'safe_exp': Operator(
        func=lambda x: _SAFE_EXP_FUNC(x),
        name='safe_exp',
        repr=lambda x: f'(e^{x})',
        arity=1,
    ),
    'safe_pow': Operator(
        func=lambda x, y: _SAFE_POW_FUNC(x, y),
        name='safe_pow',
        repr=lambda x, y: f'({x}^{y})',
        arity=2,
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

FLOAT_CONST = ['-1.0', '2.0', '3.0', '5.0', '7.0', '9.0', '10.0']


if __name__ == '__main__':
    print(_SAFE_LOG_FUNC(np.array([0, 1, -1, 3])))
