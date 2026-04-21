import React, {useState} from "react";
import ChatBox from "./components/ChatBox";
import Login from "./pages/Login";
import Signup from "./pages/Signup";

function App(){
    const [isLoggedIn, setIsLoggedIn]=useState(
        !!localStorage.getItem("token")
    );

    return(
        <div>
            {!isLoggedIn ? (
                <>
                <Signup />
                <Login setIsLoggedIn={setIsLoggedIn} />
                </>
            ) : (
                <ChatBox />
            )}
        </div>
    );
}

export default App;