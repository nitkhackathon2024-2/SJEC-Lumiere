"use client";
import React from //  { useEffect, useState }
"react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
// import { useRouter } from "next/navigation";
// import { useSearchParams } from "next/navigation";

const formData = [
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

import { ParsedUrlQuery } from "querystring";
// import axios from "axios";

interface FormProps {
  searchParams: ParsedUrlQuery;
}

export default function Form({ searchParams }: FormProps) {
  // const router = useRouter();
  // const data = router.query;
  // console.log("data: ", data);/
  // const searchParams = useSearchParams();
  console.log("data2:", searchParams);

  // const [res, setRes] = useState();

  // useEffect(() => {
  //   const fetchRes = async () => {
  //     try {
  //       const response = await axios.post(
  //         "http://localhost:8000/api/v1/uploads/",
  //         formData,
  //         {
  //           headers: {
  //             "Content-Type": "multipart/form-data",
  //           },
  //         }
  //       );
  //       console.log("Response:", response.data);
  //       setRes(response.data);
  //       console.log("res: ", res);
  //       // console.log(res);
  //     } catch (error) {
  //       console.error("Upload error:", error);
  //     }
  //   };
  //   fetchRes();
  // }, []);

  // console.log("data", formData[0].data.name);
  return (
    <main className="flex items-center w-full h-screen justify-center">
      <Tabs defaultValue={formData[0].type} className="w-fit">
        <>
          <TabsList className="grid w-full grid-cols-7">
            {formData.map((form) => (
              <TabsTrigger value={form.type} color="green" key={form.type}>
                {form.type}
              </TabsTrigger>
            ))}
          </TabsList>
          {formData.map((form) => (
            <TabsContent value={form.type} key={form.type}>
              <Card>
                <CardHeader>
                  <CardTitle>{form.type}</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  {Object.entries(form.data).map(([key, value]) => (
                    <div className="space-y-1" key={key}>
                      <Label htmlFor="name">{key.toUpperCase()}</Label>
                      <Input id="name" defaultValue={value} />
                    </div>
                  ))}
                </CardContent>
                <CardFooter>
                  <Button>Save changes</Button>
                </CardFooter>
              </Card>
            </TabsContent>
          ))}
        </>
      </Tabs>
    </main>
  );
}
