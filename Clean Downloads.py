import os
import tkinter as tk
import json
from tkinter import ttk

# Setup Vars
config = {
    "resort_folders": 0,
    "make_other_folder": 0,
    "sort_folders": 0,
    "downloads_path": ""
}

try:
    with open("dc-data/config") as config_file:
        config = json.load(config_file)
        print("JSON File Loaded!")
except :
    print("JSON File Not Found, Config Reset.")
print("")

images = [".png", ".apng", ".jpeg", ".jpg", ".jfif", ".pjpeg", ".pjp", ".gif", ".svg", ".webp", ".tiff", ".bmp", ".ico",
          ".icns", ".heic"]
zips = [".zip", ".sitx", ".7z", ".rar", ".gz", ".tar", ".tar.gz"]
videos = [".mp4", ".mov", ".mpg", ".wmv", ".rm"]
apps = [".app", ".pkg", ".dmg", ".exe"]
text_files = [".txt", ".rtf", ".log", ".doc", ".docx", ".pdf", ".json", ".readme", ".pages", ".py", ".jar", ".java"]
audio_types = [".mp3", ".wav", ".aif", ".mid", ".band", ".m4a"]

# Setup Main Tkinter Window
root = tk.Tk()
root.title("Downloads Cleaner")
root.geometry("372x185")
root.geometry("+100+100")
root.resizable(False, False)
root.iconphoto(False, tk.PhotoImage(file="dc-data/icon.png"))

style = ttk.Style()
style.theme_use("aqua")

# Tkinter Functions & Vars
resort_folders = tk.IntVar(value=config["resort_folders"])
make_other_folder = tk.IntVar(value=config["make_other_folder"])
sort_folders = tk.IntVar(value=config["sort_folders"])
path = tk.StringVar(value=config["downloads_path"])

status = tk.StringVar(value="")

def changePrefs():
    config = {
        "resort_folders": resort_folders.get(),
        "make_other_folder": make_other_folder.get(),
        "sort_folders": sort_folders.get(),
        "downloads_path": path.get()
    }
    with open("dc-data/config", "w") as config_file:
        json.dump(config, config_file)
        print("JSON File Updated!")
        print("")

    if not bool(make_other_folder.get()):
        sort_folders_checkbox.config(state="disabled")
    else:
        sort_folders_checkbox.config(state="normal")

    global downloads_contents

def clean():
    changePrefs()
    global status
    status_bar.config(fg="white")
    status.set(value="Cleaning...")
    try:
        print("Clean Cycle Started!")
        print("")
        downloads_contents = os.listdir(path.get())
        if bool(resort_folders.get()):
            for i in downloads_contents:
                type = os.path.splitext(i)[1].casefold()
                if type == "":
                    if i == "Images" or i == "ZIP Files" or i == "Videos" or i == "Apps" or i == "Text Files" or i == "Other" or i == "Audio Files":
                        for d in os.listdir(path.get() + "/" + i):
                            global item_path
                            type = os.path.splitext(d)[1].casefold()
                            if bool(sort_folders.get()) and type == "":
                                os.rename(path.get() + "/" + i + "/" + d, path.get() + "/" + d)
                                print(d + " Was Moved To Your Downloads Folder.")
                                print("")
                            elif not type == "":
                                os.rename(path.get() + "/" + i + "/" + d, path.get() + "/" + d)
                                print(d + " Was Moved To Your Downloads Folder.")
                                print("")
        downloads_contents = os.listdir(path.get())
        for i in downloads_contents:
            folder = None
            type = os.path.splitext(i)[1].casefold()
            if type in images:
                folder = "Images"
            elif type in zips:
                folder = "ZIP Files"
            elif type in videos:
                folder = "Videos"
            elif type in apps:
                folder = "Apps"
            elif type in text_files:
                folder = "Text Files"
            elif type in audio_types:
                folder = "Audio Files"
            elif bool(make_other_folder.get()):
                if bool(sort_folders.get()) and type == "":
                    if not (i == "Images" or i == "ZIP Files" or i == "Videos" or i == "Apps" or i == "Text Files" or i == "Other" or i == "Audio Files"):
                        folder = "Other"
                elif not type == "":
                    folder = "Other"

            if not folder == None:
                try:
                    os.mkdir(path.get() + "/" + folder)
                    print("'" + folder + "' Folder Created.")
                except:
                    print("'" + folder + "' Folder Already Exists.")
                os.rename(path.get() + "/" + i, path.get() + "/" + folder + "/" + i)
                print("'" + i + "' Was Moved To The '" + folder + "' Folder.")
                print("")
        print("Clean Cycle Finished!")
        root.destroy()
    except:
        print("Something went wrong.")
        print("")
        status_bar.config(fg="red")
        status.set(value="Something went wrong.")

# UI Elements
title = tk.Label(root, text="Options:")
title.grid(column=0, row=0, padx=5, pady=5, sticky="w")

resort_folders_checkbox = tk.Checkbutton(root, text="Resort folders created by Downloads Cleaner", command=changePrefs, variable=resort_folders)
resort_folders_checkbox.grid(column=0, row=1, padx=15, pady=2, sticky="w", columnspan=2)

make_other_folder_checkbox = tk.Checkbutton(root, text="Make an 'Other' folder", command=changePrefs, variable=make_other_folder)
make_other_folder_checkbox.grid(column=0, row=2, padx=15, pady=2, sticky="w", columnspan=2)

sort_folders_checkbox = tk.Checkbutton(root, text="Move user-created folders to the 'Other' folder", command=changePrefs, variable=sort_folders)
if not bool(make_other_folder.get()):
    sort_folders_checkbox.config(state="disabled")
sort_folders_checkbox.grid(column=0, row=3, padx=15, pady=2, sticky="w", columnspan=2)

start_clean_butt = tk.Button(root, text="Done", command=clean)
start_clean_butt.grid(column=1, row=5, sticky="es", padx=0, pady=5)

status_bar = tk.Label(root, textvariable=status, fg="white")
status_bar.grid(column=0, row=5, sticky="ws", padx=5, pady=5)

path_title = tk.Label(root, text="Path Of Downloads Folder:")
path_title.grid(column=0, row=4, padx=5, pady=5, sticky="w")

path_input = tk.Entry(root, textvariable=path)
path_input.grid(column=1, row=4, padx=0, sticky="w")

root.mainloop()
