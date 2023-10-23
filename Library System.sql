CREATE TABLE kitaplar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ad VARCHAR(255) NOT NULL,
    yazar VARCHAR(255) NOT NULL,
    yayin_tarihi DATE NOT NULL,
    kategori VARCHAR(255) NOT NULL
);kitaplar