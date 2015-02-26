#! /usr/bin/python

"""
    @author Nick Wilson Joseph Toney
    @version 4.25.14

    Script uses a recursive descent parser to parse an user inputted string
    and determine whether the syntax is correct or not. It then attempts to 
    evaluate the expression and return a result.
"""

import sys, re

ERROR = -999999

class Interpreter:
    """
        This class helps model an Interpreter, it contains fields for the
        current token, and the overall string that is the expression. It also
        contains methods such as getters and setters, and a tokenize function.
    """
    def __init__(self):
        """
            The constructor for the the class, it initializes the fields to
            empty values.
            @param
                self - reference to this object
        """

        """ Overall string containing the expression """
        self.line = ""

        """ The current token """
        self.currentToken = ""

    def tokenize(self):
        """
            This method uses regular expressions to "grab" the next token from
            the line. It then updates the currentToken field and trims that
            token's value off the begining of the line.
            @parm
                self - reference to this object
        """
        regex = '[\d]+|(==)|(!=)|(<=)|(>=)|[<]|[>]|[/]|[*]|[+]|[-]|[\(]|[\)]'
        regex += '|[\^]'
        possibleTokens= re.compile(regex)
        self.currentToken = re.search(possibleTokens, self.line)
        if self.currentToken == None:
            self.currentToken = ERROR
            return
        self.currentToken = self.currentToken.group(0)
        
        #update overall line by "cutting" off first token from it
        self.line = self.line.replace(self.currentToken, '', 1)


    def setLine(self, newLine):
        """
            Method sets the line field to the newline provided in the
            parameter
            @param
                self - reference to this object
                newLine - the string that line will be set too
        """
        self.line = newLine

    def getLine(self):
        """
            Method returns the objects line field.
            @param
                self - reference to this object
            @return
                line - the line field, type string
        """
        return self.line

    def getCurrentToken(self):
        """
            Method returns the current token of the object.
            @param
                self - reference to this object
            @return
                currentToken - the current token in the object, type string
        """
        return self.currentToken

def expr(interpret):
    """
        Function models grammar:
        <expr> ::= <term> <ttail>
        It performs calls to the term function and ttail if term does not
        return ERROR

        @param
            interpret - an Interpreter object
        @return
            returns result eventually after going through necessary functions
    """
    subtotal = term(interpret)
    if subtotal == ERROR:
        return ERROR
    else:
        return ttail(interpret, subtotal)

def ttail(interpret, subtotal):
    """
        Function models grammar:
        <ttail> ::= <add_sub_tok> <term> <ttail> | e
        It performs calls to the add_sub_tok, term, and ttail functions unless
        one of these returns ERROR. In the case of an empty string, e, this
        function returns the subtotal numerical value.

        @param
            interpret - an Interpreter object
            subtotal  - the current total which will eventually be used to 
                        generate the result, if no syntactical errors occur
        @return
            a numerical value representing current value of the expression
    """
    if interpret.getCurrentToken() == '+':
        add_sub_tok(interpret)
        tempValue = term(interpret)
        if tempValue == ERROR:
            return ERROR
        else:
            return ttail(interpret, subtotal + tempValue)
    elif interpret.getCurrentToken() == '-':
        add_sub_tok(interpret)
        tempValue = term(interpret)
        if tempValue == ERROR:
            return ERROR
        else:
            return ttail(interpret, subtotal - tempValue)
    else:
        return subtotal

def term(interpret):
    """
        Function models grammar:
        <term> ::= <stmt> <stail>
    """
    subtotal = stmt(interpret)
    if subtotal == ERROR:
        return ERROR
    else:
        return stail(interpret, subtotal)



def stail(interpret, subtotal):
    """
        Function models grammar:
        <stail> ::= <mult_div_tok> <stmt> <stail> | e
    """
    if interpret.getCurrentToken() == '*':
        mul_div_tok(interpret)
        tempValue = stmt(interpret)
        if tempValue == ERROR:
            return ERROR
        else:
            return stail(interpret, subtotal * tempValue)
    elif interpret.getCurrentToken() == '/':
        mul_div_tok(interpret)
        tempValue = stmt(interpret)
        if tempValue == ERROR:
            return ERROR
        else:
            return stail(interpret, subtotal / tempValue)
    else:
        return subtotal


