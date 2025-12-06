import pygame

class Node:
    def __init__(self, frame, draw_type, type_specs:dict, txt_specs:dict):
        self.frame = frame
        self.args = {"draw_type": draw_type, "type_specs":type_specs, "txt_specs":txt_specs}
        self.graphics = draw_type(**type_specs)
        self.is_selected = False

    def covert(self, pos):
        if self.args["draw_type"] == pygame.draw.rect:
            return ((self.args["type_specs"]["rect"][0] <= pos[0] <= self.args["type_specs"]["rect"][0] + self.args["type_specs"]["rect"][2]) and
                    (self.args["type_specs"]["rect"][1] <= pos[1] <= self.args["type_specs"]["rect"][1] + self.args["type_specs"]["rect"][3]))
        elif self.args["draw_type"] == pygame.draw.ellipse:
            if self.args["type_specs"]["rect"][2] > 0 and self.args["type_specs"]["rect"][3] > 0:
                return 1 >= ((pos[0] - self.args["type_specs"]["rect"][0] - self.args["type_specs"]["rect"][2]/2)/self.args["type_specs"]["rect"][2])**2 + ((pos[1] - self.args["type_specs"]["rect"][1] - self.args["type_specs"]["rect"][3]/2)/self.args["type_specs"]["rect"][2])**2
            else: return False
        else: return False

    def toggle_selected(self):
        self.is_selected = not self.is_selected

    def graphical_update(self, draw_type = None, type_specs = None):
        if not draw_type:
            draw_type = self.args["draw_type"]
        else:
            self.args["draw_type"] = draw_type
        if not type_specs:
            type_specs = self.args["type_specs"]
        else:
            self.args["type_specs"] = type_specs
        self.graphics = draw_type(**type_specs)
        if self.args["txt_specs"]["text"] != "":
            text = self.args["txt_specs"]["font"].render(self.args["txt_specs"]["text"], False, self.args["txt_specs"]["color"])
            self.frame.blit(text, self.args["type_specs"]["rect"][:2])

    def slide(self, rel):
        self.args["type_specs"]["rect"] = (self.args["type_specs"]["rect"][0] + rel[0], self.args["type_specs"]["rect"][1] + rel[1],
                                           self.args["type_specs"]["rect"][2], self.args["type_specs"]["rect"][3])

    def color(self, rgb):
        self.args["type_specs"]["color"] = rgb

    def toggle_mode(self):
        if self.args["draw_type"] == pygame.draw.rect:
            self.args["draw_type"] = pygame.draw.ellipse
        elif self.args["draw_type"] == pygame.draw.ellipse:
            self.args["draw_type"] = pygame.draw.rect

    def width(self, x, y):
        self.args["type_specs"]["rect"] = self.args["type_specs"]["rect"][0], self.args["type_specs"]["rect"][1], x, y

    # getters
    def get_pos(self):
        return self.args["type_specs"]["rect"][0], self.args["type_specs"]["rect"][1]

    def label(self, text):
        self.args["txt_specs"]["text"] = text