import graphviz

class AFND:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

    def add_transition(self, from_state, symbol, to_state):
        if from_state not in self.transitions:
            self.transitions[from_state] = {}
        if symbol not in self.transitions[from_state]:
            self.transitions[from_state][symbol] = []
        self.transitions[from_state][symbol].append(to_state)
    
    def get_transitions(self, state, symbol):
        if state in self.transitions and symbol in self.transitions[state]:
            return self.transitions[state][symbol]
        return []
    
    def visualize(self, filename):
        dot = graphviz.Digraph()

        for state in self.states:
            shape = 'doublecircle' if state in self.final_states else 'circle'
            dot.node(state, shape=shape)
        
        dot.node('', shape='none')  # état invisible pour l'état initial
        dot.edge('', self.initial_state)  # transition de l'état invisible vers l'état initial
        
        for from_state, symbols in self.transitions.items():
            for symbol, to_states in symbols.items():
                for to_state in to_states:
                    dot.edge(from_state, to_state, label=symbol)

        dot.render(filename, format='png', cleanup=True)

class AFD:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states
    
    def add_transition(self, from_state, symbol, to_state):
        if from_state not in self.transitions:
            self.transitions[from_state] = {}
        self.transitions[from_state][symbol] = to_state
    
    def get_transition(self, state, symbol):
        if state in self.transitions and symbol in self.transitions[state]:
            return self.transitions[state][symbol]
        return None
    
    def visualize(self, filename):
        dot = graphviz.Digraph()

        for state in self.states:
            state_str = str(state)  # Convertir le frozenset en chaîne de caractères
            shape = 'doublecircle' if state in self.final_states else 'circle'
            dot.node(state_str, shape=shape)
        
        dot.node('', shape='none')  # état invisible pour l'état initial
        dot.edge('', str(self.initial_state))  # transition de l'état invisible vers l'état initial
        
        for from_state, symbols in self.transitions.items():
            from_state_str = str(from_state)  # Convertir le frozenset en chaîne de caractères
            for symbol, to_state in symbols.items():
                dot.edge(from_state_str, str(to_state), label=symbol)

        dot.render(filename, format='png', cleanup=True)

def convert_afnd_to_afd(afnd):
    new_states = []
    new_transitions = {}
    initial_state = frozenset([afnd.initial_state])
    final_states = set()

    queue = [initial_state]
    new_states.append(initial_state)

    while queue:
        current_state = queue.pop(0)
        new_transitions[current_state] = {}

        for symbol in afnd.alphabet:
            next_state = frozenset(
                state for s in current_state for state in afnd.get_transitions(s, symbol)
            )

            if next_state:
                if next_state not in new_states:
                    new_states.append(next_state)
                    queue.append(next_state)

                new_transitions[current_state][symbol] = next_state

                if next_state & afnd.final_states:
                    final_states.add(next_state)

    return AFD(
        states=new_states,
        alphabet=afnd.alphabet,
        transitions=new_transitions,
        initial_state=initial_state,
        final_states=final_states
    )

def recognize_word(automate, word):
    """
    Reconnaît si un mot est accepté par un automate.
    
    :param automate: L'automate à utiliser.
    :param word: Le mot à reconnaître.
    :return: True si le mot est accepté, False sinon.
    """
    current_states = {automate.initial_state}
    
    for symbol in word:
        next_states = set()
        for state in current_states:
            if state in automate.transitions and symbol in automate.transitions[state]:
                next_states.update(automate.transitions[state][symbol])
        current_states = next_states
    
    return any(state in automate.final_states for state in current_states)

if __name__ == "__main__":
    states = {'q0', 'q1', 'q2'}
    alphabet = {'a', 'b'}
    transitions = {
        'q0': {'a': ['q0', 'q1'], 'b': ['q0']},
        'q1': {'b': ['q2'], 'a' : ['q1']},
        'q2': {'a': ['q2'], 'b': ['q2']}
    }
    initial_state = 'q0'
    final_states = {'q2'}

    # afnd = AFND(states, alphabet, transitions, initial_state, final_states)
    afd = AFD(states, alphabet, transitions, initial_state, final_states)

    # afnd.visualize('afnd')
    

    # afd = convert_afnd_to_afd(afnd)

    afd.visualize('afd')

    for state, transitions in afd.transitions.items():
        for symbol, next_state in transitions.items():
            print(f"De {state} via {symbol} à {next_state}")

    # Tester la reconnaissance de mots
    word = "ab"
    is_recognized = recognize_word(afd, word)
    if is_recognized:
        print(f"Le mot '{word}' est reconnu par l'automate: {is_recognized}")
    else:
        print(f"The word '{word}' is not recognised by the automata")

    word = "aa"
    is_recognized = recognize_word(afd, word)
    if is_recognized:
        print(f"Le mot '{word}' est reconnu par l'automate: {is_recognized}")
    else:
        print(f"The word '{word}' is not recognised by the automata")
        
    
    word = "babaabab"
    is_recognized = recognize_word(afd, word)
    if is_recognized:
        print(f"The word '{word}' is recognised by the automata: {is_recognized}")
    else:
        print(f"The word '{word}' is not recognised by the automata")
        
    word = "aabaaaaabbbbb"
    is_recognized = recognize_word(afd, word)
    if is_recognized:
        print(f"The word '{word}' is recognised by the automata: {is_recognized}")
    else:
        print(f"The word '{word}' is not recognised by the automata")
