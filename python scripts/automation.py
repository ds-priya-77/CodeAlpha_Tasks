import pandas as pd
import logging
import os
import shutil
import datetime

# Configure logging
logging.basicConfig(
    filename="automation.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class DataAutomation:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.processed_folder = os.path.join(input_folder, "Processed_Files")
        self.cleaned_folder = os.path.join(output_folder, "Cleaned_Files")
        self.archive_folder = os.path.join(input_folder, "Archived_Files")
        
        # Create necessary folders if not exist
        os.makedirs(self.processed_folder, exist_ok=True)
        os.makedirs(self.cleaned_folder, exist_ok=True)
        os.makedirs(self.archive_folder, exist_ok=True)

    def clean_data(self, file_name):
        """Cleans an Excel or CSV file and saves it to the cleaned folder."""
        try:
            file_path = os.path.join(self.input_folder, file_name)
            file_ext = os.path.splitext(file_name)[1].lower()

            if file_ext == ".csv":
                df = pd.read_csv(file_path)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file_path, engine="openpyxl")
            else:
                logging.warning(f"Skipping unsupported file: {file_name}")
                return
            
            # Clean data
            df.drop_duplicates(inplace=True)
            '''df.fillna("Unknown", inplace=True)'''
            df = df.apply(lambda col: col.fillna(col.mean()) if col.dtype in ["float64", "int64"] else col.fillna("Unknown"))

            df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

            # Save cleaned file
            cleaned_path = os.path.join(self.cleaned_folder, file_name)
            if file_ext == ".csv":
                df.to_csv(cleaned_path, index=False)
            elif file_ext == ".xlsx":
                df.to_excel(cleaned_path, index=False, engine="openpyxl")

            logging.info(f"Cleaned file saved: {cleaned_path}")

            # Move original file to processed folder
            shutil.move(file_path, os.path.join(self.processed_folder, file_name))
            logging.info(f"Moved original file to: {self.processed_folder}")

        except Exception as e:
            logging.error(f"Error processing {file_name}: {e}")

    def archive_old_files(self):
        """Archives old processed files into a ZIP."""
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_name = os.path.join(self.archive_folder, f"archive_{timestamp}.zip")

            shutil.make_archive(archive_name.replace(".zip", ""), 'zip', self.processed_folder)
            logging.info(f"Archived processed files to: {archive_name}")

            # Delete old processed files after archiving
            for file in os.listdir(self.processed_folder):
                os.remove(os.path.join(self.processed_folder, file))

        except Exception as e:
            logging.error(f"Error archiving files: {e}")

    def run_automation(self):
        """Runs the full automation process."""
        for file in os.listdir(self.input_folder):
            if file.endswith(".csv") or file.endswith(".xlsx"):
                self.clean_data(file)
        
        self.archive_old_files()
        logging.info("Automation completed successfully.")
        print(" Automation completed successfully!")

# Example usage
if __name__ == "__main__":
    input_folder = "input_files"  # Change this to your actual input folder
    output_folder = "output_files"

    automation = DataAutomation(input_folder, output_folder)
    automation.run_automation()
