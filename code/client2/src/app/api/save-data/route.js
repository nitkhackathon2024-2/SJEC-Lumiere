import { NextResponse } from "next/server";

let savedData = []; // Temporary in-memory data storage

// Handling POST requests to save data
export async function POST(req) {
  try {
    const body = await req.json();
    console.log("Received data:", body);

    // Save the received data (in-memory for now)
    savedData.push(body);

    // Return the saved data as a response
    return NextResponse.json({ success: true, data: body });
  } catch (error) {
    console.error("Error processing data:", error.message);
    return NextResponse.json(
      { success: false, message: error.message },
      { status: 500 }
    );
  }
}

// Handling GET requests to retrieve data
export async function GET() {
  try {
    // Return the previously saved data
    return NextResponse.json({ success: true, data: savedData });
  } catch (error) {
    console.error("Error retrieving data:", error.message);
    return NextResponse.json(
      { success: false, message: error.message },
      { status: 500 }
    );
  }
}
