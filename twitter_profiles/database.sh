echo "CREATE DATABASE enwiki; GRANT ALL PRIVILEGES ON * . * TO 'root' @'localhost';" | mysql -u root -p 
cat  precommit.sh ~/Downloads/enwiki-latest-categorylinks.sql postcommit.sh | mysql -u root -p enwiki
cat  precommit.sh ~/Downloads/enwiki-latest-page.sql postcommit.sh | mysql -u root -p enwiki