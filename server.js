const express = require("express");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json());

// API بسيطة
app.get("/api/status", (req, res) => {
    res.json({
        status: "online",
        vpn: "ready",
        time: new Date().toISOString()
    });
});

// مثال connect (محاكاة VPN)
app.post("/api/connect", (req, res) => {
    const { user } = req.body;

    if (!user) {
        return res.json({ success: false, message: "No user" });
    }

    return res.json({
        success: true,
        message: "VPN Connected",
        user: user,
        ip: "185.XXX.XXX.XX (mock)"
    });
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
    console.log("Server running on port " + PORT);
});
