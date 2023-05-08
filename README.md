# Mini-Lisp
LISP is an ancient programming language based on [S-expressions](https://en.wikipedia.org/wiki/S-expression) and [lambda calculus](https://en.wikipedia.org/wiki/Lambda_calculus).
All operations in Mini-LISP are written in parenthesized [prefix notation](https://en.wikipedia.org/wiki/Polish_notation). For example, a simple mathematical formula `(1 + 2) * 3` written in Mini-LISP is:
```
(* (+ 1 2) 3) 
```
As a simplified language, Mini-LISP has only three types (**Boolean**, **number** and **function**) and a few operations

## Usage
To automatically test all public test data:
```
./test.bat
```

To test specific file:
```
python Main.py -f filepath
```

Manual input:
```
python Main.py
```
then you can keep typing input data until you type "eol".


To show traceback stack:
```
python Main.py -s
```
## Feature
1. **Syntax Validation**: Print “syntax error” when parsing invalid syntax
2. **Print**: Implement print-num statement
3. **Numerical Operations**: Implement all numerical operations
4. **Logical Operations**: Implement all logical operations
5. **if Expression**: Implement if expression
6. **Variable Definition**: Able to define a variable
7. **Function**: Able to declare and call an anonymous function
8. **Named Function**: Able to declare and call a named function
9. **Recursion**: Support recursive function call
10. **Type Checking**: Print error messages for type errors
11. **Nested Function**: Nested function (static scope)
12. **First-class Function**: Able to pass functions, support closure

## Type Definition
- Boolean: Boolean type includes two values, `#t` for true and `#f` for false. 
- Number: Signed integer from $-2^{31}$ to $2^{31} – 1$, behavior out of this range is not 
defined. 
- Function: See [Function](#7-function).

## Operation Overview

||        Numerical Operator        ||
|----------|--------|----------------|
| Name     | Symbol | Example        |
| Plus     | +      | (+ 1 2) => 3   | 
| Minus    | -      | (- 1 2) => -1  | 
| Multiply | *      | (* 2 3) => 6   | 
| Divide   | /      | (/ 6 3) => 2   |
| Modulus  | mod    | (mod 8 3) => 2 | 
| Greater  | >      | (> 1 2) => #f  |
| Smaller  | <      | (< 1 2) => #t  |
| Equal    | =      | (= 1 2) => #f  |
 
 
||        Logical Operators        ||
|------|--------|-------------------|
| Name | Symbol | Example           | 
| And  | and    | (and #t #f) => #f | 
| Or   | or     | (or #t #f) => #t  |
| Not  | not    | (not #t) => #f    |

**Other Operators**: define, fun, if

Note that all operators are **reserved words**, you cannot use any of these words as ID.

## Lexical Details
### Preliminary Definitions:
```
separator ::= '\t'(tab) | '\n' | '\r' | ' '(space) 
letter ::= [a-z] 
digit ::= [0-9] 
```
### Token Definitions: 
```
number ::= 0 | [1-9]digit* | -[1-9]digit* 
ID ::= letter (letter | digit | '-')* 
bool-val ::= #t | #f
```
## Grammar
### 1. Program
```
PROGRAM :: = STMT+ 
STMT ::= EXP | DEF-STMT | PRINT-STMT 
```

### 2. Print 
```
PRINT-STMT ::= (print-num EXP) 
        | (print-bool EXP) 
```
 
### 3. Expression (EXP) 
```
EXP ::= bool-val | number | VARIABLE 
        | NUM-OP | LOGICAL-OP | FUN-EXP | FUN-CALL | IF-EXP 
```

### 4. Numerical Operations (NUM-OP) 
```
NUM-OP ::= PLUS | MINUS | MULTIPLY | DIVIDE | MODULUS | 
                | GREATER | SMALLER | EQUAL 
        PLUS ::= (+ EXP EXP+)   
        MINUS ::= (-  EXP  EXP) 
        MULTIPLY ::= (*  EXP  EXP+) 
        DIVIDE ::= (/  EXP  EXP)
        MODULUS ::= (mod  EXP  EXP)
        GREATER ::= (>  EXP  EXP)
        SMALLER ::= (< EXP  EXP)
        EQUAL ::= (= EXP  EXP+) 
```

### 5. Logical Operations (LOGICAL-OP) 
```
LOGICAL-OP ::= AND-OP | OR-OP | NOT-OP 
        AND-OP ::= (and EXP  EXP+) 
        OR-OP ::= (or EXP  EXP+) 
        NOT-OP ::= (not EXP) 
```

### 6. define Statement (DEF-STMT) 
```
DEF-STMT ::= (define id EXP) 
        VARIABLE ::= id 
```
Note: Redefining is not allowed.  
 
### 7. Function 
```
FUN-EXP ::= (fun FUN-IDs FUN-BODY) 
FUN-IDs ::= (id*) 
FUN-BODY ::= EXP 
FUN-CALL ::= (FUN-EXP PARAM*) 
        |  (FUN-NAME PARAM*) 
PARAM ::= EXP 
LAST-EXP ::= EXP 
FUN-NAME ::= id
```

### 8. if Expression 
```
IF-EXP ::= (if TEST-EXP THEN-EXP ELSE-EXP) 
TEST-EXP ::= EXP 
THEN-EXP ::= EXP 
ELSE-EXP ::= EXP 
```

### 9. Recursion
Make  your  interpreter  be  able  to  handle  recursive  function  call.
```
(define f 
  (fun (x) (if (= x 1) 
               1  
               (* x (f (- x 1)))))) 
(f 4) → 24
```

### 10. Type  Checking
For  type  specifications  of  operations,  please  check  out  the  table below:
| Op              | Parameter Type          | Output Type |
|-----------------|-------------------------|-------------|
| +, -, *, /, mod | Number(s)               | Number      |
| >, <, =         | Number(s)               | Boolean     |
| and, or, not    | Boolean(s)              | Boolean     |
| If              | Boolean(s) for test-exp | Depend on then-exp and else-exp |
| Fun             | Any                     | Function    |
| Function call   | Any                     | Depend on fun-body and parameters|
Please print a message when detecting a type error. For example: 
```
(> 1 #t) 
  → Type Error: Expect 'number' but got 'boolean'.
```

### 11. Nested Function
There could be a function inside another function. The inner one 
is able to access the local variables of the outer function.
```
fun-body ::= def-stmt* exp
```
```
(define dist-square 
  (fun (x y) 
    (define square 
      (fun (x) (* x x))) 
    (+ (square x) (square y))))
```

### 12. First-class Function
Functions can be passed like other variables. Furthermore, it 
can keep its environment. For more details, you can search for ["First-class Functions"](https://en.wikipedia.org/wiki/First-class_function) and ["Closure"](https://en.wikipedia.org/wiki/Closure_%28computer_programming%29).
```
(define chose 
  (fun (chose-fun x y) 
    (if (chose-fun x y) x y))) 
(chose (fun (x y) (> x y)) 2 1) → 2 
 
(define add-x 
  (fun (x) 
    (fun (y) (+ x y)))) 
(define f (add-x 5)) 
(f 3) → 8 

```
## References
[Peter Norvig - (How to Write a (Lisp) Interpreter (in Python))](http://norvig.com/lispy.html)