# İkinci Görev (Pozisyon Tespiti) İçin Sıfırdan Öğrenme Yol Haritası

> TEKNOFEST 2026 Havacılıkta Yapay Zekâ Yarışması — Görev 2: Pozisyon Tespiti

---

## 0. Bu Görev Aslında Ne?

Şartnameyi teknik literatüre çevirirsek: bu görev, bilgisayarlı görü alanında **"Monoküler Görsel Odometri" (Monocular Visual Odometry / Visual Ego-Motion Estimation)** olarak bilinen klasik bir problemdir. Drone'ların GPS'siz ortamda konum kestirimi yapması için kullanılan tekniklerle birebir aynı mantığı taşır (ör. PX4Flow gibi optik akış sensörleri).

**Neden zor?**
- Sadece kamera görüntüsü var, mesafe sensörü (lidar, radar) yok.
- Tek kameradan (monoküler) elde edilen harekette doğal bir **"ölçek belirsizliği" (scale ambiguity)** vardır: görüntüden sadece hareketin *yönünü* çıkarabilirsin, *büyüklüğünü* (metre cinsinden) çıkaramazsın — bunu başka bir ipucuyla (bilinen nesne boyutu, yer düzlemi varsayımı, öğrenilmiş model vb.) tamamlaman gerekir.
- Kamera açısı sabit değil (70-90°), irtifa değişebilir, görüntülerde bulanıklık/donma/piksel kaybı gibi bozulmalar olabilir.
- Hata metriği (Denklem 2), üç eksende referans ile tahmin arasındaki Öklid mesafesinin ortalamasıdır — SLAM/VO literatüründeki **ATE (Absolute Trajectory Error)** ile birebir aynı mantık.

**İki ana çözüm yaklaşımı** (şartname ikisine de izin veriyor):
1. **Klasik/Geometrik yaklaşım:** Öznitelik eşleştirme + epipolar geometri + poz kestirimi (yani "elle" matematik).
2. **Öğrenen model yaklaşımı:** CNN/RNN tabanlı uçtan uca konum regresyonu (DeepVO, PoseNet tarzı).

Aşağıdaki yol haritası seni **sıfırdan** başlatıp, önce klasik yaklaşımı anlayacak seviyeye, sonra istersen derin öğrenme yaklaşımına taşıyacak şekilde tasarlandı. Klasik yol daha açıklanabilir ve daha az veriyle çalışır; bu yüzden önce onu öğrenmeni öneririm.

---

## Aşama 1 — Programlama Temelleri (Python)

**Neden?** Bu alandaki hemen hemen tüm araçlar (OpenCV, NumPy, PyTorch) Python tabanlı. Ayrıca yarışma sunucusuyla JSON/HTTP üzerinden konuşacaksın, bu da programlama bilgisi gerektirir.

**Öğrenilecekler:**
- Python temel sözdizimi (değişkenler, döngüler, fonksiyonlar, sınıflar)
- NumPy ile dizi/matris işlemleri (görüntüler aslında sayı matrisidir)
- Dosya okuma/yazma, JSON ile çalışma
- `requests` kütüphanesi ile API/HTTP istekleri (sunucudan görüntü çekmek, sonuç göndermek için)

