import os, time
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


from data.main import main as main_data

def main():
    print("MAIN")
    data = main_data()
    

if __name__ == "__main__":
    main()