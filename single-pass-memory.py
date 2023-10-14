
collection = ["doc1.txt", "doc2.txt", "doc3.txt", "doc4.txt", "doc5.txt"]

def BSBindexConstrucction():
    n = 0
    while not all_documents_processed():
        n = n+1
        tokenstream = parse_document()
        ouputfile = SPIMI_invert(tokenstream)

        if n == 1:
            merge_output_files = [ouputfile]
        else:
            merge_output_files.append(ouputfile)

    final_index = merge(merge_output_files)

    return final_index

def SPIMI_invert(tokenstream):

    outputfile = tempfile.NamedTemporaryFile()
    dictionary = {}

    for token in tokenstream:
        if token not in dictionary:
            dictionary[token] = [1, [token]]
        else:
            dictionary[token][0] = dictionary[token][0] + 1

    for key in sorted(dictionary.keys()):
        postings_list = dictionary[key]
        postings_list[1].sort()
        postings = ','.join(str(x) for x in postings_list[1])
        outputfile.write(key + ':' + str(postings_list[0]) + ':' + postings + '\n')

    outputfile.seek(0)
    return outputfile

def all_documents_processed():
    if len(collection) == 0:
        return False
    else:
        return True

def merge(files):
    
        outputfile = tempfile.NamedTemporaryFile()
    
        dictionary = {}
        files = [open(file.name, 'r') for file in files]
    
        for file in files:
            line = file.readline()
            if line != '':
                key = line.split(':')[0]
                if key not in dictionary:
                    dictionary[key] = [line]
                else:
                    dictionary[key].append(line)
    
        while len(dictionary) > 0:
            min_key = min(dictionary.keys())
            min_list = dictionary[min_key]
            outputfile.write(min_list.pop(0))
    
            if len(min_list) == 0:
                del dictionary[min_key]
            else:
                dictionary[min_key] = min_list
    
        outputfile.seek(0)
        return outputfile
