import os
import yaml

def update_yaml_files(directory):
    # Additional lines for female and male poses
    additional_female_lines = """

    
photo_mode.character.altPoses: *AddPosesFem
photo_mode.character.bluemoonPoses: *AddPosesFem
photo_mode.character.evelynPoses: *AddPosesFem
photo_mode.character.hanakoPoses: *AddPosesFem
photo_mode.character.judyPoses: *AddPosesFem
photo_mode.character.lizzyPoses: *AddPosesFem
photo_mode.character.meredithPoses: *AddPosesFem
photo_mode.character.myersPoses: *AddPosesFem
photo_mode.character.rogueoldPoses: *AddPosesFem
photo_mode.character.panamPoses: *AddPosesFem
photo_mode.character.purpleforcePoses: *AddPosesFem
photo_mode.character.redmenacePoses: *AddPosesFem
photo_mode.character.rogueyoungPoses: *AddPosesFem
photo_mode.character.songbirdPoses: *AddPosesFem
"""
    additional_male_lines = """
    

photo_mode.character.adamPoses: *AddPosesMasc
photo_mode.character.altjohnnyPoses: *AddPosesMasc
photo_mode.character.johnnyPoses: *AddPosesMasc
photo_mode.character.goroPoses: *AddPosesMasc
photo_mode.character.jackiePoses: *AddPosesMasc
photo_mode.character.kerryPoses: *AddPosesMasc
photo_mode.character.riverPoses: *AddPosesMasc
photo_mode.character.viktorPoses: *AddPosesMasc
photo_mode.character.kurtPoses: *AddPosesMasc
photo_mode.character.reedPoses: *AddPosesMasc
"""

    # Walk through the directory and its subdirectories
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.yaml'):
                file_path = os.path.join(root, file)

                # Use UTF-8 encoding for reading and writing files
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                modified = False
                contains_female = False
                contains_male = False
                new_lines = []
                for line in lines:
                    if "photo_mode.character.femalePoses:" in line:
                        contains_female = True
                        if "&AddPosesFem" not in line:
                            line = line.strip() + " &AddPosesFem\n"
                            modified = True
                        new_lines.append(line)
                    elif "photo_mode.character.malePoses:" in line:
                        contains_male = True
                        if "&AddPosesMasc" not in line:
                            line = line.strip() + " &AddPosesMasc\n"
                            modified = True
                        new_lines.append(line)
                    else:
                        new_lines.append(line)

                # Add additional lines if modified
                if modified:
                    if contains_female:
                        new_lines.append(additional_female_lines)
                    if contains_male:
                        new_lines.append(additional_male_lines)

                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)

if __name__ == "__main__":
    folder_path = input("Enter the folder path containing the .yaml files: ")
    if not folder_path.strip():
        print("Error: Folder path cannot be empty. Please provide a valid path.")
    elif os.path.isdir(folder_path):
        try:
            update_yaml_files(folder_path)
            print("YAML files updated successfully.")
        except Exception as e:
            print(f"An error occurred while updating YAML files: {e}")
    else:
        print("Invalid folder path. Please ensure the path exists and is a directory.")
