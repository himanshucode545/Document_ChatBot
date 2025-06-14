import React from "react";
import FileUploader from "./components/FileUploader";
import QueryBox from "./components/QueryBox";
import ThemeViewer from "./components/ThemeViewer";

function App() {
  return (
    <div
      className="min-h-screen bg-cover bg-center p-4"
      style={{
        backgroundImage: `url("https://miro.medium.com/v2/resize:fit:604/1*TZKc_s_ED9Z0ZTSMMVn6sg.png")`,
      }}
    >
      <div className="backdrop-brightness-90 min-h-screen p-6">
        <h1 className="text-3xl font-bold text-center mb-6 text-white drop-shadow-lg">
          Document ChatBot
        </h1>
        <div
          className="max-w-3xl mx-auto space-y-6 p-6 rounded-xl shadow-2xl"
          style={{ backgroundColor: "#C4E1E6" }}
        >
          <FileUploader />
          <QueryBox />
          <ThemeViewer />
        </div>
      </div>
    </div>
  );
}

export default App;
