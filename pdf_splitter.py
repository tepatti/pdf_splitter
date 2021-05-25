# pdf_splitter.py

# 
# Linkki englanninkieliseen dokumentaatioon:
# https://www.blog.pythonlibrary.org/2018/04/11/splitting-and-merging-pdfs-with-python/
# Kirjoittanut ja kommentoinut Teemu Mäkelä.
#

# Tuodaan tarvittavat moduulit.
# PyPDF2 on ainoa, joka ei tule pythonin asennuksessa mukana.
# Sen saa asennettua komennolla: pip install pypdf2
import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import tkinter as tk
from tkinter.constants import *
from tkinter import filedialog


# Tämä funktio valitsee pdf-tiedoston ja kansion, mihin pdf-tiedoston sivut kopioidaan.
def select_file():
    # Avataan Resurssienhallinta-ikkuna pdf-tiedoston valitsemista varten.
    root.filename = filedialog.askopenfilename(initialdir = "/",
                                                    title = "Valitse pdf-tiedosto, jonka sivut haluat kopioida",
                                                filetypes = (("pdf files","*.pdf"),("all files","*.*")))
    # Asetetaan valitun pdf-tiedoston polku muuttujaan.
    path_from = root.filename
    # Avataan Resurssienhallinta-ikkuna tallennuskansion valitsemista varten.
    root.directoryname = filedialog.askdirectory(title = "Valitse kansio, mihin haluat sivujen kopiot")
    # Asetetaan valitun tallennuskansion polku muuttujaan.
    path_to = root.directoryname
    # Kutsuu funktiota pdf_splitter() valitulla tiedostolla ja kansiolla.
    pdf_splitter(path_from, path_to)


# Tämä funktio pilkkoo pdf-tiedoston sivut erillisiksi pdf-tiedostoiksi uuteen kansioon.
def pdf_splitter(path_from, path_to):
    # Trimmataan valitusta pdf-tiedoston sijainnista tiedoston nimi ja asetetaan se muuttujaan.
    fname = os.path.splitext(os.path.basename(path_from))[0]
    # Annetaan valittu pdf-tiedosto PdfFileReader luokalle.
    pdf = PdfFileReader(path_from)
    # Yhdistetään valitun kansion polku ja tiedoston nimi ja asetetaan ne muuttujaan.
    new_path = os.path.join(path_to, fname)
    # Luodaan uusi kansio uuteen polkuun.
    os.mkdir(new_path)
    # Suoritetaan loopin koodi jokaiselle pdf-tiedoston sivulle.
    for page in range(pdf.getNumPages()):
        # Tehdään uusi pdf-tiedoston sivu johon kirjoitetaan pdf-tiedoston yhdellä sivulla oleva sisältö.
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))
        # Asetetaan muuttujan arvoksi tiedoston nimi ja sivunumero.
        output_filename = "{}_page_{}.pdf".format(fname, page+1)
        # Asetetaan muuttujan arvoksi valitun tallennuskansion polku ja uuden yksisivuisen tiedoston nimi.
        output_directory = os.path.join(new_path, output_filename)
        # Luodaan ja avataan tiedosto. 
        with open(output_directory, "wb") as out:
            # Kirjoitetaan tiedostoon pdf-tiedoston yhden sivun sisältö.
            pdf_writer.write(out)
        # Tulostetaan komentokehotteeseen luodun tiedoston nimi.
        print("Created: {}".format(output_filename))


if __name__ == "__main__":
    # Luodaan tkinter kirjastolla ikkuna ja nimetään se "root".
    root = tk.Tk()
    # Annetaan ikkunalle otsikko.
    root.title("Jakaa pdf-tiedoston sivut omiin tiedostoihinsa")
    # Asetetaan muuttujaan "toppauksien" eli padding x ja y akselien arvot.
    paddings = {"padx": 25, "pady": 25}
    # Asetetaan muuttujaan fontti ja fonttikoko.
    entry_font = {"font": ("Helvetica", 16)}
    # Tehdään nappula, jossa on määritellyt fontti ja padding joka painettaessa kutsuu funktiota select_file.
    tk.Button(root,
              text="Klikkaa valitaksesi pdf tiedosto \n ja kansio, mihin sivut tallennetaan", 
              command=select_file, 
              **entry_font).pack(side = TOP, expand = TRUE, fill = BOTH, **paddings)
    # mainloop käynnistää ikkunan ja odottaa tapahtumia siinä kunnes käyttäjä sulkee sen.
    root.mainloop()