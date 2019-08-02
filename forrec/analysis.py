import csv


def analyze_differences(list1, list2):

    list1.sort(key=lambda file: file[2])
    list2.sort(key=lambda file: file[2])

    ok = []
    wr = []
    ex = []
    ms = []

    list_differences = []

    i = x = 0
    while i < len(list1) and x < len(list2):
        if list1[i][2] == list2[x][2]:
            if list1[i][1] == list2[x][1] and list1[i][0] == list2[x][0]:
                list_differences.append(["ok", list1[i], list2[x]])
                ok.append(list1[i][2])
            else:
                list_differences.append(["wr", list1[i], list2[x]])
                wr.append(list1[i][2])
            i += 1
            x += 1
        elif list1[i][2] < list2[x][2]:
            list_differences.append(["ex", list1[i], list1[i]])
            ex.append(list1[i][2])
            i += 1
        else:
            list_differences.append(["ms", list2[x], list2[x]])
            ms.append(list2[x][2])
            x += 1

    while i < len(list1):
        list_differences.append(["ex", list1[i], list1[i]])
        ex.append(list1[i][2])
        i += 1

    while x < len(list2):
        list_differences.append(["ms", list2[x], list2[x]])
        ms.append(list2[x][2])
        x += 1

    return list_differences


def print_differences(differences, verbose):

    ok = wr = ms = ex = 0

    for x in differences:
        if x[0] == "ok":
            ok += 1
            if verbose >= 3:
                print('\033[92m', "[ok] -", x[1][2])
        elif x[0] == "wr":
            wr += 1
            if verbose >= 1:
                print('\033[91m', "[wr] -", x[1][2])
        elif x[0] == "ms":
            ms += 1
            if verbose >= 2:
                print('\033[94m', "[ms] -", x[1][2])
        elif x[0] == "ex":
            ex += 1
            if verbose >= 2:
                print('\033[93m', "[ex] -", x[1][2])

    print('\033[0m', "\n Statistics: ")
    print('\033[0m', "Total", '\033[92m' + "Okay    -", ok)
    print('\033[0m', "Total", '\033[91m' + "Wrong   -", wr)
    print('\033[0m', "Total", '\033[93m' + "Extra   -", ex)
    print('\033[0m', "Total", '\033[94m' + "Missing -", ms)
    print('\033[0m')


def outfile_differences(file, differences):

    writer = csv.writer(file)

    for x in differences:

        output = [x[0]]
        output += x[1]
        output += x[2]

        writer.writerow(output)


