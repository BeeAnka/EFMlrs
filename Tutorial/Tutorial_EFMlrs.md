## Preprocessing
A sbml file of an Escherichia coli core model (ecoli5010.xml) is used for this tutorial and provided for download. The various in- and output files for this model are provided for download here in the tutorial section. Other models we already worked with are available for download in the folder "metabolic models".

Please make sure that your sbml input file fulills all requirements. If you are unsure check out the provided "Tutorial_Check_SBML".

**General usage**

`usage: efmlrs_pre -i <metabolic_model>.xml [--ignore_compartments <compartment name>] [--bounds]`

- efmlrs_pre: function that starts preprocessing
- -i: provide path to sbml (mandatory parameter)
- --ignore_compartments: provide one or more compartment names from sbml file that should be EXCLUDED from the model (optional parameter)
- --bounds: if efmlrs_pre is being called with this parameters all reactions bounds from the sbml model will be integrated in the stoichiometric matrix (optional parameter)

Depending on the size of the model compressions may take a while. Also due to using exact arithmetic and the sympy package for null space and reduced row echelon calculations, compression can take a while and consume quiet a lot of RAM.

**Example calls:**

Compartment C_b will be ignored and no bounds from sbml are taken:

`efmlrs_pre -i PATH2SBML/ecoli5010.xml --ignore_compartments C_b`

or compartment C_b will be ignored and bounds from sbml are taken:

`efmlrs_pre -i PATH2SBML/ecoli5010.xml --ignore_compartments C_b --bounds`

Now preprocessing and compression start. Detailed information is given via terminal output.

**Example terminal output of efmlrs_pre for E.coli 5010 without additional reaction bounds**
```
           EFMlrs     __
    (\   .-.   .-.   /_")
     \\_//^\\_//^\\_//   
      `"´   `"´   `"´    
     start compressions   

Reading input file: ecoli5010.xml
Ignoring compartments: ['C_b']
Uncompressed network size: 68 reactions ( 12 reversible ) and 56 metabolites.
========================================================================
START COMPRESSIONS
*** Compression round: 1 ***
Start deadend compression...
Done deadend compression. Network size: 56 metabolites and 68 reactions ( 12 reversible )
Start many2one compression...
Done many2one compression. Network size: 28 metabolites and 40 reactions ( 12 reversible )
Start nullspace compression...
Done nullspace compression. Network size: 25 metabolites and 37 reactions ( 12 reversible )
Start echelon compressions...
Done echelon compression. Network size: 20 metabolites and 37 reactions ( 12 reversible )
*** Compression round: 2 ***
Start deadend compression...
Done deadend compression. Network size: 20 metabolites and 37 reactions ( 12 reversible )
Start many2one compression...
Done many2one compression. Network size: 20 metabolites and 37 reactions ( 12 reversible )
Start nullspace compression...
Done nullspace compression. Network size: 20 metabolites and 37 reactions ( 12 reversible )
Start echelon compressions...
Done echelon compression. Network size: 20 metabolites and 37 reactions ( 12 reversible )
*** COMPRESSIONS DONE after: 2 rounds ***
========================================================================
Compressed network size: 37 reactions ( 9 reversible ) and 20 metabolites.
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

### mplrs - example call
 `mpirun -np <number of processes>  mplrs <infile> <outfile>`
 `mpirun -np 20 mplrs ecoli5010_cmp.ine ecoli5010_cmp.out`

### efmtool - example call
`java -jar efmtool.jar -kind stoichiometry -stoich <sfile> -rev <rvfile> -meta <mfile> -reac <rfile> -out text-doubles <outfile> -maxthreads 20`
`java -jar efmtool.jar -kind stoichiometry -stoich ecoli5010.sfile -rev ecoli5010.rvfile -meta ecoli5010.mfile -reac ecoli5010.rfile -out text-doubles ecoli5010.efms -maxthreads 20`

## Postprocessing
Depending on which output -mplrs or efmtool - is to be decompressed, EFMlrs post-processing is called without or with the parameter --efmtool. If bounds are applied or not, does not change usage of EFMlrs post-processing. All necessary information is provided in the info file. Please note that EFMlrs is determined for handling compressed data that was also originally compressed with EFMlrs. If for any reason EFM calculations were performed with the non-compressed data, efmtool does not require any post-processing. For post-processing uncompressed mplrs output one can simply manually remove the compression information in the info file and call efmlrs_post as usual. In this case only header and footer will be removed and the, during pre-processing, split reversible reactions will be merged together.

**General usage**  

`efmlrs_post -i <input file with compressed efms> -o <output file> -info <efmlrs info file> [--efmtool]`

- efmlrs_post: function that starts postprocessing
- -i: provide path and name to compressed EFMs (mandatory parameter)
- -o: provide path and name to output file where decompressed EFMs will be stored (mandatory parameter)
- --info: provide path and name to info file generated during preprocessing (mandatory parameter)
- --efmtool: if compressed EFMs from efmtool should be extracted set this (optional) parameter

**Example calls for postprocessing:**

for mplrs  
`efmlrs_post -i PATH2COMPRESSED_EFMS/ecoli5010_cmp_mplrs.efms -o PATH2OUTPUT/ecoli5010_decmp_mplrs.efms --info PATH2INFOFILE/ecoli5010.info`

for efmtool  
`efmlrs_post -i PATH2COMPRESSED_EFMS/ecoli5010_cmp_efmtool.efms -o PATH2OUTPUT/ecoli5010_decmp_efmtool.efms --info PATH2INFOFILE/ecoli5010.info --efmtool`

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
Decompressed EFMs: 5011

           EFMlrs     __
    (\   .-.   .-.   /_")
     \\_//^\\_//^\\_//   
      `"´   `"´   `"´    
   finished decompressions
```
