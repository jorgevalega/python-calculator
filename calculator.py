"""
CustomTkinter Python Calculator

A fully-featured calculator application with:
- Basic arithmetic operations
- Memory operations
- Calculation history
- Keyboard support
- Light/dark mode

Author: Jorge Valega
Date: 4th April 2025
"""

import tkinter as tk
import customtkinter as ctk
from typing import Optional, Union, List
import math

# ======================
#  APPEARANCE SETTINGS
# ======================
ctk.set_appearance_mode("System")  # Follows system theme
ctk.set_default_color_theme("blue")  # Primary color theme

# ======================
#  CALCULATOR LOGIC CLASS
# ======================
class Calculator:
    """
    Handles all calculator operations and state management.
    
    Attributes:
        current_input (str): Current displayed value
        previous_input (str): First operand in calculations
        operation (str): Current active operation (+, -, etc.)
        memory (float): Stored memory value
        history (List[str]): Calculation history log
        last_operation (str): Formatted string of last operation
    """
    
    def __init__(self):
        """Initialize calculator with default values"""
        self.current_input: str = "0"
        self.previous_input: str = ""
        self.operation: Optional[str] = None
        self.memory: float = 0.0
        self.history: List[str] = []
        self.last_operation: str = ""

    def add_to_input(self, value: str) -> None:
        """
        Add a digit or decimal to current input.
        
        Args:
            value: Digit (0-9) or decimal point to add
        """
        if value == "." and "." in self.current_input:
            return  # Prevent multiple decimals
        if self.current_input == "0" and value != ".":
            self.current_input = value
        else:
            self.current_input += value

    def set_operation(self, op: str) -> None:
        """
        Set the operation for calculation.
        
        Args:
            op: Operation symbol (+, -, *, /, etc.)
        """
        if self.current_input:
            if self.operation and self.previous_input:
                self.calculate()
            self.previous_input = self.current_input
            self.current_input = ""
            self.operation = op
            self.last_operation = f"{self.previous_input} {self.operation}"

    def calculate(self) -> Union[float, str]:
        """
        Perform the calculation based on current operation.
        
        Returns:
            Result of calculation or error message
        """
        if not self.operation or not self.previous_input:
            return self.current_input or "0"

        try:
            num1 = float(self.previous_input)
            num2 = float(self.current_input) if self.current_input else num1

            # Perform the calculation
            if self.operation == "+":
                result = num1 + num2
            elif self.operation == "-":
                result = num1 - num2
            elif self.operation == "*":
                result = num1 * num2
            elif self.operation == "/":
                result = num1 / num2 if num2 != 0 else "Error: Div/0"
            elif self.operation == "^":
                result = num1 ** num2
            elif self.operation == "√":
                result = math.sqrt(num1)
            else:
                return "Error"

            # Format result to remove .0 when not needed
            if isinstance(result, float):
                result = int(result) if result.is_integer() else result

            # Update history
            operation_str = f"{self.previous_input} {self.operation} {self.current_input if self.current_input else ''}"
            self.history.append(f"{operation_str} = {result}")
            if len(self.history) > 10:
                self.history.pop(0)

            self.current_input = str(result)
            self.operation = None
            self.last_operation = ""
            return result

        except ZeroDivisionError:
            self.clear_all()
            return "Error: Div/0"
        except Exception:
            self.clear_all()
            return "Error"

    def clear_entry(self) -> None:
        """Clear current input while keeping operation history"""
        self.current_input = "0"
        if self.operation and not self.current_input:
            self.operation = None
            self.last_operation = ""

    def clear_all(self) -> None:
        """Reset calculator to initial state (clear everything)"""
        self.current_input = "0"
        self.previous_input = ""
        self.operation = None
        self.last_operation = ""
        self.history.clear()

    def memory_add(self) -> None:
        """Add current value to memory storage"""
        try:
            self.memory += float(self.current_input)
        except ValueError:
            pass

    def memory_subtract(self) -> None:
        """Subtract current value from memory storage"""
        try:
            self.memory -= float(self.current_input)
        except ValueError:
            pass

    def memory_recall(self) -> None:
        """Recall value from memory to current input"""
        self.current_input = str(self.memory)

    def memory_clear(self) -> None:
        """Clear memory storage"""
        self.memory = 0.0

    def percentage(self) -> None:
        """Calculate percentage of current value"""
        try:
            self.current_input = str(float(self.current_input) / 100)
        except ValueError:
            pass

    def toggle_sign(self) -> None:
        """Toggle positive/negative sign of current value"""
        if self.current_input.startswith("-"):
            self.current_input = self.current_input[1:]
        else:
            self.current_input = "-" + self.current_input

