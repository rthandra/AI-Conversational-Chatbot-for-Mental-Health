import { useState, useRef, useEffect } from "react";

const Chatbot = () => {
  const [input, setInput] = useState("");
  const [messages, setMessage] = useState([]);

  const messageEndRef = useRef(null);
  const scrollToBottom = () => {
    messageEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!input) return;
    setMessage((prevMessage) => [
      ...prevMessage,
      { user: "Me", text: input, type: "user" },
    ]);
    /*sending user input to a server, receiving a response, and updating the UI with the received message*/
    setInput("");
    const query = input.replace(/\s+/g, "+");
    try {
      const response = await fetch(`http://127.0.0.1:3000/query/${query}`);
      const data = await response.json();
      const message = await data.top.res;
      console.log({ message });
      setMessage((prevMessages) => [
        ...prevMessages,
        { user: "AI", text: message, type: "bot" },
      ]);
    } catch (err) {
      console.log("error ", err);
    }
  };

  return (
    <div
      style={{
        height: "100%",
        display: "flex",
        flexDirection: "column",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <div
        style={{
          flex: 1,
          overflow: "auto",
          backgroundColor: "#f7f7f8",
          padding: "10px",
        }}
      >
        {messages.map((message, index) => (
          <div
            key={index}
            style={{
              display: "flex",
              justifyContent:
                message.type === "user" ? "flex-start" : "flex-end",
              margin: "5px",
            }}
          >
            <div
              style={{
                background: message.type === "user" ? "#4a76a8" : "#dbdbdb",
                padding: "10px 15px",
                borderRadius: "20px",
                maxWidth: "70%",
                color: message.type == "user" ? "white" : "black",
              }}
            >
              <strong style={{ marginRight: "10px" }}> {message.user} :</strong>
              <span>{message.text}</span>
            </div>
          </div>
        ))}
        <div ref={messageEndRef}></div>
      </div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(event) => setInput(event.target.value)}
          style={{
            position: "sticky",
            flexGrow: 1,
            marginRight: "10px",
            bottom: 0,
            padding: "10px",
            border: "2px solid #ccc",
            borderRadius: "10px",
            width: "92%",
          }}
        />
        <button
          type="submit"
          style={{
            padding: "10px 20px",
            background: "#4a76a8",
            color: "white",
            border: "none",
            borderRadius: "10px",
            display: "none",
          }}
        >
          send
        </button>
      </form>
    </div>
  );
};

export default Chatbot;
