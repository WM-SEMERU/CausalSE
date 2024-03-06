# Toward a Deeper Understanding of Neural Language Models for Code Generation

Neural Language Models (NLMs) for code have rapidly progressed from research prototypes to commercial developer tools, as evidenced by the recent introductions of products such as <i>VSCode IntelliSense</i> and <i>GitHub CoPilot</i>. As these models mature, there is an increasing likelihood that they will be used to assist in building production-level software systems with large user bases. While it is clear that understanding the effectiveness of these models is becoming critical, current efficacy metrics often do not capture their real world performance; the lack of statistical rigor in model evaluations can lead to exaggerated claims as well. While, in general, the performance of NLMs for code appears promising, currently much is unknown about how such models function or their limitations in practical settings. While the prospect of increased developer productivity through automatic code generation is appealing, there is a pressing need to understand these limitations, and their implications, so that future research can focus on improving the correctness, safety, and user experience of deep code generators. 

To this end, this paper introduces <b><i>codegen</i></b>, an evaluation methodology based upon statistical analyses of model predictions and causal inference to enable software oriented explanations to help interpret NLMs for code. While the theoretical underpinnings of \codegen are extensible to exploring different model properties, we provide a concrete instantiation that examines model errors according to programming language concepts, as well as how different usage settings impact model performance. Finally, we illustrate the types of results and insights our evaluation methodology can uncover by performing a case study on two popular deep learning architectures for the task of code completion

# Current Repo Structure
This project follows the structure of `fast.AI` [nbdev](https://nbdev.fast.ai/) template. The following is the folder distribution:
- `docs`: Associated web documentation of the library. 
- `dvc-icodegen`: DVC files for large python notebooks with experiments and datasets.
- `icodegen`: Auto-generated documentation after nbdev compilation.
- `nbs`: Original implementation of the interpretability librery with exploratory programming.
- `notebooks`: Complementary notebooks for testing Large Lenguage Models. 

The folders `paper_nbs` and `scratch_nbs` are intended to computational prototypes and their original paper. 

# Testbeds and Training Datasets
- Raw Training Dataset: [CodeSearchNet](https://www.dropbox.com/s/fyi3fzf2xlslfl1/raw_searchnet.zip?dl=0)
- Raw Testbeds: [link](https://www.dropbox.com/s/qy9m1fsu1w0trp2/raw_testbeds.zip?dl=0)
- Pre-processed Testbeds: [covariates](https://www.dropbox.com/s/g76orgo7v0hvh8m/covariate_testbeds.zip?dl=0)

The authors will realease the remaining models/data upon ICSE'22 acceptance. 

# Experiments
The following [link](https://www.dropbox.com/s/rg95s36vitdai1q/experiments_notebooks.zip?dl=0) contains all the notebooks with the experiments proposed on the paper. 
