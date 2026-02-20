# HR API Proje aciklamasi

Dosyayı açtıktan sonra Docker'ı yüklemek gerekir.
Ubuntu'da aşağıdaki komutla tamamlanabilir.
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl enable --now docker

Proje klasöründe çalıştırılır.
docker compose up --build

Çalıştırdıktan sonra aşağıdaki linke girilir.
http://localhost:8000

Endpointleri test etmek için buraya bakılabilir.
http://localhost:8000/docs

Projeyi durdurmak için aşağıdaki komut yeterlidir.
docker compose down
