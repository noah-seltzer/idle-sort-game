import tkinter as tk
import time
import random

class Resource:
    def __init__(self, name, initial_amount=0.0, production_rate=0.0, label_widget=None):
        self.name = name
        self.amount = initial_amount
        self.production_rate = production_rate
        self.label_widget = label_widget

    def produce(self, delta_time):
        self.amount += self.production_rate * delta_time
        if self.label_widget:
            self.label_widget.config(text=f"{self.name}: ${self.amount:.2f}")

    def consume(self, amount):
        if self.amount >= amount:
            self.amount -= amount
            if self.label_widget:
                self.label_widget.config(text=f"{self.name}: ${self.amount:.2f}")
            return True
        return False

    def set_label_widget(self, widget):
        self.label_widget = widget

    def __str__(self):
        return f"{self.name}: ${self.amount:.2f}"
class Sorter:
    def __init__(self, name, cost, numbers_per_sort, sort_speed, buy_button=None, count_label=None, canvas=None):
        self.name = name
        self.cost = cost
        self.numbers_per_sort = numbers_per_sort
        self.sort_speed = sort_speed  # Time in seconds per sort
        self.count = 0
        self.buy_button = buy_button
        self.count_label = count_label
        self.canvas = canvas
        self.sort_items = [] # List of item IDs on the canvas
        self.is_processing = False
        self.process_progress = 0.0
        self.last_process_time = 0
        self.item_width = 10
        self.item_height = 10
        self.spacing = 2

    def can_afford(self, resources):
        return resources["money"].amount >= self.cost

    def purchase(self, resources):
        if self.can_afford(resources):
            resources["money"].amount -= self.cost
            if resources["money"].label_widget:
                resources["money"].label_widget.config(text=f"{resources['money'].name}: ${resources['money'].amount:.2f}")
            self.count += 1
            if self.count_label:
                self.count_label.config(text=f"Owned: {self.count}")
            if self.buy_button:
                self.update_button_text()
            self.cost *= 1.15  # Increase cost
            return True
        return False

    def get_production_rate(self):
        return self.count * self.numbers_per_sort / self.sort_speed

    def set_buy_button(self, widget):
        self.buy_button = widget
        self.update_button_text()

    def set_count_label(self, widget):
        self.count_label = widget
        if self.count_label:
            self.count_label.config(text=f"Owned: {self.count}")

    def set_canvas(self, canvas):
        self.canvas = canvas
        canvas_width = int(self.canvas.cget("width"))
        canvas_height = int(self.canvas.cget("height"))
        self.process_area_y = canvas_height * 0.2  # Top part for processing
        self.output_area_y = canvas_height * 0.6   # Bottom part for output

    def start_processing(self):
        if self.canvas and self.count > 0 and not self.is_processing:
            self.is_processing = True
            self.process_progress = 0.0
            self.sort_items = []
            canvas_width = int(self.canvas.cget("width"))
            process_height = int(self.process_area_y) - self.item_height - 10 # Adjusted height
            if process_height < 5: # Ensure a minimum height for random placement
                process_height = 5
            start_x = 10
            for _ in range(self.numbers_per_sort):
                y_start = 10
                y_end = int(self.process_area_y) - self.item_height - 5
                if y_start >= y_end:
                    y = y_start # Fallback if range is invalid
                else:
                    y = random.randint(y_start, y_end)
                x1 = start_x
                y1 = y
                x2 = x1 + self.item_width
                y2 = y1 + self.item_height
                item = self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue")
                self.sort_items.append(item)
                start_x += self.item_width + self.spacing
            self.last_process_time = time.time()

    def update_processing_animation(self):
        if self.is_processing and self.canvas and self.sort_items:
            progress = (time.time() - self.last_process_time) / self.sort_speed
            self.process_progress = min(1.0, progress)
            target_y = int(self.output_area_y) - self.item_height / 2

            for i, item in enumerate(self.sort_items):
                original_coords = self.canvas.coords(item)
                new_y_center = original_coords[1] + (target_y - original_coords[1]) * self.process_progress + self.item_height / 2
                self.canvas.coords(item, original_coords[0], new_y_center - self.item_height / 2, original_coords[2], new_y_center + self.item_height / 2)
                self.canvas.itemconfig(item, fill="orange") # Indicate processing

            if self.process_progress >= 1.0:
                self.is_processing = False
                self.last_process_time = time.time() # Start the "sorted" pause
                self.canvas.after(500, self.move_to_output) # Short delay before moving to output

    def move_to_output(self):
        if self.canvas and self.sort_items:
            output_x_start = 10
            output_y = int(self.canvas.cget("height")) - 30 - self.item_height
            for item in self.sort_items:
                self.canvas.coords(item, output_x_start, output_y, output_x_start + self.item_width, output_y + self.item_height)
                self.canvas.itemconfig(item, fill="green") # Indicate sorted
                output_x_start += self.item_width + self.spacing
            self.canvas.after(1000, self.clear_items) # Short delay before clearing

    def clear_items(self):
        if self.canvas and self.sort_items:
            for item in self.sort_items:
                self.canvas.delete(item)
            self.sort_items = []

    def update_button_text(self):
        if self.buy_button:
            button_text = f"Buy {self.name} (Cost: ${self.cost:.2f})"
            self.buy_button.config(text=button_text)

    def __str__(self):
        return f"{self.name} (Owned: {self.count}, Cost: ${self.cost:.2f}, Sorts: {self.numbers_per_sort} nums/{self.sort_speed:.2f}s)"

