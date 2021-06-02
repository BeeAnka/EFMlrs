### Requirements for SBML files
For compressions with EFMlrs and latter calculations of EFM/Vs with either efmtool or mplrs a sbml file has to fulfill certain criteria that are as follows:
* sbml file must be valid! Check your sbml file under: http://constraint.caltech.edu:8888/validator_servlet/index.jsp
* must be compatible with COBRApy
* reactions - reversible and irreversible - have to be in the forward directions so that the flux direction goes from minimum to maximum
* reversible reactions with only positive fluxes should be made irreversible
* reactions with zero flux and FVA min = FVA max = 0, should be removed from the model to speed up run time of both * compressions and calculations

### Description
Quickcheck_sbml is a small Python script that quickly checks if a sbml fulfills the criteria listed above. It uses uses COBRApy functions to
* parse the given sbml file
* performs FBA and FVA
* checks if flux directions are within the given reaction bounds and fulfill the criteria listed above

Quickcheck_sbml outputs a list of reactions with respective FVA results. These reactions should be checked by the user. Additionally it writes (precise) FVA results for all reactions in the model to an output file (modelname_reactions.txt)

However, since modeling can be tricky there is no guarantee!  It is also highly recommended that users get familiar with theoretical background on calculating EFM/Vs (see references provided in the Readme file) and on how COBRApy handles metabolic models (adding of boundary reactions, handling of reversibilities, reaction bounds etc).

<strong>FVA and fraction_of_optimum parameter</strong>  
The fraction_of_optimum parameter in COBRApy's flux_variability_analysis() function can have huge impact on FVA results
  * COBRApy's default value is 1 - which calculates FVA for model in optimum
  * Quickcheck_sbml's default value is 0.1
  * in Quickcheck_sbml this parameter can be defined by the user

<strong>Compartments and boundary metabolites</strong>  
Often for EFM/EFV enumeration not all compartments in the model should be included. In EFMlrs these compartments can be ignored (user specified parameter). If a compartment should not included in the latter calculations, it can be removed from the model completely or make sure that for Quickcheck_sbml respective metabolites are marked as boundary metabolites in the sbml file (check if `boundaryCondition="true"` for metabolites from compartment to ignore). So that COBRApy recognizes these metabolites correctly and sets additional exchange reactions for them for FVA.  
EFMlrs and Quickcheck_sbml only consider reactions that are actually in the sbml file &rarr; boundary reactions (exchange reactions for boundary metabolites) added by COBRApy are ignored by Quickcheck_sbml as well as by EFMlrs. If these reactions should be taken into account they have to be added to the model directly. (Hint: if sbml file is written out by COBRApy added reactions will be in the written model)

<strong>Precisions and solvers</strong>  
To avoid numeric noise Quickcheck_sbml rounds all results to the 10th decimal for control and console output. Precise values and FVA results for all reactions checked are written to an extra file so that users can also check results for specific reaction.  
The precision of the results depends on the solver installed and used on the specific system. Hence, the solver and therefore its precision can differ from one computing system to another e.g. two pc with same linux distributions can have different solvers in use. Quickcheck_sbml was developed and tested under MacOS Big Sur with glpk solver.

#### General usage
`quickcheck_sbml -s ecoli5010.sbml`  
* -s path to sbml file
* -f (optional) fraction_of_optimum for COBRApy's flux_variability_analysis()

After parsing the model and performing FBA and FVA, Quickcheck_sbml outputs the results on the console. Here an example output with one reversible reaction that is actually irreversible:
```
Adding exchange reaction EX_atpmain_b for boundary metabolite: atpmain_b
Adding exchange reaction EX_ac_b for boundary metabolite: ac_b
Adding exchange reaction EX_co2_b for boundary metabolite: co2_b
Adding exchange reaction EX_etoh_b for boundary metabolite: etoh_b
Adding exchange reaction EX_for_b for boundary metabolite: for_b
Adding exchange reaction EX_h2_b for boundary metabolite: h2_b
Adding exchange reaction EX_glc_D_b for boundary metabolite: glc_D_b
Adding exchange reaction EX_lac_D_b for boundary metabolite: lac_D_b
Adding exchange reaction EX_nh4_b for boundary metabolite: nh4_b
Adding exchange reaction EX_succ_b for boundary metabolite: succ_b
------------------------------------------------
COBRAPY added 10 exchange reaction
------------------------------------------------
Ecoli_core_model
reactions: 78 (including reactions added by cobrapy)
reversibilities:  22
metabolites: 66
genes: 108
growth rate: 29.886593600352644
------------------------------------------------
fraction of optimum: 0.1
------------------------------------------------
Calculating FVA...
Checking reactions...
Writing results to file: ecoli5010_reactions.txt
------------------------------------------------
Please check the following reactions:
NOTE: FVA results are rounded to 10th decimal, exact values can be found in *_reactions.txt
------------------------------------------------
EX_glc_e: glc_D_b <=> glc_D_e
lower bound: -10.0 upper bound: 1000.0
FVA minimum: 61.0546035718 FVA maximum: 1000.0 difference: 938.9453964282
reversibility: True
------------------------------------------------
FVA results are rounded to 10th decimal, exact values can be found in *_reactions.txt
```
Here, only the lower bound has to be changed to 0 to fulfill the requirements for compressions with EFMlrs and latter EFM/V calculations.
