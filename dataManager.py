import json

class DataManager:
    
    def __init__(self, filePath: str):
        """
        Initialize the filePath
        """
        self.filePath: str = filePath

    def loadData(self, errorAdv = "data"):
        """
        Load self.data from filePath as a JSON
        """
        try:
            with open(self.filePath, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error loading {errorAdv}: File not found at {self.filePath}")
        except json.JSONDecodeError as e:
            print(f"Error loading {errorAdv} : decoding JSON in file {self.filePath}: {e}")
        except Exception as e:
            print(f"Error loading {errorAdv} : an unexpected error occurred: {e}")


    def writeData(self, data, errorAdv = "data"):
        """
        Save self.data in filePath as a JSON
        """
        try:
            with open(self.filePath, 'w') as file:
                json.dump(data, file)
        except FileNotFoundError:
            print(f"Error updating {errorAdv}: File not found at {self.filePath}")
        except TypeError as e:
            print(f"Error updating {errorAdv} : encoding JSON to file {self.filePath}: {e}")
        except Exception as e:
            print(f"Error updating {errorAdv} : an unexpected error occurred: {e}")