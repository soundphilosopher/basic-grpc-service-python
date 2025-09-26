"""
📚 Generate reference pages for MkDocs.

This script automatically generates documentation pages for all Python modules
in the project, creating a beautiful API reference section.
"""

import mkdocs_gen_files

# Define the modules we want to document
modules = [
    ("server", "Server", "Main gRPC server implementation"),
    ("services.basic_service", "Basic Service", "gRPC service implementation with Hello, Talk, and Background methods"),
    ("utils.eliza", "Eliza Chatbot", "Classic ELIZA therapeutic chatbot implementation"),
    ("utils.some", "Utilities", "Helper functions for CloudEvents and service simulation"),
]

# Generate individual module pages
for module_path, title, description in modules:
    # Create the documentation file path
    doc_path = f"reference/{module_path}.md"

    # Generate the markdown content
    with mkdocs_gen_files.open(doc_path, "w") as f:
        # Add the module header
        f.write(f"# {title}\n\n")
        f.write(f"> {description}\n\n")

        # Add the mkdocstrings directive to auto-generate docs
        f.write(f"::: {module_path}\n")

# Create the API reference overview page
with mkdocs_gen_files.open("reference/index.md", "w") as f:
    f.write("# API Reference\n\n")
    f.write("Welcome to the API documentation! Here you'll find detailed information about all the modules and their functions.\n\n")

    f.write("## 📚 Available Modules\n\n")

    for module_path, title, description in modules:
        f.write(f"### [{title}]({module_path}.md)\n")
        f.write(f"{description}\n\n")

print("📄 Generated API reference pages for MkDocs")
