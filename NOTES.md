# Notes

## Measuring speed of new line stripping

There doesn't appear to be a significant difference in three ways I tested for
stripping newlines from the end of a string I ended up using the `fast` method
anyways because array slicing intuitively seems like it should be the fastest.

    >>> def timing(f):
            def wrap(*args):
                time1 = time.time()
                ret = f(*args)
                time2 = time.time()
                print('{:s} function took {:.3f} ms'.format(f.__name__, (time2-time1)*1000.0))
                return ret
            return wrap
        
    >>> @timing
        def fast(text):
          return text[:-1]
        
    >>> @timing
        def slow(text):
          return text.strip()

    >>> @timing
        def other(text):
            return text.rstrip('\n')

    >>> slow(last)
    slow function took 0.004 ms
    '98462,98098,5'
    >>> slow(last)
    slow function took 0.002 ms
    '98462,98098,5'
    >>> slow(last)
    slow function took 0.001 ms
    '98462,98098,5'

    >>> fast(last)
    fast function took 0.004 ms
    '98462,98098,5'
    >>> fast(last)
    fast function took 0.002 ms
    '98462,98098,5'
    >>> fast(last)
    fast function took 0.002 ms
    '98462,98098,5'
    
    >>> other(last)
    other function took 0.005 ms
    '98462,98098,5'
    >>> other(last)
    other function took 0.002 ms
    '98462,98098,5'
    >>> other(last)
    other function took 0.001 ms
    '98462,98098,5'
    
## Nearest neighbors

### Scorpions (band) 
#### nearest cosine neighbors using APSP matrix
0.01326579369314096 +/- (band)
0.01580342671051016 !!!
nan 0.8Syooogeki
nan 0DFx
0.009341754174457706 2Tm2,3
0.010315889246236942 2Be3
0.010392316270728452 3 (1980s band)
0.010850689321079465 2nd Chapter of Acts
0.011149815223511994 2-4 Family
0.011205945348309654 2Cellos
#### nearest cosine neghbors using partially trained embedding matrix
0.522578626871109 Stevie Wishart
0.562618762254715 Vija Artmane
0.6081222295761108 Mikako Takahashi
0.6154393255710602 Haris Alexiou
0.6237971484661102 Wintley Phipps
0.6271282434463501 Eldridge Cleaver
0.6275804340839386 Tom Bodett
0.6302314698696136 Danakil (band)
0.6312006711959839 Safari Sound Band
0.6324273645877838 Zorica Kondža
### nearest cosine neighbors using compressed matrix
1.6152412740666477e-11 Christofer Johnsson
1.884592482070957e-11 Persian Risk
1.898137202971384e-11 Voivod (band)
1.9145907081963287e-11 Geoff Downes
1.9654611271846534e-11 The Rasmus
1.9880985746567603e-11 Vinnie Vincent
1.9925616712157534e-11 Goudie (band)
2.026745438143962e-11 Eddie Trunk
2.030975387867784e-11 Sword (band)
2.0314527837683727e-11 Kip Winger


### Metallica
#### nearest cosine neighbors using APSP matrix
0.009591674919927295 Alabama Thunderpussy
0.010469819607898945 Alas (band)
0.010735533602987957 Alastis
0.011245419756141128 Ismo Alanko
0.011906342125268532 Alarum (band)
0.011945947841018878 The Alarm
0.012661949891135449 Alaska (singer)
0.012713148158576937 Alamo Race Track
0.012810089932609348 Alamid (band)
0.013123604965083024 Ilkka Alanko
#### nearest cosine neghbors using partially trained embedding matrix
0.5498521625995636 Nagelfar
0.6031804978847504 Dixie Witch
0.6062719523906708 Leona Williams
0.6066709458827972 Richard Lewis (tenor)
0.6130003035068512 August Bungert
0.6348682045936584 Ramona (vocalist)
0.6409150063991547 Kazuhisa Uchihashi
0.6441698372364044 Roberto Abbado
0.645143061876297 Luis López Álvarez
0.6465986967086792 Lloyd Ahlquist
### nearest cosine neighbors using compressed matrix
2.5331070574452497e-11 Audiovent
2.6311508527498972e-11 Byron Stroud
2.746103344719586e-11 Jerry Cantrell
2.7900348698040034e-11 Layne Staley
2.8311242239453804e-11 Michael Schenker
2.837596824178945e-11 The Offspring
2.8685942510264795e-11 Tony Iommi
2.873257187729905e-11 Matt Sorum
2.8756996783840805e-11 James Hetfield
2.9288349523426405e-11 Brian Robertson (guitarist)


