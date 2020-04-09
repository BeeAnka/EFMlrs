from efmlrs.util.log import *


def check_row(row):
    state = 0
    for j in row:
        if state == 0:
            state = j
            continue
        if state < 0:
            if j <= 0:
                continue
            else:
                return False
        if state > 0:
            if j >= 0:
                continue
            else:
                return False
    return True


def check_reactions(smatrix, i, reversibilities):
    rm_reactions = []
    index = 0
    for val in smatrix.row(i):
        if val != 0:
            if reversibilities[index] == 0:
                rm_reactions.append(index)
            else:
                return []
        index += 1
    return rm_reactions


def find_deadends(smatrix, reversibilities):
    remove_reactions = []
    remove_metabolites = []

    for i in range(0, smatrix.shape[0]):
        tmp = check_row(smatrix.row(i))
        if tmp == False:
            continue
        else:
            rm_reactions = check_reactions(smatrix, i, reversibilities)
            if len(rm_reactions) != 0:
                remove_metabolites.append(i)
                for item in rm_reactions:
                    remove_reactions.append(item)

    remove_reactions = sorted(set(remove_reactions))
    remove_metabolites = sorted(set(remove_metabolites))
    return remove_reactions, remove_metabolites


def write_deadend_info(core_name, outer_counter, removedReactions):
    info_file_name = core_name + ".info"
    file = open(info_file_name, "a")
    file.write("deadend_" + str(outer_counter) + "\n")
    for reactions in removedReactions:
        file.write("remove")
        for rea in reactions:
            file.write(" " + str(rea))
        file.write("\n")
    file.write("end\n")
    file.close()


def run(smatrix, reactions, reversibilities, metabolites, core_name, outer_counter):
    log_module()
    inner_counter = 1
    removed_reactions = []
    while 1:
        remove_reactions, remove_metabolites = find_deadends(smatrix, reversibilities)
        if len(remove_reactions) == 0 and len(remove_metabolites) == 0:
            break

        for index in reversed(remove_reactions):
            log_delete_rea(reactions[index])
            smatrix.col_del(index)
            del reactions[index]
            del reversibilities[index]
        removed_reactions.append(remove_reactions)

        for index in reversed(remove_metabolites):
            log_delete_meta(metabolites[index])
            smatrix.row_del(index)
            del metabolites[index]

        inner_counter += 1

    write_deadend_info(core_name, outer_counter, removed_reactions)

    return smatrix, reactions, reversibilities, metabolites
