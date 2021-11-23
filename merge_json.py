from json import dump, load

def merge(file1, file2, new_name):
    with open(file1, 'r') as f:
        j1 = load(f)
    with open(file2, 'r') as f:
        j2 = load(f)

    j = j1 + j2
    with open(new_name, 'w') as f:
        dump(j, f)


merge('raw-oct-12-to-nov-18.json', 'raw-nov-18-to-nov-21.json', 'raw-thru-nov-21.json')
