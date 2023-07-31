export const HOST = 'http://127.0.0.1:8000';

export async function makeRequest(
  endpoint: string,
  method: string,
  body?: Record<string, any> | FormData,
  headers?: Record<string, string>
) {
  try {
    const url = HOST + endpoint;
    let options = {
      method,
      headers: {
        ...headers,
        Accept: 'application/json',
      },
      body: body instanceof FormData ? body : JSON.stringify(body),
    };

    if (!(body instanceof FormData)) {
      options.headers['Content-Type'] = 'application/json';
    }

    const response = await fetch(url, options);
    const resp = await response.json();
    return {resp, status: response.status};
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}
