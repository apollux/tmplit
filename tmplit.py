import os
import sys
import fileinput
import argparse

from Cheetah.Template import Template
from Cheetah.Template import NotFound

def ensure_dir_exists(path):
    d = os.path.dirname(path)
    if not os.path.exists(d):
        os.makedirs(d)

def parse_placeholder_values(placeholder_list=None, placeholder_file=None):
    if placeholder_file != None and os.path.isfile(placeholder_file):
        for line in fileinput.input(placeholder_file):
            placeholder_list.append(line)

    placeholder_values = dict()
    if placeholder_list != None:
        for placeholder in placeholder_list:
            if placeholder.find('=') != -1:
                key_value = placeholder.split('=', 1)
                placeholder_values[key_value[0].strip()] = key_value[1].strip()

    return placeholder_values

parser = argparse.ArgumentParser(description="tmplit")
parser.add_argument('--template-dir', action='store', dest='template_dir',
                    required=True)
parser.add_argument('--output-dir', action='store', dest='output_dir',
                    required=True)
parser.add_argument('--placeholder-file', action='store',
                    dest='placeholder_file')
parser.add_argument('--placeholders', '-p', action='store',
                    dest='placeholders', nargs='+', help="Provide a space"
                    " separated list of <placeholder>=<value> pairs.")

arguments = parser.parse_args()
template_dir = arguments.template_dir
output_dir = arguments.output_dir

placeholders = parse_placeholder_values(arguments.placeholders,
                                        arguments.placeholder_file)

for root, sub_folders, files in os.walk(template_dir):
    for template_file in files:
        path_to_template = os.path.join(root, template_file)
        with open(path_to_template, 'r') as template:
            t = Template(file=template, searchList=placeholders)
            print 'Processing: {}'.format(path_to_template)
            try:
                filled = str(t)
            except NotFound as e:
                print "Error while parsing: {}, {}".format(path_to_template, e)
                sys.exit(1)
        output_path = os.path.join(output_dir, os.path.relpath(path_to_template,
                                                               template_dir))
        ensure_dir_exists(output_path)
        with open(output_path, 'w+') as output:
            output.write(filled)
