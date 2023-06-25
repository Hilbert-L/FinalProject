export const host = '127.0.0.1:8000';

export async function makeRequest(
  url: string,
  method: string,
  headers: Record<string, string>,
  body: string
) {
  try {
    const response = await fetch(url, {
      method: method,
      headers: headers,
      body: body,
    });

    // Handle the response
    const data = await response.json();
    // Perform any further processing with the response data
    console.log(data);

    return data; // Return the response data if needed
  } catch (error) {
    // Handle any errors
    console.error('Error:', error);
    throw error; // Throw the error to be caught by the caller
  }
}
