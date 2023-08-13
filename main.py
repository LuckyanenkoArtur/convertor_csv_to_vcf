# import tkinter functionality
import tkinter as tk
from tkinter import filedialog
# import customization for the main tkinter
import customtkinter

# System settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    # Init default settings for App
    def __init__(self):
        super().__init__()

        self.geometry('590x400')
        self.title("Decoder CSV to VCF")
        self.resizable(width=False, height=False)

        title = customtkinter.CTkLabel(self, text="Корвертер CSV в VCF", font=('Helvetica',25), text_color='#1b91b5')
        title.grid(row=0, column=0, columnspan=2, padx=10, pady=20)

        # Create Input title with variable to keep select_csv_file_input
        self.csv_filename = tk.StringVar()
        # Create button and input field for select_csv_file
        select_csv_file_title = customtkinter.CTkLabel(self, text="Выбирите CSV файл который нужно конвертировать в VCF файл")
        select_csv_file_input = customtkinter.CTkEntry(self, width=350, height=25, textvariable=self.csv_filename)
        select_csv_file_button = customtkinter.CTkButton(self, text="Выбрать файл", command=self.on_file_select)
        # place on frame 
        select_csv_file_title.grid(row=1, column=0, pady=10,padx=10)
        select_csv_file_input.grid(row=2, column=0,padx=10, pady=10)
        select_csv_file_button.grid(row=2, column=1,padx=10, pady=10)

        # Create Input title with variable to keep select_directory_for_saving__file_vcf
        self.directory_vcf = tk.StringVar()
        # Create button and input field for select_csv_file
        select_directory_for_saving_vcf_file_title = customtkinter.CTkLabel(self, text="Выбирите папку, где сохранить VCF файл")
        select_directory_for_saving_vcf_file_input = customtkinter.CTkEntry(self, width=350, height=25, textvariable=self.directory_vcf)
        select_directory_for_saving_vcf_file_button = customtkinter.CTkButton(self, text="Выбрать папку", command=self.on_dir_select)
        # place on frame
        select_directory_for_saving_vcf_file_title.grid(row=3, column=0, pady=10,padx=10, sticky='w')
        select_directory_for_saving_vcf_file_input.grid(row=4, column=0,padx=10, pady=10)
        select_directory_for_saving_vcf_file_button.grid(row=4, column=1,padx=20, pady=10)

        convert_button = customtkinter.CTkButton(self, text="Convert", command=self.converting_logic, width=200)
        convert_button.grid(row=5, column=0, columnspan = 2 ,rowspan = 2, pady = 20)

    # Get Input from user what csv to convert
    def on_file_select(self):
        filename = filedialog.askopenfile(title='Выбирете csv файл',
                                          defaultextension='.csv',
                                          filetypes=[('Comma-Separated Values', '*.csv *.CSV')])
        if filename:
            self.csv_filename.set(filename.name)
    
    # Get Input from user where to save VCF file
    def on_dir_select (self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory_vcf.set(directory)
    
    # Logic of converting 
    def converting_logic(self):
        # import library for working with csv
        import csv
        import pathlib

        path_file = pathlib.Path(self.csv_filename.get())
        path_saving = pathlib.Path(self.directory_vcf.get())
        # filename = path.name # with extentsion path.stem ->> without extension
        
        # Open the CSV file
        with open(path_file, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)  # Create a DictReader object
            result = []  # List to store department values
            # Iterate over each row in the CSV file
            for row in reader:
                FullName = row['FullName']  # Extract value of 'department' column
                phone = row['PhoneNumber']
                result.append((FullName,phone))  # Add it to the list
            else:
                result_csv=set(result)
                with open (pathlib.Path('{}/{}.vcf'.format(path_saving,path_file.stem)), 'w', encoding='utf-8') as file:
                    for (name,phone) in result_csv: 
                        first_name, last_name, *c = [letter for letter in name.split(' ') if len(letter) > 0]
                        file.write("BEGIN:VCARD\nVERSION:3.0\nN;CHARSET=UTF-8:{first_name};{last_name};;;\nTITLE;CHARSET=UTF-8:\nORG;CHARSET=UTF-8:\nTEL;TYPE=WORK,VOICE:+7{phone}\nEMAIL;TYPE=WORK:\nURL;TYPE=WORK:\nADR;TYPE=WORK;CHARSET=UTF-8:;;;\nEND:VCARD\n".format(
                                    first_name = first_name, last_name = last_name, phone = phone))

if __name__ == "__main__":
    app = App()
    app.mainloop()