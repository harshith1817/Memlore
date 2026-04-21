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
  max-width: 70%;
  padding: 10px;
  border-radius: 10px;
  background: #334155;
  color: #e2e8f0;
`;

const UserBubble = styled.div`
  max-width: 70%;
  padding: 10px;
  border-radius: 10px;
  background: #2563eb;
  color: #ffffff;
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
`;

const MessageContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 16px;
`;

function ChatBox(){
    const [messages, setMessages]=useState([]);
    const [input, setInput]=useState("");

    const sendMessage=async()=>{
        if(!input) return;

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

            setMessages([
                ...messages,
                {user: input, bot: data.response},
            ]);

            setInput("");
        }catch (err){
            console.error(err);
        }
    };

    return(
        <Container>
            <Title>Memlore AI</Title>
            <ChatWindow>
                <MessageContainer>
                    {messages.map((m, i) => (
                    <div key={i}>
                        <Message isUser={false}>
                        <BotBubble>{m.bot}</BotBubble>
                        </Message>

                        <Message isUser={true}>
                        <UserBubble isUser>{m.user}</UserBubble>
                        </Message>
                    </div>
                    ))}
                </MessageContainer>
                <ChatFooter>
                    <InputContainer>
                        <Input
                            value={input}
                            onChange={(e)=>setInput(e.target.value)}
                            placeholder="Ask something..."
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