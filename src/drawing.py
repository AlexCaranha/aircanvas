import cv2
import numpy as np 

class DrawingCanvas:
    def __init__(self, width, height):
        self.canvas = np.zeros((height, width, 3), dtype=np.uint8)
        self.temp_canvas = np.zeros_like(self.canvas)

        self.colour = (0, 0, 255) 
        self.thickness = 5
        self.eraser_thickness = 20

        self.current_tool = "pen"
        self.drawing = False
        self.start_point = None

        # available colours
        self.colours = {
            "red": (0, 0, 255),
            "orange": (0, 165, 255),
            "yellow": (0, 255, 255),
            "green": (0, 255, 0),
            "blue": (255, 0, 0),
            "magenta": (255, 0, 255),
            "black": (0, 0, 0),
            "white": (255, 255, 255)
        }

        def start_drawing(self, point):
            self.drawing = True
            self.start_point = point

        def stop_drawing(self):
            self.drawing = False
            self.start_point = None

            if np.any(self.temp_canvas):
                self.canvas = cv2.add(self.canvas, self.temp_canvas)
                self.temp_canvas.fill(0)

        def draw(self, point):
            if not self.drawing:
                return
            
            if self.current_tool == "pen":
                cv2.line(self.canvas, self.start_point, point, self.colour, self.thickness)
                self.start_point = point

            elif self.current_tool == "eraser":
                cv2.line(self.canvas, self.start_point, point,
                        (0, 0, 0), self.eraser_thickness)
                self.start_point = point

            elif self.current_tool in ["rectangle", "circle"]:
                self.temp_canvas.fill(0)

                if self.current_tool == "rectangle":
                    cv2.rectangle(self.temp_canvas, self.start_point, point, self.color, self.thickness)

                else:
                    center = self.start_point
                    radius = int(((point[0] - center[0]) ** 2 + 
                                (point[1] - center[1]) ** 2) ** 0.5)
                    cv2.circle(self.temp_canvas, center, radius,
                            self.color, self.thickness)
                    
        def clear(self):
            self.canvas.fill(0)
            self.temp_canvas.fill(0)

        def set_colour(self, colour_name):
            if colour_name in self.colours:
                self.colour = self.colours[colour_name]

        def set_tool(self, tool_name):
            if tool_name in ["pen", "eraser", "rectangle", "circle"]:
                self.current_tool = tool_name

        def get_display(self):
            return cv2.add(self.canvas, self.temp_canvas)