import React, { useState, useRef } from "react";

interface UploadedFileResponse {
  filename: string;
  filepath: string;
  id: string;
  uploaded_at: string;
}

export default function FilePage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const API_URL = import.meta.env.VITE_API_URL;

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setSelectedFile(e.dataTransfer.files[0]);
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  };

  const uploadFile = async () => {
    if (!selectedFile) {
      setMessage("Please select a file first.");
      return;
    }

    setUploading(true);
    setMessage("");

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch(`${API_URL}/file/upload`, {
        method: "POST",
        body: formData
      });
      const data: UploadedFileResponse = await response.json();
      setMessage(`File "${data.filename}" uploaded successfully ✅`);
      setSelectedFile(null); // reset selection after upload
    } catch (error) {
      console.error(error);
      setMessage("Upload failed ❌");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 flex flex-col items-center p-10">
      <h1 className="text-4xl font-extrabold mb-8 text-gray-800">
        Upload Documents for Chatbot
      </h1>

      <div className="bg-white shadow-2xl rounded-2xl p-8 w-full max-w-lg border border-gray-200">
        {/* Drag and Drop */}
        <div
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onClick={() => fileInputRef.current?.click()}
          className="border-2 border-dashed border-purple-400 rounded-xl p-12 text-center cursor-pointer hover:border-purple-600 transition"
        >
          <p className="text-purple-600 font-semibold mb-2">
            {selectedFile ? "File Selected ✅" : "Drag & drop your file here"}
          </p>
          <p className="text-gray-500">
            Or click to select a file (PDF, TXT, DOCX)
          </p>
          {selectedFile && (
            <p className="mt-3 text-gray-700 font-medium">
              {selectedFile.name}
            </p>
          )}
        </div>

        {/* Hidden File Input */}
        <input
          type="file"
          ref={fileInputRef}
          className="hidden"
          accept=".pdf, .txt, .docx"
          onChange={handleFileChange}
        />

        {/* Upload Button */}
        <button
          onClick={uploadFile}
          disabled={uploading}
          className="mt-6 w-full py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white font-semibold rounded-xl hover:from-purple-700 hover:to-blue-700 transition disabled:opacity-50"
        >
          {uploading ? "Uploading..." : "Upload File"}
        </button>

        {/* Message */}
        {message && (
          <p
            className={`mt-4 text-center font-medium ${
              message.includes("failed") ? "text-red-500" : "text-green-600"
            }`}
          >
            {message}
          </p>
        )}
      </div>
    </div>
  );
}
