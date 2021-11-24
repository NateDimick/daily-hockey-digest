"""
TODO: use this file to write unit tests and unit test-like methods to make sure features work without running the whole damn script
maybe use pytest
because I'm used to spock I'll probably comment these tests with spock's given->when->then style
"""
from datetime import date
from jinja2 import Template
from os import remove
from os.path import join, exists
from project_directory import project_directory

def html_rendering_manual_test():
    # given dummy data
    dummy_data = [
        {
            'home_team': 'this is a test',
            'away_team': 'confirmation',
            'datetime': 'tonight',
            'stats': [
                [5, 'watermelons', 3],
                [78, 'fucks left to give', 0]
            ]
        },
        {
            'home_team': 'continue test',
            'away_team': 'roger doger',
            'datetime': 'never',
            'stats': [
                [6, 'sex number', 9],
                [19, 'a pretty shitty year', 75]
            ]
        }
    ]
    # when the template is rendered
    with open(join(project_directory,'template.html'), 'r') as f:
        template = Template(f.read())
    render_result = template.render(data=dummy_data, date=date.today())
    # then observe the result manually
    print(render_result)

from daily_digest import backup_files
def backup_files_test():
    # given a file to back up
    file_name = join(project_directory, 'requirements.txt')
    file_name_backup = file_name + '.backup'
    files = [file_name]
    # when the files are backed up with our method
    backup_files(files)
    # then the backed up file exists
    assert exists(file_name_backup)
    # cleanup delete that file
    remove(file_name_backup)

from daily_digest import do_not_run, do_not_run_file
def do_not_run_test():
    # expect do not run to be false with no changes
    assert not do_not_run()
    # when we create the do not run file
    with open(do_not_run_file, 'w') as f:
        f.write('1')
    # then the result flips
    assert do_not_run()
    # cleanup delete the file
    remove(do_not_run_file)
    # cleanup verification
    assert not exists(do_not_run_file)



if __name__ == '__main__':
    #html_rendering_manual_test()
    backup_files_test()
    do_not_run_test()