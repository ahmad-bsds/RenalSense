import json



def read_json_file(file_path):
  """Reads a JSON file and returns its contents as a Python object.

  Args:
    file_path: The path to the JSON file.

  Returns:
    The contents of the JSON file as a Python object (typically a dictionary or list).
  """

  with open(file_path, 'r') as f:
    data = json.load(f)
  return data

processed_data = []



def process_data(file: str= "./data.json"):
    """Function will load data and process this data to store in a list. List will be stored in
        the vector database.
    """
    # Loading data.
    metadata = read_json_file(file_path="../Data/response.json")

    # Iterating on data.
    embeddings = [13,4,4,55,6,5,66,564]
    # insert processed data in the list.
    processed_data.append(
        {
            "values": embeddings,
            "id": "",
            "metadata": metadata
        }
    )


process_data()
print(processed_data)