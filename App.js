import Chatbot from "./Chatbot_two";
import "./styles.css";

export default function App() {
  return (
    <div
      className="App"
      style={{
        height: "98vh",
        display: "flex",
        flexDirection: "column",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <div
        style={{ padding: "10px", backgroundColor: "#4a76a8", color: "white" }}
      >
        <h3 style={{ margin: "0" }}>Mental Health Chatbot</h3>
      </div>
      <div
        style={{
          flex: 1,
          padding: "15px",
          height: "100%",
          border: "3px solid #ccc",
          backgroundColor: "#f7f7f8",
          overflow: "scroll",
        }}
      >
        <Chatbot />
      </div>
    </div>
  );
}
