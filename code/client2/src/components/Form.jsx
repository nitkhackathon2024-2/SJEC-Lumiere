import React from "react";
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
import data from "@/../../../artifacts/structured_data";

export default function Form({ response }) {
  // Debugging logs
  console.log("Full response data:", response);
  console.log("data:", data);

  // Ensure response is an array
  const formData = Array.isArray(response)
    ? response
    : [response].filter(Boolean); // Wrap response in an array if it's not, and filter out any falsy values

  console.log("formdata: ", formData);

  return (
    <main className="flex items-center w-full h-full py-10 justify-center">
      <Tabs defaultValue={formData[0]?.file_type} className="w-fit">
        <>
          {/* Rendering tab headers */}
          <TabsList className={`grid w-full grid-cols-${formData.length}`}>
            {data.map((form, index) => (
              <TabsTrigger value={form.file_type} key={index}>
                {form.type}
              </TabsTrigger>
            ))}
          </TabsList>

          {/* Rendering tab contents */}
          {data.map((form, index) => (
            <TabsContent value={form.type} key={index}>
              <Card>
                <CardHeader>
                  <CardTitle>{form.type}</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  {Object.entries(form.data).map(([key, value]) => (
                    <div className="space-y-1" key={key}>
                      <Label htmlFor={key}>{key.toUpperCase()}</Label>
                      <Input id={key} defaultValue={value} />
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
