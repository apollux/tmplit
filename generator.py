import os
import sys

from Cheetah.Template import Template

def ensure_dir_exists(path):
	d = os.path.dirname(path)
	if not os.path.exists(d):
		os.makedirs(d)

template_dir = sys.argv[1]
output_dir = sys.argv[2]

for root, sub_folders, files in os.walk(template_dir):
	for template_file in files:
		path_to_template = os.path.join(root, template_file)
		with open(path_to_template, 'r') as template:
			t = Template(file = template, searchList = [{'name':'andre'}])
			filled = str(t)

		output_path = os.path.join(output_dir, os.path.relpath(path_to_template, template_dir))
		ensure_dir_exists(output_path)
		with open(output_path, 'w+') as output:
			output.write(filled)

