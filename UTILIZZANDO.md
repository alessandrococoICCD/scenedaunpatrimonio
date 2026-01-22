# scenedaunpatrimonio
scripts per la gesione degli upload sulla piattaforma scenedaunpatrimonio
```markdown
# GPS Metadata Injector

Uno script Python per inserire automaticamente coordinate GPS dai file Excel nei metadati EXIF delle immagini.

## 📋 Descrizione

Questo script legge dati di georeferenziazione da un file Excel (.xlsx) e li inserisce automaticamente nei metadati EXIF delle immagini corrispondenti. Ideale per archivi fotografici, cataloghi museali, collezioni digitali.

## 🎯 Caso d'Uso

Hai una cartella con immagini e un file Excel che contiene:
- **Nomi dei file** (con o senza estensione)
- **Coordinate GPS** nel formato `latitudine, longitudine`
- Altri metadati (descrizione, data, luogo, ecc.)

Lo script associa automaticamente le coordinate alle immagini e le scrive nei metadati EXIF.

## 📁 Struttura dei Dati

### File Excel (.xlsx)
Deve contenere almeno queste colonne:
- **`nomefile`**: Nome del file (es. `AS_Sapienza_FototecaPACU_FotoGiacomelli_1935_CittàUniversitaria_Ingresso principale_042`)
- **`GEOREFERENZIAZIONE`**: Coordinate nel formato `41.90215844866925, 12.51206406897339`

**Esempio:**
```csv
nomefile,GEOREFERENZIAZIONE,DESCRIZIONE,DATA
AS_Sapienza_..._042,41.902158,12.512064,Descrizione...,1935
```

### Cartella Immagini
Contiene file come:
```
AS_Sapienza_FototecaPACU_FotoGiacomelli_1935_CittàUniversitaria_Ingresso principale_042.jpg
AS_Sapienza_Fototeca Cerimoniale_De Filippo_5.jpg
```

## 🚀 Installazione

### Prerequisiti
- Python 3.6 o superiore
- pip (gestore pacchetti Python)

### macOS
```bash
# Installa Python (se non presente)
brew install python

# Installa le dipendenze
pip3 install piexif pillow pandas openpyxl

# Verifica installazione
python3 --version
```

### Linux (Ubuntu/Debian)
```bash
# Installa Python e pip
sudo apt update
sudo apt install python3 python3-pip

# Installa le dipendenze
pip3 install piexif pillow pandas openpyxl

# Se ottieni errori di permessi, usa:
pip3 install --user piexif pillow pandas openpyxl
```

### Windows
```powershell
# 1. Scarica Python da python.org (assicurati di selezionare "Add Python to PATH")
# 2. Apri PowerShell come Amministratore

# Installa le dipendenze
pip install piexif pillow pandas openpyxl

# Se hai più versioni di Python:
py -3 -m pip install piexif pillow pandas openpyxl
```

### Verifica Installazione
```bash
python3 -c "import piexif, PIL, pandas; print('Tutte le dipendenze installate correttamente')"
```

## 📖 Utilizzo

### 1. Preparazione
1. Assicurati che il file Excel sia in formato `.xlsx`
2. Verifica i nomi delle colonne nel file Excel
3. Raccogli tutte le immagini in una cartella

### 2. Configurazione dello Script
Scarica lo script `gps_metadata.py` e modifica i percorsi:

```python
# Apri il file gps_metadata.py e cerca queste righe:
csv_path = "/percorso/al/tuo/file.xlsx"        # MODIFICA QUESTO
image_folder = "/percorso/alla/tua/cartella"   # MODIFICA QUESTO
```

### 3. Esecuzione

#### macOS/Linux
```bash
# Rendi lo script eseguibile
chmod +x gps_metadata.py

# Esegui
python3 gps_metadata.py
```

#### Windows
```powershell
# Metodo 1: Con Python
python gps_metadata.py

# Metodo 2: Con py launcher
py gps_metadata.py
```

### 4. Input Interattivo
Se preferisci, puoi usare la modalità interattiva (rimuovi il commento alle righe di input nello script):

```
=== SCRIPT PER AGGIUNGERE METADATI GPS ALLE IMMAGINI ===

Percorso del file Excel (.xlsx): /Users/tuo_nome/Downloads/metadati.xlsx
Percorso della cartella immagini: /Users/tuo_nome/Downloads/immagini

Procedere? (s/n): s
```

## 🔧 Configurazione Avanzata

### Percorsi Predefiniti
Modifica queste variabili nello script per uso ripetuto:

```python
# Configurazione percorsi (modifica questi valori)
EXCEL_PATH = "/path/to/your/metadata.xlsx"      # File Excel con i metadati
IMAGE_FOLDER = "/path/to/your/images"          # Cartella con le immagini
SUPPORTED_EXTS = ['.jpg', '.jpeg', '.png', '.tif', '.tiff']  # Estensioni supportate
```

### Formati Coordinate Supportati
Lo script riconosce questi formati:
- `41.902158, 12.512064`
- `41.90215844866925, 12.51206406897339`
- `-41.902158, -12.512064` (coordinate negative)
- `N41.902158, E12.512064`

## ✅ Verifica dei Risultati

### Terminale (macOS/Linux)
```bash
# Installa exiftool se non presente
brew install exiftool        # macOS
sudo apt install exiftool    # Ubuntu/Debian

