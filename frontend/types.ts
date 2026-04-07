
export interface User {
  id: string;
  email: string;
  role: 'admin' | 'user';
  exp: number;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
}

export interface AuditLog {
  timestamp: string;
  action: string;
  endpoint: string;
  user_id?: string;
}

export interface ApiResponse<T = any> {
  data?: T;
  error?: string;
  status: number;
}
