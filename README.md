# 2020-project-2-cybergh0sts

## &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; Part 1 (_Finding George_)

1. Αρχικά, βρήκαμε με **View Page Source**, το σχόλιο που περιείχε το blog με τρόπους ασφάλισης ενός server

   > --> Link: https://blog.0day.rocks/securing-a-web-hidden-service-89d935ba1c1d

<br/>

2. Από εκεί βρήκαμε ότι μπορούμε να χρησιμοποιήσουμε το **/server-info** για να δούμε πληροφορίες 
   σχετικές με τον server

   > --> Link: http://2fvhjskjet3n5syd6yfg5lhvwcs62bojmthr35ko5bllr3iqdb4ctdyd.onion/server-info
    
<br/>
    
3. Έτσι, μέσα στις πληροφορίες αυτές, βρήκαμε ότι στο server εξηπυρετούνται δύο ιστοσελίδες και πήραμε το 2<sup>ο</sup> .onion link

    > ![alt text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/screen_1.png) 
    >
    >
    > --> Link: http://jt4grrjwzyz3pjkylwfau5xnjaj23vxmhskqaeyfhrfylelw4hvxcuyd.onion/

<br/>

4. Μετά από το **/server-info** ξανά, του 2<sup>ου</sup> onion, βρήκαμε ότι έχουμε πρόσβαση σε όλα τα **.phps** files

   > ![alt text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/screen_2.png)
    
   Παρόμοια πληροφορία μπορούμε να πάρουμε και με ακόμα έναν τρόπο. Μέσα στο **/robots.txt** αναγράφεται το εξής
   
   > Disallow: /\*.phps
   
   που δηλώνει ότι ο server δε θέλει τα Web Robots που θα διαβάσουν αυτό το αρχείο, να επισκεφθούν σελίδες με κατάληξη **.phps**.
   Αυτό άμεσα μας δηλώνει ότι κάπου στο server ενδεχομένως να υπάρχει κάποιο php source file, από το οποίο μπορούμε να δούμε το 
   back end της αντίστοιχης σελίδας. [<sup>\[1\]</sup>](#part-2)

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
   
   Ακόμα, ο έλεγχος που κάνει η php για το αποτέλεσμα της strcmp(), είναι **loose comparison (!=)** και όχι **strict (!==)**, 
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
   ως 0 και έτσι η σύγκριση **NULL == 0** επιστρέφει ***TRUE***. [<sup>\[2\]</sup>](#part-2)[<sup>\[3\]</sup>](#part-2)
   
   Άρα έπρεπε να βρούμε τρόπο να κάνουμε το όρισμα που ελέγχουμε, να μετατραπεί σε **empty array**, καθώς δίνοντας στην strcmp() σαν 
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
   
   ![alt text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/screen_3.png)
    
   Διαγράφοντας το cookie που έχει και κάνοντας reload είδαμε ότι στη θέση του 204 εμφανίζει **"Bad sha256"**.
   Τότε σκεφτήκαμε ότι το value του cookie καθορίζει το τι θα εκτυπωθεί στη θέση του 204.
   
   ![alt text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/screen_4.png)
   
   Είδαμε ότι το value του cookie τελειώνει σε %3D που είναι το (=) σε URL encoded μορφή και βρήκαμε ότι αυτό
   είναι format που συμφωνεί με την κωδικοποίηση base64. [<sup>\[4\]</sup>](#part-2)
   
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
   
   Έτσι, με payload: **<script\>alert(1)</script\>**, μετατρέποντας το σε sha256 και μετά σε base64, εμφανίστηκε το alert message
   στη σελίδα.
   
   Payload: **PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pjo1YzE0MGQzNWRjYjQ2YTYyMmUyY2VkZjVlZjVjYzM2MzhjZGZmZDFjMTE4YzkzMzFmOGM4NDY2OWYwYjc0Nzgz**

   ![alt text](https://github.com/chatziko-ys13/2020-project-2-cybergh0sts/blob/master/img/screen_5.png)
   
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

## Part 2
