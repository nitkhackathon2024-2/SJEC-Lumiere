/* eslint-disable @typescript-eslint/no-unused-vars */
"use client";
import React, { useState } from "react";
import { FileUpload } from "@/components/ui/file-upload";
import { Button } from "@/components/ui/button";
import axios from "axios";
import { useRouter } from "next/navigation";
import Form from "@/components/Form";

export default function Home() {
  const router = useRouter();
  const [files, setFiles] = useState<File[]>([]);
  const [res, setRes] = useState();
  const [notUploaded, setNotUploaded] = useState(true);

  // const handleFileUpload = (files: File[]) => {
  //   setFiles(files);
  //   console.log(files); // Debug log to view selected files
  // };

  const handleFileUpload = (uploadedFiles: File[]) => {
    setFiles([...files, ...uploadedFiles]);
    console.log(uploadedFiles); // Debug log to view selected files
  };

  // const uploadFiles = async () => {
  //   if (files.length === 0) {
  //     alert("Please upload a file first.");
  //     return;
  //   }

  //   const formData = new FormData();
  //   formData.append("file", files[0]); // Append only the first file for now

  //   try {
  //     const response = await axios.post(
  //       "http://localhost:8000/api/v1/uploads/",
  //       formData,
  //       {
  //         headers: {
  //           "Content-Type": "multipart/form-data",
  //         },
  //       }
  //     );
  //     setRes(response.data);
  //     console.log("response", response.data);
  //     setNotUploaded(false);
  //   } catch (error) {
  //     console.error("Upload error:", error);
  //   }
  // };

  const uploadFiles = async () => {
    if (files.length === 0) {
      alert("Please upload at least one file.");
      return;
    }

    const formData = new FormData();
    files.forEach((file) => formData.append("files", file)); // Append all files

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
    } catch (error) {
      console.error("Upload error:", error);
    }
  };

  return (
    <>
      {notUploaded ? (
        <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
          <main className="flex flex-col gap-8 row-start-2 items-center justify-center sm:items-start">
            <FileUpload onChange={handleFileUpload} />
            <Button variant="outline" onClick={uploadFiles}>
              Submit
            </Button>
          </main>
        </div>
      ) : (
        <Form
          props={formData as CustomFormData[]}
          response={res as unknown as ResData[]}
        />
      )}
    </>
  );
}

interface CustomFormData {
  type: string;
  data: Record<string, string | number>;
}

interface ResData {
  file_type: string;
  text: string;
}

const formData: CustomFormData[] = [
  {
    type: "Aadhar Card",
    data: {
      name: "Rahul Sharma",
      dob: "1990-05-12",
      gender: "Male",
      aadhar_number: "1234 5678 9101",
      address: "123, MG Road Bangalore Karnataka 560001",
    },
  },

  {
    type: "PAN Card",
    data: {
      name: "Rahul Sharma",
      father_name: "Ramesh Sharma",
      dob: "1990-05-12",
      pan_number: "ABCDE1234F",
    },
  },
  {
    type: "Petrol Pump Bill",
    data: {
      bill_number: "BP123456",
      date: "2024-10-10",
      time: "15:45",
      pump_name: "ABC Fuel Station",
      address: "123, MG Road Bangalore Karnataka 560001",
      fuel_type: "Petrol",
      quantity_liters: 20,
      price_per_liter: 102.5,
      total_amount: 2050,
    },
  },
  {
    type: "Electricity Bill",
    data: {
      consumer_name: "Rahul Sharma",
      consumer_number: "ELC567890",
      bill_number: "ELC123456",
      bill_date: "2024-10-05",
      due_date: "2024-10-25",
      units_consumed: 150,
      amount_due: 1350,
      address: "123, MG Road Bangalore Karnataka 560001",
    },
  },
  {
    type: "Water Bill",
    data: {
      consumer_name: "Rahul Sharma",
      consumer_number: "WTR123456",
      bill_number: "WTR654321",
      bill_date: "2024-10-08",
      due_date: "2024-10-30",
      units_consumed_cubic_meters: 30,
      amount_due: 500,
      address: "123, MG Road Bangalore Karnataka 560001",
    },
  },
  {
    type: "Driving License",
    data: {
      name: "Rahul Sharma",
      dob: "1990-05-12",
      license_number: "DL1234567890",
      issue_date: "2015-05-12",
      expiry_date: "2035-05-12",
      address: "123, MG Road Bangalore Karnataka 560001",
    },
  },
];
