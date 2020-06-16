# 2020-project-2-cybergh0sts

## &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; Part 1 (_Finding Geaorge_)

1. Αρχικά, βρήκαμε με **View Page Source**, το σχόλιο που περιείχε το blog με τρόπους ασφάλισης ενός server

   > --> Link: https://blog.0day.rocks/securing-a-web-hidden-service-89d935ba1c1d


2. Από εκεί βρήκαμε ότι μπορούμε να χρησιμοποιήσουμε το **/server-info** για να δούμε πληροφορίες 
   σχετικές με τον server

   > --> Link: http://2fvhjskjet3n5syd6yfg5lhvwcs62bojmthr35ko5bllr3iqdb4ctdyd.onion/server-info
    
    
3. Έτσι, μέσα στις πληροφορίες αυτές, βρήκαμε ότι στο server εξηπυρετούνται δύο ιστοσελίδες και πήραμε το 2<sup>ο</sup> .onion link

    > ![alt text](import screen) 
    >
    >
    > --> Link: http://jt4grrjwzyz3pjkylwfau5xnjaj23vxmhskqaeyfhrfylelw4hvxcuyd.onion/


4. Μετά από το **/server-info** ξανά, του 2<sup>ου</sup> onion, βρήκαμε ότι έχουμε πρόσβαση σε όλα τα **.phps** files

   > ![alt text](import screen)
    
   Παρόμοια πληροφορία μπορούμε να πάρουμε και με ακόμα έναν τρόπο. Μέσα στο **/robots.txt** αναγράφεται το εξής
   
   > Disallow: /\*.phps
   
   που δηλώνει ότι ο server δε θέλει τα Web Robots που θα διαβάσουν αυτό το αρχείο, να επισκεφθούν σελίδες με κατάληξη **.phps**.
   Αυτό άμεσα μας δηλώνει ότι κάπου στο server ενδεχομένως να υπάρχει κάποιο php source file, από το οποίο μπορούμε να δούμε το 
   back end της αντίστοιχης σελίδας. [<sup>\[1\]</sup>](part2)


5. Μετά, πατώντας το _Submit_ που είχε στη φόρμα, μας ανακατεύθυνε στη σελίδα **/access.php** με μήνυμα λάθους. 
   
   <ul>
   <li>Αρχικά σκεφτήκαμε να προσπαθήσουμε με <b>SQL Injection</b> να αντλήσουμε δεδομένα από τη βάση.</li>
   <li>Στη συνέχεια, εφόσον είδαμε ότι δεν μπορούμε να κάνουνμε κάτι με αυτό το attack, ψάξαμε στο <b>/server-info</b> αυτού του 
      onion και βρήκαμε αυτά που αναφέρονται στο 4.</li>
   <li>Τότε, δοκιμάσαμε να βάλουμε στο url το <b>access.phps</b> και μας εμφάνισε το source code του.</li>
   </ul><br/>
   
   > &emsp;&nbsp;&nbsp; --> Link: http://jt4grrjwzyz3pjkylwfau5xnjaj23vxmhskqaeyfhrfylelw4hvxcuyd.onion/access.phps
   
   
6. Διαβάζοντας τον κώδικα βρήκαμε πώς να βρούμε το <b>username</b>. Φτιάξαμε το παρακάτω script που το υπολόγιζε και βρήκαμε την τιμή 
   του $user (= 1337 leet 😉)
   
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
   Στη συνέχεια, είδαμε ότι έχει και έναν 2<sup>ο</sup> ελεγχο που πρέπει να παρακάμψουμε. Έπρεπε το μήκος του username να είναι **7**. 
   Έτσι απλά προσθέσαμε **3** χαρκατήρες + οι οποίοι αγνοούνται και περάσαμε τον πρώτο έλεγχο.
   
   <h6> <i> Σημείωση: Οποιουσδήποτε 3 χαρακτήρες και να βάλουμε που είναι γράμματα και όχι ψηφία περνάμε τον έλεγχο. </i> </h6>


7. Μετά είδαμε ότι το $password χρησιμοποιείται σε μια strcmp(), η οποία μπορεί να παρκαμφθεί εύκολα
   σύμφωνα με γνωστό πρόβλημα που έχει, που αν της δοθεί NULL ή κενό array σαν 1ο όρισμα, τότε επιστρέφει
   0, κάτι το οποίο θα καθιστούσε αληθή τη συνθήκη. 
   
   Άρα, έπρεπε με κάποιον τρόπο να περάσουμε κενό array σαν payload στη μεταβλητή $password. Αυτό έγινε 
   δίνοντας σαν payload το []

   > --> Link: http://jt4grrjwzyz3pjkylwfau5xnjaj23vxmhskqaeyfhrfylelw4hvxcuyd.onion/access.php?user=1337+++&password[]


8. Μετά από το /blogposts7589109238 που μας έδωσε η καινούργια σελίδα πήγαμε στην /blogspots και μέσω του indexing 
   που παρέχει ο server βρήκαμε το αρχείο post3.html που περιείχε την πρώτη αναφορά στον Γιώργο και πολλά clues.

   > --> Link: http://jt4grrjwzyz3pjkylwfau5xnjaj23vxmhskqaeyfhrfylelw4hvxcuyd.onion/blogposts7589109238/blogposts/


