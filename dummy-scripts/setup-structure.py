import os

# Define folder structure
folders = [
    "src",
    "src/nodes",
    "src/tools",
    "src/llms",
    "src/graphs",
    "src/states",
    "src/ui",
    "src/api",
    "src/config",
    "src/tracing"
]

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    init_path = os.path.join(folder, "__init__.py")
    with open(init_path, "w") as f:
        f.write("# Init for " + folder.split("/")[-1])

# Root-level files (optional)
with open("main.py", "w") as f:
    f.write("# Entry point for MedhaAI\n")

with open(".env", "w") as f:
    f.write("OPENAI_API_KEY=\nLANGCHAIN_API_KEY=\nLANGCHAIN_TRACING_V2=true\n")

with open("README.md", "w") as f:
    f.write("# MedhaAI\nIntelligent Agent for SVNIT CS Department.\n")

print("Folder structure and init files created successfully.")