### Shakira
#### nearest cosine neighbors using APSP matrix
0.008190402237661765 +/- (band)
0.008396219709599695 Celeste Buckingham
0.008423518473957614 Ricki-Lee Coulter
0.00867306844450455 7 Samurai (duo)
0.008681605686721827 6ix9ine
0.008772896510390815 Dominik Büchele
0.008800062841398004 Nikki DeLoach
0.008815724509616096 4th Avenue Jones
0.00912774312879272 7icons
0.009264260317606632 4 the Cause
#### nearest cosine neghbors using partially trained embedding matrix
0.5941698849201202 The Product G&B
0.5974563360214233 Nikolai Astrup
0.5977749526500702 Matt Andersen
0.6120772659778595 Eagle Twin
0.616774708032608 Ann Lee (singer)
0.6239891052246094 Lejaren Hiller
0.6294792294502258 Wu Tsing-fong
0.6333352327346802 Junior Jack
0.6343559920787811 Tillmann Uhrmacher
0.6378957033157349 Murray McLauchlan
### nearest cosine neighbors using compressed matrix
1.9118817640162433e-11 Amy Studt
1.9805601603195555e-11 Ralph Schuckett
2.0031420966404312e-11 Steve Blame
2.0402235456629114e-11 Selena
2.0416335289041854e-11 Martina Schindlerová
2.073841098848561e-11 4 Non Blondes
2.1174506592558373e-11 Jared Leto
2.121847142433353e-11 Tim Christensen
2.1304402686439516e-11 Anna Nalick
2.131694820661778e-11 Jim McGorman


### Daft Punk
#### nearest cosine neighbors using APSP matrix
0.011470902857891652 !!!
0.011482193008834463 +/- (band)
nan 0.8Syooogeki
nan 0DFx
0.01064674757759354 The 2 Bears
0.01065279956675591 2 Chainz
0.010737455053740463 2 in a Room
0.010823492441938809 II D Extreme
0.010944227052054556 2 Bad Mice
0.010972498912875106 2Baba
#### nearest cosine neghbors using partially trained embedding matrix
0.541138082742691 Sneaky Pete Kleinow
0.5919811427593231 Joni Harms
0.6047965288162231 John Rutter
0.6139491200447083 Malcolm McDowell
0.624408632516861 Ian Bostridge
0.6345735490322113 Uryū Ishida
0.6368706226348877 RPA & The United Nations of Sound
0.6378886103630066 Hideo Ishikawa
0.6395784318447113 Tátrai Quartet
0.6399163603782654 Zu (band)
### nearest cosine neighbors using compressed matrix
2.300981627456622e-11 KMFDM
2.3213431177282473e-11 Julien Temple
2.364664020149121e-11 The Soul Rebels
2.37592168161882e-11 Jim Rakete
2.4928170638816027e-11 Eurythmics
2.511979513286633e-11 Duran Duran
2.573941060290963e-11 Keane (band)
2.591205028323884e-11 Digitalism (band)
2.5933366565311644e-11 SZA (singer)
2.6118440743516658e-11 Jack White


### Kanye West
#### nearest cosine neighbors using APSP matrix
0.007608013130629976 Cougnut
0.009419297963807693 Celeste Buckingham
0.009614149797083082 Shea Couleé
0.010238456966265241 Jonny Buckland
0.010305822273930954 Paul Buchignani
0.01036241913670144 +/- (band)
0.010449320988044963 Jonathan Coulton
0.010538229352161088 The Count & Sinden
0.010545818457975309 Count the Stars
0.010618203727958186 The Coup
#### nearest cosine neghbors using partially trained embedding matrix
0.5747953951358795 Tina Moore
0.5959233343601227 K. T. Oslin
0.5976538360118866 Bad Moon Rising (band)
0.6106864213943481 Axel Algmark
0.6216613054275513 Oscar Levertin
0.6257630288600922 The Starlets
0.6263743937015533 Kevin Parker (musician)
0.632159948348999 Kaho Minami
0.6378994882106781 Robin Lee Bruce
0.6390561163425446 Mae West
### nearest cosine neighbors using compressed matrix
2.2070789640338262e-11 Mark Ronson
2.2362223184302366e-11 Rihanna
2.2372326213826454e-11 Dave Audé
2.353817141198533e-11 Pink (singer)
2.3931634451912487e-11 Usher (musician)
2.4075963445113757e-11 R. Kelly
2.411537636248795e-11 Kendrick Lamar
2.4271473719750247e-11 Adele
2.4535817821913497e-11 Martha Reeves
2.4877655491195583e-11 Jack White
