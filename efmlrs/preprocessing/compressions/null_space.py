from efmlrs.util.data import *
from efmlrs.util.log import *


def enumerate_rows(kernel):
    l = len(kernel[0])
    rows = []
    rows_index = []
    tuples = []
    for j in range(0, l):
        row = [item[j] for item in kernel]
        rows.append(row)
        rows_index.append(j)
        tuples.append(row)
    return list(zip(tuples, rows_index))


def check_multiplier(row1, row2):
    factor = 0
    for i, j in zip(row1, row2):
        if i == 0 and j == 0:
            continue
        if i == 0 or j == 0:
            return False
        if factor == 0:
            factor = i / j
        else:
            if i / j != factor:
                return False
    return factor


def search_multiples(kernel):
    K = enumerate_rows(kernel)
    results = []
    i = 0
    for row1, index1 in K:
        j = 0
        for row2, index2 in K:
            if j <= i:
                j += 1
                continue
            factor = check_multiplier(row1, row2)
            if factor != False:
                results.append((index1, index2, factor))
            j += 1
        i += 1
    return results


def test_results(column_index, index_multiples, smatrix, reversibilities):
    for index1, index2, factor in index_multiples:
        if index1 == column_index:
            rea1 = smatrix.col(index1)
            rea2 = smatrix.col(index2)
            tmp = rea2 / factor
            merged_rea = rea1 + tmp
            if reversibilities[index1] and reversibilities[index2]:
                new_rev_info = True
            else:
                new_rev_info = False
            return False, merged_rea, new_rev_info, index2, factor, reversibilities[index1] or reversibilities[index2]

        if index2 == column_index:
            return False, Matrix(), -1, -1, factor, reversibilities[index1] or reversibilities[index2]

    return True, Matrix(), reversibilities[column_index], -1, -1, reversibilities[column_index]


def merge_multiples(smatrix, reversibilities, reactions, index_multiples):
    smatrix_reduced = Matrix()
    reversibilities_reduced = []
    reactions_reduced = []
    merge_info = []
    j = 0

    for column_index in range(0, smatrix.shape[1]):
        use_ori, merged_rea, new_rev_info, dropped_rea, factor, reversibility_flag = test_results(column_index, index_multiples, smatrix, reversibilities)

        if use_ori is True:
            smatrix_reduced = smatrix_reduced.col_insert(j, smatrix.col(column_index))

            reversibilities_reduced.append(new_rev_info)
            reactions_reduced.append(reactions[column_index])
            merge_info.append("R" + str(column_index))
            j += 1
        else:
            if reversibility_flag is False and factor < 0:
                log_delete(reactions[column_index], reactions[dropped_rea])
            else:
                if len(merged_rea):
                    smatrix_reduced = smatrix_reduced.col_insert(j, merged_rea)
                    reversibilities_reduced.append(new_rev_info)
                    result, newnames = log_merge(reactions[dropped_rea], reactions[column_index], factor)
                    if result is False:
                        if log_merge(reactions[column_index], reactions[dropped_rea], factor) is False:
                            log_merge(reactions[dropped_rea], reactions[column_index], factor, True)
                        else:
                            reactions[dropped_rea], reactions[column_index] = reactions[column_index], reactions[
                                dropped_rea]
                    if len(newnames) > 0:
                        reactions[column_index] = newnames[0]

                    reactions_reduced.append(reactions[column_index])
                    merge_info.append("R" + str(column_index) + "," + str() + str(dropped_rea) + ":" + str(factor))
                    j += 1

            for index in reversed(range(0, len(index_multiples))):
                i1, i2, f = index_multiples[index]
                if i1 == column_index and i2 == dropped_rea:
                    continue
                if i1 == column_index or i2 == column_index or i1 == dropped_rea or i2 == dropped_rea:
                    del index_multiples[index]

    return smatrix_reduced, reversibilities_reduced, reactions_reduced, merge_info


def get_index_zero_rows(smatrix):
    index_zero_rows = []
    for index in range(0, smatrix.shape[0]):
        row = [metabolite for metabolite in smatrix.row(index) if metabolite != 0]
        if bool(row) is False:
            index_zero_rows.append(index)
    return index_zero_rows


def iterate(smatrix, metabolites, reactions, reversibilities, nullspace_infos,inner_counter):
    print("Start null space calculations round",str(inner_counter),".This may take a while")
    K = smatrix.nullspace()
    print("Done null space calculations.")
    if len(K) == 0:
        print("KERNELMATRIX is EMPTY")
        return smatrix, metabolites, reactions, reversibilities, nullspace_infos, True

    index_multiples = search_multiples(K)
    if len(index_multiples) == 0:
        return smatrix, metabolites, reactions, reversibilities, nullspace_infos, True

    new_smatrix, new_reversibilities, new_reactions, merge_info = merge_multiples(smatrix, reversibilities, reactions,
                                                                                  index_multiples)
    index_zero_rows = get_index_zero_rows(new_smatrix)

    for i in reversed(index_zero_rows):
        log_delete_meta(metabolites[i])
        del (metabolites[i])
        new_smatrix.row_del(i)

    nullspace_infos.append(merge_info)
    return new_smatrix, metabolites, new_reactions, new_reversibilities, nullspace_infos, False


def write_info(core_name, nullspace_infos, outer_counter):
    info_file_name = core_name + ".info"
    file = open(info_file_name, "a")
    file.write("nullspace_" + str(outer_counter) + "\n")
    reversed_info = nullspace_infos[::-1]

    for info in reversed_info:
        d = len(info)
        for i in range(0, d):
            file.write(str(info[i]) + " ")
        file.write("\n")
    file.write("end\n")
    file.close()


def run(smatrix, reactions, reversibilities, metabolites, core_name, outer_counter):
    log_module()
    nullspace_infos = []
    inner_counter = 1

    while 1:
        smatrix, metabolites, reactions, reversibilities, infos, last = iterate(smatrix, metabolites, reactions, reversibilities, nullspace_infos, inner_counter)
        if last is False:
            inner_counter += 1
        else:
            break

    write_info(core_name, nullspace_infos, outer_counter)
    return smatrix, reactions, reversibilities, metabolites
