## Gegeben

- Die Funktion σ(m, K) = H(K || m) mit einer Prepend-Only Konstruktion
- Es sind folgende σ(m, K) bekannt mit den dazugehörigen Nachrichten m, aber der Schlüssel K ist geheim:
  -  σ(“abcd”, K) = 632e4e5c
  - σ(“abcdef”, K) = 0f6b8802
  - σ(“abcdefghijk”, K) = 2638a819 • σ(“foobar”, K) = 782a826e
  - σ(“barfoo”, K) = 885dc316
- Zudem ist bekannt, dass die Schlüssellänge len(K) = 16 Byte lang ist. 
- Außerdem erfolgt der Angriff auf die in Aufgabe 1 erstellte Authenifizierungsfunktion H, welche [hier](authentification_function.py) zu finden ist.

## Extension Angriff

Eine wesentliche Schwachstelle einer Authentifisierungsfunktion ist die Konstruktion, die diese umgibt. In disem Fall
ist es eine Prepend-Only Konstruktion, wo der Schlüssel vor der Nachricht angehangen wird. Der Angriff zielt darauf ab
den internen Zustand der Verarbeitung von H(K || m) zu kennen, womit die Hash-Funktion simuliert werden kann und auf 
Basis einer anderen Nachricht eine gültige MIC zu erzeugen, obwohl der Schlüssel zum erzeugen dieser nicht bekannt ist.

So wird eine neue Nachricht erzeugt, die folgende Struktur besitzt:

- m' = m || padding || extension

## Angriff:

Nun wird ein beispielhafter Angriff durchgeführt. Der Code zeigt eine allgemeine Extension Angriff auf die Authenifizierungsfunktion.
Im Beispiel wird die bekannte **MIC σ("foobar", K) = 0x782a826e** benutzt. Im Code müsste es als Tuple angegeben werden
 - (b'foobar', 0x782a826)

Somit bildet die bekannte MIC laut Definition folgenden Zustan ab:
- K || "foobar"

### Bestimme die Länge
Da bekannt ist, dass der Schlüssel immer 16 Byte lang ist und jeder Zeichen ein Byte groß ist, beträgt
die gesammte Länge:
- K || "foobar" = 16 Byte + 6 Byte = 22 Byte 

### Padding berechnen

Da die Authentifizierungsfunktion Nachrichten in 4-Byte-Blöcken blockweise verarbeitet
wird jeder 4-Byte-Block seperat mit einem anderen Initialzustand gehasht. So ergeben sich zwei Fälle:

1. Am Ende bleiben weniger als 4 Bytes übrig: 
    - Der Block wird mit 0xff aufgefüllt, also einem Byte und gehasht.
2. Es sind mehr als vier Bytes übrig:
    - Die ersten 4 Bytes werden gehast und der Rest wird mit 0xff aufgefüllt und mit einem anderen Initialzustand gehasht.

Für eine Länge von 22 Bytes ergibt das:
- 5 volle 4-Byte-Blöcke (20 Byte)
- 2 übrige Bytes die mit zwei 0xff auf 2 Bytes + 0xff + 0xff aufgeüllt werden 


### Erzeugen einer neuen Nachricht
Nun wird folgende Nachricht angehangen:
- HelloWorld! (11 Bytes)
- 
Dann ergibt sich die neue Nachricht:
- K || "foobar" + padding + "HelloWorld!"
- 
Die Padding-Bytes simulieren das Padding von K || m.

Somit wird am Ende die neue Nachricht gehasht. 
m′=m∣∣padding∣∣extension
- σ(m′,K) = H(σ(m,K),extension)

Somit wurde zur Nachricht eine gültige MIC erzeugt.