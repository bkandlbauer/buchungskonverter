# Buchungskonverter

Converts weekly Lotto and Tipp3 settlement statements (XML) from the Austrian
Lotterien into accounting booking records (CSV, `;`-delimited, German
decimal format) ready for import into bookkeeping software.

The project ships in three forms:

- **Standalone Python scripts** (`convert_lotto.py`, `convert_tipp3.py`) that
  read a local XML file and write a CSV file.
- **A Firebase Cloud Function** (`functions/`) exposing the same conversion
  logic over HTTP.
- **A small web app** (`public/`) that lets a user drag & drop an XML file
  and download the converted CSV, backed by the Cloud Function.
- **Windows `.exe` builds** (`exe-dateien/`, built via PyInstaller) for users
  who prefer a double-click tool without installing Python.

## How it works

Each script parses an XML settlement file and, for every relevant XML
element (sales, commission, payouts, fees, taxes, ...), emits one booking
row with account, counter-account, amount, tax, VAT code and a German
text/description — mapped according to the fixed chart-of-accounts rules
defined in the script.

- `convert_lotto.py` reads `abrechnung_lotto.xml` and writes
  `Buchungen Lotto [<invoiceDate>].csv`, covering `drawGame`, `instantGame`,
  `eurobon` and `otherTaxableItem` sections.
- `convert_tipp3.py` reads `abrechnung_tipp3.xml` and writes
  `Buchungen Tipp3 [<invoiceDate>].csv`, covering the `drawGame` section.

Sample input files (`abrechnung_lotto.xml`, `abrechnung_tipp3.xml`) and the
corresponding source PDF statements are included in the repository root for
reference/testing.

## Running the scripts locally

Requires Python 3 (standard library only, no dependencies needed):

```bash
python3 convert_lotto.py    # reads ./abrechnung_lotto.xml
python3 convert_tipp3.py    # reads ./abrechnung_tipp3.xml
```

The resulting CSV is written to the current working directory.

## Web app / Cloud Function

`functions/` contains a Firebase Cloud Function (Python) that wraps the same
conversion logic in a Flask app with two endpoints:

- `POST /lotto` — body: raw Lotto XML, content-type `application/xml`
- `POST /tipp3` — body: raw Tipp3 XML, content-type `application/xml`

Both return the converted CSV as the response body.

Install dependencies and deploy with the Firebase CLI:

```bash
cd functions
pip install -r requirements.txt
cd ..
firebase deploy
```

`public/` is a static frontend (`index.html`, `script.js`, `style.css`)
that lets a user drop an XML file onto the page and downloads the CSV
returned by the Cloud Function. It's served via Firebase Hosting from the
same `firebase.json` config. Sample requests against the deployed function
can be found in `test.http`.

## Building the Windows executables

The `.exe` files are built with [PyInstaller](https://pyinstaller.org/)
using the provided spec file, e.g.:

```bash
pyinstaller convert_lotto.spec
```

The resulting binary is placed in `dist/`.
