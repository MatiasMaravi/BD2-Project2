import json
import os

def split_json(input_file, output_directory, max_records_per_file):
    with open(input_file, 'r') as source_file:
        output_file = None
        record_count = 0
        batch_count = 0
        records = []

        for line in source_file:
            data = json.loads(line)
            records.append(data)
            record_count += 1

            if record_count >= max_records_per_file:
                if output_file:
                    output_file.close()

                batch_count += 1
                output_filename = os.path.join(output_directory, f'batch_{batch_count}.json')
                output_file = open(output_filename, 'w')
                json.dump(records, output_file)
                records = []
                record_count = 0

        if records:
            if output_file:
                output_file.close()

            batch_count += 1
            output_filename = os.path.join(output_directory, f'batch_{batch_count}.json')
            with open(output_filename, 'w') as output_file:
                json.dump(records, output_file)

# Directorio de entrada (archivo JSON grande)
input_file = 'large_data.json'

# Directorio de salida (donde se guardarán los archivos JSON divididos)
output_directory = 'output_batches'

# Máximo número de registros por archivo
max_records_per_file = 1000  # Ajusta según tus necesidades

# Asegúrate de que el directorio de salida exista
os.makedirs(output_directory, exist_ok=True)

# Divide el archivo JSON en lotes más pequeños sin cargarlo por completo en memoria
split_json(input_file, output_directory, max_records_per_file)
