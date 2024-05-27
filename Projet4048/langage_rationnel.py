def is_rational(language):
    """
    Teste si un langage est rationnel en vérifiant s'il peut être reconnu par un automate fini.
    
    :param language: Le langage à tester.
    :return: True si le langage est rationnel, False sinon.
    """
    # Vérifier si le langage est vide
    if not language:
        return True
    
    # Créer un ensemble de mots vides et ajouter le mot vide
    empty_words = {""}
    
    # Initialiser l'ensemble des mots générés
    generated_words = empty_words.copy()
    
    # Générer de nouveaux mots jusqu'à ce que l'ensemble des mots générés ne change plus
    while True:
        new_words = set()
        for word in generated_words:
            for symbol in language.alphabet:
                for state in language.states:
                    for next_state in language.get_transitions(state, symbol):
                        new_word = word + symbol
                        if next_state in language.final_states:
                            new_words.add(new_word)
        if not new_words:
            break
        generated_words.update(new_words)
    
    # Vérifier si l'ensemble des mots générés contient un mot du langage
    return any(word in language for word in generated_words)
