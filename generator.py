import os
import sys
import fileinput

from Cheetah.Template import Template

def ensure_dir_exists(path):
	d = os.path.dirname(path)
	if not os.path.exists(d):
		os.makedirs(d)

def parse_placeholder_values():
	args_placeholder_values = dict()
	for arg in sys.argv:
		if arg.find('=') != -1:
			key_value = arg.split('=', 1)
			args_placeholder_values[key_value[0].strip()] = key_value[1].strip()

	file_placeholder_values = dict()
	if os.path.isfile(sys.argv[3]):
		for line in fileinput.input(sys.argv[3]):
			key_value = line.split('=', 1)
			file_placeholder_values[key_value[0].strip()]= key_value[1].strip()

	return dict(file_placeholder_values.items() + args_placeholder_values.items())

template_dir = sys.argv[1]
output_dir = sys.argv[2]

for root, sub_folders, files in os.walk(template_dir):
	for template_file in files:
		path_to_template = os.path.join(root, template_file)
		with open(path_to_template, 'r') as template:
			t = Template(file = template, searchList = parse_placeholder_values())
			print 'Processing: {}'.format(path_to_template)
			filled = str(t)
		output_path = os.path.join(output_dir, os.path.relpath(path_to_template, template_dir))
		ensure_dir_exists(output_path)
		with open(output_path, 'w+') as output:
			output.write(filled)

