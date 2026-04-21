import React, {useState} from "react";

function Login(){
    const[email, setEmail]=useState("");
    const[password, setPassword]=useState("");

    const login=async()=>{
        try{
            const res=await fetch(
                `http://127.0.0.1:8000/login?email=${email}&password=${password}`,
                {
                    method: "POST",
                }
            );

            const data=await res.json();
            localStorage.setItem("token", data.access_token);

            alert("Login Successful!");
        }catch(err){
            console.error(err);
        }
    };

    return(
        <div>
            <h2>Login</h2>

            <input
                type="Email"
                placeholder="Email"
                onChange={(e)=>setEmail(e.target.value)}
            />

            <input
                type="password"
                placeholder="password"
                onChange={(e)=>setPassword(e.target.value)}
            />

            <button onClick={login}>Login</button>
        </div>
    );
}

export default Login;