**Kaynaklar:**
- [Python Resmi Dokümantasyonu](https://docs.python.org/3/tutorial/) — temel referans
- freeCodeCamp – "Python for Beginners" (YouTube, ücretsiz, tam kurs)
- Corey Schafer – Python YouTube serisi (özellikle NumPy, JSON, requests videoları)
- [NumPy — Absolute Beginners Guide](https://numpy.org/doc/stable/user/absolute_beginners.html) (resmi, ücretsiz)
- "Automate the Boring Stuff with Python" — ücretsiz online kitap (automatetheboringstuff.com)
- [Python `requests` kütüphanesi dokümantasyonu](https://requests.readthedocs.io/)

---

## Aşama 2 — Matematik Temelleri (Lineer Cebir & 3D Geometri)

**Neden?** Görsel odometrinin tamamı matris/vektör işlemleridir: kamera hareketini bir dönüş matrisi (rotation) ve öteleme vektörü (translation) ile ifade edersin. Bu temelsiz sonraki aşamalar anlaşılmaz kalır.

**Öğrenilecekler:**
- Vektörler, matrisler, matris çarpımı, determinant, ters matris
- Dönüş matrisleri (rotation matrix), homojen koordinatlar
- Nokta çarpımı / çapraz çarpım (dot & cross product) — geometrik anlamları
- Koordinat sistemleri arası dönüşüm (kamera koordinatı ↔ dünya koordinatı)
- (İleri düzey, opsiyonel) Kuaterniyonlar, Euler açıları

**Kaynaklar:**
- [3Blue1Brown – "Essence of Linear Algebra"](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab) — YouTube, görsel ve sezgisel anlatım (şiddetle tavsiye edilir)
- [Khan Academy – Linear Algebra](https://www.khanacademy.org/math/linear-algebra) — ücretsiz, alıştırmalı
- MIT OCW 18.06 – Gilbert Strang, "Linear Algebra" (YouTube'da tam ders videoları)
- Cyrill Stachniss (Bonn Üniversitesi) – ["Photogrammetry I" YouTube playlist](https://www.youtube.com/@CyrillStachniss/playlists) içindeki koordinat dönüşümleri / homojen koordinatlar dersleri

---

## Aşama 3 — Görüntü İşleme Temelleri ve OpenCV

**Neden?** Öznitelik çıkarmadan, kamera modelini anlamadan önce "görüntü nedir, nasıl işlenir" bilmelisin. OpenCV, bu görevde kullanacağın ana kütüphane olacak.

**Öğrenilecekler:**
- Görüntünün piksel matrisi olarak temsili, renk uzayları (RGB, gri tonlama)
- Filtreleme (bulanıklaştırma, keskinleştirme), kenar tespiti (Canny, Sobel)
- Video kare (frame) okuma/yazma, ardışık karelerle çalışma
- Görüntü bozulmalarıyla başa çıkma (şartnamede bahsedilen bulanıklık, ölü piksel, donma gibi durumlar için ön işleme)

**Kaynaklar:**
- [OpenCV-Python Resmi Tutorials](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html) — en güvenilir kaynak
- freeCodeCamp – ["OpenCV Course – Full Tutorial with Python"](https://www.youtube.com/watch?v=oXlwWbU8l2o) (YouTube, ücretsiz tam kurs)
- "Programming Computer Vision with Python" — Jan Erik Solem, ücretsiz PDF (programmingcomputervision.com)
- PyImageSearch blog (Adrian Rosebrock) — pratik, kod odaklı OpenCV yazıları

---

## Aşama 4 — Kamera Modeli, Kalibrasyon ve Projektif Geometri

**Neden?** Şartnamede "hava aracının kamera parametre bilgileri yarışmacılarla paylaşılacaktır" deniyor — yani sana kameranın **intrinsic** (odak uzaklığı, optik merkez) parametreleri verilecek. Bunları nasıl kullanacağını bilmen şart. Ayrıca 3D dünyanın 2D görüntüye nasıl izdüşürüldüğünü (projection) anlamadan hareket kestirimi imkânsız.

**Öğrenilecekler:**
- İğne deliği (pinhole) kamera modeli
- İçsel (intrinsic) parametre matrisi K, dışsal (extrinsic) parametreler R, t
- Lens distorsiyonu ve düzeltilmesi
- Kamera kalibrasyonu (satranç tahtası yöntemi)
- Homografi (düzlemsel sahne dönüşümü) — yer düzlemine bakan bir kamera için kritik

**Kaynaklar:**
- **"Multiple View Geometry in Computer Vision"** — Hartley & Zisserman (bu alanın "İncil"i sayılır; 1-4 ve 9-11. bölümler bu görev için en kritik olanlar)
- Cyrill Stachniss – ["Photogrammetry I & II" YouTube playlist](https://www.youtube.com/@CyrillStachniss/playlists) — kamera modeli, kalibrasyon, homografi konuları çok net anlatılıyor
- Shree Nayar (Columbia Üniversitesi) – ["First Principles of Computer Vision"](https://www.youtube.com/@firstprinciplesofcomputerv3258) YouTube kanalı, "Camera Models" ve "Geometric Camera Models" playlist'leri
- [OpenCV Kamera Kalibrasyon Tutorial'ı](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html) (resmi)

---

## Aşama 5 — Öznitelik Tespiti, Eşleştirme ve Optik Akış

**Neden?** Görsel odometrinin ilk adımı: ardışık iki karede **aynı fiziksel noktaları** bulmaktır. Bunu iki şekilde yapabilirsin: (a) belirgin noktaları (köşe, kenar) tespit edip eşleştirerek, (b) optik akış ile piksellerin hareketini takip ederek. Drone'lar genelde optik akış tabanlı çalışır çünkü sahne genelde yer/zemin gibi düşük tekstürlü olabilir.

**Öğrenilecekler:**
- Köşe tespiti: Harris, Shi-Tomasi
- Öznitelik tanımlayıcıları: SIFT, ORB, AKAZE
- Eşleştirme yöntemleri: Brute-Force, FLANN
- Aykırı değer (outlier) temizleme: RANSAC
- Optik akış: Lucas-Kanade (seyrek), Farneback (yoğun)

**Kaynaklar:**
- [OpenCV – Feature Detection & Description Tutorials](https://docs.opencv.org/4.x/db/d27/tutorial_py_table_of_contents_feature2d.html)
- [OpenCV – Optical Flow Tutorial](https://docs.opencv.org/4.x/d4/dee/tutorial_optical_flow.html)
- Shree Nayar – "First Principles of Computer Vision" kanalındaki **Feature Detection** ve **Optical Flow** playlist'leri
- Cyrill Stachniss – RANSAC ve öznitelik eşleştirme dersleri (Photogrammetry II)
- PyImageSearch – "Feature Matching" ve "Optical Flow" pratik yazıları

---

## Aşama 6 — Epipolar Geometri ve Hareket Kestirimi (Klasik VO'nun Çekirdeği)

**Neden?** Burası klasik görsel odometrinin kalbi: iki kare arasındaki eşleşmiş noktalardan, kameranın **ne yöne döndüğünü ve ne yöne hareket ettiğini** matematiksel olarak çıkarırsın.

**Öğrenilecekler:**
- Epipolar geometri, temel matris (Fundamental Matrix) ve öz matris (Essential Matrix)
- 8-nokta algoritması
- `cv2.findEssentialMat` ve `cv2.recoverPose` fonksiyonları (OpenCV)
- Ölçek belirsizliği problemi (bir sonraki aşamada çözülecek)
- Basit bir "iki kare arası poz kestirimi" pipeline'ı kurmak

**Kaynaklar:**
- Hartley & Zisserman kitabı, 9-11. bölümler (Essential/Fundamental Matrix)
- Cyrill Stachniss – "Photogrammetry II" içindeki Epipolar Geometri dersleri
- [OpenCV `recoverPose` dokümantasyonu](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html)
- **Avi Singh – "Monocular Visual Odometry using OpenCV"** (blog + GitHub kod: `avisingh599/mono-vo`) — bu konuda en pratik, adım adım kodlu anlatımlardan biri; kesinlikle incelemeni öneririm

---

## Aşama 7 — Ölçek (Scale) Problemi ve Metrik Pozisyon Kestirimi

**Neden?** Bu, senin görevini diğer standart VO problemlerinden ayıran en kritik nokta: yarışma **metre cinsinden** x, y, z istiyor. Ama monoküler kameradan çıkardığın hareket bilgisi "yönü doğru, büyüklüğü belirsiz" bir vektördür. Bu belirsizliği kapatmak için bir "ölçek referansı" bulmalısın.

**Fikirler / öğrenilecekler:**
- Yer düzlemi (ground plane) varsayımı + bilinen kamera irtifası → homografi ile ölçek kestirimi
- **Şartnamedeki UAP/UAİ alanlarının çapının sabit 4,5 metre olduğunu biliyorsun** — görüntüde bu daireler görünüyorsa, piksel boyutundan gerçek dünya ölçeğini (metre/piksel) çıkarmak mümkün. Bu, bu yarışmaya özel çok değerli bir ipucu.
- Yapı-hareketten (Structure from Motion, SfM) temel kavramlar
- Video'nun ilk karelerindeki "yer değiştirme bilgisi" (translation_x/y/z, sağlıklıyken verilen) kullanılarak ölçek kalibrasyonu yapılması (şartname bunu zaten öneriyor)

**Kaynaklar:**
- Avi Singh'in mono-vo blog yazısındaki "ölçek" bölümü (pratik yaklaşım örneği)
- Google Scholar'da arama: *"monocular visual odometry scale recovery UAV"*, *"ground plane homography altitude estimation drone"*
- Cyrill Stachniss – Homografi ve düzlemsel sahne dersleri (Photogrammetry I)
- "Vision-based state estimation for UAVs" konulu akademik derleme (survey) makaleleri — Google Scholar'da bulunabilir

---

## Aşama 8 (Opsiyonel ama Rekabetçi Olmak İçin Önerilir) — Derin Öğrenme ile Pozisyon Kestirimi

**Neden?** Şartname "öğrenen modeller de kullanılabilir" diyor. Uçtan uca öğrenen bir model (CNN/RNN), görüntüdeki bulanıklık, ölü piksel, hava koşulları gibi gürültülere klasik yönteme göre daha dayanıklı olabilir ve eğitim verisinden ölçeği örtük şekilde öğrenebilir. Bu, klasik yöntemi tamamlayan/geliştiren bir katman olarak düşünülmeli.

**Öğrenilecekler:**
- Yapay sinir ağı temelleri, ileri/geri yayılım (forward/backpropagation)
- Evrişimli Sinir Ağları (CNN) — görüntüden öznitelik çıkarma
- Zaman serisi/dizisel modeller (RNN, LSTM) — ardışık karelerden hareket kestirimi için
- PyTorch ile model kurma, eğitme, kayıp fonksiyonu (regresyon için MSE)
- Önceden eğitilmiş modellerden transfer öğrenme (ResNet, FlowNet gibi omurgalar)

**Kaynaklar:**
- [PyTorch Resmi "60 Minute Blitz" ve Tutorials](https://pytorch.org/tutorials/) — resmi, pratik
- Andrew Ng – ["Deep Learning Specialization"](https://www.coursera.org/specializations/deep-learning) (Coursera) — teorik temel için çok sağlam
- Stanford CS231n – "Convolutional Neural Networks for Visual Recognition" (YouTube'da ücretsiz ders videoları + cs231n.stanford.edu notları)
- fast.ai – "Practical Deep Learning for Coders" (ücretsiz, uygulamalı)
- Makaleler (akademik, Google Scholar / arXiv üzerinden bulunabilir):
  - **DeepVO** (Wang et al., 2017) — CNN+RNN ile uçtan uca görsel odometri
  - **PoseNet** (Kendall et al., 2015) — CNN ile kamera poz regresyonu
  - **TartanVO** — genelleştirilebilir öğrenen VO modeli

---

## Aşama 9 — Hazır Görsel Odometri / SLAM Sistemlerini İnceleme

**Neden?** Sıfırdan yazmadan önce (veya kendi sistemini geliştirirken referans almak için) alanın en iyi açık kaynak sistemlerinin nasıl çalıştığını anlamak, hem fikir verir hem de "iskelet" olarak kullanılabilir.

**Öğrenilecekler / incelenecekler:**
- **ORB-SLAM3** — öznitelik tabanlı, en çok referans alınan açık kaynak SLAM/VO sistemi (GitHub: `UZ-SLAMLab/ORB_SLAM3`)
- **DSO (Direct Sparse Odometry)** — doğrudan (feature-free) yöntem örneği
- **VINS-Mono** — kamera + IMU birleşik VO (senin görevinde IMU yok ama pipeline mantığı öğretici)

**Kaynaklar:**
- Cyrill Stachniss – ["Robot Mapping / SLAM" YouTube playlist](https://www.youtube.com/@CyrillStachniss/playlists)
- **"Introduction to Visual SLAM: From Theory to Practice"** — Xiang Gao & Tao Zhang (kitap, kodlu örneklerle; İngilizce çevirisi ücretsiz PDF olarak bulunabilir) — çok pratik, adım adım C++/Python örnekli
- İlgili GitHub repoları (ORB-SLAM3, DSO) — README ve paper'ları okuyarak mimariyi kavrama

---

## Aşama 10 — Pratik Yapılacak Veri Setleri

**Neden?** Gerçek yarışma verisi yarışma gününe kadar paylaşılmayacak; bu yüzden benzer senaryolarda (havadan/aşağı bakan kamera, değişken irtifa, farklı hava koşulları) alıştırma yapman gerekiyor.

**Veri setleri:**
- **[KITTI Odometry Benchmark](https://www.cvlibs.net/datasets/kitti/eval_odometry.php)** — VO'nun standart test alanı (yerde araç, ama pipeline pratiği için ideal başlangıç)
- **[Mid-Air Dataset](https://midair.ulg.ac.be/)** — sentetik drone veri seti, **güneşli, bulutlu, kar gibi farklı hava koşulları** içeriyor; şartnamedeki senaryolara çok yakın
- **[TartanAir](https://theairlab.org/tartanair-dataset/)** — çeşitli/zorlu senaryolarda sentetik VO veri seti
- **[EuRoC MAV Dataset](https://projects.asl.ethz.ch/datasets/doku.php?id=kmavvisualinertialdatasets)** — drone görsel-eylemsizlik veri seti
- **[UZH-FPV Drone Racing Dataset](https://fpv.ifi.uzh.ch/)** — hızlı drone hareketleri
- **[VisDrone](http://aiskyeye.com/)** — havadan aşağı bakan drone görüntüleri (asıl olarak nesne tespiti içindir ama sahne/açı benzerliği için faydalı)

---

## Aşama 11 — Değerlendirme Metrikleri

**Neden?** Kendi geliştirdiğin algoritmayı yarışma kriterine (Denklem 2 — ortalama Öklid hatası) göre objektif olarak ölçmelisin.

**Öğrenilecekler:**
- ATE (Absolute Trajectory Error) ve RPE (Relative Pose Error) kavramları — şartnamedeki hata formülü ATE ile birebir aynı mantık
- Kestirilen ile referans yörüngeyi hizalama (alignment) ve karşılaştırma

**Kaynaklar:**
- **[`evo` Python paketi](https://github.com/MichaelGrupp/evo)** (Michael Grupp) — SLAM/VO yörünge değerlendirme aracı, doğrudan kullanılabilir
- [KITTI Odometry Değerlendirme Devkit'i](https://www.cvlibs.net/datasets/kitti/eval_odometry.php)
- TUM RGB-D Benchmark makalesi — ATE/RPE tanımlarının orijinal kaynağı (Sturm et al., 2012)

---

## Aşama 12 — Yarışmaya Özel Mühendislik Konuları

**Neden?** Algoritman ne kadar iyi olursa olsun, sunucuyla doğru şekilde konuşamazsan puan alamazsın.

**Öğrenilecekler:**
- `requests` ile JSON tabanlı API çağrıları yapma (GET ile kare alma, POST ile sonuç gönderme)
- Sıralı kare işleme mantığı (bir sonraki kareyi almadan önce mevcut kareye sonuç göndermek zorunlu olduğu için, senkron/asenkron akışı doğru kurgulama)
- `gps_health_status` mantığını doğru işleme (1 iken referans/kendi tahminini gönderebilirsin, 0 iken **mutlaka** kendi algoritmanla kestirmen gerekiyor — bu yüzden algoritman health=1 döneminde "kalibre olmalı")
- Görüntü bozulmalarına (blur, ölü piksel, donma, kare kaybı) karşı dayanıklı ön işleme / hata yönetimi

**Kaynaklar:**
- [Python `requests` Dokümantasyonu](https://requests.readthedocs.io/)
- [Python `json` modülü dokümantasyonu](https://docs.python.org/3/library/json.html)

---

## Önerilen Çalışma Sırası (Özet Tablo)

| # | Aşama | Tahmini Süre* | Öncelik |
|---|-------|---------------|---------|
| 1 | Python programlama | 2-3 hafta | Zorunlu |
| 2 | Lineer cebir & 3D geometri | 2-3 hafta | Zorunlu |
| 3 | Görüntü işleme + OpenCV | 2 hafta | Zorunlu |
| 4 | Kamera modeli & kalibrasyon | 2 hafta | Zorunlu |
| 5 | Öznitelik tespiti & optik akış | 2 hafta | Zorunlu |
| 6 | Epipolar geometri & poz kestirimi | 3 hafta | Zorunlu |
| 7 | Ölçek problemi çözümü | 2 hafta | Zorunlu |
| 8 | Derin öğrenme ile VO | 4+ hafta | Opsiyonel/İleri |
| 9 | Hazır SLAM/VO sistemleri incelemesi | 1-2 hafta | Önerilir |
| 10 | Veri setleriyle pratik | Sürekli | Zorunlu |
| 11 | Değerlendirme metrikleri | 3-4 gün | Zorunlu |
| 12 | Yarışma API entegrasyonu | 1 hafta | Zorunlu |

*Süreler, günde 1-2 saat düzenli çalışmayı varsayan kaba tahminlerdir; önceden programlama/matematik bilgisi varsa çok daha kısa sürer.

---

## Ekstra Stratejik İpuçları

- **Önce klasik yöntemle bir "baseline" (temel referans) sistem kur.** Çalışan bir feature-based VO pipeline'ın olsun; sonra üzerine derin öğrenme katarak iyileştirirsin.
- **UAP/UAİ alanlarının 4,5 metrelik sabit çapını ölçek kalibrasyonu için kullanmayı dene** — bu, şartnameye özel, çok değerli bir sabit referans.
- **Kamera açısının her zaman tam nadir (90°, tam aşağı) olmayacağını unutma** (70-90° aralığı) — yer düzlemi varsayımına dayalı yöntemlerde bu açıyı hesaba katmalısın.
- **"Sağlıklı" (health=1) dönemi bir kalibrasyon fırsatı olarak kullan:** İlk 1 dakika referans veri kesin sağlıklı — algoritmanı bu pencerede kendi kendine doğrulayıp parametrelerini (ör. ölçek faktörünü) ayarlayabilirsin.
- **Video bozulmalarına (blur, donma, ölü piksel) karşı test senaryoları oluştur** — Mid-Air veri setindeki farklı hava koşulu görüntüleri bunun için uygun.
- **`evo` paketiyle kendi test videolarında düzenli olarak hata ölçümü yap**, böylece yarışma formülüne (Denklem 2) yakın bir performans takibi yapmış olursun.

---

## Kısa Özet — Nereden Başlamalıyım?

1. Python + NumPy öğren.
2. 3Blue1Brown lineer cebir serisini izle.
3. OpenCV ile temel görüntü işleme yap.
4. Kamera modelini ve kalibrasyonu öğren.
5. Avi Singh'in mono-vo projesini adım adım takip ederek **çalışan bir klasik VO sistemi kur.**
6. Ölçek problemini çöz (UAP/UAİ çapı gibi ipuçlarıyla).
7. `evo` ile kendi sistemini test et.
8. Vaktin kalırsa, DeepVO/PoseNet tarzı bir derin öğrenme modeliyle iyileştirmeyi dene.
