import requests
from bs4 import BeautifulSoup
import os
import pathlib
import argparse

def convert_to_local_images(input_html_file: str, output_html_file: str):
    with open(fr"{input_html_file}", "r") as html_file:
        soup = BeautifulSoup(html_file.read(), 'html.parser')

        # Downloads the images from the HTML File.
        for index, img in enumerate(soup.find_all("img")):
            img_src = img["src"]
            response = requests.get(img_src)

            # make the folder if it doesnt exist
            stem = pathlib.Path(input_html_file).stem
            my_path = f"images/{stem}/"
            if not os.path.exists(my_path):
                os.makedirs(my_path)
            
            # save the image
            new_src = f"{my_path}{stem}_{index}"
            with open(new_src, "wb") as image_to_write:
                image_to_write.write(response.content)

            # update the source to the image's location
            img["src"] = new_src

    with open(output_html_file, "w") as html_file:
        # write the new html file
        html_file.write(soup.prettify())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="replaces html image links with local images")
    parser.add_argument("input_file", type=str, help="enter the name of the html file you want to replace the links in. Ex: 'my_website.html'")
    parser.add_argument("output_file", type=str, help="enter the name of the html file you want to save the output in. Ex: 'my_website_local_imgs.html'")
    args = parser.parse_args()

    convert_to_local_images(args.input_file, args.output_file)
