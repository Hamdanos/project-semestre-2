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
            state_name = str(state)  # Convertir l'état en chaîne de caractères
            shape = 'doublecircle' if state in self.final_states else 'circle'
            dot.node(state_name, shape=shape)
        
        dot.node('', shape='none')  # état invisible pour l'état initial
        dot.edge('', str(self.initial_state))  # transition de l'état invisible vers l'état initial
        
        for from_state, symbols in self.transitions.items():
            from_state_name = str(from_state)  # Convertir l'état de départ en chaîne de caractères
            for symbol, to_state in symbols.items():
                to_state_name = str(to_state)  # Convertir l'état d'arrivée en chaîne de caractères
                dot.edge(from_state_name, to_state_name, label=symbol)

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

if __name__ == "__main__":
    states = {'q0', 'q1', 'q2'}
    alphabet = {'a', 'b'}
    transitions = {
        'q0': {'a': ['q0', 'q1'], 'b': ['q0']},
        'q1': {'b': ['q1', 'q2'], 'a': ['q1', 'q0']},
        'q2': {}
    }
    initial_state = 'q0'
    final_states = {'q2'}

    afnd = AFND(states, alphabet, transitions, initial_state, final_states)

    afnd.visualize('afnd')

    afd = convert_afnd_to_afd(afnd)

    afd.visualize('afd')

    for state, transitions in afd.transitions.items():
        for symbol, next_state in transitions.items():
            print(f"De {state} via {symbol} à {next_state}")
