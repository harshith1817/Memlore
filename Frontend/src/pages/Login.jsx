import React, {useState} from "react";
import styled from "styled-components";
import { useNavigate } from "react-router-dom";
import { FaGoogle, FaGithub } from "react-icons/fa";

const Container = styled.div`
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  background: #0f172a;
`;

const Card = styled.div`
  width: 25%;
  height: 67.5%;
  background: #1e293b;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
`;

const Title = styled.h2`
  text-align: center;
  color: #38bdf8;
  margin-bottom: 20px;
`;

const InputDiv = styled.input`
  width: 94%;
  padding: 12px;
  border-radius: 0.7rem;
  border: none;
  outline: none;
  background: #334155;
  color: white;
`;

const Button = styled.button`
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 0.7rem;
  background: #2563eb;
  color: white;
  cursor: pointer;

  &:hover {
    background: #1d4ed8;
  }
`;

const LinkText = styled.p`
  text-align: center;
  margin-top: 1rem;
  color: #cbd5f5;
`;

const LinkSpan = styled.span`
  color: #38bdf8;
  cursor: pointer;
    &:hover {
    text-decoration: underline;
  }
`;

const EmailDiv=styled.div`
margin-bottom: 0.8rem;
`;

const PasswordDiv=styled.div`
margin-bottom: 0.8rem;
`;

const HeadDiv=styled.div`
  display: flex;
  align-items: center;
  flex-direction: column;
  color: #e2e8f0;
`;

const Text=styled.p`
    color: #94a3b8;
    font-size: 1rem;
    margin-bottom: 0.3rem;   
`;

const ErrorText = styled.p`
  font-size: 0.9rem;
  margin: 6px 0;
  text-align: center;
  font-size: 1rem;
`;

const Google=styled.button`
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 0.7rem;
  cursor: pointer;
  font-weight: 1rem;
`;

const Github=styled.button`
  width: 100%;
  padding: 12px;
  border: none;
  margin-top: 1rem;
  border-radius: 0.7rem;
  cursor: pointer;
  font-weight: 1rem;
`;

const Divider = styled.div`
  display: flex;
  align-items: center;
  margin: 1.2rem 0;
`;

const Line = styled.div`
  flex: 1;
  height: 1px;
  background: #475569;
  opacity: 0.5;
`;

const OrText = styled.span`
  margin: 0 12px;
  font-size: 0.85rem;
  color: #94a3b8;
  letter-spacing: 1px;
`;

function Login(){
    const[email, setEmail]=useState("");
    const[password, setPassword]=useState("");
    const navigate=useNavigate();
    const [serverMsg, setServerMsg] = useState("");
    const [isError, setIsError] = useState(false);

    const handleKeyDown = (e) => {
        if (e.key === "Enter") login();
    };

    const login = async () => {
    if (!email || !password) {
        setServerMsg("Please fill all fields");
        setIsError(true);
        return;
    }

    try {
        // const res = await fetch("http://localhost:8000/login", {
        const res = await fetch("https://harshith1817-Memlore.hf.space/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            email: email,
            password: password,
        }),
        });

        const data = await res.json();

      if (res.ok && data.access_token) {
        setServerMsg("Login successful!");
        setIsError(false);

        localStorage.setItem("token", data.access_token);

        setTimeout(() => {
          navigate("/chat");
        }, 1200);

      } else {
        setServerMsg(data.detail || data.error || "Login failed");
        setIsError(true);
      }
    } catch (err) {
        console.error(err);
    }
    };

    return(
        <Container>
            <Title>Memlore AI</Title>
            <Card>
                <HeadDiv>
                    <h2>Login</h2>
                </HeadDiv>
                
                <EmailDiv>
                <Text>Email address</Text>
                <InputDiv
                    type="Email"
                    placeholder="Enter your email address"
                    value={email}
                    onChange={(e)=>setEmail(e.target.value)}
                    onKeyDown={handleKeyDown}
                />
                </EmailDiv>
                
                <PasswordDiv>
                <Text>Password</Text>
                <InputDiv
                    type="password"
                    placeholder="Enter your password"
                    value={password}
                    onChange={(e)=>setPassword(e.target.value)}
                    onKeyDown={handleKeyDown}
                />
                </PasswordDiv>

                {serverMsg && (
                  <ErrorText style={{ color: isError ? "#f87171" : "#22c55e" }}>
                    {serverMsg}
                  </ErrorText>
                )}

                <Button onClick={login}>Log In</Button>

                <Divider>
                  <Line />
                  <OrText>OR</OrText>
                  <Line />
                </Divider>
                
                <Google onClick={() => {
                  // window.location.href = "http://localhost:8000/auth/google";
                  window.location.href = "https://harshith1817-Memlore.hf.space/auth/google";
                }}><FaGoogle size={15}/> Continue with Google</Google>

                <Github onClick={() => {
                  // window.location.href = "http://localhost:8000/auth/github";
                  window.location.href = "https://harshith1817-Memlore.hf.space/auth/github";
                }}><FaGithub size={15}/> Continue with Github</Github>
                <LinkText>
                    Don't have an account?{" "}
                    <LinkSpan onClick={()=>navigate("/signup")}>
                        Signup
                    </LinkSpan>
                </LinkText>
            </Card>
        </Container>
    );
}

export default Login;