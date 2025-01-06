import os

# Function to process the .xl files
def process_xl_files(directory):
    entities = {
        "base\\characters\\entities\\player\\photo_mode\\player_wa_photomode.ent": "photomode_wa.ent",
        "base\\characters\\entities\\player\\photo_mode\\player_ma_photomode.ent": "photomode_ma.ent",
        "base\\characters\\entities\\photomode_replacer\\photomode_npc_man_big.ent": "photomode_mb.ent",
        "base\\characters\\entities\\player\\photo_mode\\adam_smasher\\adam_smasher.ent": "photomode_mm.ent",
        "base\\quest\\minor_quests\\mq000\\characters\\nibbles.ent": "photomode_cat.ent"
    }

    for filename in os.listdir(directory):
        if not filename.endswith(".xl"):
            continue

        file_path = os.path.join(directory, filename)
        with open(file_path, "r") as file:
            lines = file.readlines()

        if not (lambda line: any(old_entity in lines for old_entity in entities.keys())):
            print(f"Nothing to update: {filename}")
            continue

        new_lines = []
        skip_line = False
        for line in lines:
            if "ep1" in line:
                skip_line = True
                continue
            if skip_line:
                skip_line = False
                continue
            if ".ent" in line:
                for old_entity, new_entity in entities.items():
                    line = line.replace(old_entity, new_entity)
            new_lines.append(line)

        with open(file_path, "w") as file:
            file.writelines(new_lines)

        print(f"Processed file: {filename}")

# Main function to handle processing
def main():
    directory = input("Enter the path to your Cyberpunk mod directory: ").strip()
    if not os.path.isdir(directory):
        print("Invalid directory. Please try again.")
        return

    process_xl_files(directory)

if __name__ == "__main__":
    main()
