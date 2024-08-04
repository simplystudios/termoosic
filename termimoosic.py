import os
import requests
import platform
from pyfiglet import Figlet
import time
import inquirer
import re

#  ______                                                                
# /\__  _\                                                  __           
# \/_/\ \/    __   _ __    ___ ___     ___     ___     ____/\_\    ___   
#    \ \ \  /'__`\/\`'__\/' __` __`\  / __`\  / __`\  /',__\/\ \  /'___\ 
#     \ \ \/\  __/\ \ \/ /\ \/\ \/\ \/\ \L\ \/\ \L\ \/\__, `\ \ \/\ \__/ 
#      \ \_\ \____\\ \_\ \ \_\ \_\ \_\ \____/\ \____/\/\____/\ \_\ \____\
#       \/_/\/____/ \/_/  \/_/\/_/\/_/\/___/  \/___/  \/___/  \/_/\/____/ v 1.0

# Made by ansh wadhwa
# open source under gnu 3.0
                                                                       
                                                                       


def homepage():
    f = Figlet(font="larry3d")
    print(f.renderText("Termoosic"))
    print("'THE ONLY TERMINAL MOOSIC PLAYER/DOWNLOADER YOU WILL EVER NEED'\n")

    list = ["Music Download", "Music Player", "Exit"]
    questions = [
        inquirer.List("size", message="Choose A Function", choices=list)
    ]
    answers = inquirer.prompt(questions)
    return answers["size"]

def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    if iteration == total: 
        print()

def sanitize_filename(filename):
    return re.sub(r'[^a-zA-Z0-9_\-\.]', '_', filename)

def downloadmusic():
    print("Type a song name to search or type 'exit' to exit the downloader")
    mn = input("Search A Music To Download : ")
    if len(mn) > 0:
        if mn == "exit":
            print("Exiting the downloader...")
        else:
            url = f"https://pipedapi.kavin.rocks//search?q={mn}&filter=music_songs"
            ln = requests.get(url)
            ln = ln.json()
            print(f"Showing download options for {ln['items'][0]['title']}")
            title = ln['items'][0]['title']
            sanitized_title = sanitize_filename(title)
            filename = f"{sanitized_title}.weba"
            vid = ln["items"][0]["url"]
            vidurl = vid.replace("/watch?v=", "")
            url2 = f"https://pipedapi.kavin.rocks/streams/{vidurl}"
            ln2 = requests.get(url2)
            ln2 = ln2.json()

            streams = ln2["audioStreams"]
            url_mapping = {}
            choices = []
            for item in streams:
                display_text = f"Quality: {item['quality']} Format: {item['format']}"
                choices.append(display_text)
                url_mapping[display_text] = item["url"]

            questions = [
                inquirer.List(
                    name="selected_item",
                    message="Select an item:",
                    choices=choices,
                )
            ]
            answers = inquirer.prompt(questions)
            selected_text = answers["selected_item"]
            print(selected_text)
            selected_url = url_mapping[selected_text]
            folder_path = "music"
            os.makedirs(folder_path, exist_ok=True)
            file_path = os.path.join(folder_path, filename)
            print("The File is Downloading Please Wait...")
            response = requests.get(selected_url, stream=True)
            total_length = int(response.headers.get("content-length"))
            chunk_size = 1024
            num_chunks = total_length // chunk_size

            with open(file_path, "wb") as f:
                for i, chunk in enumerate(response.iter_content(chunk_size=chunk_size)):
                    if chunk:
                        f.write(chunk)
                        printProgressBar(
                            i + 1, num_chunks, prefix="Progress:", suffix="Complete", length=50
                        )
                # Ensure the progress bar completes
                printProgressBar(num_chunks, num_chunks, prefix="Progress:", suffix="Complete", length=50)

            print(f"File Downloaded at {file_path}")
            list = ["Play", "OpenFilePath"]
            questions = [
                inquirer.List(
                    "ops",
                    message="Choose A Function",
                    choices=list,
                ),
            ]

            answers = inquirer.prompt(questions)
            print(answers)
            if answers["ops"] == "OpenFilePath":
                if platform.system() == "Windows":
                    os.startfile(folder_path)
                    print(f"Playing {filename}")
                elif platform.system() == "Darwin":  # macOS
                    os.system(f"open {folder_path}")
                else:  # Linux
                    os.system(f"xdg-open {folder_path}")

            if answers["ops"] == "Play":
                if platform.system() == "Windows":
                    os.startfile(file_path)
                    playing = True
                elif platform.system() == "Darwin":  # macOS
                    os.system(f"open {file_path}")
                    playing = True
                else:  # Linux
                    os.system(f"xdg-open {file_path}")
                    playing = True
    else:
        print("Please type a song name...")
        time.sleep(1)
        downloadmusic()

def musicplayer():
    print("\n")
    folder_path = "music"
    playing = False

    # Ensure the folder exists
    if not os.path.exists(folder_path):
        print(f"Please download songs to '{folder_path}' folder where the termimoosic.py is located for the music player to work properly")
        return

    # List all files in the folder
    files = [
        f
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]

    if not files:
        print(f"No files found in the folder '{folder_path}'.")
        return

    # Create a selection menu for the files
    questions = [
        inquirer.List(
            "file",
            message="Select a file to play:",
            choices=files,
        ),
    ]
    answers = inquirer.prompt(questions)
    selected_file = answers["file"]
    file_path = os.path.join(folder_path, selected_file)
    if platform.system() == "Windows":
        os.startfile(file_path)
    elif platform.system() == "Darwin":  # macOS
        os.system(f"open {file_path}")
        playing = True
    else:  # Linux
        os.system(f"xdg-open {file_path}")
        playing = True

def main():
    while True:
        print("| LOADING - TERMOOSIC |")
        time.sleep(2)
        choice = homepage()
        if choice == "Music Download":
            downloadmusic()
        elif choice == "Music Player":
            musicplayer()
        elif choice == "Exit":
            break

if __name__ == "__main__":
    main()
