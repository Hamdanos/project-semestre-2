import os
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

def union(af1, af2):
    """
    Réalise l'union de deux automates finis non déterministes (AFND).
    
    :param af1: Le premier AFND.
    :param af2: Le deuxième AFND.
    :return: L'AFND résultant de l'union.
    """
    # Obtention des nouvelles transitions
    new_transitions = {}
    for state in af1.states | af2.states:
        new_transitions[state] = {}
        for symbol in af1.alphabet | af2.alphabet:
            new_transitions[state][symbol] = af1.transitions.get(state, {}).get(symbol, []) + af2.transitions.get(state, {}).get(symbol, [])
    
    # Nouvel ensemble d'états finaux
    new_final_states = af1.final_states | af2.final_states
    
    # Création d'un nouvel AFND avec les paramètres combinés
    return AFND(
        states=af1.states | af2.states,
        alphabet=af1.alphabet | af2.alphabet,
        transitions=new_transitions,
        initial_state=af1.initial_state,
        final_states=new_final_states
    )

def concatenation(af1, af2):
    """
    Réalise la concaténation de deux automates finis non déterministes (AFND).
    
    :param af1: Le premier AFND.
    :param af2: Le deuxième AFND.
    :return: L'AFND résultant de la concaténation.
    """
    # Obtention des nouvelles transitions
    new_transitions = {}
    for state in af1.states:
        new_transitions[state] = {}
        for symbol in af1.alphabet:
            new_transitions[state][symbol] = af1.transitions.get(state, {}).get(symbol, []) + af2.transitions.get(af2.initial_state, {}).get(symbol, [])
    
    # Mise à jour des transitions de l'état final de af1 si final_states n'est pas vide
    if af1.final_states:
        final_state = af1.final_states.pop()
        for symbol in af1.alphabet:
            new_transitions[final_state][symbol] = af2.transitions.get(af2.initial_state, {}).get(symbol, [])
    
    # Création d'un nouvel AFND avec les paramètres combinés
    return AFND(
        states=af1.states | af2.states,
        alphabet=af1.alphabet | af2.alphabet,
        transitions=new_transitions,
        initial_state=af1.initial_state,
        final_states=af2.final_states
    )

def kleene_star(af):
    """
    Réalise l'itération de Kleene sur un automate fini non déterministe (AFND).
    
    :param af: L'AFND à itérer.
    :return: L'AFND résultant de l'itération de Kleene.
    """
    # Ajout d'un nouvel état initial et d'un nouvel état final
    new_initial_state = "q0"
    new_final_state = "qf"
    new_transitions = {**af.transitions}
    
    # Création des nouvelles transitions
    new_transitions[new_initial_state] = {symbol: af.transitions.get(af.initial_state, {}).get(symbol, []) for symbol in af.alphabet}
    new_transitions[new_final_state] = {}
    for symbol in af.alphabet:
        if af.final_states:
            final_state = af.final_states.pop()
            new_transitions[new_final_state][symbol] = [af.initial_state] + af.transitions.get(final_state, {}).get(symbol, [])
        else:
            new_transitions[new_final_state][symbol] = [af.initial_state]
    
    # Ajout de l'epsilon transition de l'état initial au nouvel état final et de l'ancien état initial au nouvel état final
    new_transitions[new_initial_state]['ε'] = [af.initial_state, new_final_state]
    
    # Création d'un nouvel AFND avec les paramètres combinés
    return AFND(
        states=af.states | {new_initial_state, new_final_state},
        alphabet=af.alphabet,
        transitions=new_transitions,
        initial_state=new_initial_state,
        final_states={new_final_state}
    )

if __name__ == "__main__":
    # Définir les automates AFND
    states_af1 = {'q0', 'q1'}
    alphabet_af1 = {'a', 'b'}
    transitions_af1 = {
        'q0': {'a': ['q0', 'q1'], 'b': ['q0']},
        'q1': {'b': ['q1']}
    }
    initial_state_af1 = 'q0'
    final_states_af1 = {'q1'}
    af1 = AFND(states_af1, alphabet_af1, transitions_af1, initial_state_af1, final_states_af1)

    states_af2 = {'q2', 'q3'}
    alphabet_af2 = {'a', 'b'}
    transitions_af2 = {
        'q2': {'a': ['q3'], 'b': ['q2']},
        'q3': {'b': ['q2']}
    }
    initial_state_af2 = 'q2'
    final_states_af2 = {'q3'}
    af2 = AFND(states_af2, alphabet_af2, transitions_af2, initial_state_af2, final_states_af2)

    # Effectuer les opérations d'automate
    # Exemple d'union
    af_union = union(af1, af2)
    af_union.visualize('af_union.dot')
    
    # Exemple de concaténation
    af_concatenation = concatenation(af1, af2)
    af_concatenation.visualize('af_concatenation.dot')
    
    # Exemple d'itération (Kleene Star)
    af_kleene_star = kleene_star(af1)
    af_kleene_star.visualize('af_kleene_star.dot')

    # Fusionner les fichiers graphiques en un seul fichier
    merge_graphs(['af_union.dot', 'af_concatenation.dot', 'af_kleene_star.dot'], 'combined_graphs.dot')

    # Convertir le fichier dot en image
    os.system("dot -Tpng combined_graphs.dot -o combined_graphs.png")

