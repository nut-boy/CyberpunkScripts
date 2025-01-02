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
        if filename.endswith(".xl"):
            file_path = os.path.join(directory, filename)
            with open(file_path, "r") as file:
                lines = file.readlines()

            with open(file_path, "w") as file:
                i = 0
                while i < len(lines):
                    line_written = False
                    for old_entity, new_entity in entities.items():
                        if old_entity in lines[i]:
                            file.write(lines[i])  # Write the original line (entity line)

                            # If the next line is a 'set', write it and add the new entity line
                            if i + 1 < len(lines) and "set" in lines[i + 1]:
                                file.write(lines[i + 1])  # Write the 'set' line
                                file.write(f"  - entity: {new_entity}\n")  # Write the new entity line
                                file.write(lines[i + 1])  # Write the 'set' line again (only once for the new entity)
                                i += 1  # Skip the next line since it's already processed
                                line_written = True
                                break
                    if not line_written:
                        file.write(lines[i])  # Write all other lines unchanged
                    i += 1  # Move to the next line

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
