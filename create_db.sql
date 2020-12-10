/* 
    Create Database and Role
*/
CREATE ROLE sudhan_flask CREATEDB LOGIN PASSWORD 'abc';

CREATE DATABASE sudhan_flask WITH OWNER sudhan_flask;
