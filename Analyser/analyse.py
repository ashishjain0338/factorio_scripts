import os
import time
import simplejson as json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
INPUT_FOLDER_PATH = r"C:\Users\DELL\AppData\Roaming\Factorio\saves"

def createJsonFile(folder_path):
    fileStore = []
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print("Folder does not exist.")
    else:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                # Get the file's creation time
                creation_time = os.path.getctime(file_path)
                # Convert it to readable format
                # readable_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(creation_time))
                readable_time = time.strftime('%Y-%m-%d', time.localtime(creation_time))
                print(f"File: {filename} | Created: {readable_time}")
                fileStore.append({
                    "filename": filename,
                    "time": readable_time
                })
        data = {"data": fileStore}

        with open("data.json", "w") as fp:
            json.dump(data, fp, indent = 4)

def createFrequencyMap(fileStore):
    freq = {}
    for files in fileStore:
        timeKey = files['time']
        freq[timeKey] = freq.get(timeKey, 0) + 1
    print(freq)
    return freq

def preprocessFreqencyMap(data):
    # Fill missing dates
    start_date = datetime.strptime("2025-02-20", "%Y-%m-%d")
    end_date = datetime.strptime("2025-04-05", "%Y-%m-%d")
    date_range = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d")
                for i in range((end_date - start_date).days + 1)]

    filled_data = [data.get(date, 0) for date in date_range]
    return (date_range, filled_data)

def plot(x, y):
    # Plotting
    plt.figure(figsize=(14, 6))
    plt.plot(x, y, marker='o', color='skyblue', linestyle='-')
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.title("Daily Counts from 2025-02-20 to 2025-04-05", fontsize=14)
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    print("Hello World")
    # createJsonFile(INPUT_FOLDER_PATH)
    with open("data.json", "r") as fp:
        data = json.load(fp)
    freqMap = createFrequencyMap(data["data"])
    (x, y) = preprocessFreqencyMap(freqMap)
    plot(x, y)
