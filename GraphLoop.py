import pygame
from GraphClasses import Node

class Loop:
    def __init__(self):
        pygame.init()

        self.win = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0], pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        self.running = True
        self.graphical_elts = []
        self.hits = []
        self.selected = []
        self.command = ""
        self.is_listening = ""
        self.targets = []
        self.bg_col = (64, 64, 64)
        self.log_font = pygame.font.SysFont("jetbrain mono", 30)
        self.log = ""

        while self.running:
            self.win.fill(self.bg_col)
            self.log_line = self.log_font.render(self.log, False, (255-self.bg_col[0], 255-self.bg_col[1], 255-self.bg_col[2]))
            self.win.blit(self.log_line, (0, self.win.get_height()-20))
            self.hits = self.for_all_gre({"update": None, "hits": None})["hits"]
            self.handle_commands()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def handle_commands(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.log = "[GraphCut] app terminated"
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = pygame.mouse.get_pressed(5)
                if x[2]:
                    if len(self.hits) == 0:
                        self.graphical_elts.append(Node(self.win, pygame.draw.ellipse, {
                            "surface": self.win, "color": (0, 32, 128),
                            "rect": (pygame.mouse.get_pos()[0] - 10, pygame.mouse.get_pos()[1] - 10, 20, 20)},
                    {"font" : pygame.font.SysFont("jetbrain mono", 30), "text": "", "color": (192, 192, 192)}))
                        self.log = "[GraphCut] node created"
                    else:
                        self.for_all_hit({"del": None})
                        self.log = "[GraphCut] node deleted"
                if x[0]:
                    self.selected = self.for_all_hit({"selected": None})["selected"]
            if event.type == pygame.MOUSEMOTION:
                if event.dict["buttons"][0] == 1:
                    self.for_all_gre({"slide": event.dict["rel"]})
            if event.type == pygame.KEYDOWN:
                self.handle_shortcuts(event.dict["unicode"])

    def handle_shortcuts(self, key):
        if self.is_listening == "" or key == "\x08":
            if key == "\x08" and len(self.command) > 0:
                self.command = self.command[:-1]
            if key == "?":
                self.selected = self.graphical_elts
                self.log = "[GraphCut] all nodes selected"
            if key == "!":
                self.selected = []
                self.targets = []
                self.log = "[GraphCut] all nodes unselected"
            if key == "." :
                self.selected.pop()
                self.log = "[GraphCut] last node unselected"
            if key == ";" :
                self.targets.append(self.selected.pop())
                self.log = "[GraphCut] last node targeted and unselected"
            if key == "," :
                for i in range(1, len(self.selected)+1):
                    if self.selected[len(self.selected) - i] not in self.targets:
                        self.targets.append(self.selected[len(self.selected) - i])
                self.log = "[GraphCut] last not-targeted node targeted"
            elif key == "c":
                self.is_listening = "color"
            elif key == "m":
                self.for_all_tar({"mode":None})
                self.targets = []
                self.log = "[GraphCut] targeted nodes' mode changed"
            elif key == "r":
                self.is_listening = "rect"
            elif key == "w":
                self.is_listening = "width"
            elif key == "t":
                self.is_listening = "text"
        else:
            self.command += key
        #if len(self.command) > 0 or key == "\x08":
        #    self.log = f"[GraphCut] {self.command}"
        if self.is_listening == "color":
            self.log = f"[GraphCut] listening mode color activated : {self.command}"
            if len(self.command.split(" ")) == 3:
                if key == "\r":
                    r, g, b = self.command.split(" ")
                    self.for_all_tar({"color" : (int(r), int(g), int(b))})
                    self.command = ""
                    self.targets = []
                    self.log = f"[GraphCut] targeted nodes' color changed to {r} {g} {b[:-1]}"
                    self.is_listening = ""
        if self.is_listening == "rect":
            self.log = f"[GraphCut] listening mode rect activated : {self.command}"
            if len(self.command.split(" ")) == 2:
                if key == "\r":
                    x, y = self.command.split(" ")
                    self.for_all_tar({"rect" : (int(x), int(y))})
                    self.command = ""
                    self.targets = []
                    self.log = f"[GraphCut] targeted nodes' rect changed to {x} {y[:-1]}"
                    self.is_listening = ""
        if self.is_listening == "width":
            self.log = f"[GraphCut] listening mode width activated : {self.command}"
            if len(self.command.split(" ")) == 2:
                if key == "\r":
                    x, y = self.command.split(" ")
                    self.for_all_tar({"width" : (int(x), int(y))})
                    self.command = ""
                    self.targets = []
                    self.log = f"[GraphCut] targeted nodes' width changed to {x} {y[:-1]}"
                    self.is_listening = ""
        if self.is_listening == "text":
            self.log = f"[GraphCut] listening mode text activated : {self.command}"
            if key == "\r":
                text = self.command
                self.for_all_tar({"text" : text[:-1]})
                self.command = ""
                self.targets = []
                self.log = f"[GraphCut] targeted nodes' text changed to : {text[:-1]}"
                self.is_listening = ""


    def for_all_gre(self, order):
        work = {"hits": []}
        for elt in self.graphical_elts:
            if "slide" in order.keys():
                elt.slide(order["slide"])
            if "update" in order.keys():
                elt.graphical_update()
            if "hits" in order.keys():
                if elt.covert(pygame.mouse.get_pos()):
                    work["hits"].append(elt)
        return work

    def for_all_hit(self, order):
        work = {"selected": self.selected}
        if "del" in order.keys():
            for elt in self.hits:
                del(self.graphical_elts[self.graphical_elts.index(elt)])
        else:
            for elt in self.hits:
                if "selected" in order.keys():
                    elt.toggle_selected()
                if elt.is_selected:
                    if elt not in work["selected"]:
                        work["selected"].append(elt)
                        self.log = "[GraphCut] node selected"
                else:
                    if elt in work["selected"]:
                        del(work["selected"][work["selected"].index(elt)])
                        self.log = "[GraphCut] node unselected"
        return work

    def for_all_tar(self, order):
        if not self.targets:
            self.targets = self.selected.copy()
        if "rect" in order.keys():
            rel = order["rect"][0] - self.targets[0].get_pos()[0], order["rect"][1] - self.targets[0].get_pos()[1]
            for target in self.targets:
                target.slide(rel)
        else:
            for target in self.targets:
                if "color" in order.keys():
                    target.color(order["color"])
                if "mode" in order.keys():
                    target.toggle_mode()
                if "width" in order.keys():
                    target.width(*order["width"])
                if "text" in order.keys():
                    target.label(order["text"])