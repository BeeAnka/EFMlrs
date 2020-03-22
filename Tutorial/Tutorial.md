## Preprocessing
Under [Tutorial/example_models](https://github.com/BeeAnka/EFMlrs/tree/master/tests/example_models) the sbml file of an Escherichia coli core model (ecoli5010.xml) that is being used for this tutorial is provided.

**General usage**

`usage: efmlrs_pre -i <metabolic_model>.xml [--ignore_compartments <compartment name>] [--bounds]`

- efmlrs_pre: function that starts preprocessing
- -i: provide path to sbml (mandatory parameter)
- --ignore_compartments: provide one or more compartment names from sbml file that should be EXCLUDED from the model (optional parameter)
- --bounds: if efmlrs_pre is being called with this parameters all reactions bounds from the sbml model will be integrated in the stoichiometric matrix (optional parameter)

Depending on the size of the model compressions may take a while. Also due to using exact arithmetics and the sympy package for null space and reduced row echelon calculations, compression can consume quiet a lot of RAM.

**Example calls:**

Compartment C_b will be ignored and no bounds from sbml are taken:

`efmlrs_pre -i PATH2SBML/ecoli5010.xml --ignore_compartments C_b`

or compartment C_b will be ignored and bounds from sbml are taken:

`efmlrs_pre -i PATH2SBML/ecoli5010.xml --ignore_compartments C_b --bounds`

Now preprocessing and compression start. Detailed information is given via terminal output.

**Example terminal output for efmlrs_pre with bounds**
```
            EFMlrs    __
    (\   .-.   .-.   /_")
     \\_//^\\_//^\\_//
      `"´   `"´   `"´
     start compressions

Reading input file: ecoli5010.xml
Ignoring compartments: C_b
Checking for additional bounds
Found 2 additional bounds in Ecoli_core_model:
Lower bound: 8.39 for reaction ATPM
Lower bound: -10.0 for reaction EX_glc_e
Ecoli_core_model consists of 71 reactions ( 13 reversible ) and 68 metabolites before compressions.
========================================================================
START COMPRESSIONS
Deadend compressions ( 1 )
Ecoli_core_model consists of 43 reactions ( 13 reversible ) and 43 metabolites after compressions.
One2Many compressions ( 1 )
Ecoli_core_model consists of 27 reactions ( 13 reversible ) and 26 metabolites after compressions.
NullSpace compressions ( 1 )
Start null space calculations round 1 .This may take a while
Done null space calculations.
Start null space calculations round 2 .This may take a while
Done null space calculations.
Start null space calculations round 3 .This may take a while
Done null space calculations.
Start null space calculations round 4 .This may take a while
Done null space calculations.
Start null space calculations round 5 .This may take a while
Done null space calculations.
Start null space calculations round 6 .This may take a while
Done null space calculations.
Ecoli_core_model consists of 11 reactions ( 13 reversible ) and 13 metabolites after compressions.
Echelon compressions ( 1 )
Start reduced row echelon form calculations 1 . This may take a while
Done reduced row echelon form calculations.
Start reduced row echelon form calculations 2 . This may take a while
Done reduced row echelon form calculations.
Ecoli_core_model consists of 11 reactions ( 13 reversible ) and 7 metabolites after compressions.
Deadend compressions ( 2 )
Ecoli_core_model consists of 11 reactions ( 13 reversible ) and 7 metabolites after compressions.
One2Many compressions ( 2 )
Ecoli_core_model consists of 9 reactions ( 13 reversible ) and 5 metabolites after compressions.
NullSpace compressions ( 2 )
Start null space calculations round 1 .This may take a while
Done null space calculations.
Ecoli_core_model consists of 9 reactions ( 13 reversible ) and 5 metabolites after compressions.
Echelon compressions ( 2 )
Start reduced row echelon form calculations 1 . This may take a while
Done reduced row echelon form calculations.
Ecoli_core_model consists of 9 reactions ( 13 reversible ) and 5 metabolites after compressions.
DONE COMPRESSIONS after:  2 rounds
========================================================================
Ecoli_core_model consists of 9 reactions ( 4 reversible ) and 5 metabolites after compressions.
Writing files

                    .-.
                  /  oo
   EFMlrs         \ -,_)
             _..._| \ `-<
        {} ." .__.\' |
       {} (         /`\
       {}(`´------´   /
          `----------´
   finished compressions
 ```
## Calculating EFMs

For calculating EFMs with mplrs it is not mandatory but highly recommended to use the *mplrs redund* function on the *ine* file created during preprocessing. For further information please refer to the [mplrs user guide](http://cgm.cs.mcgill.ca/~avis/C/lrslib/USERGUIDE.html)

## Postprocessing
Under [Tutorial/example_results](https://github.com/BeeAnka/EFMlrs/tree/master/Tutorial/example_results) example outputs with and without bounds (incl. the corresponding info files) from mplrs and efmtool are provided. In this tutorial we will proceed with the mplrs output that includes bounds ("ecoli5010_cmp_bounds_mplrs.efms").

**General usage**
```
efmlrs_post -i <input file with compressed efms> -o <output file> -info <efmlrs info file> [--efmtool]
```

- efmlrs_post: funktion that starts postprocessing
- -i: provide path and name to compressed EFMs (mandatory parameter)
- -o: provide path and name to output file where decompressed EFMs will be stored (mandatory parameter)
- --info: provide path and name to info file generated during preprocessing (mandatory parameter)
- --efmtool: if compressed EFMs from efmtool should be extracted set this (optional) parameter

**Example calls for postprocessing:**

for mplrs
```
efmlrs_post -i PATH2COMPRESSED_EFMS/ecoli5010_cmp_bounds_mplrs.efms -o PATH2OUTPUT/ecoli5010_decompressed_mplrs.efms --info PATH2INFOFILE/ecoli5010_bounds.info
```
for efmtool
```
efmlrs_post -i PATH2COMPRESSED_EFMS/ecoli5010_cmp_bounds_efmtool.efms -o PATH2OUTPUT/ecoli5010_decompressed_efmtool.efms --info PATH2INFOFILE/ecoli5010_bounds.info --efmtool
```

**Example terminal output from efmlrs_post**
```
                    .-.
                  /  oo
   EFMlrs         \ -,_)
             _..._| \ `-<
        {} ." .__.\' |
       {} (         /`\
       {}(`´------´   /
          `----------´
      start decompressions

Decompressing EFMs from MPLRS
Start decompressions
EFMs decompressed: 1000
EFMs decompressed: 2000
EFMs decompressed: 3000
EFMs decompressed: 4000
EFMs decompressed: 5000
Decompressed EFMs: 5376

           EFMlrs     __
    (\   .-.   .-.   /_")
     \\_//^\\_//^\\_//
      `"´   `"´   `"´
   finished decompressions
```