9. Από εκεί είδαμε αυτό που λέει "Winner Visitor #100013" και θυμηθήκαμε ότι είχαμε δει το Visitor σαν Name στο
   cookie της αρχικής σελίδας (http://2fvhjskjet3n5syd6yfg5lhvwcs62bojmthr35ko5bllr3iqdb4ctdyd.onion/) που μας 
   είχε δοθεί και υποψιαστήκαμε ότι θα χρησιμοποιηθεί κάπου εκεί.
    
   Διαγράφοντας το cookie που έχει και κάνοντας reload είδαμε ότι στη θέση του 204 εμφανίζει "Bad sha256".
   Άρα σκεφτήκαμε ότι το value του cookie έχει άμεση συσχέτιση με τον αριθμό 204 που αναφερόταν προηγουμένως
   ως "Visitor Number" σε συνδυασμό με το sha256.
   
   Είδαμε ότι το value του cookie τελειώνει σε %3D που είναι το (=) σε URL encoded μορφή και βρήκαμε ότι αυτό
   είναι format που συμφωνεί με την κωδικοποίηση base64.
   
   Κάνοντας decrypt το 'MjA0OmZjNTZkYmM2ZDQ2NTJiMzE1Yjg2YjcxYzhkNjg4YzFjY2RlYTljNWYxZmQwNzc2M2QyNjU5ZmRlMmUyZmM0OWE='
   είδαμε ότι παράγει το '204:fc56dbc6d4652b315b86b71c8d688c1ccdea9c5f1fd07763d2659fde2e2fc49a7'.
   
   Μετά κάναμε hashing του 204 με το sha-256 και είδαμε ότι παράγει το 2ο κομμάτι του decrypted base64.

   Άρα κατασκευάσαμε εν τέλει το καινούργιο value για το cookie σύμφωνα με τη συνάρτηση: base64( id:sha256(id) )

   Έτσι παράχθηκε το: 'MTAwMDEzOjM2MjA5NTQyMzYyNzg3ZjIyMDU0MTgyYzNlNDE0MDlmZDFiMDQ4NmVjYjI4MmMwMmRjNTdiNGY5OGU0N2RlNzA='

   Βάζοντας το στο cookie εμφανίζει την κρυφή τοποθεσία του καταλόγου με τα backups από το κινητό του Γιώργου (/sekritbackups2444).

   > --> Link: http://2fvhjskjet3n5syd6yfg5lhvwcs62bojmthr35ko5bllr3iqdb4ctdyd.onion/sekritbackups2444/


10. Κατεβάσαμε όλα τα αρχεία και πήραμε το κομμάτι του hash που περιείχε το passphrase.key.truncated
    Ακολουθώντας τις οδηγίες, πήραμε το secret "raccoon" που αναφερόταν στο 2ο .onion και φτιάξαμε ένα script, με το οποίο 
    φτιάχναμε ημερομηνίες από την αρχή του 2020 και κάναμε το hashing του passphrase με χρήση του sha256().

    Ελέγχαμε αν το κομμάτι του hash που είχε το truncated file περιέχεται σε αυτό που φτιάξαμε και εύκολα βρίσκουμε
    την ημερομηνία να είναι: 2020-02-12

    Έτσι έχοντας όλο το passphrase και κάνοντας το hashing μπορούμε να κάνουμε decrypt τα .gpg αρχεία.
    passphrase: 2020-02-12 raccoon
    hash      : d1689c23e86421529297f3eb35db2fe261de9cbe19487d923c464d96ca00e138


11. Ανοίγωντας το signallog βρίσκουμε την αναφορά στο commit με αριθμό: 2355437c5f30fd2390a314b7d52fb3d24583ef97
    Παρόλο που σίγουρα κάποο ρόλο θα διαδραμάτιζε το firefox.log, δεν το ψάξαμε όπως θα έπρεπε εξ αρχής και αρχίσαμε
    να ψάχνουμε manually τα repos του καθηγητή και του βοηθού μέχρι που βρήκαμε το αντίστοιχο commit με hash αυτό
    που βρήκαμε από το signal.log.

    Eν τέλει, προφανώς και υπήρχε και στο αρχείο firefox.log, που με ένα search github έβγαζε το λινκ απευθείας ή μέσω
    terminal εκτελώντας: sort firefox.log | uniq ή grep github firefox.log, εμφάνιζε το link του github.

      > \>\> sort firefox.log | uniq \
      >      https://en.wikipedia.org/wiki/The_Conversation \
      >      https://github.com/asn-d6/tor

      > \>\> grep github firefox.log \
      >      https://github.com/asn-d6/tor


12. Μετά βρίσκοντας το commit αυτό, βρίσκαμε τις τελικές οδηγίες για την εύρεση της τοποθεσίας του Γιώργου. 
    Ακολουθώντας εύκολα πλέον τα 4 βήματα που είχε μέσα κατασκευάσαμε τις συντεταγμένες του και ολοκληρώσαμε
    το ερώτημα!

    > Location : Vaux-Saules, 21440, France\
    > Latitude : 47.47298416481722560089\
    > Longitude: 4.7991375472458345437


- - - - - - - - - - - - - - - - - ----------------------------------------- - - - - - - - - - - - - - - - - -


## Part 2
