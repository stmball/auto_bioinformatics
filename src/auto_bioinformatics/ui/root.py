"""Root UI for AutoBioinformatics"""

from pathlib import Path
from tkinter import *
from tkinter import filedialog

import pandas as pd

from auto_bioinformatics.analysis import AutoAnalysis
from auto_bioinformatics.reporting import Reporter


class AutoBioinformaticsUI:
    """Root UI for AutoBioinformatics"""

    def __init__(self, root):
        """Set up the UI"""

        self.group_names = StringVar()
        self.filepath = StringVar()
        self.output_path = StringVar()
        self.generate_report = BooleanVar()
        self.gene_col = StringVar()

        root.title("AutoBioinformatics")
        mainframe = Frame(root, padx=20, pady=20)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        Label(mainframe, text="Choose File:").grid(column=1, row=2, sticky=W)
        Label(
            mainframe,
            text="Please enter the unique group identifiers separated by commas (e.g.: Group 1,Group 2,Group 3)",
        ).grid(row=3, column=1, columnspan=3, sticky=W)
        Label(mainframe, text="Group Names:").grid(column=1, row=4, sticky=W)
        Label(mainframe, text="Gene Name Column:").grid(column=1, row=5, sticky=W)
        Label(mainframe, text="Output Path:").grid(column=1, row=6, sticky=W)
        Label(mainframe, text="Generate Report?").grid(column=1, row=7, sticky=W)

        self.filepath_display = Label(mainframe, text="")
        self.filepath_display.grid(column=2, row=2, sticky=(W, E))

        filepath_entry = Button(
            mainframe, text="Choose File", command=self.ask_for_filepath
        ).grid(column=3, row=2, sticky=E)

        group_names_entry = Entry(
            mainframe, width=40, textvariable=self.group_names
        ).grid(column=2, row=4, sticky=(W, E))

        gene_col_entry = Entry(mainframe, width=40, textvariable=self.gene_col).grid(
            column=2, row=5, sticky=(W, E)
        )

        self.output_path_display = Label(mainframe, text="")
        self.output_path_display.grid(column=2, row=6, sticky=(W, E))
        filepath_entry = Button(
            mainframe, text="Choose Output Folder", command=self.ask_for_output_path
        ).grid(column=3, row=6, sticky=E)

        generate_report_checkbox = Checkbutton(
            mainframe, variable=self.generate_report
        ).grid(column=2, row=7, sticky=(W, E))

        Button(mainframe, text="Run Analysis", command=self.run_analysis).grid(
            column=3, row=7, sticky=E
        )

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        root.bind("<Return>", self.run_analysis)

    def ask_for_filepath(self, *args):
        """Ask the user for the filepath of the data file"""

        self.filepath = filedialog.askopenfilename()
        self.filepath_display.config(
            text=self.filepath[:10] + "..." + self.filepath[-10:]
        )

    def ask_for_output_path(self, *args):
        """Ask the user for the output directory"""

        self.output_path = filedialog.askdirectory()
        self.output_path_display.config(
            text=self.output_path[:10] + "..." + self.output_path[-10:]
        )

    def run_analysis(self, *args):
        """Run the analysis using the given parameters"""

        img_dir = Path(self.output_path) / "img"
        output_dir = Path(self.output_path) / "out"

        cols = self.group_names.get().split(",")
        data = pd.read_excel(Path(self.filepath))
        gene_col = self.gene_col.get()

        analysis = AutoAnalysis(
            data, cols, gene_name_col=gene_col, plot_dir=img_dir, output_dir=output_dir
        )
        analysis.run()

        if self.generate_report:
            reporter = Reporter(analysis, self.output_path)
            reporter.generate_report()


def run_ui():
    """Helper function to run the UI"""

    root = Tk()
    AutoBioinformaticsUI(root)
    root.mainloop()
