export const HOST = 'http://127.0.0.1:8000';

export async function makeRequest(
  endpoint: string,
  method: string,
  body?: Record<string, string>,
  headers?: Record<string, string>
) {
  try {
    const url = HOST + endpoint;
    const response = await fetch(url, {
      method,
      headers: {
          ...headers,
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
      body: body ? JSON.stringify(body) : null,
    });
    const resp = await response.json();
    return {resp, status: response.status};
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}
