const express = require('express');
const bodyParser = require('body-parser');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const cors = require('cors');
const { Admin } = require('./db'); // Importing the Admin model from db.js

const app = express();
const PORT = 8005; // Backend port
const SECRET_KEY = 'your_secret_key';

app.use(bodyParser.json());
app.use(cors({ origin: '*' }));

// Login route
app.post('/admin/login', async (req, res) => {
    const { username, password } = req.body;

    try {
        const admin = await Admin.findOne({ where: { username } });
        if (!admin) return res.status(404).json({ error: 'Admin not found' });

        const validPassword = await bcrypt.compare(password, admin.password);
        if (!validPassword) return res.status(401).json({ error: 'Invalid password' });

        const token = jwt.sign({ username }, SECRET_KEY, { expiresIn: '1h' });
        res.json({ token });
    } catch (error) {
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Start server
app.listen(PORT, () => {
    console.log(`Authentication service running on port ${PORT}`);
});
