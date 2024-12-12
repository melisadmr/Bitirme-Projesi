
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\lecturess\season 4 fall version\bitirme odevi\son olmasi dilegiyle\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1280x720")
window.configure(bg = "#101319")


canvas = Canvas(
    window,
    bg = "#101319",
    height = 720,
    width = 1280,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    640.0,
    359.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    320.0,
    83.0,
    image=image_image_2
)

canvas.create_text(
    139.0,
    62.0,
    anchor="nw",
    text="Sosyal Medya Tehdit Analizi",
    fill="#F5F6FA",
    font=("Poppins SemiBold", 28 * -1)
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    100.0,
    82.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    78.0,
    331.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    496.0,
    317.0,
    image=image_image_5
)

canvas.create_text(
    166.0,
    156.0,
    anchor="nw",
    text="Veri Grafiği",
    fill="#F5F6FA",
    font=("Poppins SemiBold", 26 * -1)
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    494.0,
    584.0,
    image=image_image_6
)

canvas.create_text(
    150.0,
    521.0,
    anchor="nw",
    text="Sonuç",
    fill="#F5F6FA",
    font=("Poppins SemiBold", 26 * -1)
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    1029.0,
    185.0,
    image=image_image_7
)

canvas.create_text(
    881.0,
    132.0,
    anchor="nw",
    text="Toplam Data",
    fill="#F5F6FA",
    font=("Poppins SemiBold", 26 * -1)
)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    1029.0,
    317.0,
    image=image_image_8
)

canvas.create_text(
    881.0,
    262.0,
    anchor="nw",
    text="Nötr Duygu Oranı",
    fill="#F5F6FA",
    font=("Poppins SemiBold", 21 * -1)
)

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    1029.0,
    450.0,
    image=image_image_9
)

canvas.create_text(
    881.0,
    398.0,
    anchor="nw",
    text="Olumsuz Duygu Oranı",
    fill="#F5F6FA",
    font=("Poppins SemiBold", 16)
)

image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    1029.0,
    584.0,
    image=image_image_10
)

canvas.create_text(
    885.0,
    520.0,
    anchor="nw",
    text="Geri Sayım",
    fill="#F5F6FA",
    font=("Poppins SemiBold", 26 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=46.0,
    y=171.0,
    width=65.0,
    height=65.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=46.0,
    y=254.0,
    width=65.0,
    height=65.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=46.0,
    y=341.0,
    width=65.0,
    height=65.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x = 46.0,
    y = 432.0,
    width = 65.0,
    height = 65.0
)
window.resizable(False, False)
window.mainloop()
