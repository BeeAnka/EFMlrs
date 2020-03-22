from efmlrs.util.data import *


def search_bounds(model):
    bounds = {}
    for r in model.reactions:
        tmp = []
        if r.reversibility is True:
            if r.lower_bound == -1000.0 and r.upper_bound == 1000.0:
                continue
            elif str(r.lower_bound) == "-inf" and str(r.upper_bound) == "inf":
                continue
            else:
                tmp.append(r.lower_bound)
                tmp.append(r.upper_bound)
                bounds[r.id] = tmp
        else:
            if r.lower_bound == 0 and r.upper_bound == 1000.0:
                continue
            elif r.lower_bound == 0 and str(r.upper_bound) == "inf":
                continue
            else:
                tmp.append(r.lower_bound)
                tmp.append(r.upper_bound)
                bounds[r.id] = tmp

    if bool(bounds) is False:
        return False
    else:
        return bounds


def format_bounds(bounds_info):
    for rea, bounds in bounds_info.items():
        if str(bounds[0]) == "-inf":
            del bounds[0]
            bounds.insert(0, -1000)
        elif str(bounds[1]) == "inf":
            del bounds[1]
            bounds.insert(1, 1000)
    bounds_info = add_boundary_names(bounds_info)
    return bounds_info


def add_boundary_names(bounds_info):
    bounds = {}
    for rea, bound in bounds_info.items():
        if bound[0] != 0 and bound[0] != -1000:
            rea_min = rea + "_min"
            bounds[rea_min] = bound[0]
        if bound[1] != 1000:
            rea_max = rea + "_max"
            bounds[rea_max] = bound[1]
    return bounds


def extend_smatrix(matrix, bounds):
    slack_reas_array = [0] * len(matrix)
    t_matrix = matrix.transpose()
    for i in range(len(bounds) + 1):
        t_matrix = np.vstack([t_matrix, slack_reas_array])
    matrix = t_matrix.transpose()
    return matrix


def get_bounds_index(reas, bounds):
    index_bounds = []
    for rea, bound in bounds.items():
        i = 0
        for reaction in reas:
            name = rea[:-4]
            if reaction == name:
                index_bounds.append(i)
            i += 1
    return index_bounds


def extend_reactions(bounds, reactions):
    index_bounds = get_bounds_index(reactions, bounds)
    extended_reas = []
    j = 0
    for rea, bounds in bounds.items():
        tmp = []
        for i in range(len(reactions)):
            if i == index_bounds[j]:
                if rea[-3:] == "max":
                    tmp.append(1)
                else:
                    tmp.append(-1)
            else:
                tmp.append(0)
        j += 1
        extended_reas.append(tmp)
    return extended_reas


def build_boundary_reactions(bounds):
    slack_reas = []
    j = 0
    for rea, bound in bounds.items():
        tmp = []
        for i in range(len(bounds)):
            if i == j:
                tmp.append(1)
            else:
                tmp.append(0)
        j += 1
        slack_reas.append(tmp)
    return slack_reas


def build_lambda_reas(bounds):
    lambda_reas = []
    for rea, bound in bounds.items():
        tmp = []
        if rea[-3:] == "min":
            tmp.append(bound)
        else:
            new_bound = bound * -1
            tmp.append(new_bound)
        lambda_reas.append(tmp)
    return lambda_reas


def putting_slack_metas_together(bounds, reactions):
    extended_reactions = extend_reactions(bounds, reactions)
    slack_reas = build_boundary_reactions(bounds)
    lambda_reas = build_lambda_reas(bounds)
    slack_metas = []
    for i in range(len(bounds)):
        tmp = extended_reactions[i] + slack_reas[i] + lambda_reas[i]
        slack_metas.append(tmp)
    return slack_metas


def add_slack_metas_2_smatrix(slack_metas, smatrix_extended):
    for i in range(len(slack_metas)):
        smatrix_extended = np.vstack([smatrix_extended, slack_metas[i]])
    return smatrix_extended


def build_new_smatrix(smatrix, bounds, reactions):
    extended_smatrix = extend_smatrix(smatrix, bounds)
    slack_metas = putting_slack_metas_together(bounds, reactions)
    smatrix_extended = add_slack_metas_2_smatrix(slack_metas, extended_smatrix)
    new_smatrix = convert_float2fraction(smatrix_extended)
    return new_smatrix


def build_new_metas(bounds, meta_ori):
    slack_metas = [("MS_" + rea) for rea, bound in bounds.items()]
    new_metas = meta_ori + slack_metas
    return new_metas


def build_new_reas(bounds, reas_ori):
    slack_reas = [("RS_" + rea) for rea, bound in bounds.items()]
    rea_lambda = ["RS_lambda"]
    new_reas = reas_ori + slack_reas + rea_lambda
    return new_reas


def build_new_reversibilities(bounds, revs_ori):
    slack_revs = [(False) for i in range(len(bounds) + 1)]
    new_revs = revs_ori + slack_revs
    return new_revs


def run(model, smatrix, reactions, reversibilities, metabolites):
    print("Checking for additional bounds")
    bound_info = search_bounds(model)
    if bool(bound_info) is True:
        bounds = format_bounds(bound_info)
        bound_counter = len(bounds)
        print("Found", bound_counter, "additional bounds in", model.name+":")
        bounds_print(bounds)

        new_smatrix = build_new_smatrix(smatrix, bounds, reactions)
        new_metabolites = build_new_metas(bounds, metabolites)
        new_reactions = build_new_reas(bounds, reactions)
        new_reversibilities = build_new_reversibilities(bounds, reversibilities)
        return new_smatrix, new_reactions, new_reversibilities, new_metabolites, bound_counter

    else:
        print("ERROR: ADDITIONAL BOUNDS SET IN PROGRAM CALL BUT NO ADDITIONAL BOUNDS FOUND IN SBML FILE")
        print("EXITING PROGRAM")
        exit(1)
