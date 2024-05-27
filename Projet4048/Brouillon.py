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

if __name__ == "__main__":
    states = {'q0', 'q1', 'q2'}
    alphabet = {'a', 'b'}
    transitions = {
        'q0': {'a': ['q0', 'q1'], 'b': ['q0']},
        'q1': {'b': ['q2']},
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




#Brouillon de tester_automate:
class AFND:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

    def is_afnd(self):
        """
        Vérifie si un automate est un AFND.
        
        :return: True si l'automate est un AFND, False sinon.
        """
        for state, transitions in self.transitions.items():
            for symbol, next_states in transitions.items():
                if symbol == 'ε' or len(next_states) > 1:
                    return True
        return False

def is_afd(automate):
    """
    Vérifie si un automate est un AFD.
    
    :param automate: L'automate à vérifier.
    :return: True si l'automate est un AFD, False sinon.
    """
    if automate.is_afnd():
        return False

    for state, transitions in automate.transitions.items():
        for symbol, next_states in transitions.items():
            if len(next_states) != 1:
                return False
    return True

# Exemple d'utilisation
if __name__ == "__main__":
    # Définir les composants de l'AFND
    states = {'q0', 'q1', 'q2'}
    alphabet = {'a', 'b'}
    transitions = {
        'q0': {'a': ['q0', 'q1'], 'b': ['q0']},
        'q1': {'b': ['q2']},
        'q2': {}
    }
    initial_state = 'q0'
    final_states = {'q2'}

    # Créer une instance de l'AFND
    afnd = AFND(states, alphabet, transitions, initial_state, final_states)

    # Tester si l'automate est un AFND
    print("L'automate est un AFND:", afnd.is_afnd())

    # Tester si l'automate est un AFD
    print("L'automate est un AFD:", is_afd(afnd))

    # Déterminer si l'automate est AFND ou AFD
    if afnd.is_afnd():
        print("L'automate est un AFND (Automate Fini Non-Déterministe).")
    elif is_afd(afnd):
        print("L'automate est un AFD (Automate Fini Déterministe).")
    else:
        print("L'automate n'est ni un AFND ni un AFD complet.")