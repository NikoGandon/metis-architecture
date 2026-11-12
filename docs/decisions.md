# Décisions de conception

## 1. Contrôle hors du LLM

- **Contexte** : les agents lisent des textes externes et peuvent être induits en erreur ou halluciner une citation.
- **Choix** : les règles qui peuvent être décidées mécaniquement (citation exacte, transitions d'état, budget, validation de schéma) sont exécutées en code autour des agents.
- **Alternatives écartées** : demander au modèle de respecter la règle dans le prompt ; ajouter un second LLM pour vérifier le premier.
- **Limites** : une règle mécanique ne juge pas le sens. Une citation exacte peut être hors contexte ; ce point reste confié aux juges.

## 2. Chaîne d'étapes explicite plutôt que LangGraph

- **Contexte** : plusieurs agents à enchaîner, avec des rejets possibles à chaque étape.
- **Choix** : fonctions simples prenant un état et renvoyant un état, persisté après chaque étape. Le flux est linéaire et lisible.
- **Alternatives écartées** : un framework de graphes d'agents comme LangGraph (non utilisé dans la dernière version du code). Le but est de garder le contrôle du flux en code simple.
- **Limites** : pas de graphe déclaratif ni d'outillage de visualisation intégré ; si les cycles se multiplient (notamment pour D1), cette décision serait à réexaminer.

## 3. Fail-closed

- **Contexte** : un audit documentaire qui laisse passer une affirmation douteuse est pire qu'un audit qui en rejette une valide.
- **Choix** : en cas d'échec de vérification, de sortie invalide ou de refus du fournisseur, l'élément est rejeté avec un motif. Un refus du fournisseur n'est ni retenté ni remplacé par un autre modèle, et il est mesuré.
- **Alternatives écartées** : nouvel essai automatique avec reformulation ; modèle de repli.
- **Limites** : des cas valides sont écartés, notamment sur des sujets sensibles.

## 4. Schémas stricts et objets immuables

- **Contexte** : les sorties de modèles sont variables ; un champ inattendu peut cacher une dérive.
- **Choix** : chaque sortie est validée par un schéma qui refuse les champs inconnus ; les objets d'état sont immuables et les changements de statut passent par des transitions autorisées.
- **Alternatives écartées** : lecture tolérante du JSON ; dictionnaires libres.
- **Limites** : un changement de schéma impose de régénérer les enregistrements de tests.

## 5. Tests rejouables et suivi des coûts

- **Contexte** : les appels LLM sont payants et non déterministes.
- **Choix** : les réponses réelles sont enregistrées et rejouées sous test, avec réseau bloqué ; un journal écrit les coûts par rôle et un budget par run refuse tout appel qui pourrait le dépasser.
- **Alternatives écartées** : mocks écrits à la main ; appels réels dans les tests.
- **Limites** : les enregistrements vieillissent quand un prompt, un schéma ou un modèle change ; ils reflètent un moment donné.

## 6. Exécution isolée du code généré (D1)

- **Contexte** : le forgeron produit du code qu'il ne faut pas exécuter dans l'environnement principal.
- **Choix** : backend d'isolation configurable (conteneur ou bubblewrap par défaut), plus un mode local non isolé explicitement nommé comme tel. Contrôles prévus : analyse syntaxique, exécution isolée, cas cachés, invariants.
- **Alternatives écartées** : exécution directe dans le processus ; mode isolé unique.
- **Limites** : D1 n'est que partiellement implémenté ; une isolation ne remplace pas la revue des résultats.
