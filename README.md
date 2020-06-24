# Ext-Oracle
*Ext-Oracle Summarization: extractive upper-bound by selecting sentences that maximizes ROUGE-2 score with respect to the target.*

## Installation
* from sources:
```
git clone https://github.com/pltrdy/extoracle_summarization
cd extoracle
pip install .
```

## Generating Oracle summary from files `(source, target)`
```
extoracle source.txt target.txt -method greedy -output oracle.txt
```

## Parameters
```
extoracle -h 
usage: Ext-Oracle Summarization [-h] [-method {greedy,combination}]
                                [-length LENGTH] [-length_oracle]
                                [-output OUTPUT] [-trunc TRUNC]
                                source target
Ext-Oracle Summarization: error: the following arguments are required: source, target
```

## References
* Paper: Ext-Oracle is discussed, and measured again summarization datasets in [Narayan (2018)](https://arxiv.org/abs/1808.08745)
* Code: this repository uses code from [nlpyang/BertSum](https://github.com/nlpyang/BertSum) (Apache 2.0).
