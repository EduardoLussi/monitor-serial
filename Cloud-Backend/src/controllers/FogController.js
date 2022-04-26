const express = require('express');
const axios = require('axios');

const Fog = require('../models/Fog');

const router = express.Router();

router.get('/Fog/:id', async (req, res) => {
    let fogs = await Fog.findAll({ where: { user: req.params.id } });
    for (let i = 0; i < fogs.length; i++) {
        const res = await axios.get(fogs[i].dataValues.address).catch(error => {
            if (!error.response) {
                fogs.splice(i, 1);
                i--;
            }
        });
        
    }
    console.log(fogs);
    return res.json(fogs);
});

module.exports = router;