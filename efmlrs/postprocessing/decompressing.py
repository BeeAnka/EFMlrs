import efmlrs.postprocessing.decompressions.one2many as one2many
import efmlrs.postprocessing.decompressions.null_space as nullspace
import efmlrs.postprocessing.decompressions.deadend as deadend


def find_counter(file):
    round_counter = 0
    bounds = 0
    file = open(file, "r")
    for line in file:
        if line.startswith("bounds"):
            bounds = line[7]
        if line.startswith("counter"):
            round_counter = line[8]
    file.close()
    return int(round_counter), int(bounds)


def build_reverse_mapping(info, counter):
    mappings = []
    for i in reversed(range(1, counter + 1)):
        file = open(info, "r")
        tmp = []
        DE = False
        O2M = False
        NS = False

        for line in file:
            if DE is True and O2M is True and NS is True:
                break
            if line.startswith("deadend_" + str(i)):
                DE = True
                deadend_cmps = deadend.parse_info(file)
                if len(deadend_cmps) != 0:
                    for reactions in deadend_cmps:
                        tmp.append(("deadend", reactions))

            if line.startswith("one2many_" + str(i)):
                O2M = True
                iterations, post, pre = one2many.parse_info(file)
                if post != pre:
                    rea_mapping = one2many.build_merge_mapping(iterations, post)
                    tmp.append(("o2many", (rea_mapping, iterations, post)))

            if line.startswith("nullspace_" + str(i)):
                NS = True
                null_cmps = nullspace.parse_info(file)
                if len(null_cmps) != 0:
                    for infos, rea_comp, rea_uncomp in reversed(null_cmps):
                        rea_mapping = nullspace.build_mapping(infos, rea_uncomp)
                        tmp.append(("nullspace", rea_mapping))

        for element in reversed(tmp):
            mappings.append(element)

        file.close()
    return mappings


def normalize_efms(decompressed, bound_info):
    lambda_val = decompressed[-1]
    del decompressed[-(bound_info + 1):]
    if lambda_val > 1:
        new_compressed = [val / lambda_val for val in decompressed]
        return new_compressed
    else:
        return decompressed


def write_decompressed_efms(decompressed, outputfile):
    for val in decompressed:
        val = float(val)
        outputfile.write(str(val) + " ")
    outputfile.write("\n")


def decompressing(compressed_efms, outputfile, mappings, bound_info):
    ofile = open(outputfile, "w")
    count = 0

    for cmp_efm in compressed_efms:
        decompressed = cmp_efm
        for infotype, mappinginfo in mappings:
            if infotype == "nullspace":
                decompressed = nullspace.decompressions(decompressed, mappinginfo)

            elif infotype == "o2many":
                mapping, iterations, post = mappinginfo
                decompressed = one2many.decompressions(decompressed, mapping, iterations, post)

            elif infotype == "deadend":
                decompressed = deadend.decompressions(decompressed, mappinginfo)
                continue

        if bound_info != 0:
            normalized_efms = normalize_efms(decompressed, bound_info)
            write_decompressed_efms(normalized_efms, ofile)
        else:
            write_decompressed_efms(decompressed, ofile)

        count += 1
        if count % 1000 == 0:
            print("EFMs decompressed:", count)
    ofile.close()
    print("Decompressed EFMs:", count)


def run(compressed_efms, compression_infos, outputfile):
    counter, bounds = find_counter(compression_infos)
    mappings = build_reverse_mapping(compression_infos, counter)
    print("Start decompressions")
    decompressing(compressed_efms, outputfile, mappings, bounds)
