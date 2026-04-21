import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ChatBox from "./components/ChatBox";
import Login from "./pages/Login";
import Signup from "./pages/Signup";

function App(){
    return(
        <Router>
            <Routes>
                <Route path="/" element={<Login/>} />
                <Route path="/signup" element={<Signup/>} />
                <Route path="/chat" element={<ChatBox/>} />
            </Routes>
        </Router>
    );
}

export default App;