import operator as op
from functools import reduce


Symbol = str                # A MiniLisp Symbol is implemented as a Python str
Number = int                # A MiniLisp Number is implemented as a Python int
Atom   = (Symbol, Number)   # Cannot be broken into pieces
List   = list               # A MiniLisp List is implemented as a Python list
Exp    = (Atom, List)
Env    = dict


class MiniLispInterpreter:
    def __init__(self):
        self.AST = None
        
    
    def interpret(self, file):
        # read file
        if file:
            with open(file, 'r') as f:
                lines = f.read().split('\n')
            f.close()
        # manual input
        else:
            lines = []
            while True:
                line = input()
                if line == "eol":
                    break
                else:
                    lines.append(line)

        self.AST = self.parse(f'({"".join(lines)})')
        env = standard_env()
        for statement in self.AST:
            eval(statement, env)


    def tokenize(self, line: str) -> List:
        # Convert a string of characters into a list of tokens.
        return line.replace('(', ' ( ').replace(')', ' ) ').split()


    def parse(self, program: str) -> Exp:
        # Read a expression from a string.
        return self.create_AST(self.tokenize(program))


    def create_AST(self, tokens: list) -> Exp:
        # Read an expression from a sequence of tokens.
        if len(tokens) == 0:
            raise SyntaxError('unexpected EOF')
        token = tokens.pop(0)
        if token == '(':
            AST = []
            while tokens[0] != ')':
                AST.append(self.create_AST(tokens))
            tokens.pop(0) # pop off ')'
            return AST
        elif token == ')':
            raise SyntaxError('unexpected )')
        else:
            return self.atom(token)


    def atom(self, token: str) -> Atom:
        # Numbers become numbers; every other token is a symbol.
        try: return int(token)
        except ValueError:
            return Symbol(token)


class Env(dict):
    # An environment: a dict of {'var': val} pairs, with an outer Env.
    def __init__(self, parms=(), args=(), outer=None):
        super().__init__(self)
        self.update(zip(parms, args))
        self.outer = outer
        

    def find(self, var):
        # Find the innermost Env where var appears.
        if var not in self and self.outer is None:
            raise NameError(f"Name {var} is not defined")
        return self if (var in self) else self.outer.find(var)


def standard_env() -> Env:
    # An environment with some MiniLisp procedures.
    env = Env()
    env.update({
        "print-num": print,
        "print-bool": lambda x: print("#t" if x else "#f"),
        '+': op_add,
        '-': op_sub,
        '*': op_mul,
        '/': op_div, 
        "mod": op_mod,
        '>': op_gt,
        '<': op_lt,
        '=': op_eq,
        "and": op_and,
        "or": op_or,
        "not": op_not,
        "#t": True,
        "#f": False,
    })
    return env


def check_args_num(rule: str, num: int):
    if len(rule) == 2:
        if int(rule[0]) > num:
            # raise TypeError("syntax error")
            raise TypeError(f"Expected {rule[0]} or more arguments, got {num}")
    else:
        if int(rule) != num:
            # raise TypeError("syntax error")
            raise TypeError(f"Expected {rule} arguments, got {num}")


def check_int_type(args):
    if not all(type(arg) is int for arg in args):
        raise TypeError("Expect 'number' but got 'boolean'.")


def check_bool_type(args):
    if not all(type(arg) is bool for arg in args):
        raise TypeError("Expect 'boolean' but got 'number'.")


def op_add(*args):
    check_args_num("2*", len(args))
    check_int_type(args)
    return reduce(op.add, args)


def op_sub(*args):
    check_args_num("2", len(args))
    check_int_type(args)
    return op.sub(*args)


def op_mul(*args):
    check_args_num("2*", len(args))
    check_int_type(args)
    return reduce(op.mul, args, 1)


def op_div(*args):
    check_args_num("2", len(args))
    check_int_type(args)
    return op.floordiv(*args)


def op_mod(*args):
    check_args_num("2", len(args))
    check_int_type(args)
    return op.mod(*args)


def op_gt(*args):
    check_args_num("2", len(args))
    check_int_type(args)
    return op.gt(*args)


def op_lt(*args):
    check_args_num("2", len(args))
    check_int_type(args)
    return op.lt(*args)


def op_eq(*args):
    check_args_num("2*", len(args))
    check_int_type(args)
    return all(args[0] == arg for arg in args)


def op_and(*args):
    check_args_num("2*", len(args))
    check_bool_type(args)
    return reduce(op.and_, args)


def op_or(*args):
    check_args_num("2*", len(args))
    check_bool_type(args)
    return reduce(op.or_, args)


def op_not(*args):
    check_args_num("1", len(args))
    check_bool_type(args)
    return op.not_(*args)


class Function:
    # A user-defined Lisp procedure.
    def __init__(self, params, body, env):
        self.params, self.body, self.env = params, body, env

    def __call__(self, *args):
        func_env = Env(self.params, args, self.env)
        func_res = None
        for statement in self.body:
            func_res = eval(statement, func_env)

        return func_res



def eval(exp: Exp, env: Env):
    # Evaluate an expression in an environment.
    if isinstance(exp, Symbol):
        return env.find(exp)[exp]
    elif isinstance(exp, Number):
        return exp

    op, *args = exp
    if op == "if":
        (test, conseq, alt) = args
        test_res = eval(test, env)
        if not isinstance(test_res, bool):
            raise TypeError("Expect 'boolean' but got 'number'.")
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    elif op == "define":
        (symbol, exp) = args
        env[symbol] = eval(exp, env)
    elif op == "fun":
        (parms, *body) = args
        return Function(parms, body, env)
    else:
        proc = eval(op, env)
        vals = [eval(arg, env) for arg in args]
        return proc(*vals)