# Verifica metadati
exiftool -GPSLatitude -GPSLongitude -GPSLatitudeRef -GPSLongitudeRef nomefile.jpg
```

### Windows PowerShell
```powershell
# Installa exiftool
# 1. Scarica da https://exiftool.org/
# 2. Estrai e aggiungi al PATH

# Verifica metadati
exiftool -GPS* nomefile.jpg
```

### Visualizzazione Grafica
- **macOS**: Preview → Strumenti → Mostra ispettore (⌘+I)
- **Windows**: Proprietà del file → Dettagli
- **Linux**: Geeqie, Shotwell, o altri visualizzatori con supporto EXIF

### Script di Verifica Incluso
```bash
# Esegui lo script di verifica
python3 verify_metadata.py nomefile.jpg
```

## 🐛 Risoluzione Problemi

### "ModuleNotFoundError: No module named 'pandas'"
**Soluzione:**
```bash
# Assicurati di usare il pip corretto
python3 -m pip install pandas

# O specifica la versione di Python
/usr/local/bin/python3 -m pip install pandas
```

### "File non trovato"
**Cause possibili:**
1. Percorsi errati
2. Nomi file non corrispondenti
3. Estensioni mancanti

**Soluzioni:**
```python
# Abilita debug nello script cercando e decommentando:
DEBUG = True  # Mostra ricerca file
```

### "Coordinate non valide"
**Controlla:**
1. Formato: deve essere `numero, numero`
2. Separatore: virgola, non punto e virgola
3. Tipo: devono essere numeri decimali validi

## 📊 Output e Log

Lo script genera un log dettagliato:
```
=== SCRIPT PER AGGIUNGERE METADATI GPS ALLE IMMAGINI ===

Leggendo file Excel... Trovate 150 righe
Colonne trovate: ['nomefile', 'GEOREFERENZIAZIONE', 'DESCRIZIONE', ...]

✓ GPS aggiunto: foto_001.jpg - Lat: 41.902158, Lon: 12.512064
✓ GPS aggiunto: foto_002.jpg - Lat: 44.497431, Lon: 11.353185
✗ foto_003.jpg: File non trovato
✗ foto_004.jpg: Coordinate non valide: [41.902158; 12.512064]

============================================================
RISULTATI:
============================================================
Righe totali nel file: 150
Immagini modificate con successo: 148
File non trovati: 1
Coordinate mancanti: 0
Errori: 1
============================================================
```

## 🔄 Utilizzo Avanzato

### Batch Processing
Crea uno script batch per processare più cartelle:

```bash
#!/bin/bash
# process_all.sh

for folder in /path/to/folders/*; do
    echo "Processando: $folder"
    python3 gps_metadata.py --excel "$folder/metadata.xlsx" --images "$folder"
done
```

### Includere Altri Metadati
Modifica lo script per includere più campi EXIF:

```python
# Aggiungi queste righe nella funzione add_gps_to_image()
exif_dict["0th"][piexif.ImageIFD.ImageDescription] = descrizione.encode('utf-8')
exif_dict["0th"][piexif.ImageIFD.DateTime] = data_scatto.encode('utf-8')
exif_dict["0th"][piexif.ImageIFD.Artist] = autore.encode('utf-8')
```

## ⚠️ Avvertenze Importanti

1. **Backup**: Sempre fare backup delle immagini originali
2. **Test**: Prova con alcune immagini prima di processare l'intera collezione
3. **Metadati Esistenti**: I dati GPS esistenti verranno sovrascritti
4. **Formati Supportati**: JPEG, PNG, TIFF (altri formati potrebbero non supportare EXIF)

## 📝 Esempio Completo

### Struttura del Progetto
```
progetto_fotografico/
├── gps_metadata.py          # Script principale
├── verify_metadata.py       # Script di verifica
├── metadati.xlsx           # File Excel con coordinate
└── immagini/               # Cartella immagini
    ├── foto_001.jpg
    ├── foto_002.jpg
    └── foto_003.jpg
```

### Comandi di Esempio
```bash
# 1. Configura percorsi
nano gps_metadata.py  # Modifica EXCEL_PATH e IMAGE_FOLDER

# 2. Esegui lo script
python3 gps_metadata.py

# 3. Verifica i risultati
python3 verify_metadata.py immagini/foto_001.jpg
exiftool immagini/foto_001.jpg | grep GPS
```

## 🤝 Contribuire

1. Fork del repository
2. Crea un branch: `git checkout -b feature/nuova-funzionalita`
3. Commit: `git commit -am 'Aggiungi nuova funzionalità'`
4. Push: `git push origin feature/nuova-funzionalita`
5. Crea una Pull Request

### Segnalazione Bug
Includi nelle issue:
1. Sistema Operativo e versione Python
2. Messaggio di errore completo
3. Esempio di file Excel e nome immagine
4. Output del comando `python --version`

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file [LICENSE](LICENSE) per i dettagli.

## 🙏 Ringraziamenti

- [piexif](https://github.com/hMatoba/piexif) per la gestione EXIF
- [Pillow](https://python-pillow.org/) per la manipolazione immagini
- [pandas](https://pandas.pydata.org/) per la lettura Excel

## 📞 Supporto

Per problemi o domande:
1. Controlla la sezione [Risoluzione Problemi](#-risoluzione-problemi)
2. Apri una [Issue](https://github.com/tuo-repo/issues)
3. Consulta il [Wiki](https://github.com/tuo-repo/wiki) per guide dettagliate

---

**Note**: Questo script è stato sviluppato per uso accademico e archivistico. Testare sempre su copie di backup prima dell'uso in produzione.
```
