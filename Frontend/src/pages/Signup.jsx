import React, { useState} from "react";
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
  margin-top: 1rem;
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

const FieldDiv = styled.div`
  margin-bottom: 0.3rem;
`;

const HeadDiv = styled.div`
  display: flex;
  align-items: center;
  flex-direction: column;
  color: #e2e8f0;
`;

const Text = styled.p`
  color: #94a3b8;
  font-size: 1rem;
  margin-bottom: 0.3rem;
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

const ErrorText = styled.p`
  color: #f87171;
  font-size: 0.9rem;
  margin: 4px 0 4px 0;
  line-height: 1.2;
`;

function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [emailError, setEmailError] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [serverMsg, setServerMsg] = useState("");
  const [isError, setIsError] = useState(false);
  const navigate = useNavigate();

  const handleKeyDown = (e) => {
  if (e.key === "Enter") signup();
  };

    const validate = () => {
    let valid = true;

    setEmailError("");
    setPasswordError("");

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setEmailError("Enter a valid email address");
      valid = false;
    }

    const passwordRegex = /^(?=.*[A-Z]).{8,}$/;
    if (!passwordRegex.test(password)) {
      setPasswordError("Min 8 chars & at least 1 uppercase letter");
      valid = false;
    }

    return valid;
  };

  const signup = async () => {
    if (!validate()) {
      return;
    }

    try {
      const res = await fetch("http://localhost:8000/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();

      if (res.ok) {
        setServerMsg("Account created successfully!");
        setIsError(false);

        setTimeout(() => {
          navigate("/");
        }, 1500);

      } else {
        setServerMsg(data.detail || data.error || "Signup failed");
        setIsError(true);
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <Container>
      <Title>Memlore AI</Title>

      <Card>
        <HeadDiv>
          <h2>Signup</h2>
        </HeadDiv>
        <Google onClick={() => {
          window.location.href = "http://localhost:8000/auth/google";
        }}><FaGoogle size={15}/> Continue with Google</Google>

        <Github onClick={() => {
          window.location.href = "http://localhost:8000/auth/github";
        }}><FaGithub size={15}/> Continue with Github</Github>

                <Divider>
                  <Line />
                  <OrText>OR</OrText>
                  <Line />
                </Divider>

        <FieldDiv>
          <Text>Email address</Text>
          <InputDiv
            type="email"
            placeholder="Enter your email address"
            value={email}
            onChange={(e) => {
              setEmail(e.target.value);
              setEmailError("");
            }}
            onKeyDown={handleKeyDown}
          />
          {emailError && <ErrorText>{emailError}</ErrorText>}
        </FieldDiv>

        <FieldDiv>
          <Text>Password</Text>
          <InputDiv
            type="password"
            placeholder="Create a password"
            value={password}
            onChange={(e) => {
              setPassword(e.target.value);
              setPasswordError("");
            }}
            onKeyDown={handleKeyDown}
          />
          {passwordError && <ErrorText>{passwordError}</ErrorText>}
        </FieldDiv>
        {serverMsg && (
          <ErrorText style={{ color: isError ? "#f87171" : "#22c55e" }}>
            {serverMsg}
          </ErrorText>
        )}
        <Button onClick={signup}>Create an account</Button>

        <LinkText>
          Already have an account?{" "}
          <LinkSpan onClick={() => navigate("/")}>
            Login
          </LinkSpan>
        </LinkText>
      </Card>
    </Container>
  );
}

export default Signup;