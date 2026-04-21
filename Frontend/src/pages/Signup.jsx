import React, {useState} from "react";

function Signup(){
    const [email, setEmail]=useState("");
    const [password, setPassword]=useState("");

    const signup=async()=>{
        try{
            await fetch(
                `http://127.0.0.1:8000/signup?email=${email}&password=${password}`,
                {
                    method: "POST",
                }
            );
            alert("User Created!");
        } catch(err){
            console.error(err);
        }
    };

    return(
        <div>
            <h2>Signup</h2>

            <input
                placeholder="Email"
                onChange={(e)=>setEmail(e.target.value)}
            />

            <input
                type="password"
                placeholder="password"
                onChange={(e)=>setPassword(e.target.value)}
            />

            <button onClick={signup}>Signup</button>
        </div>
    );
}

export default Signup;