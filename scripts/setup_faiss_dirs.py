import os

# Base directory where all FAISS indexes will be stored
BASE_DIR = os.path.join(os.getcwd(), "faiss_indexes")

# Define subfolders for each intent
INDEX_FOLDERS = {
    "academic_query": "academic_index",
    "course_syllabus": "syllabus_index",
    "faculty_details": "faculty_index",
    "lab_info": "labs_index",
    "timetable": "timetable_index",
    "placement_statistics": "placement_index",
    "contact_info": "contact_index"
}

def create_index_folders(base_dir, folders):
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        print(f"📁 Created base directory: {base_dir}")
    else:
        print(f"📁 Base directory already exists: {base_dir}")

    for intent, folder in folders.items():
        path = os.path.join(base_dir, folder)
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"✅ Created folder for '{intent}' at: {path}")
        else:
            print(f"⚠️ Folder for '{intent}' already exists at: {path}")

if __name__ == "__main__":
    create_index_folders(BASE_DIR, INDEX_FOLDERS)
