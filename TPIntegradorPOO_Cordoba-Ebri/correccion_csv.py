import csv

# Ruta del archivo CSV original y el nuevo archivo CSV
archivo_original = './TPIntegradorPOO_Cordoba-Ebri/observatorio-de-obras-urbanas.csv'
archivo_nuevo = './TPIntegradorPOO_Cordoba-Ebri/observatorio-de-obras-urbanas_correccion.csv'

def correccion_dataset():
    # Lee el archivo CSV original y crea un archivo CSV nuevo
    with open(archivo_original, 'r', encoding='utf-8') as file_in, open(archivo_nuevo, 'w', encoding='utf-8', newline='') as file_out:
        # Reemplaza las apariciones de """" por '
        file_content = file_in.read()
        file_content = file_content.replace('""""', "'")
        # Realiza el reemplazo de "" por "
        file_content = file_content.replace('""', '"')
        file_in.seek(0)


        reader = csv.reader(file_in)
        writer = csv.writer(file_out, quoting=csv.QUOTE_NONE, escapechar=' ')

        # Itera sobre cada línea del archivo CSV original
        for row in reader:
            modified_row = []
            inside_quotes = False
            temp_field = ''

            # Procesa cada campo de la línea
            for field in row:
                if field.startswith('"') and field.endswith('"'):
                    # Si el campo está entre comillas, se agrega sin modificar
                    modified_row.append(field)
                elif field.startswith('"'):
                    # Si el campo comienza con comillas, se almacena temporalmente
                    inside_quotes = True
                    temp_field += field[1:]
                elif field.endswith('"'):
                    # Si el campo termina con comillas, se agrega junto con el campo almacenado temporalmente
                    inside_quotes = False
                    temp_field += ' ' + field[:-1]
                    modified_row.append(temp_field.strip())
                    temp_field = ''
                elif inside_quotes:
                    # Si el campo está dentro de comillas, se agrega al campo almacenado temporalmente
                    temp_field += ' ' + field
                else:
                    # Si el campo no está entre comillas, se agrega sin modificar
                    modified_row.append(field)

            writer.writerow(modified_row)