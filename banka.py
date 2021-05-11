
# coding=utf-8
#Developer:Kerem YAĞAN https://github.com/keremyagan
#Öneri/Şikayet/Destek/İzin için bana ulaşın.
import json
import re
import os
import datetime
class Banka: 
    def __init__(self,tc_giris):
        self.kayityeri=""#varsayılan kayıt yeri python dosyalarının kaydedildiği yerdir,değiştirebilirsiniz
        self.tc_giris=tc_giris
        self.liste=[]

    @staticmethod
    def hata():
        print("Lütfen Sadece Sayısal Değer Giriniz.")
    def girisyapma(self,tc_giris):
        sifre_giris=input("Şifre Giriniz:")
        file=open(self.kayityeri+"Banka/"+str(tc_giris)+".txt","r",encoding="utf-8")
        icerik=file.read()
        icerik_json=json.loads(icerik)
        if icerik_json["Tc No"] == str(tc_giris) and icerik_json["Sifre"] == sifre_giris :
            print(f"Giriş Başarılı. Hoşgeldin {icerik_json['Ad']} . ")
            file.close()
            file=open(self.kayityeri+"Banka/"+str(tc_giris)+"_detaylar.txt","r",encoding="utf-8")
            icerik_detaylar=file.read()
            icerik_detaylar_json=json.dumps(icerik_detaylar)
            index=icerik_detaylar_json.find(sifre_giris)
            file.seek(index)
            islem_json=file.read()
            self.liste.append(islem_json)
            self.banka_islem(tc_giris)
          
            
        else :
            print("Giriş Hatalı. Lütfen Bilgileri Kontrol Ederek Yeniden Deneyiniz.")
                        
    def kayit(self,tc_no):
        ad=input("Adınızı Giriniz:")
        soyad=input("Soyadınızı Giriniz:")
               
        while True :
            bakiye=(input("Bakiye Giriniz:"))
            try :
                int(bakiye)
                break
            except  :
                self.hata()
                
        while True :
            ek_bakiye=(input("Ek Bakiye Giriniz:"))
            try :
                int(ek_bakiye)
                break
            except  :
                self.hata()
                
        while True :
            sifre=input("Şifre Giriniz(En Az 1 Büyük Harf,Bir Rakam ve Bir Noktalama İşareti İçermelidir,En Az 7 Karakter Olmalıdır):")
            if  (re.search("[A-Z]",sifre) and re.search("[1-9]",sifre) and   re.search("[.@,!'^+%&/()=?*-]",sifre) and (len(sifre) > 7)):
                break 
        print(f"{ad} {soyad} Kullanıcısı Oluşturuldu... ")
        bilgiler={
            "Ad" : ad ,
            "Soyad" : soyad ,
            "Tc No" : tc_no ,
            "Bakiye" : bakiye ,
            "Ek Bakiye" : ek_bakiye ,
            "Sifre" : sifre
        }


        dosya_kontrol =os.path.exists(self.kayityeri+"Banka")
        if dosya_kontrol == False :
            os.mkdir(self.kayityeri+"Banka")
        file=open(self.kayityeri+"Banka/"+str(tc_no)+".txt","w",encoding="utf-8")
        bilgiler_json=json.dumps(bilgiler)
        file.write(bilgiler_json)   
        file.close()
        print(f"{ad} {soyad} Kullanıcısı Kaydedildi... ")
        
        self.islem_detay(tc_no)
                    
    def banka_islem(self,tc_giris) :
        while True : 
            print("İŞLEMLER".center(60,"-"))
            while True:
                try:
                    islem_no=int(input("1-Para Çekme\n2-Para Yatırma\n3-Havale/EFT\n4-Şifre Değiştirme\n5-Bakiye Ek Bakiye Arası Para Transferi\n6-Çıkış\nSeçiminiz:"))
                    break
                except:
                    self.hata()
            if islem_no == 1 : #para çekme
                self.para_cekme(tc_giris)
                
            elif islem_no == 2 : #para yatırma
                self.para_yatirma(tc_giris)
            
            elif islem_no == 3 : #havale/eft
                self.para_transfer(tc_giris)
            elif islem_no==4: #şifre değiştirme
                self.sifre_degistirme(tc_giris)
            elif islem_no == 5 :
                self.bakiye_degisim(tc_giris)
            elif islem_no == 6 :
                break
                      
    def para_yatirma(self,tc_giris) :
        
        file=open(self.kayityeri+"Banka/"+str(tc_giris)+".txt","r",encoding="utf-8")
        icerik=file.read()
        
        icerik_json=json.loads(icerik)
        print(f"Hesabınızdaki:\nBakiye:{icerik_json['Bakiye']}'dir\nEk Bakiye:{icerik_json['Ek Bakiye']}'dir. ")
        while True:
            try:
                yat_para=int(input("Yatırmak İstediğiniz Miktarı Giriniz:"))
                break
            except:
                self.hata()
        file=open(self.kayityeri+"Banka/"+str(tc_giris)+".txt","r+",encoding="utf-8")
        guncel_para=yat_para+int(icerik_json["Bakiye"])
        icerik_json["Bakiye"] = guncel_para
        file.close()
        file=open(self.kayityeri+"Banka/"+str(tc_giris)+".txt","w",encoding="utf-8")
        yeni_icerik=json.dumps(icerik_json)
        
        file.write(yeni_icerik)
        file.close()
        icerik_jsonn=json.loads(yeni_icerik)
        file=open(self.kayityeri+"Banka/"+str(tc_giris)+"_detaylar"+".txt","w",encoding="utf-8")
        icerik_detay=(f"Ad:{icerik_jsonn['Ad']}\nSoyad:{icerik_jsonn['Soyad']}\nTc No:{icerik_jsonn['Tc No']}\nBakiye:{icerik_jsonn['Bakiye']}\nEk Bakiye:{icerik_jsonn['Ek Bakiye']}\nŞifre:{icerik_jsonn['Sifre']}\n")
        file.write(icerik_detay)
        file.close()
        time=datetime.datetime.now()
        
        gelenbilgi=(f"İşlem Adı:Para Yatırma Yatırılan Miktar:{yat_para} Güncel Bakiye:{icerik_json['Bakiye']} Güncel Ek Bakiye:{icerik_json['Ek Bakiye']} İşlem Zamanı:{time}\n")
        self.liste.append(gelenbilgi)
        self.islem_hareketi(tc_giris)
        print(f"Para Yatırma İşlemi Başarılı. Hesabınızdaki Güncel Bakiye:{icerik_json['Bakiye']} ")

    def para_cekme(self,tc_giris) :
        
        file=open(self.kayityeri+"Banka/"+str(tc_giris)+".txt","r",encoding="utf-8")
        icerik=file.read()
        icerik_json=json.loads(icerik)
        print(f"Hesabınızdaki:\nBakiye:{icerik_json['Bakiye']}'dir\nEk Bakiye:{icerik_json['Ek Bakiye']}'dir. ")
        while True:
            try:
                cek_para=int(input("Çekmek İstediğiniz Para Miktarını Giriniz:"))
                break
            except:
                self.hata()
        if (cek_para < int(icerik_json["Bakiye"])) or   (cek_para == int(icerik_json["Bakiye"])) :
            guncel_para=int(icerik_json["Bakiye"])-cek_para
            (icerik_json["Bakiye"]) = guncel_para
            file.close()
            file=open(self.kayityeri+"Banka/"+str(tc_giris)+".txt","w",encoding="utf-8")
            yeni_icerik=json.dumps(icerik_json)
            file.write(yeni_icerik)
            file.close()
            icerik_jsonn=json.loads(yeni_icerik)
            file=open(self.kayityeri+"Banka/"+str(tc_giris)+"_detaylar"+".txt","w",encoding="utf-8")
            icerik_detay=(f"Ad:{icerik_jsonn['Ad']}\nSoyad:{icerik_jsonn['Soyad']}\nTc No:{icerik_jsonn['Tc No']}\nBakiye:{icerik_jsonn['Bakiye']}\nEk Bakiye:{icerik_jsonn['Ek Bakiye']}\nŞifre:{icerik_jsonn['Sifre']}\n")
            file.write(icerik_detay)
            
            file.close()
            time=datetime.datetime.now()
            gelenbilgi=(f"İşlem Adı:Para Çekme Çekilen Miktar:{cek_para} Güncel Bakiye:{icerik_json['Bakiye']} Güncel Ek Bakiye:{icerik_json['Ek Bakiye']} İşlem Zamanı:{time}\n")
            self.liste.append(gelenbilgi)
            self.islem_hareketi(tc_giris)
            print(f"Para Çekme İşlemi Başarılı. Hesabınızdaki Güncel Bakiye:{icerik_json['Bakiye']} ")
            
        else :
            while True : 
                while True:
                    try:
                        kullanilsin=int(input("1-Ek Bakiye Kullanılsın\n2-Ek Bakiye Kullanılmasın,Çıkış Yap\nSeçiminiz:"))
                        break 
                    except:
                        self.hata()
                if kullanilsin == 2 :
                    break
                elif kullanilsin == 1 :
                    if (cek_para < int(icerik_json["Ek Bakiye"])+int(icerik_json["Bakiye"])) or   (cek_para == int(icerik_json["Ek Bakiye"])+int(icerik_json["Bakiye"])) :
                        guncel_para=int(icerik_json["Bakiye"])+int(icerik_json["Ek Bakiye"])-cek_para
                        icerik_json["Bakiye"] = 0
                        icerik_json["Ek Bakiye"] = guncel_para
                        file.close()
                        file=open(self.kayityeri+"Banka/"+str(tc_giris)+".txt","w",encoding="utf-8")
                        yeni_icerik=json.dumps(icerik_json)
                        file.write(yeni_icerik)
                        file.close()
                        icerik_jsonn=json.loads(yeni_icerik)
                        file=open(self.kayityeri+"Banka/"+str(tc_giris)+"_detaylar"+".txt","w",encoding="utf-8")
                        icerik_detay=(f"Ad:{icerik_jsonn['Ad']}\nSoyad:{icerik_jsonn['Soyad']}\nTc No:{icerik_jsonn['Tc No']}\nBakiye:{icerik_jsonn['Bakiye']}\nEk Bakiye:{icerik_jsonn['Ek Bakiye']}\nŞifre:{icerik_jsonn['Sifre']}\n")
                        file.write(icerik_detay)
                        file.close()
                        time=datetime.datetime.now()
                        gelenbilgi=(f"İşlem Adı:Para Çekme Çekilen Miktar:{cek_para} Güncel Bakiye:{icerik_json['Bakiye']} Güncel Ek Bakiye:{icerik_json['Ek Bakiye']} İşlem Zamanı:{time}\n")
                        self.liste.append(gelenbilgi)
                        self.islem_hareketi(tc_giris)
                        print(f"Para Çekme İşlemi Başarılı. Hesabınızdaki Güncel Bakiye:0 Güncel Ek Bakiye:{icerik_json['Ek Bakiye']} ")
                        break
                    else :
                        print("Hesabınızda Yeterli Para Bulunmamaktadır...")
                else :
                    print("Lütfen 1 ya da 2 Değerlerini Giriniz:")

    def para_transfer(self,tc_giris):
          
        file=open(self.kayityeri+"Banka/"+str(tc_giris)+".txt","r",encoding="utf-8")
        icerik=file.read()
        icerik_json=json.loads(icerik)
        file.close()
        print(f"Hesabınızdaki:\nBakiye:{icerik_json['Bakiye']}'dir\nEk Bakiye:{icerik_json['Ek Bakiye']}'dir. ")
        toplam_para=int(icerik_json["Bakiye"])+int(icerik_json["Ek Bakiye"])
        print(f"En Fazla {toplam_para} TL Gönderebilirsiniz. %2 Transfer Ücreti Alınmaktadır. ")
        while True:
            try:
                transfer_para=int(input("Transfer Etmek İstedğiniz Para Miktarını Giriniz:"))
                break
            except:
                self.hata()
        if (transfer_para < toplam_para or transfer_para == toplam_para) :
            while True:
                try:
                    transfer_hesap=int(input("Para Transfer Etmek İstedğiniz Hesap Sahibinin Tc Numarasını Giriniz:"))
                    break
                except:
                    self.hata()
            if transfer_hesap == int(icerik_json["Tc No"]) :
                print("Kendi Hesabınıza Transfer Yapamazsınız.Bakiye/Ek Bakiye Ayarları İçin Üst Menüden 5'i Tuşlayınız")
            else :
                dosya_kontrol =os.path.exists(self.kayityeri+"Banka/"+str(transfer_hesap)+".txt")
                if dosya_kontrol == False :
                    print("Girdiğiniz Bilgiler İle Eşleşen Hesap Sahibi Bulunamadı.Lütfen Tekrar Deneyiniz...")
                else :

                    file=open(self.kayityeri+"Banka/"+str(transfer_hesap)+".txt","r",encoding="utf-8")
                    icerik1=file.read()
                    file.close()
                    icerik_json1=json.loads(icerik1)
                    print(f"Hesap Sahibi:{icerik_json1['Ad']} {icerik_json1['Soyad']} ")
                    islem_onay=input("İşlemi Onaylamak İçin 'evet' Çıkmak İçin 'hayır' Yazınız:")
                    if islem_onay.lower() == "evet" : 
                        kesinti=transfer_para*2/100
                        transfer_guncelpara=transfer_para-kesinti
                        file.close()
                        icerik_json1["Bakiye"]=int(icerik_json1["Bakiye"])+transfer_guncelpara
                        file=open(self.kayityeri+"Banka/"+str(transfer_hesap)+".txt","r",encoding="utf-8")
                        transfer_icerik=file.read()
                        transfer_icerik_json=json.loads(transfer_icerik)
                        transfer_icerik_json["Bakiye"]=transfer_guncelpara+float(transfer_icerik_json["Bakiye"])
                 
                        file.close()
                        time=datetime.datetime.now()
                        gelenbilgi=(f"İşlem Adı:Para Transferi Gönderen:{icerik_json['Ad']} {icerik_json['Soyad']} Transfer Miktarı:{transfer_guncelpara} Güncel Bakiye:{transfer_icerik_json['Bakiye']} Güncel Ek Bakiye:{transfer_icerik_json['Ek Bakiye']} İşlem Zamanı:{time}\n")
                        file=open(self.kayityeri+"Banka/"+str(transfer_hesap)+"_detaylar.txt","a",encoding="utf-8")
                        file.write(gelenbilgi)
                        file.close()
                        file=open(self.kayityeri+"Banka/"+str(transfer_hesap)+".txt","w",encoding="utf-8")
                        transfer_son_icerik1=json.dumps(transfer_icerik_json)
                        file.write(transfer_son_icerik1)
                        file.close()
                        file=open(self.kayityeri+"Banka/"+str(tc_giris)+".txt","r",encoding="utf-8")
                        gonderen_icerik=file.read()
                        gonderen_icerik_json=json.loads(gonderen_icerik)
                        gonderen_icerik_json["Bakiye"]=toplam_para-transfer_para
                        gonderen_icerik_json["Ek Bakiye"] = 0
                        son_gonderen_icerik=json.dumps(gonderen_icerik_json)

                        file=open(self.kayityeri+"Banka/"+str(tc_giris)+".txt","w",encoding="utf-8")
                        file.write(son_gonderen_icerik)
                        file.close()
                        icerik_jsonn=json.loads(son_gonderen_icerik)
                        file=open(self.kayityeri+"Banka/"+str(tc_giris)+"_detaylar"+".txt","w",encoding="utf-8")
                        icerik_detay=(f"Ad:{icerik_jsonn['Ad']}\nSoyad:{icerik_jsonn['Soyad']}\nTc No:{icerik_jsonn['Tc No']}\nBakiye:{icerik_jsonn['Bakiye']}\nEk Bakiye:{icerik_jsonn['Ek Bakiye']}\nŞifre:{icerik_jsonn['Sifre']}\n")
                        file.write(icerik_detay)
                        file.close()
                        time=datetime.datetime.now()
                        gelenbilgi=(f"İşlem Adı:Para Transferi Transfer Yapılan Kişi:{icerik_json1['Ad']} {icerik_json1['Soyad']} Transfer Miktarı:{transfer_para} Güncel Bakiye:{icerik_jsonn['Bakiye']} Güncel Ek Bakiye:{icerik_jsonn['Ek Bakiye']} İşlem Zamanı:{time}\n")
                        self.liste.append(gelenbilgi)
                        self.islem_hareketi(tc_giris)

                        print("Para Transfer İşlemi Başarılı")

                    else :
                        print("Çıkış Yapıldı...")

        else :
            print("Yeterli Paraya Sahip Değilsiniz")

    def sifre_degistirme(self,tc_giris) :
        file=open(self.kayityeri+"Banka/"+str(tc_giris)+".txt","r",encoding="utf-8")
        icerik=file.read()
        icerik_json=json.loads(icerik)
        eski_sifre=icerik_json['Sifre']
        while True :
            yeni_sifre=input("Şifre Giriniz(En Az 1 Büyük Harf,Bir Rakam ve Bir Noktalama İşareti İçermelidir,En Az 7 Karakter Olmalıdır):")
            if  (re.search("[A-Z]",yeni_sifre) and re.search("[1-9]",yeni_sifre) and   re.search("[.@,!'^+%&/()=?*-]",yeni_sifre) and (len(yeni_sifre) > 7)):
                if eski_sifre == yeni_sifre :
                    print("Yeni Şifreniz Eski Şifreniz İle Aynı Olamaz...")
                
                else :
                    print("Şifreniz Oluşturuldu...")
                    file=open(self.kayityeri+"Banka/"+str(tc_giris)+".txt","r",encoding="utf-8")
                    icerik=file.read()
                    icerik_json=json.loads(icerik)
                    
                    icerik_json["Sifre"]=yeni_sifre
                    yeni_sifre_icerik=icerik_json
                    file.close()
                    file=open(self.kayityeri+"Banka/"+str(tc_giris)+".txt","w",encoding="utf-8")
                    yeni_sifre_icerik_json=json.dumps(yeni_sifre_icerik)
                    file.write(yeni_sifre_icerik_json)
                    file.close()
                    icerik_jsonn=json.loads(yeni_sifre_icerik_json)
                    file=open(self.kayityeri+"Banka/"+str(tc_giris)+"_detaylar"+".txt","w",encoding="utf-8")
                    icerik_detay=(f"Ad:{icerik_jsonn['Ad']}\nSoyad:{icerik_jsonn['Soyad']}\nTc No:{icerik_jsonn['Tc No']}\nBakiye:{icerik_jsonn['Bakiye']}\nEk Bakiye:{icerik_jsonn['Ek Bakiye']}\nŞifre:{icerik_jsonn['Sifre']}\n")
                    file.write(icerik_detay)
                    file.close()
                    file=open(self.kayityeri+"Banka/"+str(tc_giris)+"_detaylar.txt","r",encoding="utf-8")
                    icerik_detaylar=file.read()
                    icerik_detaylar_json=json.dumps(icerik_detaylar)
                    index=icerik_detaylar_json.find(yeni_sifre)
                    file.seek(index)
                    islemdetay=file.read()
                    self.liste.append(islemdetay)
                    time=datetime.datetime.now()
                    gelenbilgi=(f"İşlem Adı:Şifre Değiştirme Eski Şifre:{eski_sifre} Yeni Şifre:{yeni_sifre} İşlem Zamanı:{time}\n")
                    self.liste.append(gelenbilgi)
                    self.islem_hareketi(tc_giris)
                    print("Şifreniz Kaydedildi")
                    break
    
    def bakiye_degisim(self,tc_giris): #bakiyeden ekbakiyeye ya da tam tersi şekilde para transferi
        file=open(self.kayityeri+"Banka/"+str(tc_giris)+".txt","r",encoding="utf-8")
        icerik=file.read()
        icerik_json=json.loads(icerik)
        print(f"Güncel Bakiye:{icerik_json['Bakiye']} Güncel Ek Bakiye:{icerik_json['Ek Bakiye']} ")
        while True:
            try:
                transfer_yeri=int(input("1-Bakiyeden Ek Bakiyeye Transfer\n2-Ek Bakiyeden Bakiyeye Transfer\nSeçiminiz:"))
                break 
            except:
                self.hata()
        if transfer_yeri == 1:
            while True:
                try:
                    bakiyeden_miktar=int(input("Transfer Etmek İstediğiniz Miktarı Giriniz:"))
                    break
                except:
                    self.hata()
            if bakiyeden_miktar > icerik_json["Bakiye"] :
                print("Bakiyede Bulunan Para Miktarından Fazlasını Transfer Edemezsiniz...")
            else :
                icerik_json["Bakiye"]= int(icerik_json['Bakiye'])-bakiyeden_miktar
                icerik_json["Ek Bakiye"] = int(icerik_json['Ek Bakiye'])+bakiyeden_miktar
                son_icerik=icerik_json
                son_icerik_json=json.dumps(icerik_json)
                file.close()
                file=open(self.kayityeri+"Banka/"+str(tc_giris)+".txt","w",encoding="utf-8")
                file.write(son_icerik_json)
                file.close()
                icerik_jsonn=json.loads(son_icerik_json)
                file=open(self.kayityeri+"Banka/"+str(tc_giris)+"_detaylar"+".txt","w",encoding="utf-8")
                icerik_detay=(f"Ad:{icerik_jsonn['Ad']}\nSoyad:{icerik_jsonn['Soyad']}\nTc No:{icerik_jsonn['Tc No']}\nBakiye:{icerik_jsonn['Bakiye']}\nEk Bakiye:{icerik_jsonn['Ek Bakiye']}\nŞifre:{icerik_jsonn['Sifre']}\n")
                file.write(icerik_detay)
                file.close()
                file=open(self.kayityeri+"Banka/"+str(tc_giris)+".txt","r",encoding="utf-8")
                icerikk=file.read()
                icerikk_json=json.loads(icerikk)
                time=datetime.datetime.now()
                gelenbilgi=(f"İşlem Adı:Bakiyeden Ek Bakiyeye Transfer Transfer Miktarı:{bakiyeden_miktar} İşlem Zamanı:{time}\n")
                self.liste.append(gelenbilgi)
                self.islem_hareketi(tc_giris)
                print(f"Güncel Bakiye:{icerikk_json['Bakiye']} Güncel Ek Bakiye:{icerikk_json['Ek Bakiye']} ")
        
        elif transfer_yeri == 2 :
            while True:
                try:
                    ek_bakiyeden_miktar=int(input("Transfer Etmek İstediğiniz Miktarı Giriniz:"))
                    break
                except:
                    self.hata()
            if ek_bakiyeden_miktar > icerik_json["Ek Bakiye"] :
                print("Ek Bakiyede Bulunan Para Miktarından Fazlasını Transfer Edemezsiniz...")
            else :
                icerik_json["Bakiye"]= int(icerik_json['Bakiye'])+ek_bakiyeden_miktar
                icerik_json["Ek Bakiye"] = int(icerik_json['Ek Bakiye'])-ek_bakiyeden_miktar
                son_icerik=icerik_json
                son_icerik_json=json.dumps(icerik_json)
                file.close()
                file=open(self.kayityeri+"Banka/"+str(tc_giris)+".txt","w",encoding="utf-8")
                file.write(son_icerik_json)
                file.close()
                icerik_jsonn=json.loads(son_icerik_json)
                file=open(self.kayityeri+"Banka/"+str(tc_giris)+"_detaylar"+".txt","w",encoding="utf-8")
                icerik_detay=(f"Ad:{icerik_jsonn['Ad']}\nSoyad:{icerik_jsonn['Soyad']}\nTc No:{icerik_jsonn['Tc No']}\nBakiye:{icerik_jsonn['Bakiye']}\nEk Bakiye:{icerik_jsonn['Ek Bakiye']}\nŞifre:{icerik_jsonn['Sifre']}\n")
                file.write(icerik_detay)
                file.close()
                file=open(self.kayityeri+"Banka/"+str(tc_giris)+".txt","r",encoding="utf-8")
                icerikk=file.read()
                icerikk_json=json.loads(icerikk)
                time=datetime.datetime.now()
                gelenbilgi=(f"İşlem Adı:Ek Bakiyeden Bakiyeye Transfer Transfer Miktarı:{ek_bakiyeden_miktar} İşlem Zamanı:{time}\n")
                self.liste.append(gelenbilgi)
                self.islem_hareketi(tc_giris)
                print(f"Güncel Bakiye:{icerikk_json['Bakiye']} Güncel Ek Bakiye:{icerikk_json['Ek Bakiye']} ")

        else :
            print("Hatalı Giriş Yaptınız. Lütfen Tekrar Deneyiniz...")

    def islem_detay(self,tc_no) :
        file=open(self.kayityeri+"Banka/"+str(tc_no)+".txt","r",encoding="utf-8")
        icerik=file.read()
        icerik_json=json.loads(icerik)
        icerik_detay=(f"Ad:{icerik_json['Ad']}\nSoyad:{icerik_json['Soyad']}\nTc No:{icerik_json['Tc No']}\nBakiye:{icerik_json['Bakiye']}\nEk Bakiye:{icerik_json['Ek Bakiye']}\nŞifre:{icerik_json['Sifre']}\n")
        file.close()
        file=open(self.kayityeri+"Banka/"+str(tc_no)+"_detaylar"+".txt","w",encoding="utf-8")
        file.write(icerik_detay)
        time=datetime.datetime.now()
        detaylar=(f"İşlem Adı:Hesap Oluşturuldu İşlem Saati:{time}\n")
        file.write(detaylar)
        file.close()
            
    def islem_hareketi(self,tc_giris) :
        file=open(self.kayityeri+"Banka/"+str(tc_giris)+"_detaylar"+".txt","a",encoding="utf-8")
        file.writelines(self.liste)



def menu() :
    while True :     
        while True:
            try:
                secim=int(input("1-Giriş Yapınız\n2-Kullanıcı Oluşturunuz\n3-Çıkış\nSeçiminiz:"))            
                break
            except:
                print("Lütfen 1-3 Aralığında Değer Giriniz.")
        if secim == 3 :
            break 
        elif secim == 1 : #giriş yapma
            while True :               
                try :
                    tc_giris=int(input("TC No Giriniz:"))
                    break
                except :
                    print("Lütfen Sayısal Değer Giriniz...")
            banka=Banka(tc_giris)
            banka.girisyapma(tc_giris)
            break
        elif secim == 2 : #kullanıcı oluşturma
            while True :
                tc_no=(input("TC No Giriniz:"))
                try :
                    int(tc_no)
                    break
                except  :
                    print("Lütfen Sayısal Değer Giriniz...")
            banka=Banka(tc_giris=tc_no)
            banka.kayit(tc_no)
            break
        

        else :
            print("Hatalı Giriş Yaptınız. Lütfen 1 ile 3 arasında rakam giriniz...")

menu()
