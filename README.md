# SoDI forum comment collect
## Telepítés (Windows)
1. Szükség van a Python-ra (minimum 3.10.x verzió), amit a python.org oldalon lehet letölteni.
2. Python pip csomagkezelőjével telepíteni a virtualenv modult: python -m pip install virtualenv
3. Letölteni, clone-ozni a repository tartalmát saját számítógépre.
4. Command Line Interface segítségével (CMD.exe) odanavigálni ahol van a collect.py és a models.py stb...
5. Létrehozni egy Python virtuális környezetet a következő képpen: python -m venv venv
6. Virtuális környezet segítségével felrakni eme eszköz használatához szükséges függőségeket a következőképpen: .\venv\Scripts\pip install -r requirements.txt
(Ha valami probléma lenne az alábbi linken részletesebb infót találtok a virtuális környezettel kapcsolatban: https://docs.python.org/3/library/venv.html)
7. Ha minden sikeresen telepítve lett, akkor a virtuális környezet python-jával futtatható a collect.py a következőképpen: .\venv\Scripts\python collect.py

## Működés ismertetése
A telepítés tartalmazza az eszköz elindításának módját, így csak a működését gondoltam érdemesnek leírni.

A collect.py (virtális környezettel) elindítva egy olyan Chrome böngészőt nyit meg, ami a telepített függőségi modulok közül egy webdriver, aminek segítségével áthidatlható a cloudflare miatti DoS vagy DDoS védelem. De ez NEM egy DoS/DDoS eszköz. Ez egy szimpla modul, ami a sodifórumról szedi össze a kommenteket és menti le sqlite adatbázisba saját számítógépre. Semmilyen kártékony hatást gyakorolni nem célja és nem is eszköze ennek a scriptnek!

A kommentek alapvető adatain felül menti azt is, hogy aki írta, az regisztrált fiókról írta-e meg azt az oldalszámot, ahol található a komment, illetve még az oldalon a html forrásból kinyerhető komment ID-ját.

Amikor fut a script, először azt ellenőrzi, hogy ha van rekord már az adatbázisban, akkor van-e az utolsótól 3 nappal korábbi komment. Ha van, akkor ennek az oldalszáma fogja képezni azt az adatot, amitől kezdve a script elkezdi "update"-lni az adatokat. Erre azért van szükség, mert így a kommentek pontszámai is frissülnek, aminek elég nagy az esélye, hogy a legutóbbi mentés óta változtak és hogy ne előről kezdje a mentést ha idő közben meg kell szakítani vagy megszakad. Először a főoldal nyílik meg, ahol a legutolsó oldal oldalszáma kerül kinyerésre. Ez fogja jelenteni azt az adatot, ameddig a script futni fog. Ha ez megvan akkor elkezdi mentegetni a kommenteket. Az adatbáziskezelés olyan, hogy ha az adott oldalszám maradék nélkül osztható 50-vel VAGY az utolsó oldalon van, az új rekordokat committolja az adatbázisba. Itt nem elég szimplán hozzáadni add/merge-el a rekordokat, kell commit-tolni is. Azért nem minden oldalnál van committolva, mert hátha így rövidebb idő alatt tud dolgozni a script. Az 50-es határt olyan aranyközéputas értéknek gondolom, ahol érdemes committolni az új hozzáadott/módosított rekordokat.

A weboldal és ennek html forrása kezelése (kommentek adadtai kinyerése html kódból) Selenium és BeautifulSoup modulokkal van megoldva. Az előbbi a cloudflare védelem miatt kell, az utóbbi pedig azért, mert pusztán Selenium-mal kezelve brutálisan lassabb. BeautifulSoup sokkal gyorsabban nyeri ki az adott html kódból a szükséges adatokat.  A Selenium pedig a webdriver-es Chrome böngészővel léptet oldalról oldalra, áthidalva a cloudflare-t.
