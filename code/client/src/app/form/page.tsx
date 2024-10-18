import React from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  // CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

const formData = [
  {
    type: "Aadhar Card",
    data: {
      name: "Rahul Sharma",
      dob: "1990-05-12",
      gender: "Male",
      aadhar_number: "1234 5678 9101",
      address: {
        street: "123, MG Road",
        city: "Bangalore",
        state: "Karnataka",
        pincode: "560001",
      },
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
      address: {
        street: "456, Ring Road",
        city: "Bangalore",
        state: "Karnataka",
        pincode: "560002",
      },
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
      address: {
        street: "123, MG Road",
        city: "Bangalore",
        state: "Karnataka",
        pincode: "560001",
      },
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
      address: {
        street: "123, MG Road",
        city: "Bangalore",
        state: "Karnataka",
        pincode: "560001",
      },
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
      address: {
        street: "123, MG Road",
        city: "Bangalore",
        state: "Karnataka",
        pincode: "560001",
      },
    },
  },
];

export default function Form() {
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
                  {/* <CardDescription>
                    Make changes to your account here. Click save when
                    you&apos;re done.
                  </CardDescription> */}
                </CardHeader>
                <CardContent className="space-y-2">
                  {formData.map((fields) => (
                    <div className="space-y-1" key={fields}>
                      <Label htmlFor="name">Name</Label>
                      <Input id="name" defaultValue="Pedro Duarte" />
                    </div>
                  ))}
                  <div className="space-y-1">
                    <Label htmlFor="username">Username</Label>
                    <Input id="username" defaultValue="@peduarte" />
                  </div>
                </CardContent>
                <CardFooter>
                  <Button>Save changes</Button>
                </CardFooter>
              </Card>
            </TabsContent>
          ))}
        </>
      </Tabs>
      {/* <Tabs>
        <TabsContent value="form2">
          <Card>
            <CardHeader>
              <CardTitle>Form 2 </CardTitle>
              <CardDescription>
                Change your password here. After saving, you&apos;ll be logged
                out.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-2">
              <div className="space-y-1">
                <Label htmlFor="current">Current password</Label>
                <Input id="current" type="password" />
              </div>
              <div className="space-y-1">
                <Label htmlFor="new">New password</Label>
                <Input id="new" type="password" />
              </div>
            </CardContent>
            <CardFooter>
              <Button>Save password</Button>
            </CardFooter>
          </Card>
        </TabsContent>
        <TabsContent value="form3">
          <Card>
            <CardHeader>
              <CardTitle>Form 3</CardTitle>
              <CardDescription>
                Change your password here. After saving, you&apos;ll be logged
                out.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-2">
              <div className="space-y-1">
                <Label htmlFor="current">Current password</Label>
                <Input id="current" type="password" />
              </div>
              <div className="space-y-1">
                <Label htmlFor="new">New password</Label>
                <Input id="new" type="password" />
              </div>
            </CardContent>
            <CardFooter>
              <Button>Save password</Button>
            </CardFooter>
          </Card>
        </TabsContent>
        <TabsContent value="form4">
          <Card>
            <CardHeader>
              <CardTitle>Form 4</CardTitle>
              <CardDescription>
                Change your password here. After saving, you&apos;ll be logged
                out.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-2">
              <div className="space-y-1">
                <Label htmlFor="current">Current password</Label>
                <Input id="current" type="password" />
              </div>
              <div className="space-y-1">
                <Label htmlFor="new">New password</Label>
                <Input id="new" type="password" />
              </div>
            </CardContent>
            <CardFooter>
              <Button>Save password</Button>
            </CardFooter>
          </Card>
        </TabsContent>
      </Tabs> */}
    </main>
  );
}
