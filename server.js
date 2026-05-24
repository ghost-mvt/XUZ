const express = require("express");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json());

// 🔥 Search API (Backend Proxy)
app.get("/api/search", (req, res) => {
    const q = req.query.q;

    if (!q) {
        return res.json({
            success: false,
            message: "No query provided"
        });
    }

    // Google Search URL (proxy logic)
    const googleURL = "https://www.google.com/search?q=" + encodeURIComponent(q);

    res.json({
        success: true,
        engine: "LIBY BACKEND SEARCH",
        query: q,
        url: googleURL
    });
});

// 🔥 status
app.get("/api/status", (req, res) => {
    res.json({
        status: "online",
        service: "LIBY SEARCH BACKEND"
    });
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
    console.log("LIBY SEARCH RUNNING");
});
