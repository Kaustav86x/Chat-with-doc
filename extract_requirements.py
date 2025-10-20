import os
import re

project_dir = "."  # or specify your project path
imports = set()

# Regular expression to capture import statements
pattern = re.compile(r'^\s*(?:from|import)\s+([a-zA-Z0-9_\.]+)')

for root, _, files in os.walk(project_dir):
    for file in files:
        if file.endswith(".py"):
            with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                for line in f:
                    match = pattern.match(line)
                    if match:
                        module = match.group(1).split('.')[0]
                        if module not in ("__future__",):  # skip built-ins
                            imports.add(module)

# Common built-in modules to exclude
builtin_modules = {
    "os", "sys", "re", "json", "math", "datetime", "time", "typing", "pathlib",
    "logging", "subprocess", "itertools", "functools", "shutil", "random",
    "argparse", "http", "urllib", "traceback", "collections", "dataclasses"
}

# Filter out standard libs
third_party = sorted([pkg for pkg in imports if pkg not in builtin_modules])

# Write to requirements.txt
with open("requirements_auto.txt", "w", encoding="utf-8") as f:
    for pkg in third_party:
        f.write(pkg + "\n")

print("✅ requirements_auto.txt created successfully!")
print("Detected packages:", third_party)