# for the stat wheel, the center circle is located at (296, 302). the radius of the circle is about 160,
# TICK LOCATIONS
# POWER: (297, 274), (297, 248), (297, 219), (297, 192), (297, 164), (297, 140)
# SPEED: (332, 288), (345, 275), (368, 262), (393, 247), (416, 234), (438, 221)
# RANGE: (321, 317), (345, 331), (369, 345), (393, 359), (416, 372), (437, 384)
# DURA.: (297, 332), (297, 358), (297, 386), (297, 414), (297, 440), (297, 464)
# PREC.: (272, 317), (250, 329), (225, 344), (202, 357), (177, 372), (157, 383)
# POTE.: (272, 288), (249, 275), (225, 261), (201, 247), (178, 234), (158, 222)

# LETTER LOCATIONS
# POWER: (297, 100)
# SPEED: (477, 198)
# RANGE: (474, 404)
# DURA.: (297, 503)
# PREC.: (124, 402)
# POTE.: (120, 201)

import sys
from PIL import Image, ImageDraw, ImageFont


class ImageManager:
    def __init__(self):
        self.bg = None
        self.completed_wheel = None

    def draw_polygon(self, rankings):
        power_dict = {'E': (297, 274), 'D': (297, 248), 'C': (297, 219), 'B': (297, 192), 'A': (297, 164),
                      '∞': (297, 140)}
        speed_dict = {'E': (321, 288), 'D': (345, 275), 'C': (369, 262), 'B': (393, 247), 'A': (416, 234),
                      '∞': (438, 221)}
        range_dict = {'E': (321, 317), 'D': (345, 331), 'C': (369, 345), 'B': (393, 359), 'A': (416, 372),
                      '∞': (438, 384)}
        durability_dict = {'E': (297, 332), 'D': (297, 358), 'C': (297, 386), 'B': (297, 414), 'A': (297, 440),
                           '∞': (297, 464)}
        precision_dict = {'E': (272, 317), 'D': (250, 329), 'C': (225, 344), 'B': (202, 357), 'A': (177, 372),
                          '∞': (158, 383)}
        potential_dict = {'E': (272, 288), 'D': (249, 275), 'C': (225, 261), 'B': (201, 247), 'A': (178, 234),
                          '∞': (158, 222)}
        # open the stat wheel
        with Image.open("images/jjba_stand_stats_xeromatt_copy.png").convert("RGBA") as image:
            # create a blank image where the polygon will go
            im2 = Image.new("RGBA", image.size, (255, 255, 255, 0))
            # create a drawing context
            d = ImageDraw.Draw(im2)
            # create a font
            fnt = ImageFont.truetype("fonts/Roboto-Medium.ttf", 40)

            # draw polygon at points given in the rankings argument
            d.polygon(
                [power_dict[rankings[0]], speed_dict[rankings[1]], range_dict[rankings[2]],
                 durability_dict[rankings[3]],
                 precision_dict[rankings[4]], potential_dict[rankings[5]]], width=0, outline=(0, 0, 0, 0),
                fill=(100, 100, 100, 100))

            # put text giving every letter grade at the proper location
            d.text((285, 80), rankings[0], font=fnt, fill=(0, 0, 0, 255))
            d.text((455, 175), rankings[1], font=fnt, fill=(0, 0, 0, 255))
            d.text((455, 385), rankings[2], font=fnt, fill=(0, 0, 0, 255))
            d.text((285, 480), rankings[3], font=fnt, fill=(0, 0, 0, 255))
            d.text((115, 375), rankings[4], font=fnt, fill=(0, 0, 0, 255))
            d.text((115, 175), rankings[5], font=fnt, fill=(0, 0, 0, 255))

            self.completed_wheel = Image.alpha_composite(image, im2)
            # resizes the wheel and adds it to the background
            self.completed_wheel = self.completed_wheel.resize((400, 400))
            self.bg.paste(self.completed_wheel, (0, 320), self.completed_wheel)

    def create_background(self):
        # just opens the background image and resizes it to the proper size
        with Image.open('images/pikisuperstar_bg.jpg') as original:
            self.bg = original.copy()
        self.bg = self.bg.resize((1280, 720))

    def generate_gradient(self, color1):
        gradient1 = Image.new("RGBA", self.bg.size, color1)

        alpha = Image.linear_gradient('L').resize(self.bg.size).rotate(180)
        gradient1.putalpha(alpha)
        self.bg.paste(gradient1, (0, 0), gradient1)

    def place_names(self, stand_name, user_name, color):
        # create a drawing context
        d = ImageDraw.Draw(self.bg)

        if color == 'White':
            fill = (255, 255, 255)
        else:
            fill = (0, 0, 0)
        # create font
        fnt = ImageFont.truetype("fonts/Constantia_Font.ttf", 50)
        fnt2 = ImageFont.truetype("fonts/Constantia_Font.ttf", 70)

        # add all text to the image
        d.text((50, 50), "[STAND NAME]", font=fnt, fill=fill)
        d.text((75, 100), stand_name, font=fnt2, fill=fill)

        d.text((800, 550), '[STAND MASTER]', font=fnt, fill=fill)
        d.text((825, 600), user_name, font=fnt2, fill=fill)

    def place_stand_image(self, file_path, resize):
        with Image.open(file_path).convert("RGBA") as image:
            # resize the image if desired
            if resize:
                bigger_dimension = max([image.width, image.height])
                resize_factor = 720 / bigger_dimension
                image = image.resize((int(image.width * resize_factor), int(image.height * resize_factor)))
            # the center of the image is (700, 360)
            self.bg.paste(image, (int(700 - image.width / 2), int(360 - image.height / 2)), image)
