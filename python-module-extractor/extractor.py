import ast
import sys

modules = set()

# Get all imports with simple import statement
def visit_Import(node):
    for name in node.names:
        modules.add(name.name.split(".")[0])

# Get all imports at the top level from 'complex' import statement
def visit_ImportFrom(node):
    if node.module is not None and node.level == 0:
        modules.add(node.module.split(".")[0])

node_iter = ast.NodeVisitor()
node_iter.visit_Import = visit_Import
node_iter.visit_ImportFrom = visit_ImportFrom

# Read in file from Command line
with open(sys.argv[1],'r') as f:
    node_iter.visit(ast.parse(f.read()))

module_list = list(modules)
module_list.sort()

if(len(module_list)):
    ### Create Import File ###
    import_header = ('-----------------------\nImports for ' +sys.argv[1]+ '\n----------------------- \n')
    imports = "\n".join(module_list)

    found_imports = open("found-imports.txt","a")
    found_imports.write(imports+"\n")
    found_imports.close()