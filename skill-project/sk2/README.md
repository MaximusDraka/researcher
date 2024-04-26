<!-- WEASEL: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 Weasel Project: Detecting SKILL (Named Entity Recognition)

This project uses Spacy matcher and NER Annotator to bootstrap an NER model to detect skills names in Indeed, Livecareer and vaia.be websites

## 📋 project.yml

The [`project.yml`](project.yml) defines the data assets required by the
project, as well as the available commands and workflows. For details, see the
[Weasel documentation](https://github.com/explosion/weasel).

### ⏯ Commands

The following commands are defined by the project. They
can be executed using [`weasel run [name]`](https://github.com/explosion/weasel/tree/main/docs/cli.md#rocket-run).
Commands are only re-run if their inputs have changed.

| Command | Description |
| --- | --- |
| `info` | Info about current Spacy installation |
| `create-config` | use spacy base config to create a new config file |
| `download` | Download a spaCy model with pretrained vectors: https://spacy.io/models/ |
| `preprocess` | Convert the data to spaCy's binary format |
| `debug-data` | debug data |
| `train` | Train a named entity recognition model |
| `evaluate` | Evaluate the model and export metrics |
| `package` | Package the trained model so it can be installed |
| `visualize-model` | Visualize the model's output interactively using Streamlit |
| `visualize-data` | Explore the annotated data in an interactive Streamlit app |
| `print-model-stats` | Overview of model evaluation metrix |
| `print-eval-stats` | Overview of model evaluation metrix |
| `compare-model-eval` | Overview of model evaluation metrix |

### ⏭ Workflows

The following workflows are defined by the project. They
can be executed using [`weasel run [name]`](https://github.com/explosion/weasel/tree/main/docs/cli.md#rocket-run)
and will run the specified commands in order. Commands are only re-run if their
inputs have changed.

| Workflow | Steps |
| --- | --- |
| `all` | `preprocess` &rarr; `train` &rarr; `evaluate` |

### 🗂 Assets

The following assets are defined by the project. They can
be fetched by running [`weasel assets`](https://github.com/explosion/weasel/tree/main/docs/cli.md#open_file_folder-assets)
in the project directory.

| File | Source | Description |
| --- | --- | --- |
| [`assets/All-train-data.json`](assets/All-train-data.json) | Local | JSON-formatted training data joined after NER Annotator |
| `assets/All-test-data.jsonl` | Local | JSON-formatted test data joined after NER Annotator |

<!-- WEASEL: AUTO-GENERATED DOCS END (do not remove) -->