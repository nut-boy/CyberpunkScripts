import os
import re

female_pose_sets = {
    "photo_mode.character.altPoses",
    "photo_mode.character.bluemoonPoses",
    "photo_mode.character.evelynPoses",
    "photo_mode.character.hanakoPoses",
    "photo_mode.character.judyPoses",
    "photo_mode.character.lizzyPoses",
    "photo_mode.character.meredithPoses",
    "photo_mode.character.myersPoses",
    "photo_mode.character.rogueoldPoses",
    "photo_mode.character.panamPoses",
    "photo_mode.character.purpleforcePoses",
    "photo_mode.character.redmenacePoses",
    "photo_mode.character.rogueyoungPoses",
    "photo_mode.character.songbirdPoses"
}

male_pose_sets = {
    "photo_mode.character.adamPoses",
    "photo_mode.character.altjohnnyPoses",
    "photo_mode.character.johnnyPoses",
    "photo_mode.character.johnnyNPCPoses",
    "photo_mode.character.goroPoses",
    "photo_mode.character.jackiePoses",
    "photo_mode.character.kerryPoses",
    "photo_mode.character.riverPoses",
    "photo_mode.character.viktorPoses",
    "photo_mode.character.kurtPoses",
    "photo_mode.character.reedPoses",
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


            lines_with_pose_pack_assignments = [a for a in new_lines if any(posepack in a for posepack in male_pose_sets) or any(posepack in a for posepack in female_pose_sets)]

            # remove any lines that contain a pose pack
            new_lines = [a for a in new_lines if a not in lines_with_pose_pack_assignments]

            if (len(new_lines) > 1 and new_lines[-2] != "\n"):
                new_lines.append("\n")
            if (len(new_lines) > 1 and new_lines[-2] != "\n"):
                new_lines.append("\n")

            if female_poses_yaml_anchor != None and any(female_poses_yaml_anchor in line for line in new_lines):
                anchor = female_poses_yaml_anchor.replace("&", "*")
                for poseString in female_pose_sets:
                    if (any(f"{poseString}: ${anchor}" in line for line in lines)):
                        continue
                    new_lines.append(f"{poseString}: {anchor}\n")

            if (len(new_lines) > 0 and new_lines[-1] != "\n"):
                new_lines.append("\n")

            if male_poses_yaml_anchor != None and any(male_poses_yaml_anchor in line for line in new_lines):
                anchor = male_poses_yaml_anchor.replace("&", "*")
                for poseString in male_pose_sets:
                    if (any(f"{poseString}: ${anchor}" in line for line in lines)):
                        continue
                    new_lines.append(f"{poseString}: {anchor}\n")

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
