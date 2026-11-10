# The Nose-tral Network

### The documentation

*A project by Dibyajyoti Pradhan, featuring the AI model **Aroma-GPT**.*

## Abstract

The Nose-tral Network is a project that combines two kinds of smell AI. The first, **Aroma-GPT's smell model**, reads the chemical structure of a molecule and predicts which of 138 smell words describe it, reaching an average ROC-AUC of {{auc}} on molecules it had never seen. The second is an **electronic nose**: eight gas sensors whose readings are interpreted by a second model that must name the smell from the numbers alone.

The electronic nose is currently **simulated in code**. It demonstrates how the full pipeline works. The author's next step is to rebuild it with real smelling devices, test it, and update this documentation with the results.

This book describes the idea, the data, how each model was built and trained, how well it works, and where it falls short. It is written to be readable by someone with no background, and each chapter can be read on its own.

## Contents
