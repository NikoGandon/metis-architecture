# Architecture de Mêtis

Documentation de conception. Aucun code du projet n'est reproduit.

## 1. Flux principal de D0

```mermaid
flowchart TD
    Q[Question] --> COL[Collecter<br/>PubMed, PMC OA, arXiv]
    COL --> EXT[Extraire<br/>agent LLM]
    EXT --> FIL[Filtrer<br/>citation exacte + pré-filtres, sans LLM]
    FIL --> AUD[Auditer<br/>agent LLM]
    AUD --> REF[Chercher des réfutations<br/>agent LLM + nouvelles requêtes]
    REF --> EVA[Évaluer les preuves adverses]
    EVA --> ROU[Router<br/>verdict]
    ROU --> RAP[Rapport]
    FIL -. rejet .-> RAP
```

Légende : les étapes sont enchaînées par du code, l'état est persisté après chacune. Les rejets mécaniques sortent du flux sans solliciter de juge.

## 2. Composants

```mermaid
flowchart LR
    subgraph Orchestration
        ORC[Chaîne d'étapes]
        ETAT[État immuable + transitions]
    end
    subgraph Agents LLM
        AG[Extracteur, auditeur,<br/>contradicteur, routeur, forgeron]
    end
    subgraph Contrôles sans LLM
        VER[Vérification de citation]
        PRE[Pré-filtres]
        SCH[Schémas stricts]
        BUD[Budget par run]
    end
    subgraph Infrastructure
        CLI[Client LLM<br/>+ rejeu des réponses]
        LED[Journal des coûts par rôle]
        COLL[Collecteurs de sources]
        SBX[Exécution isolée - D1]
    end
    ORC --> ETAT
    ORC --> AG
    ORC --> VER
    ORC --> PRE
    AG --> CLI
    CLI --> SCH
    CLI --> BUD
    CLI --> LED
    ORC --> COLL
    AG -.-> SBX
```

Légende : les agents n'ont accès qu'au client LLM, qui valide les sorties, applique le budget et journalise. Les contrôles sont appelés par l'orchestration, jamais par les agents. Le lien vers l'exécution isolée concerne D1.

## 3. Séquence d'un cas clé : citation inexacte

```mermaid
sequenceDiagram
    participant O as Orchestration
    participant E as Agent extracteur
    participant V as Vérification (code)
    participant A as Agent auditeur
    participant S as État / rapport
    O->>E: document source
    E-->>O: affirmation + citation proposée
    O->>V: citation, texte source
    alt citation absente de la source
        V-->>O: refus
        O->>S: statut rejeté, motif enregistré
        Note over A: l'auditeur n'est jamais appelé
    else citation présente
        V-->>O: acceptée
        O->>A: affirmation + contexte autour de la citation
        A-->>O: jugement structuré
        O->>S: statut mis à jour
    end
```

Légende : une citation reformulée ou inventée par le modèle est arrêtée par une comparaison de texte, avant tout jugement sémantique et sans dépendre de la bonne volonté du modèle.
