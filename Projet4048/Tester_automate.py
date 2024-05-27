import graphviz

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

def visualize_automate(automate, filename):
    """
    Visualise un automate en utilisant graphviz et enregistre l'image.
    
    :param automate: L'automate à visualiser.
    :param filename: Le nom du fichier où l'image sera sauvegardée.
    """
    dot = graphviz.Digraph()

    # Ajouter les états
    for state in automate.states:
        if state in automate.final_states:
            dot.node(state, shape='doublecircle')
        else:
            dot.node(state)

    # Ajouter les transitions
    for state, transitions in automate.transitions.items():
        for symbol, next_states in transitions.items():
            for next_state in next_states:
                dot.edge(state, next_state, label=symbol)

    # Spécifier l'état initial
    dot.node('start', shape='plaintext', label='')
    dot.edge('start', automate.initial_state)

    # Sauvegarder et visualiser le fichier
    dot.render(filename, format='png', cleanup=True)

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

    # Visualiser l'automate
    visualize_automate(afnd, 'automate')
