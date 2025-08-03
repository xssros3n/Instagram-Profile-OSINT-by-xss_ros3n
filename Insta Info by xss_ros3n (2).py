import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
from PIL import Image, ImageTk
import instaloader
import requests
import re
import io

def extract_username(input_str):
    if "instagram.com" in input_str:
        match = re.search(r"instagram\.com/([^/?]+)", input_str)
        return match.group(1) if match else None
    return input_str

def fetch_info():
    global profile_image_data
    user_input = entry.get().strip()
    username = extract_username(user_input)
    if not username:
        messagebox.showerror("Invalid Input", "Please enter a valid Instagram username or profile link.")
        return

    try:
        output_text.config(state='normal')
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"[*] Fetching data for {username}...\n\n")
        L = instaloader.Instaloader()
        profile = instaloader.Profile.from_username(L.context, username)

        output_text.insert(tk.END, f"Username    : {profile.username}\n")
        output_text.insert(tk.END, f"Full Name   : {profile.full_name or 'N/A'}\n")
        output_text.insert(tk.END, f"Bio         : {profile.biography or 'N/A'}\n")
        output_text.insert(tk.END, f"External URL: {profile.external_url or 'None'}\n")
        output_text.insert(tk.END, f"Followers   : {profile.followers}\n")
        output_text.insert(tk.END, f"Following   : {profile.followees}\n")
        output_text.insert(tk.END, f"Posts       : {profile.mediacount}\n")
        output_text.insert(tk.END, f"Is Verified?: {profile.is_verified}\n")
        output_text.insert(tk.END, f"Is Private? : {profile.is_private}\n\n")

        # Download profile picture into memory only
        pic_url = profile.profile_pic_url
        img_response = requests.get(pic_url)
        profile_image_data = img_response.content
        show_profile_pic(profile_image_data)

        download_btn.config(state="normal")
        output_text.config(state='disabled')

    except Exception as e:
        output_text.insert(tk.END, f"[-] Error: {e}\n")
        output_text.config(state='disabled')

def show_profile_pic(img_data):
    try:
        img = Image.open(io.BytesIO(img_data))
        img = img.resize((240, 240))  # Enlarged size
        img_tk = ImageTk.PhotoImage(img)
        img_label.config(image=img_tk)
        img_label.image = img_tk
    except Exception as e:
        output_text.insert(tk.END, f"[!] Failed to load image preview: {e}\n")

def download_profile_pic():
    if not profile_image_data:
        messagebox.showwarning("No Image", "No profile picture to save.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg")])
    if file_path:
        with open(file_path, "wb") as f:
            f.write(profile_image_data)
        messagebox.showinfo("Saved", f"Profile picture saved to:\n{file_path}")

# GUI Setup
profile_image_data = None
root = tk.Tk()
root.title("Osint Xss Ros3n")
root.configure(bg="#111111")
root.geometry("360x740")

# Title
title = tk.Label(root, text="Osint Xss Ros3n", font=("Helvetica", 18, "bold"), fg="#00ffff", bg="#111111")
title.pack(pady=5)

# Entry
entry = tk.Entry(root, font=("Helvetica", 12), width=30, justify="center", bg="#1f1f1f", fg="#ffffff")
entry.pack(pady=8)

# Fetch Button
fetch_btn = tk.Button(root, text="Fetch Info", font=("Helvetica", 12), command=fetch_info, bg="#00aa00", fg="white")
fetch_btn.pack(pady=6)

# Profile Image
img_label = tk.Label(root, bg="#111111")
img_label.pack(pady=6)

# Download Button
download_btn = tk.Button(root, text="Download Profile Picture", command=download_profile_pic,
                         font=("Helvetica", 11), bg="#222222", fg="white", state="disabled")
download_btn.pack(pady=4)

# Info Text Box
output_text = scrolledtext.ScrolledText(
    root, wrap=tk.WORD,
    font=("Segoe UI Emoji", 10),  # Emoji & special char support
    width=42, height=17,
    bg="#000000", fg="#00ff00", borderwidth=2
)
output_text.pack(padx=10, pady=8)
output_text.config(state='disabled')

root.mainloop()