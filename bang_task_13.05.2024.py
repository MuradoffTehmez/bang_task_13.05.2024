class BankaHesabi:
    def __init__(self, hesab_nomresi, ad, soyad, balans=0):
        self.hesab_nomresi = hesab_nomresi
        self.ad = ad
        self.soyad = soyad
        self.balans = balans
        self.kredit_icazesi = False
        self.kredit_tarixcesi = []

    def __str__(self):
        return f"Hesab Sahibi: {self.ad} {self.soyad}, Hesab Nömrəsi: {self.hesab_nomresi}, Balans: {self.balans} AZN"

    def balans_artir(self, mebleg):
        self.balans += mebleg
        print(f"{self.ad} {self.soyad}, hazırkı balansınız: {self.balans} AZN")
        return self.balans

    def pul_cixar(self, mebleg):
        if mebleg <= self.balans:
            self.balans -= mebleg
            print(f"{self.ad} {self.soyad}, çıxarılan məbləğ: {mebleg} AZN, yeni balansınız: {self.balans} AZN")
            return self.balans
        else:
            print("Balansınızda yetərli vəsait yoxdur.")
            return False

    def balans_goster(self):
        print(f"{self.ad} {self.soyad}, balansınız: {self.balans} AZN")
        return self.balans

    def kredit_tarixcesi_goster(self):
        if self.kredit_tarixcesi:
            print(f"{self.ad} {self.soyad}, kredit tarixçəniz:")
            for tarixce in self.kredit_tarixcesi:
                print(tarixce)
        else:
            print(f"{self.ad} {self.soyad}, kredit tarixçəniz mövcud deyil.")


class KreditHesabi(BankaHesabi):
    def __init__(self, hesab_nomresi, ad, soyad, balans=0):
        self.illik_muddet = 12
        self.kredit_meblegi = 0
        self.odenilen_mebleg = 0
        self.qalan_borc = self.kredit_meblegi - self.odenilen_mebleg
        self.ayliq_odenis = self.kredit_meblegi / self.illik_muddet
        self.odenis_sayi = 1
        self.ayliq_odenisler = [(self.ayliq_odenis * ay) for ay in range(1, 13)]
        super().__init__(hesab_nomresi, ad, soyad, balans)

    def kredit_gotur(self, goturulen_mebleg):
        if not self.kredit_meblegi:
            if goturulen_mebleg > 0:
                self.kredit_meblegi = goturulen_mebleg
                self.ayliq_odenis = self.kredit_meblegi / self.illik_muddet
                self.kredit_icazesi = True
                self.kredit_tarixcesi.append(f"{self.ad} {self.soyad}, {goturulen_mebleg} AZN kredit götürdü.")
                print(f"{self.ad} {self.soyad}, {goturulen_mebleg} AZN kredit götürdünüz. Aylıq ödəniş məbləği: {self.ayliq_odenis:.2f} AZN")
                return True
            else:
                print("Məbləğ düzgün daxil edilməyib.")
                return False
        else:
            print(f"{self.ad} {self.soyad}, mövcud kreditiniz: {self.kredit_meblegi} AZN")
            return False

    def kredit_goster(self):
        if self.kredit_icazesi:
            print(f"{self.ad} {self.soyad}, kredit borcunuz: {self.qalan_borc} AZN")
            return True
        else:
            print(f"{self.ad} {self.soyad}, kredit borcunuz mövcud deyil.")
            return False

    def kredit_ode(self, odenilen_mebleg):
        if self.kredit_icazesi:
            if (self.odenilen_mebleg >= self.ayliq_odenisler[self.odenis_sayi - 1]) or self.odenilen_mebleg == 0:
                if odenilen_mebleg <= self.balans:
                    if odenilen_mebleg >= self.ayliq_odenis:
                        self.balans -= odenilen_mebleg
                        self.odenilen_mebleg += odenilen_mebleg
                        self.qalan_borc = self.kredit_meblegi - self.odenilen_mebleg
                        self.odenis_sayi += 1
                        self.kredit_tarixcesi.append(f"{self.ad} {self.soyad}, {odenilen_mebleg} AZN kredit ödənişi etdi. Qalan borc: {self.qalan_borc:.2f} AZN")

                        if self.qalan_borc > 0:
                            print(f"{self.ad} {self.soyad}, {odenilen_mebleg} AZN kredit ödənişi etdiniz. Qalan borcunuz: {self.qalan_borc:.2f} AZN")
                        elif self.qalan_borc < 0:
                            print(f"{self.ad} {self.soyad}, artıq ödəniş etdiniz. Qalan borcunuz: {self.qalan_borc:.2f} AZN")
                        else:
                            print(f"{self.ad} {self.soyad}, kreditiniz bağlandı.")
                            self.kredit_icazesi = False
                    else:
                        if odenilen_mebleg == self.qalan_borc:
                            self.balans -= odenilen_mebleg
                            self.odenilen_mebleg += odenilen_mebleg
                            self.kredit_tarixcesi.append(f"{self.ad} {self.soyad}, {odenilen_mebleg} AZN kredit ödənişi etdi. Kredit bağlandı.")
                            print(f"{self.ad} {self.soyad}, kredit borcunuz bağlandı.")
                            self.kredit_icazesi = False
                            return True
                        else:
                            print(f"{self.ad} {self.soyad}, məbləğ aylıq ödənişdən azdır.")
                            return False
                else:
                    print(f"{self.ad} {self.soyad}, balansınızda yetərli vəsait yoxdur.")
                    return False
            else:
                print(f"{self.ad} {self.soyad}, minimum ödəniş: {self.ayliq_odenisler[self.odenis_sayi - 1] - self.odenilen_mebleg} AZN")
                return False
        else:
            print(f"{self.ad} {self.soyad}, kredit üçün müraciət edin.")

    def istifadeci_girisi(self):
        username = input("İstifadəçi adınızı daxil edin: ")
        password = input("Şifrənizi daxil edin: ")

        if username == "istifadeci" and password == "sifre":
            return True
        else:
            print("Yanlış istifadəçi adı və ya şifrə!")
            return False

