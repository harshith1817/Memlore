import React, {useState} from "react";
import styled from "styled-components";
import { IoSend } from "react-icons/io5";
import "./ChatBox.css"

const Container = styled.div`
  height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #0f172a;
`;

const Message = styled.div`
  display: flex;
  justify-content: ${(props) => (props.isUser ? "flex-end" : "flex-start")};
  margin: 10px 0;
`;

const BotBubble = styled.div`
    padding: 10px;
    background: #334155;
    color: #e2e8f0;
    align-self: flex-start;
    border-radius: 1rem 1rem 1rem 0;
    max-width: 70%;
    word-wrap: break-word;
    font-size: 1rem;
    text-align: left;

`;

const UserBubble = styled.div`
    max-width: 70%;
    padding: 10px;
    border-radius: 1rem 1rem 0 1rem;
    background: #2563eb;
    color: #ffffff;
    align-self: flex-end;
    word-wrap: break-word;
    font-size: 1rem;
    text-align: left;
`;

const InputContainer = styled.div`
  width: 98.5%;
  display: flex;
  align-items: center;
  background: #020617;
  border-radius: 25px;
  padding: 5px;
`;

const Input = styled.input`
  flex: 1;
  padding: 12px;
  border: none;
  outline: none;
  background: transparent;
  color: white;
  font-size: 14px;
`;

const SendButton = styled.button`
  background: #2563eb;
  border: none;
  border-radius: 50%;
  padding: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const Title = styled.h1`
  text-align: center;
  color: #38bdf8;
`;

const ChatFooter = styled.div`
  width: 98%;
  padding: 10px;
  display: flex;
  justify-content: center;
`;

const ChatWindow = styled.div`
  width: 50%;
  height: 80vh;
  padding-top: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 10px;
  background: #1e293b;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
`;

const MessageContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 16px;
`;

const EmptyState = styled.div`
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: #94a3b8;
  text-align: center;
`;

const SuggestionBox = styled.div`
  display: flex;
  gap: 10px;
  margin-top: 10px;
  flex-wrap: wrap;
  justify-content: center;
`;

const Suggestion = styled.button`
  background: #334155;
  border: none;
  padding: 8px 12px;
  border-radius: 8px;
  color: #e2e8f0;
  cursor: pointer;

  &:hover {
    background: #475569;
  }
`;

function ChatBox(){
    const [messages, setMessages]=useState([]);
    const [input, setInput]=useState("");
    const handleSuggestion = (text) => {
    setInput(text);
    setTimeout(() => sendMessage(), 100);
    };

    const handleKeyDown = (e) => {
        if (e.key === "Enter") sendMessage();
    };

    const sendMessage=async()=>{
        if(!input) return;

        const userMessage=input;

        setMessages(prev=>[
            ...prev,
            {type: "user", text: userMessage}
        ]);

        setInput("");

        try{
            const res=await fetch(
                `http://127.0.0.1:8000/query?q=${input}`,
                {
                    headers:{
                        token: localStorage.getItem("token"),
                    },
                }
            );

            const data=await res.json();

            setMessages(prev => [
            ...prev,
            { type: "bot", text: data.response }
            ]);

        }catch (err){
            console.error(err);
        }
    };

    return(
        <Container>
            <Title>Memlore AI</Title>
            <ChatWindow>
                <MessageContainer>
                {messages.length === 0 ? (
                    <EmptyState>
                    <div style={{ fontSize: "40px" }}>🧠</div>

                    <h2 style={{ color: "#38bdf8" }}>Memlore AI</h2>
                    <p>Ask about your memories or anything you’ve stored</p>

                    <SuggestionBox>
                        <Suggestion onClick={() => handleSuggestion("What do I like?")}>
                        What do I like?
                        </Suggestion>

                        <Suggestion onClick={() => handleSuggestion("What do you remember about me?")}>
                        My memories
                        </Suggestion>

                        <Suggestion onClick={() => handleSuggestion("Summarize my interests")}>
                        My interests
                        </Suggestion>
                    </SuggestionBox>
                    </EmptyState>
                ) : (
                    messages.map((m, i) => (
                        <Message key={i} isUser={m.type==="user"}>
                            {m.type==="user" ? (
                                <UserBubble>{m.text}</UserBubble>
                            ):(
                                <BotBubble>{m.text}</BotBubble>
                            )}
                        </Message>
                    ))
                )}
                </MessageContainer>
                <ChatFooter>
                    <InputContainer>
                        <Input
                            value={input}
                            onChange={(e)=>setInput(e.target.value)}
                            placeholder="Ask about your memories..."
                            onKeyDown={handleKeyDown}
                        />
                        <SendButton onClick={sendMessage}>
                            <IoSend color="white" size={18} />
                        </SendButton>
                    </InputContainer>
                </ChatFooter>
            </ChatWindow>
        </Container>
    );
}

export default ChatBox;