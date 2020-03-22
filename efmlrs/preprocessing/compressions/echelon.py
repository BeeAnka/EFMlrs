from efmlrs.util.log import *
from efmlrs.util.data import *


def find_redundant_metabolites(smatrix, inner_counter):
    print("Start reduced row echelon form calculations",str(inner_counter),". This may take a while")
    echelon = smatrix.T.rref(simplify=True, pivots=False)
    print("Done reduced row echelon form calculations.")
    columns = echelon.shape[1]
    rows = echelon.shape[0]
    redundant_metas = []
    j = 0
    for i in range(0, rows):
        row = echelon.row(i)
        while j < columns and row[j] != 1:
            redundant_metas.append(j)
            j += 1
        j += 1
    return redundant_metas


def remove_redundant_metabolites(smatrix, metabolites, redundant_metas):
    for i in reversed(redundant_metas):
        log_delete_meta(metabolites[i])
        del (metabolites[i])
        smatrix.row_del(i)
    return smatrix, metabolites


def run(smatrix, metabolites):
    log_module()
    inner_counter = 1

    while 1:
        redundant_metas = find_redundant_metabolites(smatrix, inner_counter)
        if len(redundant_metas) == 0:
            break
        smatrix, metabolites = remove_redundant_metabolites(smatrix, metabolites, redundant_metas)
        inner_counter += 1

    return smatrix, metabolites
