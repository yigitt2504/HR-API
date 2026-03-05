# HR API Project Description

We need to download Docker after opening the folder.
We use these codes to do it.

sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl enable --now docker

Run this code on the project folder itself.
docker compose up --build

After opening the UI at http://localhost:3000, you can use the following functions:

Employee Management – Add, update, or remove employees from the system.

All changes are automatically saved to the backend database, and the UI updates in real-time.

Use this code to stop the project.
docker compose down


# HR API Proje Açıklaması

Dosyayı açtıktan sonra Docker'ı yüklemek gerekir.
Ubuntu'da aşağıdaki komutlarla tamamlanabilir.

sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl enable --now docker

Proje klasöründe çalıştırılır.
docker compose up --build

http://localhost:3000 adresinde UI açıldıktan sonra aşağıdaki fonksiyonlar kullanılabilir:

Çalışan Yönetimi – Sisteme yeni çalışan ekleyebilir, mevcut çalışanları güncelleyebilir veya silebilirsiniz.

Yapılan tüm değişiklikler otomatik olarak backend veritabanına kaydedilir ve UI gerçek zamanlı olarak güncellenir.

Projeyi durdurmak için aşağıdaki komut yeterlidir.
docker compose down
