from json import dump, load

def merge(file1, file2, new_name):
    with open(file1, 'r') as f:
        j1 = load(f)
    with open(file2, 'r') as f:
        j2 = load(f)

    j = j1 + j2
    with open(new_name, 'w') as f:
        dump(j, f, indent=4)


merge('2021-processed-results.json', 'backlog.json', '2021-processed-results.json')
merge('2021-raw-requests.json', 'raw.json', '2021-raw-requests.json')