# Nümunə istifadə
mustafa_hesabi = KreditHesabi(123456, "Mustafa", "Əliyev", 3000)
ivan_hesabi = KreditHesabi(789012, "İvan", "Petrov", 5000)

# Kredit götürmək
if mustafa_hesabi.istifadeci_girisi():
    if not mustafa_hesabi.kredit_gotur(10000):
        print("Mustafa üçün kredit götürmə əməliyyatı uğursuz oldu.")

if ivan_hesabi.istifadeci_girisi():
    if not ivan_hesabi.kredit_gotur(15000):
        print("İvan üçün kredit götürmə əməliyyatı uğursuz oldu.")

# Kredit ödəmək
if mustafa_hesabi.istifadeci_girisi():
    if not mustafa_hesabi.kredit_ode(1000):
        print("Mustafa üçün kredit ödəmə əməliyyatı uğursuz oldu.")

if ivan_hesabi.istifadeci_girisi():
    if not ivan_hesabi.kredit_ode(1500):
        print("İvan üçün kredit ödəmə əməliyyatı uğursuz oldu.")

# Balansları göstərmək
print(mustafa_hesabi)
print(ivan_hesabi)

# Kredit tarixçələrini göstərmək
mustafa_hesabi.kredit_tarixcesi_goster()
ivan_hesabi.kredit_tarixcesi_goster()

# Kredit borclarını göstərmək
if mustafa_hesabi.istifadeci_girisi():
    if not mustafa_hesabi.kredit_goster():
        print("Mustafa üçün kredit borcu göstərmə əməliyyatı uğursuz oldu.")

if ivan_hesabi.istifadeci_girisi():
    if not ivan_hesabi.kredit_goster():
        print("İvan üçün kredit borcu göstərmə əməliyyatı uğursuz oldu.")

# Balansdan pul çıxarmaq
if mustafa_hesabi.istifadeci_girisi():
    if not mustafa_hesabi.pul_cixar(2000):
        print("Mustafa üçün pul çıxarma əməliyyatı uğursuz oldu.")

if ivan_hesabi.istifadeci_girisi():
    if not ivan_hesabi.pul_cixar(1000):
        print("İvan üçün pul çıxarma əməliyyatı uğursuz oldu.")

# Balansları artırmaq
if mustafa_hesabi.istifadeci_girisi():
    mustafa_hesabi.balans_artir(3000)

if ivan_hesabi.istifadeci_girisi():
    ivan_hesabi.balans_artir(4000)
