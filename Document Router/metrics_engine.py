import os
import csv

category_stats = { 
    "Intellectual Property": {"file_count": 0, "total_characters": 0},
    "Service Complaint": {"file_count": 0, "total_characters": 0},
    "TECH": {"file_count": 0, "total_characters": 0}
}

if __name__ == "__main__":

    folders = os.listdir("storage")

    for folder in folders: 

        if folder.startswith('.'):
            continue

        if folder not in category_stats:
            continue

        print("folder name", folder)

        directory = f"storage/{folder}"

        files = os.listdir(directory)

        for file_name in files:
            
            if file_name.startswith('.'): 
                continue

            file_path = os.path.join(directory, file_name)

            with open(file_path, 'r') as f:
                
                summary_string = f.read()

                char_count = len(summary_string)

                category_stats[folder]["file_count"] += 1
                category_stats[folder]["total_characters"] += char_count

    with open("report.csv", "w", newline="") as csvfile:

        writer = csv.writer(csvfile)

        writer.writerow(["Category", "Total Files", "Average Summary Length"])

        for storage_key in category_stats.keys():

            info_dictionary = category_stats[storage_key]

            file_count = info_dictionary["file_count"]

            char_length = info_dictionary["total_characters"]

            avg_summary_length = char_length / file_count

            writer.writerow([storage_key, file_count, avg_summary_length])


