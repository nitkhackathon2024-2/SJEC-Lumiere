"use client";
import React, { useState } from "react";
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

export default function Form() {
  const [formData, setFormData] = useState(data); // Initialize form data
  const [savedData, setSavedData] = useState(null); // To display the saved JSON

  const handleSave = async () => {
    try {
      const response = await fetch("/api/save-data", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData), // Send the form data
      });

      const result = await response.json();
      if (result.success) {
        setSavedData(result.data); // Store the saved data to display
        console.log("Data saved successfully.");
      } else {
        console.error("Failed to save data:", result.message);
      }
    } catch (error) {
      console.error("Error saving data:", error);
    }
  };

  if (!formData || formData.length === 0) {
    return <p>Loading...</p>; // Render loading or fallback UI if no data
  }

  return (
    <main className="flex flex-col items-center w-full h-full py-10 justify-center">
      <Tabs defaultValue={formData[0]?.type} className="w-fit">
        <>
          {/* Rendering tab headers */}
          <TabsList className={`grid w-full grid-cols-${formData.length}`}>
            {formData.map((form, index) => (
              <TabsTrigger value={form.type} key={index}>
                {form.type}
              </TabsTrigger>
            ))}
          </TabsList>

          {/* Rendering tab contents */}
          {formData.map((form, index) => (
            <TabsContent value={form.type} key={index}>
              <Card>
                <CardHeader>
                  <CardTitle>{form.type}</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  {Object.entries(form.data).map(([key, value]) => (
                    <div className="space-y-1" key={key}>
                      <Label htmlFor={key}>{key.toUpperCase()}</Label>
                      <Input
                        id={key}
                        defaultValue={value}
                        onChange={(e) =>
                          setFormData((prevData) =>
                            prevData.map((f, i) =>
                              i === index
                                ? {
                                    ...f,
                                    data: {
                                      ...f.data,
                                      [key]: e.target.value,
                                    },
                                  }
                                : f
                            )
                          )
                        }
                      />
                    </div>
                  ))}
                </CardContent>
                <CardFooter>
                  <Button onClick={handleSave}>Save changes</Button>
                </CardFooter>
              </Card>
            </TabsContent>
          ))}
        </>
      </Tabs>

      {/* Display saved data as JSON */}
      {savedData && (
        <div className="mt-8 w-4/5 bg-gray-100 p-4 rounded">
          <h2 className="text-lg font-semibold">Saved Data:</h2>
          <pre className="text-sm overflow-auto">
            {JSON.stringify(savedData, null, 2)}
          </pre>
        </div>
      )}
    </main>
  );
}
