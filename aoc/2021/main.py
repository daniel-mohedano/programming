import importlib
import os


if __name__ == '__main__':
    # Get python scripts in current folder
    solutions = sorted([f.replace('.py', '') for f in os.listdir('.') if os.path.isfile(f) and f.startswith('day')], 
                       key=lambda x: int(x.replace('day', '')))
    
    # Import their solutions
    for sol in solutions:
        print("================================================================")
        mod = importlib.import_module(sol)
        mod.main()
    print("================================================================")
