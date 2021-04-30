const express = require('express');

const Fog = require('../models/Fog');

const router = express.Router();

router.get('/Fog/:id', async (req, res) => {
    const fogs = await Fog.findAll({ where: { user: req.params.id } });
    return res.json(fogs);
});

module.exports = router;