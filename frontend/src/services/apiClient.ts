const API_URL = import.meta.env.VITE_API_URL as string;

// ===== Types =====
export interface RefreshResponse {
  accessToken: string;
}

//  Refresh Access Token
export async function refreshAccessToken(): Promise<string | null> {
  const refreshToken = localStorage.getItem("refreshToken");
  if (!refreshToken) return null;

  try {
    const res = await fetch(`${API_URL}/admin/refresh`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refreshToken })
    });

    if (!res.ok) return null;

    const data: RefreshResponse = await res.json();
    const newAccessToken = data.accessToken;

    localStorage.setItem("accessToken", newAccessToken);

    return newAccessToken;
  } catch (err) {
    console.error("Refresh failed:", err);
    return null;
  }
}

//  Reusable GET method with auto-refresh
export async function getWithAuth<T>(url: string): Promise<T | null> {
  let token = localStorage.getItem("accessToken");

  let res = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    }
  });

  // If Access token expired → refresh token
  if (res.status === 401) {
    console.log("Access token expired → refreshing...");

    const newToken = await refreshAccessToken();
    if (!newToken) {
      console.log("Refresh failed — redirect to login");
      return null;
    }

    // Retry same GET request with new token
    res = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${newToken}`
      }
    });
  }

  // Handle non-OK responses
  if (!res.ok) {
    console.error("API error:", res.status);
    return null;
  }

  return (await res.json()) as T;
}

export async function requestWithAuth<T>(
  url: string,
  method: "POST" | "PUT" | "DELETE",
  body: any
): Promise<T | null> {
  let token = localStorage.getItem("accessToken");

  let res = await fetch(url, {
    method,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(body)
  });

  // If access token expired → refresh
  if (res.status === 401) {
    console.log("Access token expired → refreshing...");

    const newToken = await refreshAccessToken();
    if (!newToken) {
      console.log("Refresh failed → redirect login");
      return null;
    }

    // retry request with new token
    res = await fetch(url, {
      method,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${newToken}`
      },
      body: JSON.stringify(body)
    });
  }

  // Handle errors again after retry
  if (!res.ok) {
    const errorData = await res.json();
    console.error("API Error:", errorData.message);
    return null;
  }

  return (await res.json()) as T;
}

export async function createWithAuth<T>(url: string, body: any) {
  return requestWithAuth<T>(url, "POST", body);
}

export async function updateWithAuth<T>(url: string, body: any) {
  return requestWithAuth<T>(url, "PUT", body);
}

export async function deleteWithAuth<T>(url: string, body: any) {
  return requestWithAuth<T>(url, "DELETE", body);
}