def create_gui(resources, sorters):
    window = tk.Tk()
    window.title("Number Sorting Factory")

    # Resource Display
    resource_frame = tk.LabelFrame(window, text="Resources")
    resource_frame.pack(padx=10, pady=10, fill=tk.X)

    resource_labels = {}
    for i, (name, resource) in enumerate(resources.items()):
        label = tk.Label(resource_frame, text=f"{name}: ${resource.amount:.2f}")
        label.pack(pady=2, anchor=tk.W)
        resource.set_label_widget(label)
        resource_labels[name] = label

    # Sorter Frame and Visuals
    sorter_frame = tk.LabelFrame(window, text="Sorters")
    sorter_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    sorter_canvases = {}
    sorter_info_frames = {}

    for name, sorter in sorters.items():
        info_frame = tk.Frame(sorter_frame)
        info_frame.pack(pady=5, fill=tk.X)
        sorter_info_frames[name] = info_frame

        count_label = tk.Label(info_frame, text=f"{sorter.name}: Owned {sorter.count}")
        count_label.pack(side=tk.LEFT)
        sorter.set_count_label(count_label)

        buy_button = tk.Button(info_frame, text=f"Buy {sorter.name} (Cost: ${sorter.cost:.2f})",
                               command=lambda s=sorter: purchase_sorter(s, resources))
        buy_button.pack(side=tk.LEFT, padx=5)
        sorter.set_buy_button(buy_button)

        canvas = tk.Canvas(sorter_frame, width=200, height=100, bg="lightgray", bd=2, relief=tk.SUNKEN)
        canvas.pack(pady=2, fill=tk.X)
        sorter.set_canvas(canvas)
        sorter_canvases[name] = canvas

        # Add visual cues for processing and output areas (optional)
        canvas_width = int(canvas.cget("width"))
        process_line_y = int(canvas.cget("height")) * 0.2
        output_line_y = int(canvas.cget("height")) * 0.6
        canvas.create_line(0, process_line_y, canvas_width, process_line_y, fill="gray", dash=(2, 2))
        canvas.create_text(5, process_line_y - 5, anchor=tk.NW, text="Input", fill="gray")
        canvas.create_line(0, output_line_y, canvas_width, output_line_y, fill="gray", dash=(2, 2))
        canvas.create_text(5, output_line_y - 5, anchor=tk.NW, text="Processing", fill="gray")
        canvas.create_text(5, int(canvas.cget("height")) - 15, anchor=tk.NW, text="Output", fill="gray")

    return window, resources, sorters

def purchase_sorter(sorter, resources):
    if sorter.purchase(resources):
        print(f"Purchased 1 {sorter.name}")

def game_loop(window, resources, sorters):
    last_time = time.time()
    money_production_rate = 0.0

    while True:
        current_time = time.time()
        delta_time = current_time - last_time
        last_time = current_time

        money_production_rate = sum(sorter.get_production_rate() for sorter in sorters.values()) * 0.01 # Example
        resources["money"].production_rate = money_production_rate
        resources["money"].produce(delta_time)

        for sorter in sorters.values():
            if sorter.count > 0 and not sorter.is_processing and random.random() < 0.02 * sorter.count: # Chance to start sorting
                sorter.start_processing()
            if sorter.is_processing:
                sorter.update_processing_animation()

        window.update()
        time.sleep(0.01)

def main():
    resources = {
        "money": Resource("Money", initial_amount=20.0)
    }

    sorters = {
        "Bubble Sorter": Sorter("Bubble Sorter", 10.0, 5, 3.0),
        "Insertion Sorter": Sorter("Insertion Sorter", 30.0, 8, 2.0),
        "Merge Sorter": Sorter("Merge Sorter", 75.0, 12, 1.5),
        "Quick Sorter": Sorter("Quick Sorter", 150.0, 15, 1.0)
    }

    window, game_resources, game_sorters = create_gui(resources, sorters)
    game_loop(window, game_resources, game_sorters)

if __name__ == "__main__":
    main()