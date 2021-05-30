# EFMlrs - Elementary flux mode enumeration via mplrs
EFMlrs is the first program that gives users the ability to enumerate EFMs and EFVs in metabolic models on HPC clusters via mplrs. It can be used as a stand-alone program but also seamlessly integrates in existing workflows. In particular, EFMlrs adds EFM/EFV capabilities via mplrs and the possibility to make use of HPC systems to COBRApy.

## Background
Mathematically, the problem of elementary flux mode (EFM) determination is identical with the enumeration of corners and edges in a polyhedron for which two approaches: the double description method ([DDM](https://people.inf.ethz.ch/fukudak/lect/pclect/notes2016/PolyComp2016.pdf0)) and the lexicographic reverse search ([lrs](http://cgm.cs.mcgill.ca/%7Eavis/doc/avis/Av98a.pdf)) - have proven particularly useful. Due to performance issues reverse search-based algorithms have been mostly ignored by the metabolic modeling community in the past and (to the extent of my knowledge) all methods available for calculating EFMs are based on the DDM, with [efmtool](https://csb.ethz.ch/tools/software/efmtool.html) being one of its most popular implementations in the metabolic modeling community. However, the DDM and its various implementations require a huge amount of random access memory and lack scalability. Hence, calculating EFMs is currently limited to small and medium-sized networks. Yet, in 2017 D. Avis introduced an improved version of lrs - [mplrs](http://cgm.cs.mcgill.ca/~avis/C/lrs.html) algorithm that allows for parallelization on High-performance computing (HPC) systems. In contrast to approaches based on the DDM, mplrs is almost ideally parallelizable with negligible memory demands per thread. mplrs can make use of up to two thousand threads in parallel so that for the first time EFMs can be calculated for models that are too big to be calculated using tools based on the DDM e.g. efmtool. For further information please refer to the provided links and references.

## Introduction
EFMlrs is a Python package for pre- and post-processing sbml models for EFM calculations that comes together with a designated workflow. EFMlrs uses [Cobrapy](https://opencobra.github.io/cobrapy/) to process metabolic models, performs loss-free compressions of the stoichiometric matrix, and generates suitable inputs for mplrs as well as efmtool, providing support not only for our proposed new method but also for the already established one. By leveraging COBRApy, EFMlrs also allows the application of additional reaction boundaries, the exclusion of certain compartments and seamlessly integrates into existing workflows

## Installation
pip install EFMlrs

## Requirements
- Python 3.7 or higher
- pip

<strong>Please read the provided Tutorials (Tutorial_EFMlrs) and carefully and also check your sbml input, see Tutorial_Check_SBML.</strong>

### Required Python packages
- cobrapy 0.17.1
- numpy 1.18.1
- pandas 1.0.1
- sympy 1.5.1

Note that installation via pip will also take care of all Python related dependencies.

### Tools for calculating EFMs
#### mplrs
- Download latest version from (http://cgm.cs.mcgill.ca/~avis/C/lrslib/archive/)
- Default installation: make mplrs

NOTE: mplrs uses MPI for parallelization and therefore requires the MPI library.

#### efmtool
- Download and unzip latest version from (https://csb.ethz.ch/tools/software/efmtool.html)
- efmtool is a java program and be run directly without further installation

Note: A [Java VM](http://java.sun.com) is required on your system.

For more detailed information on how to use either [mplrs](http://cgm.cs.mcgill.ca/~avis/C/lrs.html) or [efmtool](https://csb.ethz.ch/tools/software/efmtool.html) please refer directly to the provided information given on the respective homepage.

## Description
The following description is a basic overview of how the EFMlrs package processes data. A schematic workflow of EFMlrs can be found in the pdf "Overview" as well. More detailed background information, on the program as well as on the usage of mplrs algorithm in the context of metabolic modeling, is provided here in the references.

Calculations of EFMs using EFMlrs consist of three main parts:
* Pre-processing sbml models incl. loss-free compression of the stoichiometric matrix and user-defined options: ignoring specific compartments and including additional reaction bounds
* Calculations of EFMs with either mplrs or efmtool
* Post-processing and decompressing output from efmtool and mplrs

### Pre-processing
As input EFMlrs parses a sbml model. In the first step all necessary information e.g. reaction and metabolite names, reaction reversiblities and if specified also reactions bounds, as well as flux rates, are processed from the provided sbml model. For reading the model and processing the given information the Python package [COBRApy](https://opencobra.github.io/cobrapy/) is being used. Then four uncompressed files containing all necessary information are created. These files are suitable as input files for the efmtool. All internal calculations are done using integers and fractions so that exact arithmetic is guaranteed.

During the next steps several loss-free compressions are performed in loops on the stoichiometric matrix. These compressions are needed to accelerate the latter calculations. When all compressions are finished the compressed input files for efmtool are being generated. In a final step the compressed data is being transformed into the H-representation (see [cdd reference manual](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.130.9984&rep=rep1&type=pdf) for more information on cdd input formats). This file format is the input format for the mplrs algorithm. Additionally, an info file, needed for post-processing the data, and a log file, containing all information on the performed compressions, are generated as well.

#### Overview of files created during post-processing
- Uncompressed input files for efmtool:
modelname.sfile, modelname.rfile, modelname.rvfile and modelname.mfile
- Compressed input files for efmtool:
modelname_cmp.sfile, modelname_cmp.rfile, modelname_cmp.rvfile and modelname_cmp.mfile
- Uncompressed input file for mplrs: modelname.ine
- Compressed input file for mplrs: modelname_cmp.ine
- an info file that is needed for post-processing (model_name.info)
- a log file with detailed information on the performed compressions (modelname_compression.log

### Calculating elementary flux modes
The calculations of elementary flux modes can be done with mplrs as well as with efmtool. The computations are intentionally not directly included in the program as mplrs is meant to be executed on HPC cluster, whereas pre- and post-processing, as well as computations with efmtool, can be done on a single machine.

### post-processing
During post-processing the resulting EFMs are extracted from mplrs output and decompressed. For efmtool outputs only decompressions are necessary. The decompressions are the exact reverse operations of the preceding compressions. Therefore, besides mplrs respectively efmtool output and the info file (generated during preprocessing) are needed.

## References
[mplrs](https://arxiv.org/abs/1511.06487): Avis, D., Jordan, C.: mplrs: A scalable parallel vertex/facetenumeration code (2017), arXiv:1511.06487  
[lrs](http://cgm.cs.mcgill.ca/%7Eavis/doc/avis/Av98a.pdf): D. Avis, “lrs: A Revised Implementation of the Reverse Search Vertex Enumeration Algorithm,” in Polytopes – Combinatorics and Computation, 2000, pp. 177–198  
[DDM](https://people.inf.ethz.ch/fukudak/lect/pclect/notes2016/PolyComp2016.pdf0): Fukuda, ETH Zurich - Course Catalogue, 2016  
[efmtool](https://academic.oup.com/bioinformatics/article/24/19/2229/246674): Terzer, M., Stelling, J.: Large-scale computation of elementary fluxmodes with bit pattern trees (2008), doi:10.1093/bioinformatics/btn401  
[cdd reference manual](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.130.9984&rep=rep1&type=pdf)  
COBRApy on [github](https://opencobra.github.io/cobrapy/) and [code documentation](https://cobrapy.readthedocs.io/en/latest/)  
EFMlrs (coming soon): Buchner and Zanghellini: EFMlrs: A Python package for elementary flux mode enumeration via lexicographic reverse search'


## Authors
- Bianca Allegra Buchner (MSc)
- Univ.-Prof. Dipl.-Ing. Dr. Jürgen Zanghellini, [University of Vienna](https://ufind.univie.ac.at/en/person.html?id=108792)

I'm a bioinformatician and currently doing my Ph.D. at the [University of Natural Resources and Life Sciences](https://boku.ac.at/en/). My group focuses on [metabolic modeling and computational biology](https://boku.ac.at/dbt/arbeitsgruppenresearch-groups/research-group-mattanovich-gasser-sauer/associated-research-groups/metabolic-modelling).

## Acknowledgments
This work has been supported and funded by the COMET center [acib](https://www.acib.at).

## License
* Free software: GPLv3 license
* Documentation: https://EFMlrs.readthedocs.org.
