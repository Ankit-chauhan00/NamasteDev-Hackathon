import { NextResponse } from "next/server";
import { cookies } from "next/headers";

export async function POST(req: Request) {
  const token = (await cookies()).get("token")?.value;

  if (!token) {
    return NextResponse.json({ detail: "Not authenticated" }, { status: 401 });
  }

  const body = await req.json();

  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const err = await res.json();
    return NextResponse.json(err, { status: res.status });
  }

  const data = await res.json();
  return NextResponse.json(data);
}