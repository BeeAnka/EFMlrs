from efmlrs.util.data import *
from efmlrs.util.log import *


def rv_check(row, reversibilities):
    skip = False
    for i, rev in zip(range(0, len(reversibilities)), reversibilities):
        if rev == 1:
            if row[i] != 0:
                skip = True
                break
        else:
            continue
    return skip


def count_check(row):
    count_pos = 0
    count_neg = 0
    for reaction in row:
        if reaction == 0:
            continue
        elif reaction < 0:
            count_neg += 1
        else:
            count_pos += 1
        if count_pos > 1 and count_neg > 1:
            break
    if count_pos == 0 or count_neg == 0:
        return True
    if count_pos > 1 and count_neg > 1 or count_pos + count_neg < 2:
        return True
    return False


def get_index(row, index):
    pos = [(i, abs(j)) for i, j in zip(index, row) if j > 0]
    neg = [(i, abs(j)) for i, j in zip(index, row) if j < 0]
    if len(pos) == 1:
        return pos, neg
    else:
        return neg, pos


def is_zero(row):
    return all(i == 0 for i in row)


def remove_zero_rows(smatrix, metabolites):
    drops = []
    metadrops = []
    count = 0
    for index, row in smatrix.iterrows():
        if is_zero(row) is True:
            drops.append(index)
            metadrops.append(count)
        count += 1
    smatrix.drop(drops, axis=0, inplace=True)
    for i in reversed(metadrops):
        log_delete_meta(metabolites[i])
        del metabolites[i]


def merge_compress(smatrix, reversibilities, metabolites):
    inner_counter = 1
    compress = []
    while 1:
        remove = []
        for index, row in smatrix.iterrows():
            if rv_check(row, reversibilities) is True:
                continue
            if count_check(row) is True:
                continue
            remove, keep = get_index(row, smatrix.columns.values)
            compress.append((remove, keep))
            break
        if len(remove) == 0:
            break

        remove_index, remove_factor = remove[0]
        smatrix.loc[:, remove_index] /= remove_factor

        for column_index, factor in keep:
            smatrix.loc[:, column_index] /= factor
            smatrix.loc[:, column_index] += smatrix.loc[:, remove_index]

        smatrix.drop(remove_index, axis=1, inplace=True)
        remove_zero_rows(smatrix, metabolites)
        inner_counter += 1
    return compress


def cut_reactions(compressions, reversibilities, reactions):
    remove_entry = []
    for remove, keep in compressions:
        index = remove[0][0]
        remove_entry.append(index)
        remove_factor = remove[0][1]
        rm_rea_index = reactions[index]
        rea_names, factors = [reactions[names[0]] for names in keep], [factor[1] for factor in keep]
        result, new_names = log_merge_many(rm_rea_index, rea_names, remove_factor, factors)

        if result is False:
            if len(rea_names) == 1:
                reactions[index], reactions[keep[0][0]] = reactions[keep[0][0]], reactions[index]
                log_merge_many(rea_names[0], [rm_rea_index], remove_factor, factors, force=True)
            else:
                log_merge_many(rm_rea_index, rea_names, remove_factor, factors, force=True)

        if len(new_names) > 0:
            for i in range(0, len(keep)):
                index, factor = keep[i]
                reactions[index] = new_names[i]

    for i in reversed(sorted(remove_entry)):
        del reversibilities[i]
        del reactions[i]
    return reversibilities, reactions


def write_o2m_info(core_name, compressions, rea_pre_merge, rea_post_merge, outer_counter):
    info_file_name = core_name + ".info"
    file = open(info_file_name, "a")
    file.write("one2many_" + str(outer_counter) + "\n")
    file.write("merged " + str(rea_pre_merge) + ":" + str(rea_post_merge) + " reactions\n")

    for remove, keep in compressions:
        for rea_index, factor in remove:
            file.write("remove R" + str(rea_index) + ":" + str(factor) + " ")
        for rea_index, factor in keep:
            file.write("keep R" + str(rea_index) + ":" + str(factor) + " ")
        file.write("\n")
    file.write("end\n")
    file.close()


def run(smatrix, reactions, reversibilities, metabolites, core_name, outer_counter):
    log_module()
    smatrix = convert_matrix2df(smatrix)
    rea_pre_merge = len(smatrix.columns.values)
    compressions = merge_compress(smatrix, reversibilities, metabolites)
    rea_post_merge = len(smatrix.columns.values)
    reversibilities, reactions = cut_reactions(compressions, reversibilities, reactions)
    write_o2m_info(core_name, compressions, rea_pre_merge, rea_post_merge, outer_counter)
    smatrix = convert_df2matrix(smatrix)

    return smatrix, reactions, reversibilities, metabolites
