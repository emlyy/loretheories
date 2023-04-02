# Tietokantasovellus
## Lore Theories

Lore Theories on sovellus, jossa voi jakaa teorioita kaikista mediatyypeistä, kuten videopeleistä, elokuvista ja kirjoista. Käyttäjä voi julkaista teorian, jonka muut käyttäjät voivat lukea ja kommentoida.

Sovelluksen ominaisuuksia:
- käyttäjä voi luoda uuden tunnuksen, kirjautua sisään ja ulos
- käyttäjä voi lisätä uuden teorian antamalla otsikon, tekstin ja categoria-tägit
- käyttäjä voi lukea muiden teoriota, kommentoida ja antaa tähden
- käyttäjä näkee etusivulla kaikkien teorioiden top 5 -listan (tähtien määrä) ja listan eri kategorioista
- käyttäjä voi etsiä teorioita, joiden osana on annettu sana
- käyttäjä voi poistaa kirjoittamansa kommentin tai teorian
- ylläpitäjä voi lisätä ja poistaa teorioita ja kommentteja

## Sovellus on testattavissa paikallisesti

## Ohjeet käynnistämiseen paikallisesti
Kloonaa ensin tämä repositorio omalle koneellesi. Siirry juurikansioon ja luo virtuualiympäristö:
```
cd loretheories/
python3 -m venv venv
source venv/bin/activate
```

Voit asentaa sovelluksen riippuvuudet komennolla:
```
(venv) $ pip install -r requirements.txt
```
Luo `.env` tiedosto juurikansioon. Määritä `.env` tiedoston sisältö seuraavanlaiseksi:
```
DATABASE_URL=<tietokannan-paikallinen-osoite>
SECRET_KEY=<salainen-avain>
```
Tietokannan osoitteena pitäisi toimia `"postgresql+psycopg2://"`

Salaisen avaimen voit luoda Python-tulkin avulla:
```
$ python3
>>> import secrets
>>> secrets.token_hex(16)
```
Luo tarvittavat taulut komennolla:
```
(venv) $ psql < schema.sql
```
Sovelluksen voi suorittaa virtuaaliympäristössä komennolla:
``` 
flask run
``` 
