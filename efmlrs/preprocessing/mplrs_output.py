from efmlrs.util.data import *


def remove_reversible(smatrix, reversibilities):
    reconfigured_smatrix = []

    for line in smatrix:
        vtmp = []
        for i in range(0, len(line)):
            if reversibilities[i] == 1:
                vtmp.append(line[i])
                vtmp.append(-line[i])
            else:
                vtmp.append(line[i])
        reconfigured_smatrix.append(vtmp)
    return reconfigured_smatrix


def write_header(file, name):
    file.write("* " + name + "\n")
    file.write("H-representation" + "\n")


def write_smatrix(file, smatrix):
    d = len(smatrix[0])
    s = len(smatrix)
    m = s + d

    file.write("linearity " + str(s))
    for i in range(1, s + 1):
        file.write(" " + str(i))
    file.write("\n")
    file.write("begin" + "\n")
    file.write(str(m) + " " + str((d + 1)) + " rational \n")

    for line in smatrix:
        file.write(format(0) + " ")
        for val in line:
            file.write(format(val) + " ")
        file.write("\n")

    for i in range(0, d):
        file.write(format(0) + " ")
        for j in range(0, d):
            if i == j:
                file.write(format(1) + " ")
            else:
                file.write(format(0) + " ")
        file.write("\n")
    file.write("end" + "\n")


def write_lrs(name, reconf_smatrix):
    name += ".ine"
    mplrs_file = open(name, "w")
    write_header(mplrs_file, name)
    write_smatrix(mplrs_file, reconf_smatrix)
    mplrs_file.close()


def run(core_name):
    smatrix = read_sfile(core_name + "_cmp")
    reversibilities = read_rvfile(core_name + "_cmp")

    if len(smatrix) == 0:
        print("*** SMATRIX EMPTY! ***")
        print("*** NO INE FILE CREATED! ***")
        return
    reconfigured_smatrix = remove_reversible(smatrix, reversibilities)
    write_lrs(core_name, reconfigured_smatrix)
