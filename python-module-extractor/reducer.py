# Get All Found modules
print("Reducing List")
found_modules = []
with open("found-imports.txt",'r') as f:
    found_modules = f.readlines()
f.close()

# Remove duplicate found imports
condensed_list  = []
for found_module in found_modules:
    if found_module not in condensed_list:
        condensed_list.append(found_module)
condensed_list.sort()

# Write New list to file
found_imports = open('found-imports.txt','w') 
new_imports = "".join(condensed_list)
found_imports.write(new_imports)
found_imports.close()