def mergefiles(file_list, output_file):
    out_file = open(output_file, 'w')
    i=0
    for f in file_list:
        in_file = open(f)
        something = in_file.read().splitlines()[0]
        if something:
            i+=int(something)
        else:
            i+=0
        out_file.seek(0)
        with open(output_file,'r+') as file:
            file.truncate(0)

        out_file.write(str(i))
        in_file.close()

    out_file.write('\n# Custom Merger Success #\n')
    out_file.flush()
    out_file.close()
    return True