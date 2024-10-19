/* eslint-disable @typescript-eslint/no-unused-vars */
"use client";
import React, { useState } from "react";
import { FileUpload } from "@/components/ui/file-upload";
import { Button } from "@/components/ui/button";
import axios from "axios";
import { Loader2 } from "lucide-react";
import Form from "@/components/Form";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();
  const [files, setFiles] = useState([]);
  const [res, setRes] = useState();
  const [notUploaded, setNotUploaded] = useState(true);
  const [uploading, setUploading] = useState(false);

  const handleFileUpload = (files) => {
    setFiles(files);
    console.log(files); // Debug log to view selected files
  };

  const uploadFiles = async () => {
    if (files.length === 0) {
      alert("Please upload a file first.");
      return;
    }

    setUploading(true);
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
      setRes(response.data);
      console.log("response", response.data);
      setNotUploaded(false);
      router.push("/form");
    } catch (error) {
      console.error("Upload error:", error);
    }
  };

  return (
    <>
      {/* {notUploaded ? ( */}
      <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
        <main className="flex flex-col gap-8 row-start-2 items-center justify-center sm:items-start">
          <FileUpload onChange={handleFileUpload} />
          {uploading ? (
            <Button disabled>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Please wait
            </Button>
          ) : (
            <Button variant="outline" onClick={uploadFiles}>
              Submit
            </Button>
          )}
        </main>
      </div>
      {/* // ) : ( */}
      {/* //   <Form */}
      {/* //     // props={formData as CustomFormData[]} */}
      {/* //     response={res} */}
      {/* //   /> */}
      {/* // )} */}
    </>
  );
}
