FROM php:8.2-apache
COPY src/   /var/www/html/
COPY tests/ /var/www/tests/
EXPOSE 80
