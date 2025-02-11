import os

def get_absolute_path(file_name):
    # Get the absolute path of the file
    abs_path = os.path.abspath(file_name)
    return abs_path

# Example usage
file_name = "firebaseAuth.json"  # or use input() to get it from user
absolute_path = get_absolute_path(file_name)
print(f"The absolute path is: {absolute_path}")