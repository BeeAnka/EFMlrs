# EFMlrs
## Background
Mathematically, the problem of elementary flux mode (EFM) determination is identical with the enumeration of corners and edges in a polyhedron for which two approaches: the double description method (DDM) and the lexicographic reverse search (lrs) - have proven particularly useful. Due to performance issues reverse search-based algorithms have been mostly ignored by the metabolic modeling community in the past and (to the extent of my knowledge) all methods available for calculating EFMs are based on the DDM, with [efmtool](https://csb.ethz.ch/tools/software/efmtool.html) being one of its most popular implementations in the metabolic modeling community. However, the DDM and its various implementations require a huge amount of random access memory and lack scalability. Hence, calculating EFMs is currently limited to small and medium-sized networks. Yet, in 2017 D. Avis introduced an improved version of lrs - [mplrs algorithm](http://cgm.cs.mcgill.ca/~avis/C/lrs.html) that allows for parallelization on (high performance) clusters of machines. In contrast to approaches based on the DDM, mplrs is almost ideally parallelizable with negligible memory demands per thread. mplrs can make use of up to two thousand threads in parallel so that for the first time EFMs can be calculated for models that are too big to be calculated using tools based on the DDM e.g. efmtool. For further information please refer to the provided links and references.

## Introduction
EFMlrs is a Python package for pre- and post-processing sbml models for EFM calculations that comes together with a designated workflow. EFMlrs uses COBRApy to process metabolic models, performs loss-free compressions of the stoichiometric matrix, and generates suitable inputs for mplrs as well as efmtool, providing support not only for our proposed new method but also for the already established one. By leveraging COBRApy, EFMlrs also allows the application of additional reaction boundaries, the exclusion of certain compartments and seamlessly integrates into existing workflows

## Installation
pip install EFMlrs

## Requirements
### Basic requirements
- Python 3.7 or higher

### Required Python packages
- cobrapy 0.17.1
- numpy 1.18.1
- pandas 1.0.1
- sympy 1.5.1

Note that installation via pip will also take care of all Python related dependencies.

### Requirements for sbml model
- must be compatible with cobrapy
- reaction direction and bounds must be consistent in order to guarantee correct compressions and results e.g. reversibilities will be taken according to lower and upper bounds NOT according to the tag "reversible" in the sbml file (HINT: Check reaction bounds and directions by performing a FVA with cobrapy and compare the results with information stored in the sbml file)

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

### Preprocessing
As input EFMlrs parses a sbml model. In the first step all necessary information e.g. reaction and metabolite names, reaction reversiblities and if specified also reactions bounds, as well as flux rates, are processed from the provided sbml model. For reading the model and processing the given information the Python package [cobrapy](https://opencobra.github.io/cobrapy/) is being used. Then four uncompressed files containing all necessary information are created. These files are suitable as input files for the efmtool. All internal calculations are done using integers and fractions so that exact arithmetic is guaranteed.

During the next steps several loss-free compressions are performed in loops on the stoichiometric matrix. These compressions are needed to accelerate the latter calculations. When all compressions are finished the compressed input files for efmtool are being generated. In a final step the compressed data is being transformed into the H-representation (see [cdd reference manual](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.130.9984&rep=rep1&type=pdf) for more information on cdd input formats). This file format is the input format for the mplrs algorithm. Additionally, an info file, needed for post-processing the data, and a log file, containing all information on the performed compressions, are generated as well.

#### Overview of files created during postprocessing
- Uncompressed input files for efmtool:
modelname.sfile, modelname.rfile, modelname.rvfile and modelname.mfile
- Compressed input files for efmtool:
modelname_cmp.sfile, modelname_cmp.rfile, modelname_cmp.rvfile and modelname_cmp.mfile
- Uncompressed input file for mplrs: modelname.ine
- Compressed input file for mplrs: modelname_cmp.ine
- an info file that is needed for postprocessing (model_name.info)
- a log file with detailed information on the performed compressions (modelname_compression.log

### Calculating elementary flux modes
The calculations of elementary flux modes can be done with mplrs as well as with efmtool.

### Postprocessing
During postprocessing the resulting EFMs are extracted from mplrs output and decompressed. For efmtool outputs only decompressions are necessary. The decompressions are the exact reverse operations of the preceding compressions. Therefore, besides mplrs respectively efmtool output and the info file (generated during preprocessing) are needed.

## References
EFMlrs: Theoretical description and performance comparison of efmtool, polco and mplrs (coming soon)
mplrs: Avis, D., Jordan, C.: mplrs: A scalable parallel vertex/facetenumeration code (2017), arXiv:1511.06487
efmtool:  Terzer, M., Stelling, J.: Large-scale computation of elementary fluxmodes with bit pattern trees (2008), doi:10.1093/bioinformatics/btn401

## Authors
- Bianca Allegra Buchner (MSc)
- Univ.-Prof. Dipl.-Ing. Dr. Jürgen Zanghellini, [University of Vienna](https://ufind.univie.ac.at/en/person.html?id=108792)

I'm a bioinformatician and currently doing my Ph.D. at the [University of Natural Resources and Life Sciences](https://boku.ac.at/en/). My group focuses on [metabolic modeling and computational biology](https://boku.ac.at/dbt/arbeitsgruppenresearch-groups/research-group-mattanovich-gasser-sauer/associated-research-groups/metabolic-modelling).

## Acknowledgments
This work has been supported and funded by the COMET center [acib](https://www.acib.at).

## License
* Free software: GPLv3 license
* Documentation: https://EFMlrs.readthedocs.org.
