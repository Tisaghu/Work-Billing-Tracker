
# Work Billing Tracker

A professional, extensible tool for tracking your work billing hours, designed for a modern PyQt5 desktop GUI. Built in Python, this project helps you log, analyze, and visualize your daily, weekly, and monthly work time, making it easy to meet your goals and generate reports for employers or personal productivity.

## Features

- **Modern GUI:** Use a clean, intuitive PyQt5 desktop app with calendar-based date selection.
- **Flexible Time Entry:** Add multiple time chunks per day using a dialog interface.
- **Calendar View:** Select dates easily in the GUI with a calendar widget.
- **Stats Panel:** See billed minutes/hours and goal progress for today, week, and month.
- **CSV Storage:** All data is saved in a portable CSV file for easy backup and analysis.
- **Modular Codebase:** Clean separation of models, storage, calculations, and UI components.
- **Extensible:** Easy to add new features, such as PTO/holiday tracking, custom goals, or export formats.

## Getting Started

### Requirements
- Python 3.7+
- PyQt5 (`pip install pyqt5`)


### Running the App
Navigate to the main project directory in terminal then:
1. Install dependencies:
   ```sh
   pip install pyqt5
   ```
2. Run the app:
   ```sh
   python main.py
   ```


### Packaging as an EXE (Windows)
Navigate to the main project directory in terminal then:
1. Install PyInstaller:
   ```sh
   pip install pyinstaller
   ```
2. Build:
   ```sh
   pyinstaller --onefile --windowed --name Work_Billing_Tracker src/Main.py
   ```
   The executable will be in the `dist` folder.


## File Structure

```
Work-Billing-Tracker/
├── Main.py                # Main GUI entry point
├── models.py              # WorkChunk and Day data models
├── storage.py             # CSV read/write logic
├── calculations.py        # Business logic (totals, date ranges)
├── stats_panel.py         # StatsPanel widget for GUI
├── add_time_dialog.py     # AddTimeDialog widget for GUI
├── work_chunks.csv        # Your time log data
├── README.md              # Project documentation
```


## Contributing
Pull requests and suggestions are welcome! Please open an issue for feature requests or bug reports.

## License
MIT License (see LICENSE file)

## Author
Created by Tisaghu 

