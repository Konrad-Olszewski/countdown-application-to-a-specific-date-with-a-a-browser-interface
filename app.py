# Import potrzebnych bibliotek
from flask import Flask, render_template, request, redirect, jsonify, url_for
import datetime

# Tworzenie instancji aplikacji Flask
app = Flask(__name__)

# Inicjalizacja zmiennej globalnej przechowującej docelową datę
docelowa_data = None
# Inicjalizacja zmiennej globalnej przechowującej dodatkowy tekst  
dodatkowy_tekst = None  

# Funkcja pobierająca datę z fomularza i ustawiająca jej format
@app.route('/', methods=['GET', 'POST'])
def czas():
    global docelowa_data
    global dodatkowy_tekst

    # Domyślny format daty
    format_daty = "%Y-%m-%d %H:%M:%S"  

    if request.method == 'POST':
        # Sprawdzenie czy został wybrany plik z datą 
        if 'plik_z_datą' in request.files:
            plik = request.files['plik_z_datą']
            if plik.filename != '':
                try:
                    data = datetime.datetime.strptime(plik.read().decode('utf-8').strip(), "%Y-%m-%d %H:%M:%S")
                    docelowa_data = data
                    dodatkowy_tekst = 'Data z pliku'
                except ValueError:
                    return render_template('formularz.html', blad="Błąd w formacie pliku.")
            # Przypadek braku pliku z dtaą, pobranie danych z formularza
            else:
                rok = int(request.form['rok'])
                miesiac = int(request.form['miesiac'])
                dzien = int(request.form['dzien'])
                godzina = int(request.form['godzina'])
                minuta = int(request.form['minuta'])
                sekunda = int(request.form['sekunda'])
                docelowa_data = datetime.datetime(rok, miesiac, dzien, godzina, minuta, sekunda)
                dodatkowy_tekst = request.form.get('dodatkowy_tekst', '')
                format_daty = request.form.get('format', "%Y-%m-%d")  # Pobierz wybrany format daty
        
        # Sprawdzenie jaki format daty został wybrany
        if format_daty == "YYYY-MM-DD":
            # Ustawienie formatu "YYYY-MM-DD"
            format_daty = "%Y-%m-%d %H:%M:%S"
        elif format_daty == "DD/MM/YYYY":
            # Ustawienie formatu "DD/MM/YYYY"
            format_daty = "%d/%m/%Y %H:%M:%S"
        elif format_daty == "MM/DD/YYYY":
            # Ustawienie formatu "MM/DD/YYYY"
            format_daty = "%m/%d/%Y %H:%M:%S"
       
    # Renderowanie strony w zależności od istnienia docelowej daty
    if docelowa_data is None:
        return render_template('formularz.html', format_daty=format_daty)
    else:
        return render_template('czas.html', docelowa_data=docelowa_data, dodatkowy_tekst=dodatkowy_tekst, format_daty=format_daty)

# Funkcja obliczająca czas do danej daty
@app.route('/aktualny_czas')
def aktualny_czas():
    # Sprawdzenie czy data jest wprowadzona
    if docelowa_data is None:
        return jsonify({"czas": "Koniec"})

    # Wprowadzenie aktualnego czasu
    aktualny_czas = datetime.datetime.now()
    # Obliczenie różnicy
    czas_do_docelowej_daty = docelowa_data - aktualny_czas

    # Sprawdzenie czy data docelowa juzż minęła
    if czas_do_docelowej_daty.total_seconds() <= 0:
        return jsonify({"czas": "Koniec"})

    # Obliczenia czasu pozostałego do docelowej daty w różnych jednostkach
    days = czas_do_docelowej_daty.days
    seconds = czas_do_docelowej_daty.seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_time = f"{days} dni {int(hours):02d} godzin {int(minutes):02d} minut {int(seconds):02d} sekund"

    return jsonify({"czas": formatted_time})

# Funkcja powodująca powrót do formularza
@app.route('/powrot_do_formularza', methods=['GET'])
def powrot_do_formularza():
    return render_template('formularz.html')

# Funkcja ustawiająca datę docelową jako Wakacje 2024
@app.route('/ustaw_wakacje', methods=['GET'])
def ustaw_wakacje():
    global docelowa_data
    global dodatkowy_tekst
    # Ustawienie docelowej daty na datę wakacji
    docelowa_data = datetime.datetime(2024, 6, 21, 0, 0, 1)
    dodatkowy_tekst = 'Wakacje 2024'
    return redirect(url_for('czas'))

# Funkcja ustawiająca datę docelową jako Święta Bożego Narodzenia
@app.route('/BN', methods=['GET'])
def BN():
    global docelowa_data
    global dodatkowy_tekst
    # Ustawienie docelowej daty na datę Świąt Bożego Narodzenia
    docelowa_data = datetime.datetime(2023, 12, 25, 0, 0, 1)
    dodatkowy_tekst = 'Święta Bożego Narodzenia 2023'
    return redirect(url_for('czas'))

# Funkcja ustawiająca datę docelową jako Święta Wielkanocne
@app.route('/WN', methods=['GET'])
def WN():
    global docelowa_data
    global dodatkowy_tekst
    # Ustawienie docelowej daty na datę Świąt Wielkanocnych
    docelowa_data = datetime.datetime(2024, 3, 31, 0, 0, 1)
    dodatkowy_tekst = 'Święta Wielkanocne 2024'
    return redirect(url_for('czas'))

# Uruchomienie aplikacji
if __name__ == '__main__':
    app.run(debug=True)