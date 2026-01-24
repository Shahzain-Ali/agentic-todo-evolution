import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ all: string[] }> }
) {
  try {
    const { all } = await params;
    const path = all.join('/');

    // Handle sign-out - clear the session cookie
    if (path === 'sign-out') {
      const response = NextResponse.json({ success: true });
      response.cookies.delete('session');
      return response;
    }

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

    // Create response with session cookie
    const nextResponse = NextResponse.json(data);

    // Set session cookie with the JWT token
    // BUT: Don't set cookie for sign-up - user should login manually after registration
    if (data.session && data.session.token && path !== 'sign-up/email') {
      nextResponse.cookies.set('session', data.session.token, {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'lax',
        maxAge: 60 * 60 * 24, // 24 hours
        path: '/',
      });
    }

    return nextResponse;
  } catch (error) {
    console.error('Auth API error:', error);
    return NextResponse.json(
      { error: 'Authentication request failed' },
      { status: 500 }
    );
  }
}

// Handle GET requests (for session checks)
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ all: string[] }> }
) {
  try {
    const { all } = await params;
    const path = all.join('/');

    // Handle session check
    if (path === 'get-session' || path === 'session') {
      const sessionToken = request.cookies.get('session')?.value;

      if (!sessionToken) {
        return NextResponse.json({ session: null, user: null });
      }

      // Verify session with backend
      try {
        const response = await fetch(`${BACKEND_URL}/api/auth/session`, {
          headers: {
            'Authorization': `Bearer ${sessionToken}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          return NextResponse.json(data);
        }
      } catch {
        // Session invalid
      }

      return NextResponse.json({ session: null, user: null });
    }

    return NextResponse.json({ error: 'Not found' }, { status: 404 });
  } catch (error) {
    console.error('Auth API GET error:', error);
    return NextResponse.json(
      { error: 'Request failed' },
      { status: 500 }
    );
  }
}
