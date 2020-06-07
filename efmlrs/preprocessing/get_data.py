import cobra
import io
from contextlib import redirect_stderr
import efmlrs.preprocessing.boundaries as boundaries
from efmlrs.util.data import *


def read_model(input_filename):
    """
    Reads metabolic model from sbml file using the "cobra.io.read_sbml_model" functions. Reads io string during reading
    model.

    :param input_filename: sbml file with cobrapy compatible metabolic model
    :return:
        - model - cobrapy model
        - console_output - information from cobrapy during reading model
    """

    stream = io.StringIO()
    with redirect_stderr(stream):
        model = cobra.io.read_sbml_model(input_filename)
    console_output = stream.getvalue()
    return model, console_output


def get_added_reas_metas(model, added_info):
    """
    Extracts information on added exchange reactions and metabolites from cobrapy during reading sbml model.

    :param model: cobrapy model
    :param added_info: information from cobrapy during reading model
    :return:
        - ex_reas - list with reaction names added during reading sbml with cobrapy
        - ex_metas - list with metabolite names added during reading sbml with cobrapy
    """
    ex_reas = []
    ex_metas = []
    external = []

    for rea in added_info.split():
        if rea.startswith("EX"):
            ex_reas.append(rea)

    for rea in ex_reas:
        meta = rea[3:]
        external.append(meta)

    for meta in model.metabolites:
        for ex_meta in external:
            if ex_meta == meta.id:
                ex_metas.append(meta)

    return ex_reas, ex_metas


def rm_reactions(model, rea_list):
    """
    Removes exchange reaction that were added by cobrapy.

    :param model: cobrapy model
    :param list rea_list: list of reaction names that will be removed
    :return:
        - model - altered cobrapy model
    """
    model.remove_reactions(rea_list)
    return model


def rm_metabolites(model, meta_list):
    """
    Removes metabolites that were added by cobrapy.

    :param model: cobrapy model
    :param list meta_list: list of metabolite names that will be removed
    :return: model: altered cobrapy model
    """
    model.remove_metabolites(meta_list)
    return model


def rm_metas_in_specified_compartment(comp, model):
    """
    Removes metabolites in specified compartment.

    :param str comp: comparment to ignore
    :param model: cobrapy model
    :return: model: altered cobrapy model
    """
    metas_in_compartment2remove = []
    for meta in model.metabolites:
        if meta.compartment == comp:
            metas_in_compartment2remove.append(meta)
    model.remove_metabolites(metas_in_compartment2remove)
    return model


def compartments_2_rm(model, comp_list):
    """
    Checks if compartment were specified to ignore and removes metabolites that belong to specified compartments.

    :param model: cobrapy model
    :param list comp_list: list of compartments that will be removed
    :return: model: altered cobrapy model
    """
    if comp_list is None:
        return model
    else:
        for comp in comp_list:
            rm_metas_in_specified_compartment(comp, model)
        return model


def orphaned_metas_rm(model):
    """
    Searches and removes orphaned metabolites from cobrapy model.

    :param model: cobrapy model
    :return: model: altered cobrapy model
    """
    metabolites = [meta.id for meta in model.metabolites]
    orphaned_metas = []
    for meta in metabolites:
        meta_id = model.metabolites.get_by_id(meta)
        involved_reas = len(meta_id.reactions)
        if involved_reas == 0:
            orphaned_metas.append(meta_id)
    model.remove_metabolites(orphaned_metas)
    return model


def get_smatrix(model):
    """
    Gets stoichiometric matrix from cobrapy model using the cobrapy function
    "cobra.util.array.create_stoichiometric_matrix".

    :param model: cobrapy model
    :return: matrix: stoichiometric matrix
    """
    matrix = cobra.util.array.create_stoichiometric_matrix(model)
    return matrix


def check_bounds(model, smatrix, reactions, reversibilities, metabolites):
    """
    Calls boundaries script.

    :param model: cobrapy model
    :param smatrix: stoichiometric matrix
    :param reactions: list of reaction names
    :param reversibilities: list of reaction reversibilities
    :param metabolites: list of metabolite names
    :return:
        - smatrix - matrix stoichiometric matrix
        - reactions - list of reactions names
        - reversibilities - list of reaction reversibilities
        - metabolites - list of metabolite names
        - bound_counter - integer number of added bounds
    """
    smatrix, reactions, reversibilities, metabolites, bound_counter = boundaries.run(model, smatrix, reactions,
                                                                                     reversibilities, metabolites)
    return smatrix, reactions, reversibilities, metabolites, bound_counter


def write_bound_info(core_name, bound_counter):
    """
    Writes boundary information to info file.

    :param core_name: string that consists of path to and name of the input file excluding file extension
    :param int bound_counter: integer number of added bounds
    :return: None
    """
    info_file_name = core_name + ".info"
    file = open(info_file_name, "w")
    file.write("bounds " + str(bound_counter) + "\n")
    file.close()


def run(inputfile, ignore_compartments, boundflag):
    """
    Entry point for get_data. Takes sbml file as input. Removes exchange reactions that were added by cobrapy during
    reading. Using cobrapy the model name and properties are extracted. Removes orphaned metabolites. As specified by
    user input ignores compartments a and creates boundary reactions and metabolites. Converts stoichiometric matrix
    coefficients into fractions for precise arithmetic in later calculations and converts stoichiometric matrix from
    list of lists to sympy matrix. Creates the following files: sfile (smatrix), mfile (metabolite names),
    rfile (reaction names), rvfile (reaction reversibilities) and info file.

    :param inputfile: sbml file with cobrapy compatible metabolic model
    :param str ignore_compartments: (optional) user input as string with compartment name that will be ignored
    :param bool boundflag: (optional) user input as bool flag if boundaries from sbml file will be taken into account
    :return:
        - smatrix - sympy matrix of stoichiometric matrix
        - reactions - list of reactions names
        - reversibilities - list of reaction reversibilities
        - metabolites - list of metabolite names
        - model - cobrapy model
        - core_name - path to input file without extensions
    """

    print("Reading input file:", inputfile)
    model, added_info = read_model(inputfile)
    ex_reas, ex_metas = get_added_reas_metas(model, added_info)
    model = rm_reactions(model, ex_reas)
    model = rm_metabolites(model, ex_metas)
    core_name = inputfile[:-4]

    print("Ignoring compartments:", ignore_compartments)
    model = compartments_2_rm(model, ignore_compartments)
    model = orphaned_metas_rm(model)

    model.reactions.sort()
    model.metabolites.sort()
    smatrix = get_smatrix(model)
    reactions = [rea.id for rea in model.reactions]
    reversibilities = [rea.reversibility for rea in model.reactions]
    metabolites = [meta.id for meta in model.metabolites]

    if boundflag is True:
        smatrix, reactions, reversibilities, metabolites, bound_counter = check_bounds(model, smatrix, reactions,
                                                                                       reversibilities, metabolites)
        write_bound_info(core_name, bound_counter)
        smatrix = write_initial_files_with_bounds(core_name, smatrix, reactions, reversibilities, metabolites)
    else:
        bound_counter = 0
        write_bound_info(core_name, bound_counter)
        smatrix_fract = convert_float2fraction(smatrix)
        smatrix = write_initial_files_no_bounds(core_name, smatrix_fract, reactions, reversibilities, metabolites)

    return smatrix, reactions, reversibilities, metabolites, model, core_name
