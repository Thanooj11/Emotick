var express = require('express');
var pg = require("pg");
var app = express();
 
var connectionString = "postgres://postgres:password123@localhost:8000/emotick";
 
app.get('/', function (req, res, next) {
    pg.connect(connectionString,function(err,client,done) {
       if(err){
           console.log("not able to get connection "+ err);
           res.status(400).send(err);
       } 
       client.query('SELECT * FROM emotick where id = 1041', [1],function(err,result) {
           done(); // closing the connection;
           if(err){
               console.log(err);
               res.status(400).send(err);
           }
           res.status(200).send(result.rows);
       });
    });
});
 
app.listen(8000, function () {
    console.log('Server is running.. on Port 8000');
});
