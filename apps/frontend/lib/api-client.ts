/**
 * API Client for authenticated requests
 *
 * This client proxies requests through Next.js API routes
 * which handle JWT token extraction from httpOnly cookies.
 */

interface RequestOptions extends RequestInit {
  headers?: Record<string, string>;
}

/**
 * Make an authenticated request to the API
 *
 * Requests go through Next.js API proxy at /api/proxy/[...path]
 * which reads the session cookie and forwards to backend
 */
export async function authenticatedRequest<T>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<T> {
  // Route through Next.js API proxy to handle auth
  const proxyUrl = `/api/proxy${endpoint}`;

  const response = await fetch(proxyUrl, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    credentials: 'include', // Include cookies
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || errorData.error || `Request failed with status ${response.status}`);
  }

  return response.json();
}

/**
 * Get tasks for the current user
 */
export async function getTasks() {
  return authenticatedRequest<unknown[]>('/api/tasks');
}

/**
 * Create a new task
 */
export async function createTask(data: { title: string; description?: string }) {
  return authenticatedRequest('/api/tasks', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

/**
 * Update a task
 */
export async function updateTask(id: string, data: { title?: string; description?: string; completed?: boolean }) {
  return authenticatedRequest(`/api/tasks/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  });
}

/**
 * Delete a task
 */
export async function deleteTask(id: string) {
  return authenticatedRequest(`/api/tasks/${id}`, {
    method: 'DELETE',
  });
}
