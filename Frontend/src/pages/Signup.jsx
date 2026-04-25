import React, { useState } from "react";
import styled from "styled-components";
import { useNavigate } from "react-router-dom";

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
  height: 55%;
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
  margin-bottom: 0.8rem;
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

function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const signup = async () => {
    if (!email || !password) {
      alert("Please fill all fields");
      return;
    }

    try {
      const res = await fetch("http://127.0.0.1:8000/signup", {
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

      if (res.ok) {
        alert("Account created successfully!");
        navigate("/");
      } else {
        alert(data.detail || "Signup failed");
      }
    } catch (err) {
      console.error("Signup error:", err);
    }
  };

  return (
    <Container>
      <Title>Memlore AI</Title>

      <Card>
        <HeadDiv>
          <h2>Signup</h2>
        </HeadDiv>

        <FieldDiv>
          <Text>Email address</Text>
          <InputDiv
            type="email"
            placeholder="Enter your email address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </FieldDiv>

        <FieldDiv>
          <Text>Password</Text>
          <InputDiv
            type="password"
            placeholder="Create a password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </FieldDiv>

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