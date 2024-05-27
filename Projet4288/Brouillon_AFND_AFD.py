import graphviz

class AFND:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        """
        Initialisation de l'AFND avec les paramètres de base.
        
        :param states: Un ensemble d'états.
        :param alphabet: Un ensemble de symboles d'entrée.
        :param transitions: Un dictionnaire représentant les transitions. Le format est {état: {symbole: [liste d'états]}}.
        :param initial_state: L'état initial de l'automate.
        :param final_states: Un ensemble d'états finaux.
        """
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

    def add_transition(self, from_state, symbol, to_state):
        """
        Ajouter une transition à l'automate.
        
        :param from_state: L'état de départ de la transition.
        :param symbol: Le symbole de la transition.
        :param to_state: L'état d'arrivée de la transition.
        """
        if from_state not in self.transitions:
            self.transitions[from_state] = {}
        if symbol not in self.transitions[from_state]:
            self.transitions[from_state][symbol] = []
        self.transitions[from_state][symbol].append(to_state)
    
    def get_transitions(self, state, symbol):
        """
        Obtenir les états accessibles à partir d'un état donné avec un symbole donné.
        
        :param state: L'état de départ.
        :param symbol: Le symbole de transition.
        :return: Une liste d'états accessibles.
        """
        if state in self.transitions and symbol in self.transitions[state]:
            return self.transitions[state][symbol]
        return []
    
    def visualize(self, filename):
        """
        Visualiser l'AFND en utilisant graphviz.
        
        :param filename: Nom du fichier de sortie pour le schéma.
        """
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
        """
        Initialisation de l'AFD avec les paramètres de base.
        
        :param states: Un ensemble d'états.
        :param alphabet: Un ensemble de symboles d'entrée.
        :param transitions: Un dictionnaire représentant les transitions. Le format est {état: {symbole: état}}.
        :param initial_state: L'état initial de l'automate.
        :param final_states: Un ensemble d'états finaux.
        """
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states
    
    def add_transition(self, from_state, symbol, to_state):
        """
        Ajouter une transition à l'automate.
        
        :param from_state: L'état de départ de la transition.
        :param symbol: Le symbole de la transition.
        :param to_state: L'état d'arrivée de la transition.
        """
        if from_state not in self.transitions:
            self.transitions[from_state] = {}
        self.transitions[from_state][symbol] = to_state
    
    def get_transition(self, state, symbol):
        """
        Obtenir l'état accessible à partir d'un état donné avec un symbole donné.
        
        :param state: L'état de départ.
        :param symbol: Le symbole de transition.
        :return: L'état accessible ou None si la transition n'existe pas.
        """
        if state in self.transitions and symbol in self.transitions[state]:
            return self.transitions[state][symbol]
        return None
    
    def visualize(self, filename):
        """
        Visualiser l'AFD en utilisant graphviz.
        
        :param filename: Nom du fichier de sortie pour le schéma.
        """
        dot = graphviz.Digraph()

        for state in self.states:
            shape = 'doublecircle' if state in self.final_states else 'circle'
            dot.node(state, shape=shape)
        
        dot.node('', shape='none')  # état invisible pour l'état initial
        dot.edge('', self.initial_state)  # transition de l'état invisible vers l'état initial
        
        for from_state, symbols in self.transitions.items():
            for symbol, to_state in symbols.items():
                dot.edge(from_state, to_state, label=symbol)

        dot.render(filename, format='png', cleanup=True)

def convert_afnd_to_afd(afnd):
    """
    Convertir un AFND en AFD.
    
    :param afnd: Une instance de la classe AFND.
    :return: Une instance de la classe AFD.
    """
    new_states = []
    new_transitions = {}
    initial_state = frozenset([afnd.initial_state])
    final_states = set()

    # Utiliser une file pour la BFS
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

# Exemple d'utilisation de la conversion
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

    # Visualiser l'AFND
    afnd.visualize('afnd')

    # Convertir l'AFND en AFD
    afd = convert_afnd_to_afd(afnd)

    # Visualiser l'AFD
    afd.visualize('afd')

    # Afficher les transitions de l'AFD
    for state, transitions in afd.transitions.items():
        for symbol, next_state in transitions.items():
            print(f"De {state} via {symbol} à {next_state}")
