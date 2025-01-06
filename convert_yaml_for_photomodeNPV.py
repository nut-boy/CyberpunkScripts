import os
import re

female_pose_sets = {
    "altPoses",
    "bluemoonPoses",
    "evelynPoses",
    "hanakoPoses",
    "judyPoses",
    "lizzyPoses",
    "meredithPoses",
    "myersPoses",
    "rogueoldPoses",
    "panamPoses",
    "purpleforcePoses",
    "redmenacePoses",
    "rogueyoungPoses",
    "songbirdPoses"
}

male_pose_sets = {
    "adamPoses",
    "altjohnnyPoses",
    "johnnyPoses",
    "johnnyNPCPoses",
    "goroPoses",
    "jackiePoses",
    "kerryPoses",
    "riverPoses",
    "viktorPoses",
    "kurtPoses",
    "reedPoses",
}

female_poses_yaml_anchor = None
male_poses_yaml_anchor = None

anchor_regex = r"&\w+"
def add_anchor(line, fallback):

    contains_anchor = lambda line: re.search(anchor_regex, line)

    # Check for anchor
    match = contains_anchor(line)
    anchor = match.group() if match else fallback
    if anchor == None:
        anchor = fallback

    lineWithoutAnchor = line.split("&")[0]

    return f"{lineWithoutAnchor.strip()} {anchor}\n", anchor

def update_file_content(lines):
    new_lines = []
    female_poses_yaml_anchor = None
    male_poses_yaml_anchor = None

    for line in lines:
        if "femalePoses:" in line:
            line, female_poses_yaml_anchor = add_anchor(line, "&AddPosesFem")
        elif "malePoses:" in line:
            line, male_poses_yaml_anchor = add_anchor(line, "&AddPosesMasc")

        new_lines.append(line)

    return new_lines, female_poses_yaml_anchor, male_poses_yaml_anchor


def update_yaml_files(directory):

    # Walk through the directory and its subdirectories
    for root, _, files in os.walk(directory):
        for file in files:
            if not file.lower().endswith('.yaml'):
                continue

            file_path = os.path.join(root, file)

            print(f"scanning {file}")
            # Use UTF-8 encoding for reading and writing files
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            new_lines, female_poses_yaml_anchor, male_poses_yaml_anchor = update_file_content(lines)

            new_lines.append("\n")
            new_lines.append("\n")
            wasAdded = False

            if female_poses_yaml_anchor != None and any(female_poses_yaml_anchor in line for line in new_lines):
                for posePack in female_pose_sets:
                    poseString = f"photo_mode.character.{posePack}"
                    if not (any(poseString in line for line in lines)):
                        wasAdded = True
                        new_lines.append(f"{poseString}: {female_poses_yaml_anchor.replace("&", "*")}\n")

            if wasAdded:
                new_lines.append("\n")

            if male_poses_yaml_anchor != None and any(male_poses_yaml_anchor in line for line in new_lines):
                for posePack in male_pose_sets:
                    poseString = f"photo_mode.character.{posePack}"
                    if not (any(poseString in line for line in lines)):
                        new_lines.append(f"{poseString}: {male_poses_yaml_anchor.replace("&", "*")}\n")

            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)


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
