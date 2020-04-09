import cobra
import io
from contextlib import redirect_stderr
import efmlrs.preprocessing.boundaries as boundaries
from efmlrs.util.data import *


def read_model(input_filename):
    stream = io.StringIO()
    with redirect_stderr(stream):
        model = cobra.io.read_sbml_model(input_filename)
    console_output = stream.getvalue()
    return model, console_output


def get_added_reas_metas(model, added_info):
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
    model.remove_reactions(rea_list)
    return model


def rm_metabolites(model, meta_list):
    model.remove_metabolites(meta_list)
    return model


def rm_metas_in_specified_compartment(comp, model):
    metas_in_compartment2remove = []
    for meta in model.metabolites:
        if meta.compartment == comp:
            metas_in_compartment2remove.append(meta)
    model.remove_metabolites(metas_in_compartment2remove)
    return model


def compartments_2_rm(model, comp_list):
    if comp_list is None:
        return model
    else:
        for comp in comp_list:
            rm_metas_in_specified_compartment(comp, model)
        return model

def orphaned_metas_rm(model):
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
    matrix = cobra.util.array.create_stoichiometric_matrix(model)
    return matrix


def check_bounds(model, smatrix, reactions, reversibilities, metabolites):
    smatrix, reactions, reversibilities, metabolites, bound_counter = boundaries.run(model, smatrix, reactions,
                                                                                     reversibilities, metabolites)
    return smatrix, reactions, reversibilities, metabolites, bound_counter


def write_bound_info(core_name, bound_counter):
    info_file_name = core_name + ".info"
    file = open(info_file_name, "w")
    file.write("bounds " + str(bound_counter) + "\n")
    file.close()


def run(inputfile, ignore_compartments, boundflag):
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
        smatrix, reactions, reversibilities, metabolites, bound_counter = check_bounds(model, smatrix, reactions,reversibilities, metabolites)
        write_bound_info(core_name, bound_counter)
        smatrix = write_initial_files_with_bounds(core_name, smatrix, reactions, reversibilities, metabolites)
    else:
        bound_counter = 0
        write_bound_info(core_name, bound_counter)
        smatrix_fract = convert_float2fraction(smatrix)
        smatrix = write_initial_files_no_bounds(core_name, smatrix_fract, reactions, reversibilities, metabolites)

    return smatrix, reactions, reversibilities, metabolites, model, core_name
