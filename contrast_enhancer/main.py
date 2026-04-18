import tkinter as tk
from src.gui import ContrastEnhancerApp

def main():
    root = tk.Tk()
    app = ContrastEnhancerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
