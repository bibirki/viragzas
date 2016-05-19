from lxml import html
from lxml import etree
import requests
page = requests.get('http://www.baumkunde.de/baumlisten/baumliste_az_scientific.php')
tree = html.fromstring(page.content)
#a főoldalról kérdezd le az összes fafajhoz tartozó oldal linkjét
linkek = tree.xpath('//div[@class="box"]/a/@href')

with open("fagyujtemeny_.csv", "w") as text_file:
	#a 670-ik fánál nincs hónaptáblázat ezért megáll a kód, így két részletben írtam ki a fájlt és aztán összemásoltam, biztos lehet elegánsabban try-al vagy valami.
    for x in linkek[:669]:
        falink = x.split("/")[1]
		#nyisd meg az összes fafaj lapot egyesével
        faoldal = requests.get('http://www.baumkunde.de/'+falink)
		#töltsd le a fafaj lapok tartalmát
        subtree = html.fromstring(faoldal.content)
		#keresd meg a hónapokat tartalmazó időcsíkot (ami egy táblázat és kettő van belőle)
        zeitstreifen_ = subtree.xpath('//table[@class="zeitstreifen"]')
		#válaszd ki az első táblázatot
        zeitstreifen = zeitstreifen_[0]
		#válaszd ki a táblázat sorait
        trs = zeitstreifen.getchildren()
		#válaszd ki az első sor összes celláját
        tds= trs[0].getchildren()
		#válaszd ki azokat a cellákat amiknek van bluete nevű classjuk
        bl = trs[0].find_class('bluete')
		#csinálj egy üres listát ami a virágzási hónapokat fogja tárolni számként (pl. május=4 mert 0-val kezdjük)
        honaplista=[]
		for z in bl:
			#add hozzá a listához azoknak a hónapoknak az indexét ahol virágik az adott fafaj
            honaplista.append(trs[0].index(z))
		#az adatmodell szempontjából jobb ha nemcsak azoknak a hónapoknak a számát tudjuk amelyikben virágzik, hanem minden hónapnál tudjuk hogy virágzik-e vagy sem. 0 ha nem virágzik.
        honapok = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		#írd át azokat a 0-kat 1-re amelyiknek az indexe megegyezik a virágzási hónap számával
        for i in honaplista:
            honapok[i] = 1
		#mivel csv-ben akarjuk megkapni az adatokat írd át a listát vesszőkkel elválasztott számokra (csak el kell tűntetni a szögletes zárójelet)
        honapok_str_ = str(honapok).strip('[]')
		#írd a fa nevét és a hónapoknak megfelelő nullákat és egyeket egy stringbe
        fagyujtemeny = falink +',' + honapok_str_
        print fagyujtemeny
		#írd az így keletkezett stringet a fájlba
        text_file.write('%s\n' % fagyujtemeny)
text_file.close()