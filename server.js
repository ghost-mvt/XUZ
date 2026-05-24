const express = require("express");
const cors = require("cors");
const fs = require("fs");
const { exec } = require("child_process");

const app = express();

app.use(cors());
app.use(express.json());

let users = [];

// 🔐 status
app.get("/api/status",(req,res)=>{
  res.json({
    system:"LIBY VPN PRO",
    status:"running",
    users: users.length
  });
});

// 👤 create user
app.post("/api/user/create",(req,res)=>{
  const user = {
    name:req.body.name,
    id:Date.now(),
    ip:"10.0.0." + (users.length+2)
  };

  users.push(user);

  res.json({
    success:true,
    user:user
  });
});

// 📡 connect user (real hook placeholder)
app.post("/api/connect",(req,res)=>{
  const user = users.find(u=>u.name === req.body.name);

  if(!user){
    return res.json({success:false,message:"User not found"});
  }

  // هنا لاحقاً تربط WireGuard
  res.json({
    success:true,
    message:"VPN Tunnel Ready",
    config:"wg-generated-config",
    ip:user.ip
  });
});

// 🌍 list users
app.get("/api/users",(req,res)=>{
  res.json(users);
});

const PORT = process.env.PORT || 3000;

app.listen(PORT,()=>{
  console.log("LIBY VPN PRO RUNNING");
});
