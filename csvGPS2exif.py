#PER LE ISTRUZIONI LEGGI UTILIZZANDO.md
#!/usr/bin/env python3
import os
import sys
import csv
from pathlib import Path
import piexif
from PIL import Image

def parse_coordinates(coord_str):
    """Analizza la stringa di coordinate (lat, lon)"""
    try:
        # Pulisci la stringa
        coord_str = coord_str.strip()
        coord_str = coord_str.replace('[', '').replace(']', '').replace('"', '')
        
        # Dividi latitudine e longitudine
        parts = [p.strip() for p in coord_str.split(',')]
        if len(parts) >= 2:
            lat = float(parts[0])
            lon = float(parts[1])
            return lat, lon
        return None
    except Exception as e:
        print(f"Errore parsing coordinate '{coord_str}': {e}")
        return None

def decimal_to_dms(decimal):
    """Converti coordinate decimali in gradi, minuti, secondi"""
    degrees = int(abs(decimal))
    minutes = int((abs(decimal) - degrees) * 60)
    seconds = (abs(decimal) - degrees - minutes/60) * 3600
    return (degrees, 1), (minutes, 1), (int(seconds * 100), 100)

def add_gps_to_image(image_path, lat, lon):
    """Aggiunge dati GPS ai metadati EXIF dell'immagine"""
    try:
        # Apri l'immagine per verificare che esista
        img = Image.open(image_path)
        
        # Carica gli EXIF esistenti o crea nuovo dizionario
        try:
            exif_dict = piexif.load(image_path)
        except:
            exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}}
        
        # Converti coordinate in formato EXIF
        lat_dms = decimal_to_dms(abs(lat))
        lon_dms = decimal_to_dms(abs(lon))
        
        # Prepara dati GPS
        gps_ifd = {
            piexif.GPSIFD.GPSLatitudeRef: b'N' if lat >= 0 else b'S',
            piexif.GPSIFD.GPSLatitude: lat_dms,
            piexif.GPSIFD.GPSLongitudeRef: b'E' if lon >= 0 else b'W',
            piexif.GPSIFD.GPSLongitude: lon_dms,
            piexif.GPSIFD.GPSVersionID: (2, 3, 0, 0)
        }
        
        # Aggiungi i dati GPS al dizionario EXIF
        exif_dict["GPS"] = gps_ifd
        
        # Converti in byte EXIF
        exif_bytes = piexif.dump(exif_dict)
        
        # Salva l'immagine con i nuovi EXIF
        img.save(image_path, exif=exif_bytes, quality=95)
        
        print(f"✓ GPS aggiunto: {os.path.basename(image_path)} - Lat: {lat}, Lon: {lon}")
        return True
        
    except Exception as e:
        print(f"✗ Errore con {os.path.basename(image_path)}: {e}")
        return False

def find_image_file(base_name, image_folder):
    """Trova il file immagine corrispondente al nome base"""
    # Possibili estensioni
    extensions = ['.jpg', '.jpeg', '.JPG', '.JPEG', '.png', '.PNG', '.tif', '.tiff']
    
    # Cerca prima il nome esatto (potrebbe già includere l'estensione)
    if os.path.exists(os.path.join(image_folder, base_name)):
        return os.path.join(image_folder, base_name)
    
    # Cerca con estensioni
    for ext in extensions:
        full_path = os.path.join(image_folder, base_name + ext)
        if os.path.exists(full_path):
            return full_path
    
    # Cerca anche se il nome base ha già un'estensione ma è diversa
    path_obj = Path(base_name)
    if path_obj.suffix:
        # Il nome base ha già un'estensione
        for ext in extensions:
            # Prova sia con l'estensione originale che con altre
            base_without_ext = path_obj.stem
            full_path = os.path.join(image_folder, base_without_ext + ext)
            if os.path.exists(full_path):
                return full_path
    
    return None

def process_csv_file(csv_path, image_folder):
    """Processa il file CSV e aggiorna le immagini"""
    if not os.path.exists(csv_path):
        print(f"Errore: File CSV non trovato: {csv_path}")
        return
    
    if not os.path.exists(image_folder):
        print(f"Errore: Cartella immagini non trovata: {image_folder}")
        return
    
    # Leggi il CSV
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        # Sniffa il delimiter
        sample = f.read(1024)
        f.seek(0)
        
        sniffer = csv.Sniffer()
        delimiter = sniffer.sniff(sample).delimiter
        
        # Leggi il CSV
        reader = csv.DictReader(f, delimiter=delimiter)
        
        # Pulisci i nomi delle colonne
        reader.fieldnames = [name.strip() for name in reader.fieldnames]
        
        print(f"Colonne trovate: {reader.fieldnames}")
        
        # Contatori
        total = 0
        processed = 0
        not_found = 0
        errors = 0
        
        for row in reader:
            total += 1
            
            # Estrai dati
            filename = row.get('nomefile', '').strip()
            georef = row.get('GEOREFERENZIAZIONE', '').strip()
            
            if not filename:
                print(f"  Riga {total}: Nome file vuoto")
                errors += 1
                continue
            
            if not georef:
                print(f"  {filename}: Nessuna coordinata")
                errors += 1
                continue
            
            # Trova il file immagine
            image_path = find_image_file(filename, image_folder)
            
            if not image_path:
                print(f"  {filename}: File non trovato")
                not_found += 1
                continue
            
            # Analizza le coordinate
            coords = parse_coordinates(georef)
            if not coords:
                print(f"  {filename}: Coordinate non valide: {georef}")
                errors += 1
                continue
            
            lat, lon = coords
            
            # Aggiungi GPS all'immagine
            if add_gps_to_image(image_path, lat, lon):
                processed += 1
            else:
                errors += 1
        
        # Risultati
        print(f"\n{'='*60}")
        print("RISULTATI:")
        print(f"{'='*60}")
        print(f"Righe totali nel CSV: {total}")
        print(f"Immagini modificate con successo: {processed}")
        print(f"File non trovati: {not_found}")
        print(f"Errori: {errors}")
        print(f"{'='*60}")

def main():
    print("=== SCRIPT PER AGGIUNGERE METADATI GPS ALLE IMMAGINI ===")
    print()
    
    # Chiedi i percorsi (modifica qui per hardcodare i percorsi)
    #csv_path = input("Percorso del file CSV/TSV: ").strip().strip('"')
    #image_folder = input("Percorso della cartella immagini: ").strip().strip('"')
    
    # Per hardcodare i percorsi, decommenta e modifica queste righe:
    csv_path = "/Users/labfoto/Downloads/ICCD_scenedaunpatrimonio_DATA-ENTRY.csv"
    image_folder = "/Users/labfoto/Downloads/JPG"
    
    print()
    print(f"File CSV: {csv_path}")
    print(f"Cartella immagini: {image_folder}")
    print()
    
    # Conferma
    confirm = input("Procedere? (s/n): ").strip().lower()
    if confirm != 's':
        print("Operazione annullata.")
        return
    
    # Processa i file
    process_csv_file(csv_path, image_folder)

if __name__ == "__main__":
    # Verifica le dipendenze
    try:
        import piexif
        from PIL import Image
    except ImportError as e:
        print("Dipendenze mancanti. Installa con:")
        print("python3 -m pip install --user piexif pillow")
        sys.exit(1)
    
    main()
