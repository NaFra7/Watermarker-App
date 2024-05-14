import tkinter
from tkinter import *
from tkinter import filedialog, ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont

FILE_PATH = "Downloads"
filename = ""
username = "YourUsernameHere"  # e.g. C:\Users\--->YourUserName<----


# ----- Functions ----- #

def apply_watermark():
    """Gets the text entered into the field, prepares the watermark as a new image, combines the images,
    and then saves the final image to the Pictures folder. The final image is also displayed for the user,
    while the entry field and Selected File are readied for the next file"""
    global filename
    text = text_entry.get()
    img_one = Image.open(filename).convert("RGBA")

    watermark = Image.new("RGBA", img_one.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(watermark)

    w, h = img_one.size
    x, y = int(w / 2), int(h / 2)
    if x > y:
        font_size = y
    elif y > x:
        font_size = x
    else:
        font_size = x

    font = ImageFont.truetype("arial.ttf", int(font_size / 10))
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 180), anchor='ms')
    final_img = Image.alpha_composite(img_one, watermark)

    first_split = filename.split('/')[-1]
    f = first_split.split('.')[0]
    save_path = f'C:\\Users\\{username}\\Pictures\\watermarked_{f}.png'
    final_img.save(save_path)
    final_img.show()

    text_entry.delete(0, tkinter.END)
    selected_img.config(text='Selected File: None')
    image_label.config(image="")


def open_image():
    """Opens a window for user to select an image, updates the UI to give confirmation of the file selected,
    and then displays the image"""
    global filename
    filename = filedialog.askopenfilename(title="Select Image",
                                          filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ico")])
    f = filename.split('/')[-1]
    selected_img.config(text=f"Selected File: {f}")
    display_image(filename)


def display_image(filename):
    """Displays the selected file for visual verification before submitting for watermark"""
    image = Image.open(filename)
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.photo = photo


# -------- UI SETUP ------ #
window = Tk()
window.title("Watermark Your Image")
mainframe = ttk.Frame(window, padding="2 2 12 12")
mainframe.grid(column=0, row=0)
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)
logo = PhotoImage(file='logo.png')

# ----- Buttons ----- #
buttons = ttk.Frame(mainframe, padding="1 1 1 1")
buttons.grid(column=0, row=0)
add_text = ttk.Button(buttons, text="Submit Text", command=apply_watermark)
add_text.grid(column=0, row=4)
upload_img = ttk.Button(buttons, text="Upload Image", command=open_image)
upload_img.grid(column=0, row=1, columnspan=2)

# ----- Labels ----- #
ttk.Label(buttons, compound="top", image=logo).grid(column=0, row=0, sticky=N, columnspan=2)
selected_img = ttk.Label(buttons, text="Selected File: None", wraplength=500)
selected_img.grid(column=0, row=5, columnspan=2)
ttk.Label(buttons, text="Type Watermark text in the box below:").grid(column=0, row=3, columnspan=2)
image_label = ttk.Label(mainframe, text="", compound="image")
image_label.grid(column=1, row=0, columnspan=1, rowspan=2)

# ------ Entry ----- #
text_entry = ttk.Entry(buttons, width=30)
text_entry.grid(column=1, row=4)

text_entry.focus()
window.mainloop()
