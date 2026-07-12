import { useAuthStore } from "@/stores/authStore";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "/api/v1";

export interface Envelope<T> {
  data: T;
  meta: Record<string, unknown>;
  errors: unknown;
}

let refreshPromise: Promise<string | null> | null = null;

async function refreshAccessToken(): Promise<string | null> {
  const { refreshToken } = useAuthStore.getState();
  if (!refreshToken) return null;

  const response = await fetch(`${API_BASE_URL}/auth/token/refresh/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh: refreshToken }),
  });

  if (!response.ok) return null;

  const body = await response.json();
  const access: string | undefined = body.data?.access ?? body.access;
  if (!access) return null;

  useAuthStore.getState().setAccessToken(access);
  return access;
}

function tryRefreshAccessToken(): Promise<string | null> {
  if (!refreshPromise) {
    refreshPromise = refreshAccessToken().finally(() => {
      refreshPromise = null;
    });
  }
  return refreshPromise;
}

function extractErrorMessage(errors: unknown): string {
  if (!errors) return "Request failed";
  if (typeof errors === "string") return errors;
  if (typeof errors === "object") {
    const record = errors as Record<string, unknown>;
    if (typeof record.detail === "string") return record.detail;
    for (const value of Object.values(record)) {
      if (typeof value === "string") return value;
      if (Array.isArray(value) && typeof value[0] === "string") return value[0];
    }
  }
  return "Request failed";
}

export async function apiClient<T>(
  endpoint: string,
  options: RequestInit = {},
  retried = false
): Promise<T> {
  const headers: Record<string, string> = {
    ...(options.headers as Record<string, string>),
  };

  const isFormData = typeof FormData !== "undefined" && options.body instanceof FormData;
  if (!isFormData && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }

  const token = useAuthStore.getState().accessToken;
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const response = await fetch(`${API_BASE_URL}${endpoint}`, { ...options, headers });

  if (
    response.status === 401 &&
    !retried &&
    endpoint !== "/auth/token/" &&
    endpoint !== "/auth/token/refresh/" &&
    endpoint !== "/auth/register/"
  ) {
    const newToken = await tryRefreshAccessToken();
    if (newToken) return apiClient<T>(endpoint, options, true);
    useAuthStore.getState().logout();
    if (typeof window !== "undefined") window.location.href = "/login";
    throw new Error("Session expired");
  }

  if (response.status === 204) return {} as T;

  const body = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(extractErrorMessage(body?.errors ?? body));
  }

  // Unwrap the { data, meta, errors } envelope
  return (body?.data ?? body) as T;
}
