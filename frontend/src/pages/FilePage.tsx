import { useState, useRef, useEffect } from "react";
import { TimerIcon, CheckIcon, CircleX } from "lucide-react";

interface VectorStatus {
  status: "idle" | "processing" | "ready" | "cancelled";
  progress: number;
  time_taken: number;
}

export default function FilePage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState<VectorStatus["status"]>("idle");
  const [timeTaken, setTimeTaken] = useState<number | null>(null);

  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const API_URL = import.meta.env.VITE_API_URL;

  // ---------------------------------------
  // ALWAYS SYNC WITH BACKEND ON LOAD
  // ---------------------------------------
  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const res = await fetch(`${API_URL}/file/vector-status`);
        const data: VectorStatus = await res.json();

        setStatus(data.status);
        setProgress(data.progress);
        setTimeTaken(data.time_taken);
      } catch (err) {
        console.error("Initial status fetch failed");
      }
    };

    fetchStatus();
  }, []);

  // ---------------------------------------
  // Poll while processing
  // ---------------------------------------
  useEffect(() => {
    let interval: ReturnType<typeof setInterval>;

    if (status === "processing") {
      interval = setInterval(async () => {
        try {
          const res = await fetch(`${API_URL}/file/vector-status`);
          const data: VectorStatus = await res.json();

          setProgress(data.progress);

          if (data.status !== "processing") {
            setStatus(data.status);
            setTimeTaken(data.time_taken);
            clearInterval(interval);
          }
        } catch (err) {
          console.error("Status polling failed");
        }
      }, 1000);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [status]);

  const uploadFile = async () => {
    if (!selectedFile) {
      setMessage("Please select a file first.");
      return;
    }

    setUploading(true);
    setMessage("");
    setProgress(0);
    setStatus("idle");
    setTimeTaken(null);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      await fetch(`${API_URL}/file/upload`, {
        method: "POST",
        body: formData
      });

      setMessage("Building knowledge base...");
      setStatus("processing");
      setSelectedFile(null);
    } catch (error) {
      setMessage("Upload failed");
    } finally {
      setUploading(false);
    }
  };

  const cancelProcess = async () => {
    await fetch(`${API_URL}/file/vector-cancel`, {
      method: "POST"
    });

    setStatus("cancelled");
    setProgress(0);
  };

  const isDisabled = uploading || status === "processing" || status === "ready";

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 flex flex-col items-center p-10">
      <h1 className="text-4xl font-extrabold mb-8 text-amber-800">
        Upload Documents for Chatbot
      </h1>

      <div className="bg-white shadow-2xl rounded-2xl p-8 w-full max-w-lg border border-gray-200">
        {/* Drag & Drop */}
        <div
          onClick={() => !isDisabled && fileInputRef.current?.click()}
          className={`border-2 border-dashed rounded-xl p-12 text-center transition 
            ${isDisabled ? "border-gray-300 cursor-not-allowed" : "border-amber-600 cursor-pointer hover:border-orange-400"}`}
        >
          <p className="text-gray-500">
            {status === "ready"
              ? "Knowledge base already built"
              : "Click to upload your file"}
          </p>

          {selectedFile && (
            <p className="text-xl mt-3 text-gray-700 font-medium">
              {selectedFile.name}
            </p>
          )}
        </div>

        <input
          type="file"
          ref={fileInputRef}
          className="hidden"
          accept=".pdf,.txt,.docx"
          onChange={(e) => e.target.files && setSelectedFile(e.target.files[0])}
          disabled={isDisabled}
        />

        <button
          onClick={uploadFile}
          disabled={isDisabled}
          className="mt-6 w-full py-3 bg-amber-300 text-black font-semibold rounded-xl disabled:opacity-50"
        >
          {uploading
            ? "Uploading..."
            : status === "ready"
              ? "Completed"
              : "Upload File"}
        </button>

        {/* Cancel Button */}
        {status === "processing" && (
          <button
            onClick={cancelProcess}
            className="mt-4 w-full py-2 bg-red-500 text-white rounded-xl hover:bg-red-600 transition"
          >
            Cancel Process
          </button>
        )}

        {/* Progress */}
        {status === "processing" && (
          <div className="mt-6">
            <div className="w-full bg-gray-200 rounded-full h-4">
              <div
                className="bg-gradient-to-r from-amber-300 to-amber-600 h-4 rounded-full transition-all duration-500"
                style={{ width: `${progress}%` }}
              />
            </div>
            <p className="text-center mt-2 text-gray-600">
              Processing: {progress}%
            </p>
          </div>
        )}

        {/* Ready */}
        {status === "ready" && (
          <div className="mt-8 text-center">
            <div className="flex flex-row gap-3 ">
              <CheckIcon className="ml-24 text-green-500 h-6 w-6 mt-1" />
              <p className="text-green-600 font-bold text-lg w-fit">
                Ready to ask questions!
              </p>
            </div>
            {timeTaken !== null && (
              <div className="flex flex-row gap-4 mt-5">
                <TimerIcon className="ml-24 h-6 w-5 mt-1" />
                <p className="text-gray-600 mt-1 w-fit">
                  Built in {timeTaken} seconds
                </p>
              </div>
            )}
          </div>
        )}

        {/* Cancelled */}
        {status === "cancelled" && (
          <div className="flex flex-row gap-4 mt-9">
            <CircleX className="ml-32 h-5 w-5 mt-2 text-xl text-red-500 font-bold" />
            <p className="text-xl mt-1 w-fit text-red-500 font-bold">
              Process cancelled
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