def stmt(interpret):
    """
        Function models grammar:
        <stmt> ::= <logic> <ltail>
    """
    subtotal = logic(interpret)
    if subtotal == ERROR:
        return ERROR
    else:
        return ltail(interpret, subtotal)

def ltail(interpret, num):
    """
        Function models grammar:
        <ltail> ::= <log_tok> <logic> <ltail> | e
    """
    subtotal = ERROR
    token = interpret.getCurrentToken()
    if token == "<":
        log_tok(interpret)
        
        subtotal = logic(interpret)
        if subtotal == ERROR:
            return num
        subtotal = int(num < subtotal)

    elif token == ">":
        log_tok(interpret)
        subtotal = logic(interpret)
        if subtotal == ERROR:
            return num
        subtotal = int(num > subtotal)

    elif token == "<=":
        log_tok(interpret)
        subtotal = logic(interpret)
        if subtotal == ERROR:
            return num
        subtotal = int(num <= subtotal)

    elif token == ">=":
        log_tok(interpret)
        subtotal = logic(interpret)
        if subtotal == ERROR:
            return num
        subtotal = int(num >= subtotal)

    elif token == "!=":
        log_tok(interpret)
        subtotal = logic(interpret)
        if subtotal == ERROR:
            return num
        subtotal = int(num != subtotal)

    elif token == "==":
        log_tok(interpret)
        subtotal = logic(interpret)
        if subtotal == ERROR:
            return num
        subtotal =  int(num == subtotal)

    else:
        return num

    tail = ltail(interpret, subtotal)
    if tail == ERROR:
        return subtotal
    return tail

def logic(interpret):
    """
        Function models grammar:
        <logic> ::= <exp> ^ <logic> | <exp>
    """
    temptotal = expp(interpret)
    if temptotal == ERROR:
        return temptotal
    else:
        if interpret.getCurrentToken() == '^':
            interpret.tokenize()
            tempTerm = logic(interpret)
            if tempTerm == ERROR:
                return ERROR
            return temptotal ** tempTerm
        else:
            return temptotal

def expp(interpret):
    """
        Function models grammar:
        <exp> ::= ( <expr> ) | <num>
    """
    if interpret.getCurrentToken() == '(':
        interpret.tokenize()
        temptotal = expr(interpret)
        if temptotal == ERROR:
            return ERROR
        elif interpret.getCurrentToken() != ')':
            return ERROR
        else:
            interpret.tokenize()
            return temptotal
    else:
        return num(interpret)



def log_tok(interpreter):
    newToken = interpreter.getCurrentToken()
    interpreter.tokenize()
    return newToken

def num(interpreter):
    newToken = interpreter.getCurrentToken()
    interpreter.tokenize()
    return int(newToken)

def add_sub_tok(interpreter):
    newToken = interpreter.getCurrentToken()
    interpreter.tokenize()
    return newToken

def mul_div_tok(interpreter):
    """
        <mul_div_tok> -> * | /
        Function gets rid of a * or / token from the overall string, and 
        returns the new token.
    """
    newToken = interpreter.getCurrentToken()
    interpreter.tokenize()
    return newToken

def main():
    """
        This function provides an entry point into the program.
    """
    


    user_input = ""

    while (user_input != 'q'):
        user_input = raw_input("Please enter an expression> ")
#// call to token
        user_input = user_input.replace(' ', '').replace('\n', '')
        print user_input

        if user_input[-1] != ';':
                print "Syntax error"
        else:
            user_input = user_input.replace(';', '')
            interpret = Interpreter()
            interpret.setLine(user_input)
            interpret.tokenize()
            value = expr(interpret)
            if value != ERROR:
                print "Syntax OK"
                print value
            else:
                print "Syntax error"


    print "Goodbye"
    sys.exit(0)


main()
