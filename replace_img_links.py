import requests
from bs4 import BeautifulSoup
import os
import pathlib

def convert_to_local_images(input_html_file: str, output_html_file: str):
    with open(fr"{input_html_file}", "r") as html_file:
        soup = BeautifulSoup(html_file.read(), 'html.parser')

        # Downloads the images from the HTML File.
        for index, img in enumerate(soup.find_all("img")):
            img_src = img["src"]
            response = requests.get(img_src)

            # make the folder if it doesnt exist
            my_path = f"images/{pathlib.Path(input_html_file).stem}/"
            if not os.path.exists(my_path):
                os.makedirs(my_path)
            
            # save the image
            new_src = f"{my_path}{input_html_file}_{index}"
            with open(new_src, "wb") as image_to_write:
                image_to_write.write(response.content)

            # update the source to the image's location
            img["src"] = new_src

    with open(output_html_file, "w") as html_file:
        # write the new html file
        html_file.write(soup.prettify())

if __name__ == "__main__":
    for file in ["BL.html", "BR.html", "FL.html", "FR.html"]:
        convert_to_local_images(file, file.replace(".html", "_local_images.html"))
