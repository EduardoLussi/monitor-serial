const express = require("express");
const cors = require("cors");

const FogController = require('./controllers/FogController');

const app = express();

const server = require('http').Server(app);

app.use(cors());

app.use(FogController);

server.listen(3333);