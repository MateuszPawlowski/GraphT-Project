# Mateusz Pawlowski
# Classes used in thompson's construction
import argparse
class State:
    """A state with one or two edges, all edges labeled by label"""
    # Constructor for the class
    def __init__(self, label=None, edges=[]):
        # Every state has 0, 1. or 2 edges from it.
        self.edges = edges
        # Label for the arrows. None means espilon
        self.label = label


class Fragment:
    """An NFA fragment with a start state and an accept state"""
    # Constructor
    def __init__(self, start, accept):
        # Start state of NFA fragment
        self.start = start
        # Accept state of NFA fragment
        self.accept = accept


def shunt(infix):
    """Return the infix regular expression in postfix"""
    # Convert input to a stack-ish list
    infix = list(infix)[::-1]

    # Operator stack
    opers = []

    # Output list
    postfix = []

    # Operator precedence
    prec = {'*': 100, '+':90, '.': 80, '?':70, '|': 60, ')': 40, '(': 20}

    # Loop through the input one character at a time
    while infix:
        # Pop a character from the input
        c = infix.pop()

        # Decide what to do based on the character
        if c == '(':
            # Push and open bracket to the opers stack
            opers.append(c)
        elif c == ')':
            # Pop the operators stack until you find a (
            while opers[-1] != '(':
                postfix.append(opers.pop())
            # Get rid of the '('
            opers.pop()
        elif c in prec:
            # Push any operators on the opers stack with higher prec to the output
            while opers and prec[c] < prec[opers[-1]]:
                postfix.append(opers.pop())
            # Push c to the operator stack
            opers.append(c)
        else:
            # Typically we just push the character to the output
            postfix.append(c)

    # Pop all operators to the output
    while opers:
        postfix.append(opers.pop())

    # Convert output list to string
    return ''.join(postfix)

def compile(infix):
    """Return an NFA Fragment representing the infix regular expression"""
    # Convert infix to postfix
    postfix = shunt(infix)
    # Make postfix a stack of characters
    postfix = list(postfix)[::-1]

    # A stack of NFA fragments
    nfa_stack = []

    while postfix:
        # Pop a character from postfix
        c = postfix.pop()
        if c == '.':
            # Pop two fragments of the stack
            frag1 = nfa_stack.pop()
            frag2 = nfa_stack.pop()
            # Point frag2's accept state at frag1's start state
            frag2.accept.edges.append(frag1.start)
            # The new start state is frag2's
            start = frag2.start
            # The new accept state is frag1's
            accept = frag1.accept
        elif c == '|':
            # Pop two fragments of the stack
            frag1 = nfa_stack.pop()
            frag2 = nfa_stack.pop()
            # Create new start and accept states
            accept = State()
            start = State(edges=[frag2.start, frag1.start])
            # Point the old accept states at the new one
            frag2.accept.edges.append(accept)
            frag1.accept.edges.append(accept)
        elif c == '*':
            # Pop a single fragment of the stack
            frag = nfa_stack.pop()
            # Create new start and accept states
            accept = State()
            start = State(edges=[frag.start, accept])
            # Point the arrows
            frag.accept.edges = [frag.start, accept]
        elif c == '?':
            # Pop a single fragment of the stack
            frag = nfa_stack.pop()
            # Create new start and accept states
            accept = State()
            start = State(edges=[frag.start, accept])
            # Point the arrows
            frag.accept.edges = [frag.start, accept]
        elif c == '+':
            # Pop a single fragment of the stack
            frag = nfa_stack.pop()
            # Create a new start and accept states
            accept = State()
            start = frag.start
            # Point the arrows
            frag.accept.edges = [frag.start, accept]
        else:
            accept = State()
            start = State(label=c, edges=[accept])
                  
        # Create new instance of the Fragment to represent  the new NFA
        newfrag = Fragment(start, accept)
        #Push the new NFA to the NFA stack
        nfa_stack.append(newfrag)

    # The NFA stack should have exactly NFA on it
    return nfa_stack.pop()

# Add a state to a set and follow all of the e(epsilon) arrows
def followes(state, current):
    # Only do something when we haven't already seen the state
    if state not in current:
        # Put the state itself into current
        current.add(state)
        # See wheter state is labelled by e(epsilon)
        if state.label is None:
            # Loop through the states pointed to by this state
            for x in state.edges:
                # Follow all of their e(epsilons) too
                followes(x, current)
                    

def match(regex, s):
    # This function will return True if and only if the regular expression
    # regex (fully) matches the string s. It returns False otherwise
    
    # Compile the regular expression into an NFA
    nfa = compile(regex)

    # Try to match the regular expression to the string s
    # The current set of states
    current = set()
    # Add the first state, and follow all e(epsilon) arrows
    followes(nfa.start, current)
    # The previous set of states
    previous = set()

    # Loop through characters in s
    for c in s:
        # Keep track of where we were
        previous = current
        # Create a new empty set for states we're about to be in
        current = set()
        # Loop through the previous set
        for state in previous:
            # Only follow arrows not labelled by e(epsilon)
            if state.label is not None:
                # If the label of the state is equal to the character we've read
                if state.label == c:
                    # Add the state at the end of the arrow to current
                    followes(state.edges[0], current)



    # Ask the NFA if it matches the string s
    return nfa.accept in current

if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='This is a software development Year 3 ' +
            'project for graph theory. It is a program to execute regular expressions on ' + 
            'strings using an algorithm known as Thompsons Construction. The shunting ' +
            'algorithm is used which uses the Thompsons Construction. To run the program ' +
            'type in: python3 project.py To see the code type in: vi project.py ' +
            'created by Mateusz Pawlowski - G0i0361162')

    args = parser.parse_args()

    tests = [
        # Tests for '.', '|', '*'
        ["a.b|b*", "bbbbb", True],
        ["a.b|b*", "bbbbx", False],
        ["b**", "b", True],
        ["b*", "", True],
    
        # Tests for '?'
        ["a?", "", True],
        ["a?", "a", True],
        ["a?b|b*", "bbb", True],
        ["a?b", "a",False],
        ["a?b", "b", True],

        # Tets for '+'
        ["a+", "", False],
        ["a+", "a", True],
        ["a+b|b", "bbb", True],
        ["a+b|b*", "a", False],
        ["a+|b", "a", True],
        ["a+|b", "", False]
        ]

    for test in tests:
        assert match(test[0], test[1]) == test[2], test[0] + \
        (" Should match " if test[2] else " Should not match ") + test[1]
