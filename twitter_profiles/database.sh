echo "CREATE DATABASE enwiki; GRANT ALL PRIVILEGES ON * . * TO 'root' @'localhost';" | mysql -u root -p 
mysql -u root -p enwiki < ~/Downloads/enwiki-latest-categorylinks.sql
mysql -u root -p enwiki < ~/Downloads/enwiki-latest-page.sql