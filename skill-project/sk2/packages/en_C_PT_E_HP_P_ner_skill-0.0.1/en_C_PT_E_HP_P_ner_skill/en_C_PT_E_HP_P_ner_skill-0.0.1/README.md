Spacy pipeline for skill extraction

| Feature | Description |
| --- | --- |
| **Name** | `en_C_PT_E_HP_P_ner_skill` |
| **Version** | `0.0.1` |
| **spaCy** | `>=3.7.3,<3.8.0` |
| **Default Pipeline** | `tok2vec`, `ner` |
| **Components** | `tok2vec`, `ner` |
| **Vectors** | 0 keys, 0 unique vectors (0 dimensions) |
| **Sources** | n/a |
| **License** | `Public Domain License` |
| **Author** | [Tom Larminier]() |

### Label Scheme

<details>

<summary>View label scheme (1 labels for 1 components)</summary>

| Component | Labels |
| --- | --- |
| **`ner`** | `SKILL` |

</details>

### Accuracy

| Type | Score |
| --- | --- |
| `ENTS_F` | 74.66 |
| `ENTS_P` | 83.74 |
| `ENTS_R` | 67.36 |
| `TOK2VEC_LOSS` | 3961.87 |
| `NER_LOSS` | 399661.14 |