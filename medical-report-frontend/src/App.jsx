import { useState } from "react";
import axios from "axios";

function App() {
  const [isRegister, setIsRegister] = useState(false);

  const [name, setName] = useState("");

  const [email, setEmail] = useState("");

  const [password, setPassword] = useState("");

  const [loggedIn, setLoggedIn] = useState(false);

  const [selectedFile, setSelectedFile] = useState(null);

  const [analysis, setAnalysis] = useState("");

  const [reports, setReports] = useState([]);

  // ---------------- REGISTER ----------------

  const registerUser = async () => {
    try {
      const response = await axios.post(
        "https://ai-medical-report-assistant.onrender.com/register",

        {
          name: name,
          email: email,
          password: password,
        }
        
      );

      alert(response.data.message);

      setIsRegister(false);

      setName("");
      setEmail("");
      setPassword("");

    } catch (error) {
      alert("Registration Failed");
      console.log(error);
    }
  };

  // ---------------- LOGIN ----------------

  const loginUser = async () => {
    try {
      const response = await axios.post(
  "https://ai-medical-report-assistant.onrender.com/login",
  {
    email: email,
    password: password,
  }
);

console.log("FULL RESPONSE:", response);
console.log("FULL RESPONSE DATA:", response.data);

alert(JSON.stringify(response.data));

localStorage.setItem(
  "token",
  response.data.access_token
);

console.log("Saved Token:", response.data.access_token);
console.log("Token in Storage:", localStorage.getItem("token"));

setLoggedIn(true);

alert("Login Successful");

    } catch (error) {
      alert("Login Failed");
      console.log(error);
    }
  };

  // ---------------- UPLOAD ----------------

  const uploadReport = async () => {

    if (!selectedFile) {
      alert("Please choose a PDF");
      return;
    }

    const formData = new FormData();

    formData.append("file", selectedFile);

    try {

      const token = localStorage.getItem("token");

      console.log("Upload Token:", token);
console.log("Authorization Header:", `Bearer ${token}`);

      const response = await axios.post(
        "https://ai-medical-report-assistant.onrender.com/upload-report",
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setAnalysis(response.data.analysis);

      alert("Report Uploaded Successfully");

    } catch (error) {

      alert("Upload Failed");

      console.log(error);

    }

  };

  // ---------------- MY REPORTS ----------------

  const getReports = async () => {

    try {

      const token = localStorage.getItem("token");

      const response = await axios.get(
        "https://ai-medical-report-assistant.onrender.com/my-reports",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setReports(response.data);

    } catch (error) {

      alert("Unable to Fetch Reports");

      console.log(error);

    }

  };
  // ---------------- DASHBOARD ----------------

  if (loggedIn) {
    return (
      <div
        style={{
          textAlign: "center",
          width: "500px",
          margin: "40px auto",
          background: "#ffffff",
          padding: "30px",
          borderRadius: "10px",
          boxShadow: "0px 0px 10px lightgray",
        }}
      >
        <h1>🏥 AI Medical Report Assistant</h1>

        <h2>Dashboard</h2>

        <p>Welcome!</p>

        <input
          type="file"
          onChange={(e) => setSelectedFile(e.target.files[0])}
        />

        <br />
        <br />

        <button onClick={uploadReport}>
          Upload Report
        </button>

        <br />
        <br />

        <h3>AI Analysis</h3>

        <div
  style={{
    border: "1px solid lightgray",
    padding: "15px",
    borderRadius: "8px",
    backgroundColor: "#f8f9fa",
    textAlign: "left",
    whiteSpace: "pre-wrap"
  }}
>
  {analysis}
</div>

        <br />

        <button onClick={getReports}>
          My Reports
        </button>

        <br />
        <br />

        <h3>Uploaded Reports</h3>

        {reports.length === 0 ? (
          <p>No reports uploaded.</p>
        ) : (
          reports.map((report) => (
            <div
              key={report.id}
              style={{
                border: "1px solid lightgray",
                margin: "10px",
                padding: "10px",
                borderRadius: "5px",
              }}
            >
              <b>{report.filename}</b>

              <p>{report.analysis}</p>
            </div>
          ))
        )}

        <br />

        <button
          onClick={() => {
            localStorage.removeItem("token");
            setLoggedIn(false);
            setReports([]);
            setAnalysis("");
          }}
        >
          Logout
        </button>
      </div>
    );
  }

  // ---------------- REGISTER PAGE ----------------

  if (isRegister) {
    return (
      <div
        style={{
          textAlign: "center",
          width: "450px",
          margin: "50px auto",
          background: "white",
          padding: "30px",
          borderRadius: "10px",
          boxShadow: "0px 0px 10px lightgray",
        }}
      >
        <h1>🏥 AI Medical Report Assistant</h1>

        <h2>Register</h2>

        <input
          type="text"
          placeholder="Enter Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        <br />
        <br />

        <input
          type="email"
          placeholder="Enter Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <br />
        <br />

        <input
          type="password"
          placeholder="Enter Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <br />
        <br />

        <button onClick={registerUser}>
          Register
        </button>

        <br />
        <br />

        <button onClick={() => setIsRegister(false)}>
          Already have an account? Login
        </button>
      </div>
    );
  }

  // ---------------- LOGIN PAGE ----------------

  return (
    <div
      style={{
        textAlign: "center",
        width: "450px",
        margin: "50px auto",
        background: "white",
        padding: "30px",
        borderRadius: "10px",
        boxShadow: "0px 0px 10px lightgray",
      }}
    >
      <h1>🏥 AI Medical Report Assistant</h1>

      <h2>Login</h2>

      <input
        type="email"
        placeholder="Enter Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <br />
      <br />

      <input
        type="password"
        placeholder="Enter Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <br />
      <br />

      <button onClick={loginUser}>
        Login
      </button>

      <br />
      <br />

      <button onClick={() => setIsRegister(true)}>
        New User? Register
      </button>
    </div>
  );
}

export default App;