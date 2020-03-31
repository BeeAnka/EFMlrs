def get_rev_info(infofile):
    file = open(infofile, "r")
    rev_info = []
    for line in file:
        if line.startswith("rv:"):
            rv = line.strip().split(":")[1]
            for val in rv.replace(" ", ""):
                if int(val) == 1:
                    rev_info.append(True)
                else:
                    rev_info.append(False)
    file.close()
    return rev_info


def remove_zeros(row):
    for val in row:
        if val != 0:
            return row
    return None


def parse_lrs(inputfile, reversibilities):
    mplrs_output = open(inputfile, "r")
    uncmp_efms = []
    zero_counter = 0
    found_begin = False

    for line in mplrs_output:
        if line == "":
            continue
        if line.startswith("*"):
            continue
        if line.startswith("begin"):
            found_begin = True
            continue
        if found_begin == False:
            continue
        break

    for line in mplrs_output:
        if line.startswith("end"):
            break
        val = line.split()
        row = []

        j = 0
        i = 1
        while i < len(val):
            if reversibilities[j] == 0:
                row.append(int(val[i]))
            else:
                tmp = int(val[i]) - int(val[i + 1])
                row.append(tmp)
                i += 1
            j += 1
            i += 1

        efms = remove_zeros(row)

        if efms is None:
            zero_counter += 1
        elif efms is not None:
            uncmp_efms.append(efms)
            if len(uncmp_efms) % 10000 == 0:
                print("EFMs extracted:" + str(len(uncmp_efms)))

    mplrs_output.close()
    return uncmp_efms


def get_mplrs_efms(inputfile, infofile):
    reversibilities = get_rev_info(infofile)
    compressed_efms = parse_lrs(inputfile, reversibilities)
    return compressed_efms


def get_efmtool_efms(inputfile):
    ifile = open(inputfile, "r")
    compressed_efms = []
    for line in ifile:
        cmp_efm = [float(val) for val in line.strip().split()]
        compressed_efms.append(cmp_efm)
    return compressed_efms
