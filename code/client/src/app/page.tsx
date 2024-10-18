/* eslint-disable @typescript-eslint/no-unused-vars */
"use client";
import React, { useState } from "react";
import { FileUpload } from "@/components/ui/file-upload";
import { Button } from "@/components/ui/button";
import axios from "axios";

export default function Home() {
  const [files, setFiles] = useState<File[]>([]);

  const handleFileUpload = (files: File[]) => {
    setFiles(files);
    console.log(files); // Debug log to view selected files
  };

  const uploadFiles = async () => {
    if (files.length === 0) {
      alert("Please upload a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", files[0]); // Append only the first file for now

    try {
      const response = await axios.post(
        "http://localhost:8000/api/v1/uploads/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      console.log("Response:", response.data);
    } catch (error) {
      console.error("Upload error:", error);
    }
  };

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-8 row-start-2 items-center justify-center sm:items-start">
        <FileUpload onChange={handleFileUpload} />
        <Button variant="outline" onClick={uploadFiles}>
          Submit
        </Button>
      </main>
    </div>
  );
}
