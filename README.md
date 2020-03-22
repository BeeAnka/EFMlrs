# EFMlrs
EFMlrs is a Python package combined with a designated workflow that makes it easy for users to calculate elementary flux modes (EFMs) using a new approach in metabolic modelling - the [mplrs algorithm](http://cgm.cs.mcgill.ca/~avis/C/lrs.html). Besides this new approach also [efmtool](https://csb.ethz.ch/tools/software/efmtool.html) is supported, as it uses the most common and established algorithm for calculating EFMs - the double description method.

The mplrs algorithm can make use of up to two thousand threads in parallel so that for the first time EFMs can be calculated for models that are too big to be calculated using tools e.g. efmtool that are based on the double description method. Furthermore the EFMlrs package provides a method that makes it possible to integrate reaction bounds from the sbml files, so that subsets of EFMs can be calculated. This feature is compatible with both algorithms, the mplrs algorithm and the efmtool. EFMlrs can be used as a stand alone console python program but is flexible enough to be integrated in already established workflows.

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

Note that installtion via pip will also take care of all Python related dependencies.

### Requirements for sbml model
- must be compatible with cobrapy
- reaction direction and bounds must be consistent in order to guarantee correct compressions and results e.g. reversibilities will be taken according to lower and upper bounds NOT according to the tag "reversible" in the sbml file (HINT: Check reaction bounds and directions by performing a FVA with cobrapy and compare the results wih the information stored in the sbml file)

### Tools for calculating EFMs
For installtion of [mplrs](http://cgm.cs.mcgill.ca/~avis/C/lrs.html) and [efmtool](https://csb.ethz.ch/tools/software/efmtool.html) please directly refer to the provided information given on their homepages.

## Description
The following description is a basic overview on how the EFMlrs package processes data. More detailed background information, on the program as well as on the usage of mplrs algorithm in context of metabolic modelling, is provided here (link to papers).

EFMlrs consits of two main parts:
* Preprocsessing and compressing the input data
* Postprocessing and decompressing the resulting EFMs

### Preprocessing
As input EFMlrs takes a sbml model. In the first step all necessary information e.g. reaction and metabolite names, reaction reversiblities and if specified also reactions bounds, as well as flux rates, are processed from the provided sbml model. For reading the model and processing the given information the Python package [cobrapy](https://opencobra.github.io/cobrapy/) is being used. Then four uncompressed files containing all necessary information are created. These files are suitable as input files for the efmtool. All internal calculations are done using integers and fractions so that exact arithmetic is guaranteed. Since efmtool only accepts intergers or floats as input formats the file containing the stoichiometric matrix is created twice - one containing fractions and integers and one consisting only of integers.

During the next steps several loss-free compressions are performed in loops on the stoichiometric matrix. These compressions are neeeded in order to accelerate the latter calculations. When all compressions are finished the compressed input files for efmtool are being generated. In a final step the compressed data is being transformed into the H-representation. This file format is the input format for the mplrs algorithm. Additionally an info file, needed for postprocessing the data, and a log file, containing all information on the performed compressions, are generated as well.

#### Overview of files created during postprocessing
- Uncompressed input files for efmtool:
modelname.sfile, modelname_fractions.sfile, modelname.rfile, modelname.rvfile and modelname.mfile
- Compressed input files for efmtool:
modelname_cmp.sfile, modelname_cmp_fractions.sfile, modelname_cmp.rfile, modelname_cmp.rvfile and modelname_cmp.mfile
- Compressed input file for mplrs: modelname.ine
- an info file that is needed for postprocessing (model_name.info)
- a log file with detailed information on the performed compressions (modelname_compression.log

### Calculating elementary flux modes
The calculations of elementary flux modes can be done with mplrs as well as with efmtool.

### Postprocessing
During postprocessing the resulting EFMs are extracted from mplrs output and decompressed. For efmtool outputs only decompressions are necessary. The decompressions are the excat reverse opertations of the preceding compressions. Therefor, besides the mplrs respectively the efmtool output, the info file generated during preprocessing is needed as well.

## Authors
- Bianca Allegra Buchner (MSc)
- Univ.-Prof. Dipl.-Ing. Dr. Jürgen Zanghellini, [University of Vienna](https://ufind.univie.ac.at/en/person.html?id=108792)

I'm a bioinformatician and currently doing my Ph.D at the [University of Natural Resources and Life Sciences](https://boku.ac.at/en/). My group focses on [metabolic modelling and computitional biology](https://boku.ac.at/dbt/arbeitsgruppenresearch-groups/research-group-mattanovich-gasser-sauer/associated-research-groups/metabolic-modelling).

## Acknowledgments
This work has been supported and founded by the COMET center [acib](https://www.acib.at).

## License
* Free software: GPLv3 license
* Documentation: (COMING SOON!) https://EFMlrs.readthedocs.org.