# ======================
#  GUI APPLICATION CLASS
# ======================
class CalculatorApp(ctk.CTk):
    """
    Main application window for the calculator.
    
    Attributes:
        calculator: Instance of Calculator class
        display_frame: Frame containing display labels
        button_frame: Frame containing all buttons
        display_label: Main display for current input
        history_label: Secondary display for operations
    """
    
    def __init__(self):
        """Initialize the application window"""
        super().__init__()
        
        # Window configuration
        self.title("Scientific Calculator")
        self.geometry("400x650")
        self.resizable(False, False)
        
        # Calculator logic instance
        self.calculator = Calculator()
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=4)
        
        # Create UI components
        self.display_frame = self._create_display_frame()
        self.display_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.button_frame = self._create_button_frame()
        self.button_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        # Keyboard bindings
        self.bind("<Key>", self._on_key_press)

    def _create_display_frame(self) -> ctk.CTkFrame:
        """
        Create the display area with history and main display.
        
        Returns:
            Configured CTkFrame containing display labels
        """
        frame = ctk.CTkFrame(self, corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        
        # History display (smaller, top-aligned)
        self.history_label = ctk.CTkLabel(
            frame,
            text="",
            anchor="e",
            font=("Arial", 14),
            text_color=("gray50", "gray70")  # Lighter color for history
        )
        self.history_label.grid(row=0, column=0, sticky="e", padx=20, pady=(10, 0))
        
        # Main display
        self.display_label = ctk.CTkLabel(
            frame,
            text="0",
            anchor="e",
            font=("Arial", 40),
            wraplength=350  # Allow text wrapping for long numbers
        )
        self.display_label.grid(row=1, column=0, sticky="e", padx=20, pady=(0, 10))
        
        return frame

    def _create_button_frame(self) -> ctk.CTkFrame:
        """
        Create the button grid with reorganized layout (memory buttons on top).
        
        Returns:
            Configured CTkFrame containing all calculator buttons
        """
        frame = ctk.CTkFrame(self, corner_radius=10)
        
        # Configure grid (4 columns, 6 rows)
        for i in range(4):
            frame.grid_columnconfigure(i, weight=1)
        for i in range(6):
            frame.grid_rowconfigure(i, weight=1)
        
        # Button layout configuration
        # Reorganized with memory buttons at top row
        buttons = [
            # Row 0: Memory functions
            ("MC", 0, 0), ("MR", 0, 1), ("M-", 0, 2), ("M+", 0, 3),
            # Row 1: Clear and advanced functions
            ("C", 1, 0), ("√", 1, 1), ("^", 1, 2), ("/", 1, 3),
            # Row 2: Numbers 7-9 and multiply
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("*", 2, 3),
            # Row 3: Numbers 4-6 and subtract
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("-", 3, 3),
            # Row 4: Numbers 1-3 and add
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("+", 4, 3),
            # Row 5: Special functions and equals
            ("AC", 5, 0), ("0", 5, 1), (".", 5, 2), ("=", 5, 3),
        ]
        
        # Create and place buttons
        for (text, row, col) in buttons:
            button = ctk.CTkButton(
                frame,
                text=text,
                command=lambda t=text: self._on_button_click(t),
                font=("Arial", 20),
                height=50,
                corner_radius=10
            )
            button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        return frame

    def _update_display(self) -> None:
        """Update both display labels based on calculator state"""
        # Format main display (remove trailing .0 if needed)
        display_text = self.calculator.current_input
        if "." in display_text:
            display_text = display_text.rstrip("0").rstrip(".")
        self.display_label.configure(text=display_text)
        
        # Update history display
        if self.calculator.last_operation:
            # Show current operation (e.g., "25 +")
            history_text = self.calculator.last_operation
        elif self.calculator.history:
            # Show last complete operation without result
            history_text = self.calculator.history[-1].split("=")[0].strip()
        else:
            history_text = ""
        self.history_label.configure(text=history_text)

    def _on_button_click(self, button_text: str) -> None:
        """
        Handle button click events.
        
        Args:
            button_text: Text label of the clicked button
        """
        if button_text == "AC":
            self.calculator.clear_all()
        elif button_text == "C":
            self.calculator.clear_entry()
        elif button_text.isdigit() or button_text == ".":
            self.calculator.add_to_input(button_text)
        elif button_text in "+-*/^√":
            self.calculator.set_operation(button_text)
        elif button_text == "=":
            self.calculator.calculate()
        elif button_text == "±":
            self.calculator.toggle_sign()
        elif button_text == "%":
            self.calculator.percentage()
        elif button_text == "MC":
            self.calculator.memory_clear()
        elif button_text == "M+":
            self.calculator.memory_add()
        elif button_text == "M-":
            self.calculator.memory_subtract()
        elif button_text == "MR":
            self.calculator.memory_recall()
        
        self._update_display()

    def _on_key_press(self, event: tk.Event) -> None:
        """
        Handle keyboard input events.
        
        Args:
            event: Tkinter key event object
        """
        key_mapping = {
            '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
            '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
            '.': '.', '+': '+', '-': '-', '*': '*', '/': '/',
            '=': '=', '\r': '=', '\x08': 'C', '%': '%',
            '^': '^', 'q': '√', 'Q': '√',
            'c': 'C', 'a': 'AC', 'm': 'M+', 'r': 'MR'
        }
        
        if event.char in key_mapping:
            self._on_button_click(key_mapping[event.char])

# ======================
#  APPLICATION ENTRY POINT
# ======================
if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
