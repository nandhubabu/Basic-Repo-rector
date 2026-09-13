import ast
import os
from dotenv import load_dotenv
import google.generativeai as genai
import re

load_dotenv()

# --- CONFIGURATION ---
# ⚠️ SAFETY: Replace with your actual key, but do not share this file publicly!
# You can also use os.getenv("GOOGLE_API_KEY") if you set it in your environment.
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- 1. The Tool (The Visitor Class) ---
class DependencyFinder(ast.NodeVisitor):
    """
    Scans a Python Abstract Syntax Tree (AST) to find all imports.
    """
    def __init__(self):
        self.found_imports = []

    def visit_Import(self, node):
        for alias in node.names:
            self.found_imports.append(alias.name)

    def visit_ImportFrom(self, node):
        if node.module:
            self.found_imports.append(node.module)

# --- 2. The Analysis Phase (Mapping the Code) ---
print("🕵️  Starting Analysis Phase...")

queue = ['main.py'] 
visited = set()
project_graph = {} 

while queue:
    current_file = queue.pop(0)
    if current_file in visited:
        continue
    visited.add(current_file)

    try:
        with open(current_file, 'r', encoding='utf-8') as f:
            code_text = f.read()
        tree = ast.parse(code_text)
    except FileNotFoundError:
        print(f"   ⚠️ Could not find file: {current_file}")
        continue
    except SyntaxError:
        print(f"   ❌ Syntax Error in {current_file}")
        continue

    finder = DependencyFinder()
    finder.visit(tree)

    internal_dependencies = []
    for module_name in finder.found_imports:
        candidate_filename = module_name + ".py"
        if os.path.exists(candidate_filename):
            internal_dependencies.append(candidate_filename)
            if candidate_filename not in visited:
                queue.append(candidate_filename)
    
    project_graph[current_file] = internal_dependencies

print("\n✅ Dependency Graph Built:", project_graph)

# --- 3. The Agent Setup ---
system_prompt = """
You are a basic Python code simplifier. Simplify the given Python code to make it very easy to understand and work with.
Use only basic Python features that work in any environment. Avoid complex syntax, advanced libraries, or expert-level code.
Make it simple, clear, and straightforward. Output only the simplified code, no explanations.
"""

model = genai.GenerativeModel(
    model_name="gemini-pro-latest",
    system_instruction=system_prompt
)

def refactor_file(filename):
    print(f"\n🔄 Refactoring: {filename}...")
    
    with open(filename, 'r') as f:
        legacy_code = f.read()
        
    dependency_list = project_graph.get(filename, []) # Safety get
    
    # Initialize the variable to avoid NameError
    context_code = "" 
    
    for dep_file in dependency_list:
        if os.path.exists(dep_file):
            with open(dep_file, 'r') as f:
                context_code += f"\n\n# --- Context from {dep_file} ---\n" + f.read()

    user_message = f"""
    Legacy Code:
    {legacy_code}

    Context:
    {context_code}
    """
    
    # Send to Gemini
    response = model.generate_content(user_message)
    
    # Extract code from the response (assuming it's in a ```python block)
    code_match = re.search(r'```python\s*(.*?)\s*```', response.text, re.DOTALL)
    if code_match:
        generated_code = code_match.group(1)
    else:
        generated_code = response.text  # Fallback if no code block found
    
    return generated_code

# --- 4. The Execution Loop (Dynamic Scheduling) ---
print("\n🚀 Starting Refactoring Process...")

# Keep running until the graph is empty
while project_graph:
    
    # Create a safe snapshot of keys to iterate over
    files_to_check = list(project_graph.keys())
    
    progress_made = False 
    
    for filename in files_to_check:
        dependencies = project_graph[filename]
        
        # Check for Leaf Node (No dependencies left)
        if dependencies == []:
            print(f"   🍃 Leaf node found: {filename}")
            
            # --- ACTION ---
            # 1. Get new code from Gemini
            generated_code = refactor_file(filename)
            
            # 2. Save to Disk (Overwrite the old file)
            with open(filename, 'w') as f:
                f.write(generated_code)
            print(f"   💾 Saved new code to {filename}")
            
            # --- UPDATE GRAPH ---
            print(f"   ✅ Marking {filename} as done.")
            del project_graph[filename]
            
            # Remove this file from everyone else's dependency list
            for other_file, other_deps in project_graph.items():
                if filename in other_deps:
                    other_deps.remove(filename)
            
            progress_made = True
    
    if not progress_made:
        print("⚠️ Cycle detected or stuck! Breaking loop.")
        break

print("\n🎉 Refactoring Complete!")