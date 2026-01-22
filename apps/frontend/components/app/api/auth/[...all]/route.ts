import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

export async function POST(
  request: NextRequest,
  { params }: { params: { all: string[] } }
) {
  try {
    const path = params.all.join('/');
    const body = await request.json();

    const response = await fetch(`${BACKEND_URL}/api/auth/${path}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    const data = await response.json();

    if (!response.ok) {
      return NextResponse.json(data, { status: response.status });
    }

    return NextResponse.json(data);
  } catch (error) {
    console.error('Auth API error:', error);
    return NextResponse.json(
      { error: 'Authentication request failed' },
      { status: 500 }
    );
  }
}
