# from PIL import Image, ImageTk
# from tkinter import Canvas
#
#
# class CanvasHandler:
#     def set_canvas_image(self, canvas: Canvas, image: Image, canvas_width: int, canvas_height: int)->Canvas:
#         print(canvas)
#         print(image)
#         print(canvas_width)
#         print(canvas_height)
#         original_width, original_height = image.size
#         scaling_factor = min(canvas_width / original_width, canvas_height / original_height)
#         new_width = int(original_width * scaling_factor)
#         new_height = int(original_height * scaling_factor)
#         resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
#         image = ImageTk.PhotoImage(resized_image)
#         x_offset = (canvas_width - new_width) // 2
#         y_offset = (canvas_height - new_height) // 2
#         canvas.create_image(x_offset, y_offset, image=image, anchor="nw")
#         return canvas


from PIL import Image, ImageTk
from tkinter import Canvas


class CanvasHandler:
    def __init__(self, canvas, canvas_width, canvas_height):
        # Store a reference to all images to prevent garbage collection
        self.image_refs = []
        self.canvas = canvas
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

    def set_canvas_image(self, image):
        # Get original image dimensions
        original_width, original_height = image.size

        # Calculate scaling factor to fit image proportionally within the canvas
        scaling_factor = min(self.canvas_width / original_width, self.canvas_height / original_height)
        # scaling_factor = min(self.canvas_width / original_width, self.canvas_height / original_height)
        new_width = int(original_width * scaling_factor)
        new_height = int(original_height * scaling_factor)

        # Resize the image
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        tk_image = ImageTk.PhotoImage(resized_image)

        # Center the image in the canvas
        x_offset = (self.canvas_width - new_width) // 2
        # x_offset = (self.canvas_width - new_width) // 2
        y_offset = (self.canvas_height - new_height) // 2
        self.image_refs = []
        # Display the image
        self.canvas.create_image(x_offset, y_offset, image=tk_image, anchor="nw")

        # Save a reference to the image to prevent garbage collection
        self.image_refs.append(tk_image)

        # return canvas
