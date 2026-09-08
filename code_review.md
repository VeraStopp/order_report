# Kodgranskning av order_report.py

## Utgångsläge
Scripten går att köra och skapa fyra outputs:
1. overview
2. returns by category
3. sales by category
4. sales by region

### Fynd 1 - Flera ansvar är sammanblandade
**Observation:** Koden saknar tydlig ansvarsuppdelning. Logik för filhantering, validering, beräkningar och rapportgenerering ligger i samma modul.

**Konsekvens:** Det gör koden svårttestad och svår att återanvända. 

**Förslag:** Dela upp koden i fristående moduler där logik för beräkningar/transformationer skiljs helt från I/O-hantering. 


### Fynd 2 - Saknar logging och spårbarhet
**Observation:** Programmet använder enbart print()-satser för att informera om vad som händer. 

**Konsekvens:** Det finns ingen historik eller spårbarhet över när programmet körs och det går inte att styra vilka meddelanden som ska visas. 

**Förslag:** Använd pythons logging-modul och konfigurera loggnivåerna samt loggning till en fil. 


### Fynd 3 - Bristfällig felhantering
**Observation:** Koden fångar alla fel med en bred except Exception as error.

**Konsekvens:** Svårt att veta vad som faktiskt gick fel. Gör felsökning mycket svårt.

**Förslag:** Använd specifika exception-typer.


### Fynd 4 - Hårdkodade värden och avsaknad av konfigurationsfil
**Observation:** Filsökvägar och kolumnnamn är hårdkodade direkt i skriptet.

**Konsekvens:** Om filsökvägar ändras måste man ändra direkt i skriptkoden. Det gör programmet oflexibelt.

**Förslag:** Flytta konstanter, obligatoriska kolumner och sökvägar till en central konfigurationsfil.


### Fynd 5 - Otydliga och generiska namn
**Observation:** Flera variabler har allmänna eller numrerade namn t ex data, required och result1.

**Konsekvens:** Koden blir svårläst och det framgår inte av variabelnamnet vad datastrukturer faktiskt innehåller.

**Förslag:** Använd mer beskrivande namn som speglar innehållet t ex orders_df, sales_by_category, REQUIRED_COLUMNS


## Prioritering

### Hög prioritet
1. Fynd 1 - Flera ansvar är sammanblandade
2. Fynd 3 - Bristfällig felhantering

### Medelprioritet
4. Fynd 4 - Hårdkodade värden och avsaknad av konfigurationsfil
5. Fynd 2 - Saknar logging och spårbarhet

### Låg prioritet
6. Fynd 5 - Otydliga och generiska namn