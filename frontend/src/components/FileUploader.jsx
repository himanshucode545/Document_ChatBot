import React, { useState } from "react";
import axios from "axios";

const FileUploader = () => {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await axios.post("http://localhost:8000/upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setStatus(`Uploaded successfully: ${res.data.chunks} chunks`);
    } catch (error) {
      setStatus("Upload failed");
    }
  };

  return (
    <div className="bg-gray-800 p-4 rounded-lg shadow text-white">
      <h2 className="text-xl font-semibold mb-3">Upload Document</h2>
      <input
        type="file"
        className="text-sm text-gray-300 file:bg-gray-700 file:text-white file:rounded file:px-4 file:py-1 file:border-none"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button
        className="ml-3 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded transition"
        onClick={handleUpload}
      >
        Upload
      </button>
      {status && <p className="mt-3 text-sm">{status}</p>}
    </div>
  );
};

export default FileUploader;
