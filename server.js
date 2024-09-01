// server.js
require('dotenv').config();
const express = require('express');
const app = express();
const path = require('path');
const port = process.env.PORT || 3000;

app.use(express.static(path.join(__dirname, 'public'))); // 'public' ফোল্ডার থেকে স্ট্যাটিক ফাইল সার্ভ করা

// API রুট যা .env থেকে টোকেন প্রদান করে
app.get('/get-token', (req, res) => {
    res.json({ TELEGRAM_BOT_TOKEN: process.env.TELEGRAM_BOT_TOKEN });
});

app.listen(port, () => {
    console.log(`Server চলছে পোর্ট ${port} এ`);
});