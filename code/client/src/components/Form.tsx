"use client";
import React from "react"; //  { useEffect, useState }
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

interface FormData {
  type: string;
  data: Record<string, string | number>;
}

interface ResData {
  file_type: string;
  text: string;
}

interface FormProps {
  props: FormData[];
  response: ResData[];
}

export default function Form({ props, response }: FormProps) {
  console.log("props", props);
  console.log("res", response);
  return (
    <main className="flex items-center w-full h-screen justify-center">
      <Tabs defaultValue={props[0].type} className="w-fit">
        <>
          <TabsList className="grid w-full grid-cols-7">
            {props.map((form) => (
              <TabsTrigger value={form.type} color="green" key={form.type}>
                {form.type}
              </TabsTrigger>
            ))}
          </TabsList>
          {props.map((form) => (
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
                  {/* <p>{response[0]!.type}</p> */}
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
